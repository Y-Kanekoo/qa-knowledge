"""Opt-in RSS delivery CLI; use `python -m scripts.notify_rss` from the repo root.

Without --enabled (or with --dry-run), only collection/reporting runs. It neither
creates state nor contacts notification/state APIs in those modes.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import asdict
from pathlib import Path

from scripts._delivery import deliver_articles
from scripts._delivery_state import GitHubContentsStateStore, StateError
from scripts._notification_senders import DiscordSender, GitHubIssueSender
from scripts._safe_logging import CredentialRedactingFormatter, redact_credentials
from scripts.check_rss import (
    check_feeds,
    format_markdown,
    format_text,
    load_existing_urls,
    load_feeds_config,
    validate_feeds_config,
)

logger = logging.getLogger(__name__)


def positive_int(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("days must be non-negative")
    return number


def _deliver(articles, args, webhook_url, token):
    if not args.repository or not token:
        return {name: {"status": "missing_configuration"} for name in ("discord", "github_issue")}
    try:
        store = GitHubContentsStateStore(args.repository, args.state_branch, args.state_path, token)
    except StateError:
        return {name: {"status": "missing_configuration"} for name in ("discord", "github_issue")}
    outcomes = {}
    senders = (
        ("discord", "discord:qa-rss", 10, lambda: DiscordSender(webhook_url)),
        ("github_issue", "github:qa-rss-issues", args.issue_batch_size,
         lambda: GitHubIssueSender(args.repository, token, webhook_url)),
    )
    for name, destination, batch_size, factory in senders:
        try:
            sender = factory()
        except ValueError:
            outcomes[name] = {"status": "missing_configuration"}
            continue
        try:
            report = deliver_articles(store, destination, articles, sender, batch_size=batch_size)
            outcomes[name] = {"status": "complete" if report.complete else "incomplete", **asdict(report)}
        except StateError:
            # Another destination remains independent, but it must also reserve
            # its own durable state successfully before it can send anything.
            outcomes[name] = {"status": "state_error"}
        logger.info("配信先 %s: %s", name, outcomes[name]["status"])
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser(description="配信先別台帳によるRSS通知（既定では送信しない）")
    parser.add_argument("--enabled", action="store_true", help="明示的に台帳付きの実通知を有効にする")
    parser.add_argument("--dry-run", action="store_true", help="フィード取得と出力のみ。台帳APIも通知APIも呼ばない")
    parser.add_argument("--format", choices=["text", "markdown"], default="text")
    parser.add_argument("--days", type=positive_int, default=365)
    parser.add_argument("--status-file", type=Path)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", ""))
    parser.add_argument("--state-branch", default="rss-delivery-state")
    parser.add_argument("--state-path", default=".state/rss-delivery.json")
    parser.add_argument("--issue-batch-size", type=int, default=500, help="Issueあたりの記事上限（1〜500）")
    args = parser.parse_args()
    if not 1 <= args.issue_batch_size <= 500:
        parser.error("--issue-batch-size must be between 1 and 500")
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(CredentialRedactingFormatter(webhook_url))
    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)
    status = {"collection": "pending", "delivery": "disabled", "article_count": 0, "destinations": {}}
    exit_code = 0
    try:
        config = load_feeds_config()
        if validate_feeds_config(config):
            raise ValueError("Invalid feeds configuration")
        articles = check_feeds(config, load_existing_urls(), dry_run=args.dry_run, days_limit=args.days)
        output = format_markdown(articles) if args.format == "markdown" else format_text(articles)
        if output:
            print(redact_credentials(redact_credentials(output, webhook_url), token))
        status.update(collection="succeeded", article_count=len(articles))
        if args.dry_run:
            status["delivery"] = "dry_run"
        elif args.enabled:
            status["destinations"] = _deliver(articles, args, webhook_url, token)
            complete = all(result["status"] == "complete" for result in status["destinations"].values())
            status["delivery"] = "ledger_complete" if complete else "ledger_incomplete"
            exit_code = 0 if complete else 1
    except Exception as exc:
        logger.error("RSS処理に失敗しました: %s", type(exc).__name__)
        if status["collection"] == "pending":
            status["collection"] = "failed"
        if args.enabled:
            status["delivery"] = "not_completed"
        exit_code = 1
    logger.info("収集結果: %s / 配信結果: %s", status["collection"], status["delivery"])
    if args.status_file:
        try:
            args.status_file.write_text(json.dumps(status, ensure_ascii=False) + "\n", encoding="utf-8")
        except OSError:
            logger.error("ステータスファイルを保存できませんでした")
            exit_code = 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
