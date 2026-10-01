"""Redact Discord credentials before diagnostics or reports leave the process."""

import logging
import re
from urllib.parse import quote, urlsplit

# Match full URLs and the path-only form used by HTTP debug logs. This also
# protects historical/unknown webhook URLs that are not in the environment.
_WEBHOOK = re.compile(
    r"(?:https?://(?:[\w-]+\.)?discord(?:app)?\.com)?"
    r"/api(?:/v\d+)?/webhooks/[^\s<>\"'`]+",
    re.IGNORECASE,
)


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
    return _WEBHOOK.sub("[REDACTED_WEBHOOK]", text)


class CredentialRedactingFormatter(logging.Formatter):
    """Sanitize the final formatted message, including exception tracebacks."""

    def __init__(self, webhook_url: str = "") -> None:
        super().__init__("[%(levelname)s] %(message)s")
        self.webhook_url = webhook_url

    def format(self, record: logging.LogRecord) -> str:
        return redact_credentials(super().format(record), self.webhook_url)
