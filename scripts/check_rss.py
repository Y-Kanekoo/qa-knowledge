#!/usr/bin/env python3
"""RSSフィードを巡回し、未収録のQA関連記事を検出するスクリプト。

feeds.yml に定義されたフィードを取得し、entries/ の既存URLと照合して
新着記事をリストアップする。GitHub Actions から週次実行される想定。
"""

import argparse
import json
import logging
import os
import re
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

import feedparser
import frontmatter
import requests
import yaml

try:
    from scripts._safe_logging import CredentialRedactingFormatter, CredentialRedactingStreamHandler, redact_credentials
    from scripts._url import normalize_url
except ImportError:
    from _safe_logging import CredentialRedactingFormatter, CredentialRedactingStreamHandler, redact_credentials
    from _url import normalize_url

# モジュールレベルのロガー
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = PROJECT_ROOT / "feeds.yml"
ENTRIES_DIR = PROJECT_ROOT / "entries"
DRAFTS_DIR = PROJECT_ROOT / "drafts"


def load_feeds_config() -> dict:
    """feeds.yml を読み込む。"""
    with open(FEEDS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_feeds_config(config: dict) -> list[str]:
    """feeds.yml の構造を検証する。"""
    errors: list[str] = []
    feeds = config.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        errors.append("feeds: フィードが定義されていません")
        return errors
    for i, feed in enumerate(feeds):
        for key in ("name", "url", "company"):
            if not feed.get(key):
                errors.append(f"feeds[{i}]: '{key}' が未設定です")
        url = feed.get("url", "")
        if url and not url.startswith("http"):
            errors.append(f"feeds[{i}]: url が不正です: {url}")
        lang = feed.get("language", "en")
        if lang not in ("en", "ja"):
            errors.append(f"feeds[{i}]: language は 'en' または 'ja' を指定: {lang}")
    keywords = config.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        errors.append("keywords: キーワードが定義されていません")
    return errors


def load_existing_urls(directories: tuple[Path, ...] | None = None) -> set[str]:
    """公開済み・下書き保存済みURLを収集する。"""
    urls: set[str] = set()

    files = [path for directory in (directories or (ENTRIES_DIR, DRAFTS_DIR)) for path in directory.glob("*.md")]
    for md_file in files:
        if md_file.name == "_template.md":
            continue
        try:
            post = frontmatter.load(md_file)
            url = post.metadata.get("url", "")
            if url:
                urls.add(normalize_url(url))
        except (yaml.YAMLError, OSError) as e:
            logger.warning("%s の読み込みに失敗しました: %s", md_file.name, type(e).__name__)
            continue

    return urls


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """テキストにキーワードが含まれるか判定する（単語境界考慮）。"""
    text_lower = text.lower()
    for keyword in keywords:
        kw = keyword.lower()
        # 英語キーワードは単語境界で検索（日本語キーワードは部分一致のまま）
        if kw.isascii():
            # 区切り文字（スペース、ハイフン等）を柔軟にマッチ
            parts = re.split(r"[\s\-_/]+", kw)
            pattern = r"\b" + r"[\s\-_/]+".join(re.escape(p) for p in parts) + r"\b"
            if re.search(pattern, text_lower, re.ASCII):
                return True
        else:
            if kw in text_lower:
                return True
    return False


def parse_published_date(entry: dict) -> str:
    """フィードエントリから公開日をYYYY-MM-DD形式で取得する。"""
    # published_parsed が最も一般的
    for date_field in ("published_parsed", "updated_parsed"):
        parsed = entry.get(date_field)
        if parsed:
            try:
                dt = datetime(*parsed[:6], tzinfo=UTC)
                return dt.strftime("%Y-%m-%d")
            except (TypeError, ValueError):
                continue

    # 文字列から日付部分を抽出
    for date_field in ("published", "updated"):
        date_str = entry.get(date_field, "")
        if date_str:
            match = re.search(r"(\d{4}-\d{2}-\d{2})", date_str)
            if match:
                return match.group(1)

    return ""


def get_entry_text(entry: dict) -> str:
    """フィードエントリからフィルタリング対象のテキストを取得する。"""
    parts = []
    parts.append(entry.get("title", ""))
    # summary / description / content
    parts.append(entry.get("summary", ""))
    parts.append(entry.get("description", ""))
    if "content" in entry:
        for content in entry["content"]:
            parts.append(content.get("value", ""))
    # タグ / カテゴリ
    for tag in entry.get("tags", []):
        parts.append(tag.get("term", ""))
    return " ".join(parts)


def check_feeds(
    config: dict,
    existing_urls: set[str],
    dry_run: bool = False,
    days_limit: int = 365,
    *,
    today: datetime | None = None,
    feed_outcomes: list[bool] | None = None,
) -> list[dict]:
    """全フィードを巡回し、新着QA関連記事を検出する。"""
    feeds = config.get("feeds", [])
    keywords = config.get("keywords", [])
    new_articles: list[dict] = []

    # 日付フィルタの基準日
    cutoff_date = ((today or datetime.now(tz=UTC)) - timedelta(days=days_limit)).date()
    seen_urls = set(existing_urls)

    for feed_config in feeds:
        name = feed_config["name"]
        feed_url = feed_config["url"]
        company = feed_config["company"]
        language = feed_config.get("language", "en")
        skip_filter = feed_config.get("skip_keyword_filter", False)

        if dry_run:
            logger.info("フィードを取得中: %s (%s)", name, feed_url)

        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            logger.warning("%s の取得に失敗しました: %s", name, type(e).__name__)
            if feed_outcomes is not None:
                feed_outcomes.append(False)
            continue

        http_status = getattr(parsed, "status", None)
        version = getattr(parsed, "version", None)
        if type(http_status) is int and http_status >= 400:
            logger.warning("%s の取得に失敗しました: HTTP %d", name, http_status)
            if feed_outcomes is not None:
                feed_outcomes.append(False)
            continue
        if version == "" or (parsed.bozo and not parsed.entries):
            logger.warning("%s のフィード形式を確認できませんでした", name)
            if feed_outcomes is not None:
                feed_outcomes.append(False)
            continue

        if feed_outcomes is not None:
            feed_outcomes.append(True)

        feed_new_count = 0
        for entry in parsed.entries:
            link = entry.get("link", "")
            if not link:
                continue

            # 既存エントリとの重複チェック
            if normalize_url(link) in seen_urls:
                continue

            # 日付フィルタ（古い記事の除外）
            published = parse_published_date(entry)
            if published and days_limit:
                try:
                    pub_date = datetime.strptime(published, "%Y-%m-%d").date()
                    if pub_date < cutoff_date:
                        continue
                except ValueError:
                    pass  # 日付形式不一致はフィルタをスキップ（記事は処理継続）

            # QAキーワードフィルタリング（skip_keyword_filter の場合はスキップ）
            if not skip_filter:
                entry_text = get_entry_text(entry)
                if not matches_keywords(entry_text, keywords):
                    continue

            title = entry.get("title", "（タイトル不明）")

            new_articles.append(
                {
                    "blog": name,
                    "company": company,
                    "title": title,
                    "url": link,
                    "published": published,
                    "language": language,
                }
            )
            seen_urls.add(normalize_url(link))
            feed_new_count += 1

        if dry_run:
            logger.info("  → 新着QA記事: %d件", feed_new_count)

    return new_articles


def send_discord_notification(webhook_url: str, articles: list[dict]) -> bool:
    """Discord Webhook にリッチEmbed形式で新着記事を通知する。

    Args:
        webhook_url: Discord Webhook URL
        articles: 新着記事のリスト

    Returns:
        送信成功なら True
    """
    if not articles:
        logger.info("新着記事なし: Discord通知をスキップします")
        return True

    # 10件ずつに分割して送信
    batch_size = 10
    for i in range(0, len(articles), batch_size):
        batch = articles[i : i + batch_size]
        embeds = []
        for article in batch:
            embed = {
                "title": article["title"],
                "url": article["url"],
                "color": 5814783,  # QA Knowledge テーマカラー（青紫）
                "fields": [
                    {"name": "企業", "value": article["company"], "inline": True},
                    {"name": "フィード", "value": article["blog"], "inline": True},
                    {"name": "公開日", "value": article["published"] or "不明", "inline": True},
                ],
                "footer": {"text": "QA Knowledge RSS監視"},
            }
            embeds.append(embed)

        payload = {
            "content": f"新着QA関連記事: {len(articles)}件" if i == 0 else None,
            "embeds": embeds,
        }

        try:
            resp = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=30,
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            status = getattr(getattr(e, "response", None), "status_code", None)
            logger.error(
                "Discord通知の送信に失敗しました: %s (HTTP %s)",
                type(e).__name__,
                status if type(status) is int and 100 <= status <= 599 else "unknown",
            )
            return False

    logger.info("Discord通知を送信しました: %d件", len(articles))
    return True


def format_text(articles: list[dict]) -> str:
    """通常のテキスト形式で出力する。"""
    if not articles:
        return "新着QA関連記事はありません。"

    lines = [f"新着QA関連記事: {len(articles)}件", ""]
    for article in articles:
        lines.append(f"  [{article['blog']}] {article['title']}")
        lines.append(f"    URL: {article['url']}")
        lines.append(f"    公開日: {article['published'] or '不明'}")
        lines.append("")

    return "\n".join(lines)


def format_markdown(articles: list[dict]) -> str:
    """GitHub Issue用のMarkdown形式で出力する。"""
    if not articles:
        return ""

    lines = [
        "## 新着QA関連記事が見つかりました",
        "",
        f"RSSフィード監視により {len(articles)} 件の未収録記事を検出しました。",
        "収録する場合は `python scripts/scaffold.py <URL> --company <企業名>` でエントリを作成してください。",
        "",
        "| ブログ | タイトル | 公開日 |",
        "|--------|---------|--------|",
    ]

    for article in articles:
        title_link = f"[{article['title']}]({article['url']})"
        lines.append(f"| {article['blog']} | {title_link} | {article['published'] or '-'} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    def positive_int(value: str) -> int:
        """非負整数のバリデータ。"""
        n = int(value)
        if n < 0:
            raise argparse.ArgumentTypeError(f"0以上の整数を指定してください: {value}")
        return n

    parser = argparse.ArgumentParser(description="RSSフィードを巡回し、未収録のQA関連記事を検出する。")
    parser.add_argument(
        "--format",
        choices=["text", "markdown", "json"],
        default="text",
        help="出力形式（デフォルト: text）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="各フィードの取得状況を表示する（デバッグ用）",
    )
    parser.add_argument(
        "--days",
        type=positive_int,
        default=365,
        help="この日数以内の記事のみ対象（デフォルト: 365）",
    )
    parser.add_argument(
        "--notify",
        choices=["discord"],
        default=None,
        help="通知先（discord: Discord Webhook で通知）",
    )
    parser.add_argument(
        "--allow-partial-feeds",
        action="store_true",
        help="一部フィードが失敗しても取得済み記事を収集処理へ渡す",
    )
    parser.add_argument("--github-output", type=Path, help="GitHub Actionsの件数・新着判定の出力先")
    args = parser.parse_args()

    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    handler = CredentialRedactingStreamHandler(sys.stderr)
    handler.setFormatter(CredentialRedactingFormatter(webhook_url))
    logging.basicConfig(
        level=logging.DEBUG if args.dry_run else logging.INFO,
        handlers=[handler],
        force=True,
    )

    try:
        config = load_feeds_config()
        errors = validate_feeds_config(config)
        if errors:
            for err in errors:
                logger.error("設定エラー: %s", err)
            return 1

        existing_urls = load_existing_urls()
        if args.dry_run:
            logger.info("既存エントリ: %d件", len(existing_urls))

        feed_outcomes: list[bool] = []
        articles = check_feeds(
            config,
            existing_urls,
            dry_run=args.dry_run,
            days_limit=args.days,
            feed_outcomes=feed_outcomes,
        )
        if feed_outcomes and not any(feed_outcomes):
            logger.error("全フィードの取得に失敗しました")
            return 1

        safe_articles = [
            {
                key: redact_credentials(value, webhook_url) if isinstance(value, str) else value
                for key, value in article.items()
            }
            for article in articles
        ]
        if args.format == "json":
            output = json.dumps(safe_articles, ensure_ascii=False)
        elif args.format == "markdown":
            output = format_markdown(safe_articles)
        else:
            output = format_text(safe_articles)
        if output:
            # JSON のエスケープ後に置換すると構文が壊れるため、フィールドごとに秘匿化済み。
            print(output)

        if args.github_output:
            with args.github_output.open("a", encoding="utf-8") as stream:
                stream.write(f"article_count={len(articles)}\nhas_new_articles={str(bool(articles)).lower()}\n")

        partial = bool(feed_outcomes and not all(feed_outcomes))
        if partial:
            logger.warning("一部フィードの取得に失敗しました")
        exit_code = 1 if partial and not args.allow_partial_feeds else 0
        if args.notify == "discord":
            if args.dry_run:
                logger.info("dry-run: Discord通知をスキップします")
            elif not webhook_url:
                logger.error("DISCORD_WEBHOOK_URL が未設定です。Discord配信は完了していません")
                exit_code = 1
            elif articles and not send_discord_notification(webhook_url, safe_articles):
                exit_code = 1
        return exit_code
    except Exception as exc:
        # サードパーティの例外本文や traceback を Actions ログへ渡さない。
        logger.error("RSS処理に失敗しました: %s", type(exc).__name__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
