"""Mock provider APIs: success, rejection, ambiguity, limits, and secret hygiene."""

from unittest.mock import Mock

import pytest
import requests

from scripts._delivery import Outcome
from scripts._notification_senders import DiscordSender, GitHubIssueSender
from tests.test_rss_reporting import ARTICLE
from tests.test_safe_logging import FAKE_TOKEN, FAKE_WEBHOOK


def response(status, body):
    return Mock(status_code=status, json=Mock(return_value=body))


@pytest.mark.parametrize("status,body,expected", [
    (200, {"id": "12345"}, Outcome.CONFIRMED),
    (200, {"id": ""}, Outcome.UNCERTAIN),
    (200, {}, Outcome.UNCERTAIN),
    (204, {}, Outcome.UNCERTAIN),
    (302, {}, Outcome.UNCERTAIN),
    (400, {}, Outcome.REJECTED),
    (404, {}, Outcome.REJECTED),
    (429, {}, Outcome.REJECTED),
    (500, {}, Outcome.UNCERTAIN),
])
def test_discord_provider_outcomes(status, body, expected):
    session = Mock(post=Mock(return_value=response(status, body)))
    assert DiscordSender(FAKE_WEBHOOK, session)([ARTICLE]) is expected
    call = session.post.call_args
    assert call.kwargs["params"] == {"wait": "true"}
    assert call.kwargs["allow_redirects"] is False
    assert call.kwargs["json"]["allowed_mentions"] == {"parse": []}
    assert "Authorization" not in call.kwargs.get("headers", {})


@pytest.mark.parametrize("status,body,expected", [
    (201, {"number": 123}, Outcome.CONFIRMED),
    (201, {"number": True}, Outcome.UNCERTAIN),
    (201, {}, Outcome.UNCERTAIN),
    (200, {"number": 123}, Outcome.UNCERTAIN),
    (302, {}, Outcome.UNCERTAIN),
    (403, {}, Outcome.REJECTED),
    (422, {}, Outcome.REJECTED),
    (429, {}, Outcome.REJECTED),
    (500, {}, Outcome.UNCERTAIN),
])
def test_issue_provider_outcomes(status, body, expected):
    session = Mock(post=Mock(return_value=response(status, body)))
    assert GitHubIssueSender("example/repo", "synthetic-token", session=session)([ARTICLE]) is expected
    call = session.post.call_args
    assert call.args == ("https://api.github.com/repos/example/repo/issues",)
    assert call.kwargs["allow_redirects"] is False
    assert call.kwargs["headers"]["Authorization"] == "Bearer synthetic-token"


@pytest.mark.parametrize("sender_type", ["discord", "github"])
def test_timeout_is_uncertain_and_never_logs_raw_exception(sender_type, caplog):
    session = Mock(post=Mock(side_effect=requests.Timeout(FAKE_WEBHOOK)))
    sender = (DiscordSender(FAKE_WEBHOOK, session) if sender_type == "discord"
              else GitHubIssueSender("example/repo", "synthetic-token", session=session))
    assert sender([ARTICLE]) is Outcome.UNCERTAIN
    assert FAKE_TOKEN not in caplog.text


def test_malformed_success_response_is_uncertain():
    session = Mock()
    session.post.return_value = Mock(status_code=200, json=Mock(side_effect=ValueError(FAKE_WEBHOOK)))
    assert DiscordSender(FAKE_WEBHOOK, session)([ARTICLE]) is Outcome.UNCERTAIN


def test_discord_rejects_invalid_batch_before_network():
    session = Mock()
    sender = DiscordSender(FAKE_WEBHOOK, session)
    assert sender([]) is Outcome.REJECTED
    assert sender([ARTICLE] * 11) is Outcome.REJECTED
    session.post.assert_not_called()


def test_issue_keeps_normal_digest_in_single_request_and_sanitizes_body():
    session = Mock(post=Mock(return_value=response(201, {"number": 10})))
    sender = GitHubIssueSender("example/repo", "synthetic-github-token", FAKE_WEBHOOK, session)
    articles = [{**ARTICLE, "title": f"{FAKE_WEBHOOK} synthetic-github-token"} for _ in range(21)]
    assert sender(articles) is Outcome.CONFIRMED
    body = session.post.call_args.kwargs["json"]["body"]
    assert FAKE_TOKEN not in body
    assert "synthetic-github-token" not in body
    assert body.count(ARTICLE["url"]) == 21
    session.post.assert_called_once()


def test_oversized_issue_is_rejected_without_network():
    session = Mock()
    sender = GitHubIssueSender("example/repo", "synthetic-token", session=session)
    assert sender([{**ARTICLE, "title": "x" * 61000}]) is Outcome.REJECTED
    session.post.assert_not_called()


@pytest.mark.parametrize("url", ["", "http://discord.com/api/webhooks/1/token", "https://example.com/webhook"])
def test_discord_does_not_accept_insecure_or_unrelated_endpoints(url):
    with pytest.raises(ValueError):
        DiscordSender(url, Mock())
