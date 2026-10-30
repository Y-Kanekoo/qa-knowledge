"""サイト用の入力に選択外の文書を混ぜない。"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.prepare_site_docs import SITE_DOCS_DIR, STATIC_PAGES, prepare_site_docs


def test_prepared_site_contains_only_approved_pages(tmp_path):
    expected = {Path(name) for name in STATIC_PAGES}
    for relative_path in expected:
        source = tmp_path / relative_path
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_bytes(("既存文書: " + str(relative_path)).encode())

    article = tmp_path / "entries/example.md"
    article.parent.mkdir()
    article.write_bytes(b"original article bytes")
    (article.parent / "_template.md").write_text("template")
    (tmp_path / "README.md").write_text("unrelated document")
    (tmp_path / ".env").write_text("synthetic-setting=unused")
    expected.add(Path("entries/example.md"))

    assert set(prepare_site_docs(tmp_path)) == expected
    actual = {path.relative_to(tmp_path / SITE_DOCS_DIR) for path in (tmp_path / SITE_DOCS_DIR).rglob("*.md")}
    assert actual == expected
    for relative_path in expected:
        assert (tmp_path / SITE_DOCS_DIR / relative_path).read_bytes() == (tmp_path / relative_path).read_bytes()


def test_preparation_rejects_symlink_destination(tmp_path):
    (tmp_path / "entries").mkdir()
    (tmp_path / "entries/example.md").write_text("article")
    for name in STATIC_PAGES:
        source = tmp_path / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("page")
    (tmp_path / SITE_DOCS_DIR).symlink_to(tmp_path / "entries", target_is_directory=True)

    with pytest.raises(ValueError, match="シンボリックリンク"):
        prepare_site_docs(tmp_path)


def test_preparation_rejects_symlink_source(tmp_path):
    entries = tmp_path / "entries"
    entries.mkdir()
    outside = tmp_path / "outside.md"
    outside.write_text("excluded")
    (entries / "example.md").symlink_to(outside)
    for name in STATIC_PAGES:
        source = tmp_path / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("page")

    with pytest.raises(ValueError, match="公開用文書を確認できません"):
        prepare_site_docs(tmp_path)
    assert not (tmp_path / SITE_DOCS_DIR).exists()


def test_preparation_refreshes_only_changed_pages(tmp_path):
    for name in STATIC_PAGES:
        source = tmp_path / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("original")
    entry = tmp_path / "entries/example.md"
    entry.parent.mkdir()
    entry.write_text("article")

    prepare_site_docs(tmp_path)
    staged_entry = tmp_path / SITE_DOCS_DIR / "entries/example.md"
    staged_index = tmp_path / SITE_DOCS_DIR / "index.md"
    entry_mtime = staged_entry.stat().st_mtime_ns
    index_mtime = staged_index.stat().st_mtime_ns
    prepare_site_docs(tmp_path)
    assert staged_entry.stat().st_mtime_ns == entry_mtime
    assert staged_index.stat().st_mtime_ns == index_mtime

    entry.write_text("updated article")
    prepare_site_docs(tmp_path)
    assert staged_entry.read_text() == "updated article"
    assert staged_index.stat().st_mtime_ns == index_mtime


def test_preparation_preserves_config_directory_marker(tmp_path):
    for name in STATIC_PAGES:
        source = tmp_path / name
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text("page")
    entry = tmp_path / "entries/example.md"
    entry.parent.mkdir()
    entry.write_text("article")
    target_root = tmp_path / SITE_DOCS_DIR
    target_root.mkdir()
    (target_root / ".gitkeep").write_text("marker")
    (target_root / "stale.md").write_text("stale")

    prepare_site_docs(tmp_path)
    assert (target_root / ".gitkeep").read_text() == "marker"
    assert not (target_root / "stale.md").exists()
    prepare_site_docs(tmp_path)
    assert (target_root / ".gitkeep").read_text() == "marker"


def test_mkdocs_cli_builds_from_clean_checkout(tmp_path):
    root = Path(__file__).parents[1]
    (tmp_path / "scripts").mkdir()
    for name in ("mkdocs.yml", "scripts/mkdocs_hooks.py", "scripts/prepare_site_docs.py"):
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    for name in STATIC_PAGES:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# page\n")
    entry = tmp_path / "entries/example.md"
    entry.parent.mkdir()
    entry.write_text("# article\n")
    (tmp_path / SITE_DOCS_DIR).mkdir()
    (tmp_path / SITE_DOCS_DIR / ".gitkeep").touch()

    env = os.environ.copy()
    env["PYTHONPATH"] = ""
    command = Path(sys.executable).with_name("mkdocs")
    result = subprocess.run([str(command), "build", "--strict"], cwd=tmp_path, env=env,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr[-1000:]
    assert (tmp_path / "site/entries/example/index.html").is_file()
