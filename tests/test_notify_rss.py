"""Offline end-to-end tests for opt-in collection, senders, and durable state."""

import json
import logging
import os
import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests
import yaml

from scripts import notify_rss
from scripts._delivery_state import StateError
from scripts._notification_senders import DiscordSender, GitHubIssueSender
from tests.test_delivery import MemoryCAS, record
from tests.test_notification_senders import response
from tests.test_rss_reporting import ARTICLE, CONFIG
from tests.test_safe_logging import FAKE_WEBHOOK


@pytest.fixture
def runner(monkeypatch, tmp_path):
    store = MemoryCAS()
    discord = Mock(post=Mock(return_value=response(200, {"id": "12345"})))
    github = Mock(post=Mock(return_value=response(201, {"number": 123})))
    state_factory = Mock(return_value=store)
    collector = Mock(return_value=[ARTICLE])
    monkeypatch.setattr(notify_rss, "GitHubContentsStateStore", state_factory)
    monkeypatch.setattr(notify_rss, "DiscordSender", lambda url: DiscordSender(url, discord))
    monkeypatch.setattr(
        notify_rss, "GitHubIssueSender", lambda repo, token, url: GitHubIssueSender(repo, token, url, github),
    )
    monkeypatch.setattr(notify_rss, "check_feeds", collector)
    monkeypatch.setattr(notify_rss, "load_feeds_config", lambda: CONFIG)
    monkeypatch.setattr(notify_rss, "load_existing_urls", lambda: set())
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", FAKE_WEBHOOK)
    monkeypatch.setenv("GITHUB_TOKEN", "synthetic-github-token")
    monkeypatch.setenv("GITHUB_REPOSITORY", "example/repo")
    # A missed injection must fail locally, never contact a provider.
    monkeypatch.setattr(requests.Session, "request", Mock(side_effect=AssertionError("Live network forbidden")))
    status_file = tmp_path / "status.json"

    def run(*args):
        monkeypatch.setattr(
            "sys.argv", ["notify_rss", "--format", "markdown", "--status-file", str(status_file), *args],
        )
        root = logging.getLogger()
        handlers, level = root.handlers[:], root.level
        try:
            code = notify_rss.main()
        finally:
            for handler in root.handlers:
                if handler not in handlers:
                    handler.close()
            root.handlers = handlers
            root.setLevel(level)
        return code, json.loads(status_file.read_text())

    run.store = store
    run.discord = discord.post
    run.github = github.post
    run.state_factory = state_factory
    run.collector = collector
    return run


@pytest.mark.parametrize("flags,delivery", [((), "disabled"), (("--dry-run",), "dry_run"),
                                          (("--enabled", "--dry-run"), "dry_run")])
def test_default_and_dry_run_never_touch_state_or_notification_apis(runner, flags, delivery, capsys):
    code, status = runner(*flags)
    assert code == 0
    assert status["delivery"] == delivery
    assert ARTICLE["url"] in capsys.readouterr().out
    runner.state_factory.assert_not_called()
    runner.discord.assert_not_called()
    runner.github.assert_not_called()
    runner.collector.assert_called_once()


def test_success_and_next_day_do_not_repeat_either_destination(runner):
    code, status = runner("--enabled")
    assert code == 0
    assert status["delivery"] == "ledger_complete"
    assert status["destinations"]["discord"]["delivered"] == 1
    assert status["destinations"]["github_issue"]["delivered"] == 1
    code, status = runner("--enabled")
    assert code == 0
    assert status["article_count"] == 1  # Collection data is preserved.
    assert status["destinations"]["discord"]["already_delivered"] == 1
    assert status["destinations"]["github_issue"]["already_delivered"] == 1
    assert runner.discord.call_count == runner.github.call_count == 1


def test_discord_rejection_does_not_block_issue_and_only_discord_retries(runner):
    runner.discord.return_value = response(404, {})
    code, status = runner("--enabled")
    assert code == 1
    assert status["destinations"]["discord"]["rejected"] == 1
    assert status["destinations"]["github_issue"]["delivered"] == 1
    runner.discord.return_value = response(200, {"id": "12345"})
    code, status = runner("--enabled")
    assert code == 0
    assert status["destinations"]["discord"]["delivered"] == 1
    assert runner.discord.call_count == 2
    assert runner.github.call_count == 1


def test_discord_unknown_result_blocks_automatic_retry_but_issue_succeeds(runner):
    runner.discord.side_effect = requests.Timeout(FAKE_WEBHOOK)
    code, status = runner("--enabled")
    assert code == 1
    assert status["destinations"]["discord"]["pending"] == 1
    assert status["destinations"]["github_issue"]["delivered"] == 1
    runner.discord.side_effect = None
    code, status = runner("--enabled")
    assert code == 1
    assert status["destinations"]["discord"]["pending"] == 1
    assert runner.discord.call_count == runner.github.call_count == 1


def test_partial_discord_batches_resume_only_unconfirmed_rejected_urls(runner):
    articles = [{**ARTICLE, "url": f"https://example.com/{i}"} for i in range(21)]
    runner.collector.return_value = articles
    runner.discord.side_effect = [response(200, {"id": "12345"}), response(429, {})]
    code, status = runner("--enabled")
    assert code == 1
    discord = status["destinations"]["discord"]
    assert (discord["delivered"], discord["rejected"], discord["not_attempted"]) == (10, 10, 1)
    assert runner.github.call_count == 1  # Preserve a single Issue digest for normal runs.
    assert status["destinations"]["github_issue"]["delivered"] == 21
    runner.discord.side_effect = None
    code, status = runner("--enabled")
    assert code == 0
    assert status["destinations"]["discord"]["already_delivered"] == 10
    assert status["destinations"]["discord"]["delivered"] == 11
    assert runner.discord.call_count == 4
    assert runner.github.call_count == 1


def test_issue_unknown_result_does_not_repeat_or_undo_discord_success(runner):
    runner.github.return_value = response(201, {})
    code, status = runner("--enabled")
    assert code == 1
    assert status["destinations"]["github_issue"]["pending"] == 1
    assert status["destinations"]["discord"]["delivered"] == 1
    runner("--enabled")
    assert runner.discord.call_count == runner.github.call_count == 1


def test_issue_partial_failure_keeps_confirmed_issue_batches(runner):
    runner.collector.return_value = [{**ARTICLE, "url": f"https://example.com/{i}"} for i in range(3)]
    runner.github.side_effect = [response(201, {"number": 1}), response(422, {})]
    code, status = runner("--enabled", "--issue-batch-size", "1")
    assert code == 1
    issue = status["destinations"]["github_issue"]
    assert (issue["delivered"], issue["rejected"], issue["not_attempted"]) == (1, 1, 1)
    runner.github.side_effect = None
    code, status = runner("--enabled", "--issue-batch-size", "1")
    assert code == 0
    assert status["destinations"]["github_issue"]["already_delivered"] == 1
    assert runner.github.call_count == 4
    assert runner.discord.call_count == 1


def test_read_only_state_permission_prevents_all_live_sends(runner, capsys):
    runner.store.fail_write = StateError("HTTP 403")
    code, status = runner("--enabled")
    assert code == 1
    assert ARTICLE["url"] in capsys.readouterr().out
    assert status["destinations"]["discord"]["status"] == "state_error"
    assert status["destinations"]["github_issue"]["status"] == "state_error"
    runner.discord.assert_not_called()
    runner.github.assert_not_called()


def test_missing_token_never_falls_back_to_untracked_sends(runner, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN")
    code, status = runner("--enabled")
    assert code == 1
    assert status["destinations"]["discord"]["status"] == "missing_configuration"
    runner.state_factory.assert_not_called()
    runner.discord.assert_not_called()
    runner.github.assert_not_called()


def test_missing_discord_configuration_does_not_block_issue(runner, monkeypatch):
    monkeypatch.delenv("DISCORD_WEBHOOK_URL")
    code, status = runner("--enabled")
    assert code == 1
    assert status["destinations"]["discord"]["status"] == "missing_configuration"
    assert status["destinations"]["github_issue"]["delivered"] == 1
    runner.discord.assert_not_called()
    runner.github.assert_called_once()


def test_receipt_failure_retains_pending_and_other_destination_proceeds(runner):
    original = runner.store.compare_and_swap
    failed = False

    def cas(snapshot, state):
        nonlocal failed
        records = state["destinations"].get("discord:qa-rss", {})
        if not failed and any(item["status"] == "delivered" for item in records.values()):
            failed = True
            raise StateError("Ambiguous state write result")
        original(snapshot, state)

    runner.store.compare_and_swap = cas
    code, status = runner("--enabled")
    assert code == 1
    assert record(runner.store)["status"] == "pending"
    assert status["destinations"]["github_issue"]["delivered"] == 1
    runner("--enabled")
    assert runner.discord.call_count == runner.github.call_count == 1


def test_workflow_opt_in_does_not_grant_write_permissions_or_double_send(tmp_path):
    path = Path(__file__).parents[1] / ".github/workflows/check-rss.yml"
    workflow = yaml.safe_load(path.read_text())
    job = workflow["jobs"]["check-rss"]
    assert job["permissions"] == {"contents": "read", "issues": "write"}
    assert workflow["concurrency"] == {"group": "qa-rss-notifications", "cancel-in-progress": False}
    steps = job["steps"]
    legacy = next(step for step in steps if step.get("id") == "rss")
    ledger = next(step for step in steps if step.get("id") == "ledger_rss")
    assert legacy["if"] == "vars.RSS_DELIVERY_LEDGER_ENABLED != 'true'"
    assert ledger["if"] == "vars.RSS_DELIVERY_LEDGER_ENABLED == 'true'"
    assert "GITHUB_TOKEN" not in legacy["env"]
    assert "--enabled" in ledger["run"]
    issue = next(step for step in steps if "create-issue-from-file" in step.get("uses", ""))
    assert "RSS_DELIVERY_LEDGER_ENABLED != 'true'" in issue["if"]
    assert "steps.ledger_rss.outcome == 'failure'" in steps[-1]["if"]

    result = next(step for step in steps if step.get("id") == "result")
    (tmp_path / "rss_status.json").write_text(json.dumps({
        "collection": "succeeded", "delivery": "ledger_incomplete", "article_count": 1,
        "destinations": {"discord": {"status": "incomplete", "pending": 1},
                         "github_issue": {"status": "complete", "delivered": 1}},
    }))
    output, summary = tmp_path / "outputs", tmp_path / "summary"
    subprocess.run(["bash", "-e", "-c", result["run"]], cwd=tmp_path, check=True,
                   env={**os.environ, "GITHUB_OUTPUT": str(output), "GITHUB_STEP_SUMMARY": str(summary)})
    assert "has_new_articles=true" in output.read_text()
    assert "pending: 1" in summary.read_text()
    assert "github_issue: complete" in summary.read_text()
