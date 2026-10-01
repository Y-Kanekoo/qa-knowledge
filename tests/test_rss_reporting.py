"""RSS reporting, failure propagation, and safe within-run deduplication."""

import json
import logging
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
import requests
import yaml

from scripts import check_rss
from tests.test_safe_logging import FAKE_TOKEN, FAKE_WEBHOOK

ARTICLE = {
    "blog": "Example Blog", "company": "Example", "title": "Testing guide",
    "url": "https://example.com/testing", "published": "2026-10-01", "language": "en",
}
CONFIG = {
    "feeds": [{"name": "Blog", "url": "https://example.com/feed", "company": "Example"}],
    "keywords": ["testing"],
}


@pytest.fixture
def run_main(monkeypatch, tmp_path):
    monkeypatch.setattr(check_rss, "load_feeds_config", lambda: CONFIG)
    monkeypatch.setattr(check_rss, "load_existing_urls", lambda: set())
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [ARTICLE])
    # Guard against accidental live Discord calls in every CLI regression test.
    post = Mock(side_effect=AssertionError("Unexpected network request"))
    monkeypatch.setattr(check_rss.requests, "post", post)
    monkeypatch.delenv("DISCORD_WEBHOOK_URL", raising=False)
    status_file = tmp_path / "status.json"

    def run(*args):
        monkeypatch.setattr("sys.argv", [
            "check_rss.py", "--format", "markdown", "--status-file", str(status_file), *args,
        ])
        # main configures a production handler; restore pytest's handlers after.
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
        return code, json.loads(status_file.read_text())

    run.post = post
    return run


@pytest.mark.parametrize("articles", [[], [ARTICLE]])
def test_requested_discord_missing_configuration_fails(run_main, monkeypatch, articles, capsys):
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: articles)
    code, status = run_main("--notify", "discord")
    assert code == 1
    assert status == {"collection": "succeeded", "delivery": "missing_configuration", "article_count": len(articles)}
    out, err = capsys.readouterr()
    assert "DISCORD_WEBHOOK_URL" in err
    assert "DISCORD_WEBHOOK_URL" not in out
    run_main.post.assert_not_called()


def test_read_only_collection_does_not_require_webhook(run_main):
    code, status = run_main()
    assert code == 0
    assert status["delivery"] == "not_requested"
    run_main.post.assert_not_called()


def test_dry_run_never_sends_even_when_notification_requested(run_main, monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    code, status = run_main("--notify", "discord", "--dry-run")
    assert code == 0
    assert status["delivery"] == "dry_run"
    run_main.post.assert_not_called()


def test_successful_discord_delivery_is_explicit(run_main, monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    run_main.post.side_effect = None
    run_main.post.return_value = Mock()
    code, status = run_main("--notify", "discord")
    assert code == 0
    assert status["delivery"] == "sent"
    run_main.post.assert_called_once()


def test_empty_result_is_not_claimed_as_sent(run_main, monkeypatch):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [])
    code, status = run_main("--notify", "discord")
    assert code == 0
    assert status["delivery"] == "no_articles"
    run_main.post.assert_not_called()


def test_http_failure_preserves_article_report_without_credentials(run_main, monkeypatch, capsys):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    response = requests.Response()
    response.status_code = 404
    run_main.post.side_effect = requests.HTTPError(f"404 for url: {FAKE_WEBHOOK}", response=response)
    code, status = run_main("--notify", "discord")
    out, err = capsys.readouterr()
    assert code == 1
    assert status == {"collection": "succeeded", "delivery": "failed", "article_count": 1}
    assert ARTICLE["url"] in out
    assert "HTTP 404" in err
    assert "HTTPError" not in out
    assert FAKE_TOKEN not in out + err + json.dumps(status)


def test_unexpected_exception_never_prints_raw_traceback(run_main, monkeypatch, capsys):
    monkeypatch.setattr(check_rss, "load_feeds_config", Mock(side_effect=ValueError(FAKE_WEBHOOK)))
    code, status = run_main("--notify", "discord")
    out, err = capsys.readouterr()
    assert code == 1
    assert status["collection"] == "failed"
    assert out == ""
    assert FAKE_TOKEN not in err
    assert "ValueError" in err
    run_main.post.assert_not_called()


def test_public_report_redacts_injected_credentials(run_main, monkeypatch, capsys):
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    monkeypatch.setattr(check_rss, "check_feeds", lambda *args, **kwargs: [{**ARTICLE, "title": FAKE_WEBHOOK}])
    code, _ = run_main()
    out, err = capsys.readouterr()
    assert code == 0
    assert FAKE_TOKEN not in out + err
    assert ARTICLE["url"] in out


def test_duplicates_across_feeds_are_returned_once_without_mutating_existing(monkeypatch):
    entries = [{"title": "testing", "link": ARTICLE["url"]},
               {"title": "testing", "link": ARTICLE["url"] + "?utm_source=rss"}]
    monkeypatch.setattr(check_rss.feedparser, "parse", lambda url: SimpleNamespace(bozo=False, entries=entries))
    config = {**CONFIG, "feeds": CONFIG["feeds"] * 2}
    existing = {"https://example.com/another-article"}
    assert len(check_rss.check_feeds(config, existing, days_limit=0)) == 1
    assert existing == {"https://example.com/another-article"}


def test_filtered_duplicate_does_not_hide_later_eligible_article(monkeypatch):
    entries = [{"title": "cooking", "link": ARTICLE["url"]},
               {"title": "testing", "link": ARTICLE["url"]}]
    monkeypatch.setattr(check_rss.feedparser, "parse", lambda url: SimpleNamespace(bozo=False, entries=entries))
    assert len(check_rss.check_feeds(CONFIG, set(), days_limit=0)) == 1


def test_workflow_keeps_diagnostics_out_of_public_issues_and_fails_on_delivery_error():
    workflow = yaml.safe_load((Path(__file__).parents[1] / ".github/workflows/check-rss.yml").read_text())
    steps = workflow["jobs"]["check-rss"]["steps"]
    rss = next(step for step in steps if step.get("id") == "rss")
    assert "2>&1" not in rss["run"]
    assert "|| true" not in rss["run"]
    assert "--notify discord" in rss["run"]
    assert rss["continue-on-error"] is True
    assert steps[-1]["if"] == "always() && steps.rss.outcome == 'failure'"
    assert "exit 1" in steps[-1]["run"]


def test_partial_batch_failure_stops_without_claiming_success(monkeypatch, caplog):
    response = requests.Response()
    response.status_code = 404
    post = Mock(side_effect=[Mock(), requests.HTTPError(FAKE_WEBHOOK, response=response)])
    monkeypatch.setattr(check_rss.requests, "post", post)
    articles = [{**ARTICLE, "url": f"https://example.com/{i}"} for i in range(21)]
    assert check_rss.send_discord_notification(FAKE_WEBHOOK, articles) is False
    assert post.call_count == 2
    assert FAKE_TOKEN not in caplog.text
    assert "通知を送信しました" not in caplog.text


def test_invalid_configuration_is_a_collection_failure(run_main, monkeypatch):
    monkeypatch.setattr(check_rss, "load_feeds_config", lambda: {"feeds": []})
    code, status = run_main("--notify", "discord")
    assert code == 1
    assert status["collection"] == "failed"
    assert status["article_count"] == 0
    run_main.post.assert_not_called()


def test_report_rendering_failure_does_not_publish_successful_collection(run_main, monkeypatch):
    monkeypatch.setattr(check_rss, "format_markdown", Mock(side_effect=ValueError(FAKE_WEBHOOK)))
    code, status = run_main("--notify", "discord")
    assert code == 1
    assert status["collection"] == "failed"
    run_main.post.assert_not_called()
