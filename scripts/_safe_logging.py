"""Redact Discord credentials before diagnostics or reports leave the process."""

import logging
import re
from urllib.parse import quote, urlsplit

# URL はホストを確認し、HTTP デバッグログ中のパス単独表記は
# Discord の ID・トークン形式に限って伏せ字にする。
_FULL_DISCORD_WEBHOOK = re.compile(
    r"https?://(?:[\w-]+\.)*discord(?:app)?\.com(?::\d+)?"
    r"/api(?:/v\d+)?/webhooks/[^\s<>\"'`]+",
    re.IGNORECASE,
)
_WEBHOOK = re.compile(
    r"(?P<url>https?://[^\s<>\"'`]*?)?"
    r"(?P<path>/api(?:/v\d+)?/webhooks/[^\s<>\"'`]+)",
    re.IGNORECASE,
)
_PATH_ONLY_WEBHOOK = re.compile(r"/api(?:/v\d+)?/webhooks/\d{6,}/[A-Za-z0-9_-]{20,}", re.IGNORECASE)
_ENCODED_DISCORD_WEBHOOK = re.compile(
    r"https?%3A%2F%2F(?:[\w-]+(?:\.|%2E))*discord(?:app)?(?:\.|%2E)com"
    r"(?:%3A\d+)?%2Fapi(?:%2Fv\d+)?%2Fwebhooks%2F[^\s<>\"'`]+",
    re.IGNORECASE,
)


def _redact_webhook_match(match: re.Match[str]) -> str:
    url = match.group("url")
    if url:
        try:
            host = urlsplit(url).hostname or ""
        except ValueError:
            return "[REDACTED_WEBHOOK]"
        if not any(host == domain or host.endswith("." + domain) for domain in ("discord.com", "discordapp.com")):
            return match.group(0)
    elif not _PATH_ONLY_WEBHOOK.match(match.group("path")):
        return match.group(0)
    return "[REDACTED_WEBHOOK]"


def redact_credentials(text: str, webhook_url: str = "") -> str:
    """Remove webhook URLs and configured token variants, never logging inputs."""
    secrets = {webhook_url} if webhook_url else set()
    if webhook_url:
        try:
            path = urlsplit(webhook_url).path
            if "/webhooks/" in path:
                secrets.add(path)
                token = path.split("/webhooks/", 1)[1].split("/")
                if len(token) > 1 and token[1]:
                    secrets.add(token[1])
        except ValueError:
            pass
    variants = set()
    for secret in secrets:
        variants.update((secret, quote(secret, safe=""), secret.replace("/", r"\/")))
    for secret in sorted(variants, key=len, reverse=True):
        text = text.replace(secret, "[REDACTED]")
    text = _FULL_DISCORD_WEBHOOK.sub("[REDACTED_WEBHOOK]", text)
    text = _ENCODED_DISCORD_WEBHOOK.sub("[REDACTED_WEBHOOK]", text)
    return _WEBHOOK.sub(_redact_webhook_match, text)


class CredentialRedactingFormatter(logging.Formatter):
    """Sanitize the final formatted message, including exception tracebacks."""

    def __init__(self, webhook_url: str = "") -> None:
        super().__init__("[%(levelname)s] %(message)s")
        self.webhook_url = webhook_url

    def format(self, record: logging.LogRecord) -> str:
        return redact_credentials(super().format(record), self.webhook_url)


class CredentialRedactingStreamHandler(logging.StreamHandler):
    """ログ整形に失敗しても、元のログ引数を stderr に出さない。"""

    def handleError(self, record: logging.LogRecord) -> None:
        # 標準実装は record の未加工の引数を stderr に書き出す。
        try:
            self.stream.write("[ERROR] ログ出力に失敗しました\n")
            self.flush()
        except Exception:
            pass
