"""Credential handling uses synthetic values only and never calls the network."""

import io
import logging
from urllib.parse import quote

import pytest

from scripts._safe_logging import CredentialRedactingFormatter, redact_credentials

FAKE_TOKEN = "synthetic-webhook-token-not-a-real-credential"
FAKE_WEBHOOK = f"https://discord.com/api/webhooks/123456/{FAKE_TOKEN}"


@pytest.mark.parametrize("value", [
    FAKE_WEBHOOK,
    "/api/webhooks/123456/" + FAKE_TOKEN,
    quote(FAKE_WEBHOOK, safe=""),
    FAKE_WEBHOOK.replace("/", r"\/"),
    FAKE_TOKEN,
])
def test_configured_credential_variants_are_removed(value):
    result = redact_credentials("request failed: " + value, FAKE_WEBHOOK)
    assert FAKE_TOKEN not in result
    assert "request failed:" in result


@pytest.mark.parametrize("url", [
    FAKE_WEBHOOK,
    FAKE_WEBHOOK.replace("discord.com", "discordapp.com"),
    FAKE_WEBHOOK.replace("discord.com", "canary.discord.com"),
    FAKE_WEBHOOK.replace("/api/", "/api/v10/"),
    "/api/webhooks/123456/" + FAKE_TOKEN,
])
def test_unknown_webhook_urls_are_removed(url):
    assert FAKE_TOKEN not in redact_credentials(url)


def test_normal_article_urls_are_preserved():
    text = "[テスト](https://example.com/articles?source=rss)"
    assert redact_credentials(text, FAKE_WEBHOOK) == text


def test_formatter_redacts_arguments_and_traceback():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(CredentialRedactingFormatter(FAKE_WEBHOOK))
    log = logging.getLogger("safe-logging-test")
    log.addHandler(handler)
    try:
        try:
            raise ValueError(FAKE_WEBHOOK)
        except ValueError:
            log.exception("request %s failed", FAKE_WEBHOOK)
    finally:
        log.removeHandler(handler)
    output = stream.getvalue()
    assert FAKE_TOKEN not in output
    assert "ValueError" in output
    assert "[REDACTED]" in output
