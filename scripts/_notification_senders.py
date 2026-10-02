"""Classify provider responses without leaking credentials or retrying ambiguity."""

import re

import requests

from scripts._delivery import Outcome
from scripts._safe_logging import redact_credentials
from scripts.check_rss import format_markdown

# These responses definitively reject the request. Transport errors, redirects,
# 5xx responses, or malformed success responses must remain uncertain.
_REJECTED = {400, 401, 403, 404, 405, 410, 413, 415, 422, 429}


def _post(session, url, **kwargs):
    try:
        return session.post(url, timeout=30, allow_redirects=False, **kwargs)
    except requests.RequestException:
        return None


class DiscordSender:
    def __init__(self, webhook_url: str, session=None) -> None:
        if not re.fullmatch(
            r"https://(?:[\w-]+\.)?discord(?:app)?\.com/api(?:/v\d+)?/webhooks/[0-9]+/[^/?#\s]+",
            webhook_url,
        ):
            raise ValueError("A valid Discord webhook configuration is required")
        self.webhook_url = webhook_url
        self.session = session or requests.Session()

    def __call__(self, articles: list[dict]) -> Outcome:
        if not articles or len(articles) > 10:
            return Outcome.REJECTED

        def clean(value, limit):
            return redact_credentials(str(value), self.webhook_url)[:limit] or "不明"

        embeds = [{
            "title": clean(article.get("title", ""), 200),
            "url": redact_credentials(article["url"], self.webhook_url),
            "color": 5814783,
            "fields": [
                {"name": "企業", "value": clean(article.get("company", ""), 100), "inline": True},
                {"name": "フィード", "value": clean(article.get("blog", ""), 100), "inline": True},
                {"name": "公開日", "value": clean(article.get("published", ""), 20), "inline": True},
            ],
            "footer": {"text": "QA Knowledge RSS監視"},
        } for article in articles]
        response = _post(self.session, self.webhook_url, params={"wait": "true"}, json={
            "content": f"新着QA関連記事: {len(articles)}件",
            "embeds": embeds,
            "allowed_mentions": {"parse": []},
        })
        if response is None:
            return Outcome.UNCERTAIN
        if response.status_code in _REJECTED:
            return Outcome.REJECTED
        if response.status_code != 200:
            return Outcome.UNCERTAIN
        try:
            message_id = response.json().get("id")
            if isinstance(message_id, str) and message_id.isdecimal() and int(message_id) > 0:
                return Outcome.CONFIRMED
        except (ValueError, TypeError, AttributeError):
            pass
        return Outcome.UNCERTAIN


class GitHubIssueSender:
    def __init__(self, repository: str, token: str, webhook_url: str = "", session=None) -> None:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository) or not token:
            raise ValueError("GitHub repository and token configuration are required")
        self.url = f"https://api.github.com/repos/{repository}/issues"
        self.token = token
        self.webhook_url = webhook_url
        self.session = session or requests.Session()

    def __call__(self, articles: list[dict]) -> Outcome:
        if not articles or len(articles) > 500:
            return Outcome.REJECTED
        body = redact_credentials(format_markdown(articles), self.webhook_url)
        body = redact_credentials(body, self.token)
        if len(body) > 60000:
            return Outcome.REJECTED  # Reduce --issue-batch-size; nothing was sent.
        response = _post(self.session, self.url, headers={
            "Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github+json",
        }, json={
            "title": "[new-article] 新着QA関連記事が見つかりました",
            "body": body,
            "labels": ["new-article"],
        })
        if response is None:
            return Outcome.UNCERTAIN
        if response.status_code in _REJECTED:
            return Outcome.REJECTED
        if response.status_code != 201:
            return Outcome.UNCERTAIN
        try:
            number = response.json().get("number")
            if type(number) is int and number > 0:
                return Outcome.CONFIRMED
        except (ValueError, TypeError, AttributeError):
            pass
        return Outcome.UNCERTAIN
