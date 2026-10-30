"""Discord 以外の記事リンクを保持し、架空の Webhook だけを伏せ字にする。"""

from scripts._safe_logging import redact_credentials

FAKE_PATH = "/api/webhooks/123456/synthetic-path-token-not-a-real-credential"


def test_unrelated_article_url_with_webhook_path_is_preserved():
    article_url = "https://docs.example.com/guides" + FAKE_PATH
    assert redact_credentials(article_url) == article_url


def test_unrelated_host_without_discord_id_shape_is_preserved():
    article_url = "https://docs.example.com/api/webhooks/abc/example"
    assert redact_credentials(article_url) == article_url


def test_unknown_discord_url_and_standalone_path_are_redacted():
    assert redact_credentials("https://canary.discord.com" + FAKE_PATH) == "[REDACTED_WEBHOOK]"
    assert redact_credentials(FAKE_PATH) == "[REDACTED_WEBHOOK]"


def test_discord_webhook_nested_inside_another_url_is_redacted():
    text = "https://docs.example.com/redirect?target=https://discord.com" + FAKE_PATH
    assert "synthetic-path-token" not in redact_credentials(text)
