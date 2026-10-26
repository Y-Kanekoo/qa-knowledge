"""下書き保存→補完→公開の契約と、実ワークフローのプロセステスト。"""

import os
import shutil
import subprocess
import sys
import threading
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import feedparser
import frontmatter
import pytest
import yaml

from scripts import check_rss, generate_index
from scripts.collect_articles import collect_articles, restore_pending_drafts
from scripts.promote_draft import promote_draft
from scripts.scaffold import draft_path, format_output, save_draft
from scripts.validate_frontmatter import validate_file

ROOT = Path(__file__).resolve().parent.parent
ARTICLE = {
    "blog": "QA Blog", "company": "Example", "title": "日本語の記事",
    "url": "https://example.com/new", "published": "2026-10-23", "language": "ja",
}


def published_entry(root, meta):
    path = root / "entries" / "existing.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(frontmatter.dumps(frontmatter.Post("本文", **meta)), encoding="utf-8")
    return path


def run_python(root, *args):
    return subprocess.run([sys.executable, *args], cwd=root, text=True, capture_output=True)


def index_snapshot(root):
    files = [root / "index.md", *sorted((root / "indexes").glob("*.md"))]
    return {str(p.relative_to(root)): p.read_bytes() for p in files}


def complete(path):
    post = frontmatter.load(path)
    post.metadata.update(content_type="blog", qa_domains=["test-automation"], tags=["unit-testing"])
    post.content = "## 概要\n\nテストの分離を説明した記事。\n\n## 何が学べるか\n\n- DBを分離したテストの実装手順。\n"
    path.write_text(frontmatter.dumps(post), encoding="utf-8")


def test_draft_survives_strict_validation_failure_and_promotes_after_completion(tmp_path, sample_entry_meta):
    published_entry(tmp_path, sample_entry_meta)
    with patch.multiple(generate_index, ENTRIES_DIR=tmp_path / "entries", INDEXES_DIR=tmp_path / "indexes",
                        INDEX_MD=tmp_path / "index.md"):
        generate_index.main()
        before = index_snapshot(tmp_path)
        draft, = collect_articles([ARTICLE], tmp_path)
        original = draft.read_bytes()
        assert validate_file(draft, draft=True) == []
        assert validate_file(draft)  # 公開検証は空の分類を許さない
        with pytest.raises(ValueError, match="公開前検証"):
            promote_draft(draft, tmp_path)
        assert draft.read_bytes() == original
        generate_index.main()
        assert index_snapshot(tmp_path) == before
        assert "総エントリ数 | 1" in (tmp_path / "index.md").read_text()
        complete(draft)
        target = promote_draft(draft, tmp_path)
        assert not draft.exists()
        assert validate_file(target) == []
        assert frontmatter.load(target)["added_at"] == datetime.now(tz=UTC).date().isoformat()
        generate_index.main()
        result = (tmp_path / "index.md").read_text()
        assert "総エントリ数 | 2" in result
        assert ARTICLE["title"] in result
        assert f"最終更新 | {datetime.now(tz=UTC).date()}" in result
        assert collect_articles([ARTICLE], tmp_path) == []


def test_no_articles_no_writes_and_duplicates_preserve_edits(tmp_path):
    assert collect_articles([], tmp_path) == []
    assert not list(tmp_path.iterdir())
    draft, = collect_articles([ARTICLE, {**ARTICLE, "url": "http://www.example.com/new/?utm_source=rss"}], tmp_path)
    complete(draft)
    before = draft.read_bytes()
    assert collect_articles([ARTICLE], tmp_path) == []
    assert draft.read_bytes() == before
    assert len(list((tmp_path / "drafts").glob("*.md"))) == 1


def test_unicode_titles_and_quotes_are_lossless_and_do_not_collide(tmp_path):
    first = {**ARTICLE, "title": '日本語 "引用"\\\n次の行', "company": '企業 "A"'}
    second = {**first, "url": "https://example.com/別記事"}
    paths = collect_articles([first, second], tmp_path)
    assert len(set(paths)) == 2
    for path in paths:
        assert frontmatter.load(path)["title"] == first["title"]
        assert frontmatter.load(path)["company"] == first["company"]
        assert path.name.isascii()
    assert draft_path("Example", "日本語", ARTICLE["url"], tmp_path) == draft_path(
        "Example", "日本語", "http://www.example.com/new/?utm_source=rss", tmp_path,
    )


@pytest.mark.parametrize("bad", [{}, "新着QA関連記事はありません。", [None], [dict(ARTICLE, title=None)],
                                 [dict(ARTICLE, published="invalid")], [dict(ARTICLE, url="file:///tmp/no")]])
def test_invalid_input_fails_without_writing(tmp_path, bad):
    with pytest.raises(ValueError):
        collect_articles(bad, tmp_path)
    assert not list(tmp_path.iterdir())


def test_all_input_is_validated_before_any_draft_is_saved(tmp_path):
    with pytest.raises(ValueError):
        collect_articles([ARTICLE, {**ARTICLE, "url": "https://example.com/b", "language": "unknown"}], tmp_path)
    assert not list(tmp_path.iterdir())


def test_unknown_date_remains_draft_and_body_is_required_for_promotion(tmp_path):
    draft, = collect_articles([{**ARTICLE, "published": ""}], tmp_path)
    assert frontmatter.load(draft)["published_at"] == ""
    assert validate_file(draft, draft=True) == []
    complete(draft)
    with pytest.raises(ValueError, match="published_at"):
        promote_draft(draft, tmp_path)
    post = frontmatter.load(draft)
    post["published_at"] = "2026-10-23"
    post.content = "## 概要\n\n\n## 何が学べるか\n\n-\n"
    draft.write_text(frontmatter.dumps(post), encoding="utf-8")
    with pytest.raises(ValueError, match="本文"):
        promote_draft(draft, tmp_path)
    assert draft.exists()


def test_promote_never_overwrites_or_duplicates_published_entry(tmp_path, sample_entry_meta):
    draft, = collect_articles([ARTICLE], tmp_path)
    complete(draft)
    target = tmp_path / "entries" / draft.name
    target.parent.mkdir()
    target.write_text("existing content", encoding="utf-8")
    with pytest.raises(FileExistsError):
        promote_draft(draft, tmp_path)
    assert target.read_text() == "existing content"
    assert draft.exists()
    target.unlink()
    published_entry(tmp_path, {**sample_entry_meta, "url": ARTICLE["url"]})
    with pytest.raises(ValueError, match="公開済み"):
        promote_draft(draft, tmp_path)
    assert draft.exists()


def test_save_draft_never_overwrites(tmp_path):
    path = tmp_path / "draft.md"
    save_draft(path, "first")
    with pytest.raises(FileExistsError):
        save_draft(path, "second")
    assert path.read_text() == "first"


def test_index_is_deterministic_and_invalid_entry_does_not_rewrite_indexes(tmp_path, sample_entry_meta):
    entry = published_entry(tmp_path, sample_entry_meta)
    with patch.multiple(generate_index, ENTRIES_DIR=tmp_path / "entries", INDEXES_DIR=tmp_path / "indexes",
                        INDEX_MD=tmp_path / "index.md"):
        generate_index.main()
        before = index_snapshot(tmp_path)
        assert "最終更新 | 2024-07-01" in (tmp_path / "index.md").read_text()
        generate_index.main()
        assert index_snapshot(tmp_path) == before
        entry.write_text(format_output("Incomplete", ARTICLE["url"], "2026-10-23", "ja", "Example"))
        with pytest.raises(ValueError, match="インデックスは更新しません"):
            generate_index.main()
        assert index_snapshot(tmp_path) == before


def test_three_day_and_365_day_windows_have_different_boundary_results():
    today = datetime(2026, 10, 26, 0, 30, tzinfo=UTC)
    offsets = [0, 2, 3, 4, 364, 365, 366]
    entries = [{"title": "QA test", "link": f"https://example.com/day-{days}",
                "published": (today - timedelta(days=days)).date().isoformat()} for days in offsets]
    entries.append({"title": "QA test (date unknown)", "link": "https://example.com/unknown"})
    config = {"feeds": [{"name": "Blog", "company": "Example", "url": "https://example.com/rss"}],
              "keywords": ["test"]}
    parsed = feedparser.FeedParserDict(bozo=False, entries=entries)
    with patch.object(check_rss.feedparser, "parse", return_value=parsed):
        narrow = check_rss.check_feeds(config, set(), days_limit=3, today=today)
        wide = check_rss.check_feeds(config, set(), days_limit=365, today=today)
    assert {a["url"].rsplit("/", 1)[-1] for a in narrow} == {"day-0", "day-2", "day-3", "unknown"}
    assert {a["url"].rsplit("/", 1)[-1] for a in wide} == {
        "day-0", "day-2", "day-3", "day-4", "day-364", "day-365", "unknown",
    }


def test_pending_drafts_preserve_edits_and_do_not_restore_published_urls(tmp_path, sample_entry_meta):
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()
    git("init", "-b", "main")
    git("config", "user.email", "test@example.com")
    git("config", "user.name", "Test")
    path, = collect_articles([ARTICLE], tmp_path)
    complete(path)
    edited = path.read_bytes()
    git("add", ".")
    git("commit", "-m", "pending draft")
    ref = git("rev-parse", "HEAD")
    path.unlink()
    restore_pending_drafts(ref, tmp_path)
    assert path.read_bytes() == edited
    path.write_text(path.read_text() + "local edits")
    local = path.read_bytes()
    restore_pending_drafts(ref, tmp_path)
    assert path.read_bytes() == local
    path.unlink()
    published_entry(tmp_path, {**sample_entry_meta, "url": ARTICLE["url"]})
    restore_pending_drafts(ref, tmp_path)
    assert not path.exists()


@pytest.fixture
def process_repo(tmp_path, sample_entry_meta):
    shutil.copytree(ROOT / "scripts", tmp_path / "scripts")
    published_entry(tmp_path, sample_entry_meta)
    result = run_python(tmp_path, "scripts/generate_index.py")
    assert result.returncode == 0, result.stderr
    (tmp_path / "bin").mkdir()
    gh = tmp_path / "bin" / "gh"
    # 外部境界だけを置換。実GitHub/Discordにアクセスしない。
    gh.write_text("#!/bin/sh\nprintf '0\\n'\n")
    gh.chmod(0o755)
    return tmp_path


@pytest.fixture
def rss_server():
    payload = [b""]
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/rss+xml")
            self.end_headers()
            self.wfile.write(payload[0])
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield payload, f"http://127.0.0.1:{server.server_port}/feed"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def setup_feed(root, rss_server, articles):
    payload, url = rss_server
    items = "".join(f"<item><title>{a['title']}</title><link>{a['url']}</link>"
                    f"<pubDate>{datetime.now(tz=UTC):%a, %d %b %Y %H:%M:%S GMT}</pubDate></item>" for a in articles)
    payload[0] = f'<rss version="2.0"><channel><title>QA Blog</title>{items}</channel></rss>'.encode()
    config = {"feeds": [{"name": "新着QA関連記事はありません。", "url": url, "company": "Example", "language": "ja"}],
              "keywords": ["test"],}
    (root / "feeds.yml").write_text(yaml.safe_dump(config), encoding="utf-8")


def workflow(name):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def shell_step(root, step, output):
    env = {**os.environ, "PATH": f"{root / 'bin'}:{Path(sys.executable).parent}:{os.environ['PATH']}",
           "RUNNER_TEMP": str(root), "GITHUB_OUTPUT": str(output), "GITHUB_REPOSITORY": "fixture/qa-knowledge",
           "DISCORD_WEBHOOK_URL": ""}
    return subprocess.run(["bash", "--noprofile", "--norc", "-e", "-o", "pipefail", "-c", step["run"]],
                          cwd=root, env=env, capture_output=True, text=True)


@pytest.mark.parametrize("article_count", [0, 1])
def test_collection_workflow_executes_real_producers_and_keeps_public_indexes(process_repo, rss_server, article_count):
    root = process_repo
    setup_feed(root, rss_server, [{**ARTICLE, "title": "QA test"}] * article_count)
    before = index_snapshot(root)
    steps = workflow("collect-articles.yml")["jobs"]["collect"]["steps"]
    output = root / "output"
    for step in steps:
        if "run" in step and not step["run"].startswith("pip install"):
            result = shell_step(root, step, output)
            assert result.returncode == 0, result.stderr + result.stdout
    outputs = dict(line.split("=", 1) for line in output.read_text().splitlines())
    assert outputs == {"added_count": str(article_count), "has_changes": str(bool(article_count)).lower()}
    assert len(list((root / "drafts").glob("*.md"))) == article_count
    assert index_snapshot(root) == before
    action = next(step for step in steps if step.get("uses", "").startswith("peter-evans/create-pull-request"))
    assert action["if"] == "steps.collect.outputs.has_changes == 'true' && steps.collect.outputs.added_count != '0'"
    assert action["with"]["add-paths"] == "drafts/*.md"
    assert action["with"]["branch"] == "auto/collect-articles"
    assert "labels" not in action["with"]
    # 同じ実RSSを再収集してもPR更新の条件を満たさない。
    for step in steps:
        if step.get("id") == "collect":
            result = shell_step(root, step, root / "rerun-output")
            assert result.returncode == 0, result.stderr
    assert (root / "rerun-output").read_text() == "added_count=0\nhas_changes=false\n"


def test_workflow_failure_cannot_create_pr(process_repo):
    (process_repo / "feeds.yml").write_text("feeds: []\nkeywords: []\n")
    step = next(s for s in workflow("collect-articles.yml")["jobs"]["collect"]["steps"]
                if s.get("run", "").startswith("python scripts/check_rss.py"))
    output = process_repo / "output"
    result = shell_step(process_repo, step, output)
    assert result.returncode != 0
    assert not output.exists()
    assert not (process_repo / "drafts").exists()


@pytest.mark.parametrize("article_count", [0, 1])
def test_rss_workflow_uses_count_not_message_or_stderr(process_repo, rss_server, article_count):
    setup_feed(process_repo, rss_server, [{**ARTICLE, "title": "QA test"}] * article_count)
    steps = workflow("check-rss.yml")["jobs"]["check-rss"]["steps"]
    step = next(s for s in steps if s.get("id") == "rss")
    output = process_repo / "output"
    result = shell_step(process_repo, step, output)
    assert result.returncode == 0, result.stderr
    assert f"article_count={article_count}\nhas_new_articles={str(bool(article_count)).lower()}" in output.read_text()
    assert "exit_code=0" in output.read_text()
    report = (process_repo / "rss_result.txt").read_text()
    assert bool(report) == bool(article_count)
    if not article_count:
        # 元のテキストメッセージは部分一致するが、新判定はfalse。
        assert "新着QA関連記事" in check_rss.format_text([])
    assert "--days 365" in step["run"]
    assert "--days 3" in next(s["run"] for s in workflow("collect-articles.yml")["jobs"]["collect"]["steps"]
                               if s.get("run", "").startswith("python scripts/check_rss.py"))


def test_invalid_json_cli_fails_without_success_outputs(process_repo):
    source = process_repo / "invalid.json"
    source.write_text("not JSON")
    output = process_repo / "output"
    result = run_python(process_repo, "scripts/collect_articles.py", "--input", str(source),
                        "--github-output", str(output))
    assert result.returncode != 0
    assert not output.exists()
    assert not (process_repo / "drafts").exists()


def test_mkdocs_excludes_drafts_even_with_root_docs_dir():
    config = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
    from mkdocs.config import load_config
    # MkDocsの実際のpathspecで公開・検索対象からの除外を確認。
    configured = load_config(config_file=str(ROOT / "mkdocs.yml"))
    assert config["exclude_docs"] == "drafts/\n"
    assert configured.exclude_docs.match_file("drafts/incomplete.md")
    assert not configured.exclude_docs.match_file("entries/complete.md")


def test_scaffold_cli_defaults_to_drafts_and_refuses_overwrite_or_entries(process_repo, rss_server):
    setup_feed(process_repo, rss_server, [])
    _, url = rss_server
    result = run_python(process_repo, "scripts/scaffold.py", url, "--company", "Example")
    assert result.returncode == 0, result.stderr
    path, = (process_repo / "drafts").glob("*.md")
    original = path.read_bytes()
    assert frontmatter.load(path)["status"] == "draft"
    assert validate_file(path, draft=True) == []
    repeated = run_python(process_repo, "scripts/scaffold.py", url, "--company", "Example")
    assert repeated.returncode != 0
    assert path.read_bytes() == original
    refused = run_python(process_repo, "scripts/scaffold.py", url, "--company", "Example",
                         "--output", "entries/incomplete.md")
    assert refused.returncode != 0
    assert not (process_repo / "entries" / "incomplete.md").exists()


def test_rss_config_failure_remains_failed_in_workflow(process_repo):
    (process_repo / "feeds.yml").write_text("feeds: []\nkeywords: []\n")
    steps = workflow("check-rss.yml")["jobs"]["check-rss"]["steps"]
    step = next(s for s in steps if s.get("id") == "rss")
    output = process_repo / "output"
    result = shell_step(process_repo, step, output)
    assert result.returncode == 0  # 後続のエラー伝播ステップがジョブを失敗にする
    assert output.read_text() == "exit_code=1\n"
    issue_step = next(s for s in steps if s.get("uses", "").startswith("peter-evans/create-issue"))
    assert issue_step["if"] == "steps.rss.outputs.has_new_articles == 'true'"
    error_step = steps[-1]
    assert error_step["if"] == "always() && steps.rss.outputs.exit_code != '0'"
    assert shell_step(process_repo, error_step, output).returncode == 1
    assert (process_repo / "rss_result.txt").read_text() == ""
