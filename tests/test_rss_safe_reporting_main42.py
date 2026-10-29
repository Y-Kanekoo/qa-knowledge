"""現行の GitHub output 契約と秘密情報の境界を合成値で確認する。"""

import json
import logging
from types import SimpleNamespace
from unittest.mock import Mock
from urllib.parse import quote

import requests

from scripts import check_rss
from tests.test_safe_logging import FAKE_TOKEN, FAKE_WEBHOOK

ARTICLE = {
    "blog": "Example", "company": "Example", "title": "testing guide",
    "url": "https://example.invalid/testing-guide", "published": "2026-10-01", "language": "en",
}
CONFIG = {
    "feeds": [{"name": "Example", "url": "https://example.invalid/feed", "company": "Example"}],
    "keywords": ["testing"],
}


def run_main(monkeypatch, tmp_path, *options, config=CONFIG, output_format="markdown"):
    output_path = tmp_path / "github_output"
    monkeypatch.setattr("sys.argv", [
        "check_rss.py", "--format", output_format, "--github-output", str(output_path), *options,
    ])
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    monkeypatch.setattr(check_rss, "load_feeds_config", lambda: config)
    monkeypatch.setattr(check_rss, "load_existing_urls", lambda: set())
    root = logging.getLogger()
    handlers, level = root.handlers[:], root.level
    try:
        code = check_rss.main()
    finally:
        for handler in root.handlers:
            if handler not in handlers:
                handler.close()
        root.handlers = handlers
        root.setLevel(level)
    return code, output_path.read_text() if output_path.exists() else ""


def test_discord_http_error_keeps_issue_report_and_failure(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [ARTICLE])
    response = requests.Response()
    response.status_code = 503
    response._content = FAKE_WEBHOOK.encode()
    post = Mock(side_effect=requests.HTTPError(FAKE_WEBHOOK, response=response))
    monkeypatch.setattr(check_rss.requests, "post", post)

    code, github_output = run_main(monkeypatch, tmp_path, "--notify", "discord")
    out, err = capsys.readouterr()
    assert code == 1
    assert ARTICLE["url"] in out
    assert "article_count=1\nhas_new_articles=true\n" == github_output
    assert "HTTPError" in err and "HTTP 503" in err
    assert FAKE_TOKEN not in out + err + github_output
    post.assert_called_once()


def test_partial_feed_exception_keeps_issue_report_and_failure(monkeypatch, tmp_path, capsys):
    config = {**CONFIG, "feeds": [CONFIG["feeds"][0],
                                  {"name": "Second", "url": "https://example.invalid/second", "company": "Example"}]}
    parsed = SimpleNamespace(bozo=False, entries=[{"title": ARTICLE["title"], "link": ARTICLE["url"]}])
    monkeypatch.setattr(check_rss.feedparser, "parse", Mock(side_effect=[RuntimeError(FAKE_WEBHOOK), parsed]))
    post = Mock(side_effect=AssertionError("unexpected network request"))
    monkeypatch.setattr(check_rss.requests, "post", post)

    code, github_output = run_main(monkeypatch, tmp_path, config=config)
    out, err = capsys.readouterr()
    assert code == 1
    assert ARTICLE["url"] in out
    assert github_output == "article_count=1\nhas_new_articles=true\n"
    assert "Example" in err
    assert "RuntimeError" in err
    assert FAKE_TOKEN not in out + err + github_output
    post.assert_not_called()


def test_unexpected_exception_has_no_public_report_or_output(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(check_rss, "check_feeds", Mock(side_effect=ValueError(FAKE_WEBHOOK)))
    post = Mock(side_effect=AssertionError("unexpected network request"))
    monkeypatch.setattr(check_rss.requests, "post", post)

    code, github_output = run_main(monkeypatch, tmp_path, "--notify", "discord")
    out, err = capsys.readouterr()
    assert code == 1
    assert out == "" and github_output == ""
    assert "ValueError" in err
    assert FAKE_TOKEN not in err
    post.assert_not_called()


def test_public_article_field_is_sanitized(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [{**ARTICLE, "title": FAKE_WEBHOOK}])
    post = Mock(side_effect=AssertionError("unexpected network request"))
    monkeypatch.setattr(check_rss.requests, "post", post)

    code, github_output = run_main(monkeypatch, tmp_path)
    out, err = capsys.readouterr()
    assert code == 0
    assert ARTICLE["url"] in out
    assert github_output == "article_count=1\nhas_new_articles=true\n"
    assert FAKE_TOKEN not in out + err + github_output
    post.assert_not_called()


def test_json_report_remains_parseable_after_redaction(monkeypatch, tmp_path, capsys):
    other_token = "another-synthetic-webhook-token"
    title = quote(FAKE_WEBHOOK.replace(FAKE_TOKEN, other_token), safe="") + '" quoted title'
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [{**ARTICLE, "title": title}])
    post = Mock(side_effect=AssertionError("unexpected network request"))
    monkeypatch.setattr(check_rss.requests, "post", post)

    code, github_output = run_main(monkeypatch, tmp_path, output_format="json")
    out, err = capsys.readouterr()
    parsed = json.loads(out)
    assert code == 0
    assert len(parsed) == 1 and parsed[0]["url"] == ARTICLE["url"]
    assert parsed[0]["title"].endswith('" quoted title')
    assert github_output == "article_count=1\nhas_new_articles=true\n"
    assert FAKE_TOKEN not in out + err + github_output
    assert other_token not in out + err + github_output
    post.assert_not_called()


def test_json_collection_accepts_partial_feed_results(monkeypatch, tmp_path, capsys):
    config = {**CONFIG, "feeds": [CONFIG["feeds"][0],
                                  {"name": "Second", "url": "https://example.invalid/second", "company": "Example"}]}
    parsed_feed = SimpleNamespace(bozo=False, entries=[{"title": ARTICLE["title"], "link": ARTICLE["url"]}])
    monkeypatch.setattr(check_rss.feedparser, "parse", Mock(side_effect=[RuntimeError(FAKE_WEBHOOK), parsed_feed]))
    post = Mock(side_effect=AssertionError("unexpected network request"))
    monkeypatch.setattr(check_rss.requests, "post", post)

    code, github_output = run_main(
        monkeypatch, tmp_path, "--allow-partial-feeds", config=config, output_format="json",
    )
    out, err = capsys.readouterr()
    assert code == 0
    assert json.loads(out)[0]["url"] == ARTICLE["url"]
    assert "一部フィードの取得に失敗" in err
    assert github_output == "article_count=1\nhas_new_articles=true\n"
    assert FAKE_TOKEN not in out + err + github_output
    assert "--allow-partial-feeds" in (
        check_rss.PROJECT_ROOT / ".github/workflows/collect-articles.yml"
    ).read_text()
    post.assert_not_called()


def test_discord_http_status_object_cannot_expose_secret(monkeypatch, tmp_path, capsys):
    class SecretStatus(int):
        def __str__(self):
            return FAKE_WEBHOOK

    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [ARTICLE])
    response = requests.Response()
    response.status_code = SecretStatus(503)
    error = requests.HTTPError(FAKE_WEBHOOK, response=response)
    monkeypatch.setattr(check_rss.requests, "post", Mock(side_effect=error))

    code, github_output = run_main(monkeypatch, tmp_path, "--notify", "discord")
    out, err = capsys.readouterr()
    assert code == 1
    assert ARTICLE["url"] in out
    assert github_output == "article_count=1\nhas_new_articles=true\n"
    assert "HTTP unknown" in err
    assert FAKE_TOKEN not in out + err + github_output


def test_existing_entry_exception_logs_only_class(monkeypatch, tmp_path, caplog):
    entry = tmp_path / "entry.md"
    entry.write_text("synthetic entry")
    monkeypatch.setattr(check_rss.frontmatter, "load", Mock(side_effect=OSError(FAKE_WEBHOOK)))

    assert check_rss.load_existing_urls(directories=(tmp_path,)) == set()
    assert "entry.md" in caplog.text
    assert "OSError" in caplog.text
    assert FAKE_TOKEN not in caplog.text
