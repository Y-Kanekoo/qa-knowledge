#!/usr/bin/env python3
"""RSSフィードを巡回し、未収録のQA関連記事を検出するスクリプト。

feeds.yml に定義されたフィードを取得し、entries/ の既存URLと照合して
新着記事をリストアップする。GitHub Actions から週次実行される想定。
"""

import argparse
import logging
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode

import feedparser
import frontmatter
import yaml

# モジュールレベルのロガー
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = PROJECT_ROOT / "feeds.yml"
ENTRIES_DIR = PROJECT_ROOT / "entries"


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


def load_existing_urls() -> set[str]:
    """entries/ 内の全 .md ファイルから url フィールドを収集する。"""
    urls: set[str] = set()
    if not ENTRIES_DIR.exists():
        return urls

    for md_file in ENTRIES_DIR.glob("*.md"):
        if md_file.name == "_template.md":
            continue
        try:
            post = frontmatter.load(md_file)
            url = post.metadata.get("url", "")
            if url:
                urls.add(normalize_url(url))
        except (yaml.YAMLError, IOError) as e:
            logger.warning("%s の読み込みに失敗: %s", md_file.name, e)
            continue

    return urls


def normalize_url(url: str) -> str:
    """URLを正規化する（スキーム・www・トラッキングパラメータ対応）。"""
    parsed = urlparse(url)
    scheme = "https"
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = parsed.path.rstrip("/")
    # UTM等のトラッキングパラメータを除去
    params = parse_qs(parsed.query, keep_blank_values=True)
    clean_params = {k: v for k, v in params.items()
                    if not k.lower().startswith(("utm_", "fbclid", "gclid"))}
    query = urlencode(clean_params, doseq=True) if clean_params else ""
    normalized = f"{scheme}://{netloc}{path}"
    if query:
        normalized += f"?{query}"
    return normalized


def matches_keywords(text: str, keywords: list[str]) -> bool:
    """テキストにキーワードが含まれるか判定する（単語境界考慮）。"""
    text_lower = text.lower()
    for keyword in keywords:
        kw = keyword.lower()
        # 英語キーワードは単語境界で検索（日本語キーワードは部分一致のまま）
        if kw.isascii():
            # 区切り文字（スペース、ハイフン等）を柔軟にマッチ
            parts = re.split(r'[\s\-_/]+', kw)
            pattern = r'\b' + r'[\s\-_/]+'.join(re.escape(p) for p in parts) + r'\b'
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
                dt = datetime(*parsed[:6], tzinfo=timezone.utc)
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


def check_feeds(config: dict, existing_urls: set[str], dry_run: bool = False, days_limit: int = 365) -> list[dict]:
    """全フィードを巡回し、新着QA関連記事を検出する。"""
    feeds = config.get("feeds", [])
    keywords = config.get("keywords", [])
    new_articles: list[dict] = []

    # 日付フィルタの基準日
    cutoff_date = (datetime.now(tz=timezone.utc) - timedelta(days=days_limit)).date()

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
            logger.warning("%s の取得に失敗しました: %s", name, e)
            continue

        if parsed.bozo and not parsed.entries:
            logger.warning("%s のパースに問題があります: %s", name, parsed.bozo_exception)
            continue

        feed_new_count = 0
        for entry in parsed.entries:
            link = entry.get("link", "")
            if not link:
                continue

            # 既存エントリとの重複チェック
            if normalize_url(link) in existing_urls:
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

            new_articles.append({
                "blog": name,
                "company": company,
                "title": title,
                "url": link,
                "published": published,
                "language": language,
            })
            feed_new_count += 1

        if dry_run:
            logger.info("  → 新着QA記事: %d件", feed_new_count)

    return new_articles


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


def main() -> None:
    def positive_int(value: str) -> int:
        """非負整数のバリデータ。"""
        n = int(value)
        if n < 0:
            raise argparse.ArgumentTypeError(f"0以上の整数を指定してください: {value}")
        return n

    parser = argparse.ArgumentParser(
        description="RSSフィードを巡回し、未収録のQA関連記事を検出する。"
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        help="出力形式（デフォルト: text）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="各フィードの取得状況を表示する（デバッグ用）",
    )
    parser.add_argument(
        "--days", type=positive_int, default=365,
        help="この日数以内の記事のみ対象（デフォルト: 365）",
    )
    args = parser.parse_args()

    # ロギングの設定
    logging.basicConfig(
        level=logging.DEBUG if args.dry_run else logging.INFO,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    # 設定と既存URLの読み込み
    config = load_feeds_config()

    # feeds.yml のバリデーション
    errors = validate_feeds_config(config)
    if errors:
        for err in errors:
            logger.error("設定エラー: %s", err)
        sys.exit(1)

    existing_urls = load_existing_urls()

    if args.dry_run:
        logger.info("既存エントリ: %d件", len(existing_urls))

    # フィード巡回
    articles = check_feeds(config, existing_urls, dry_run=args.dry_run, days_limit=args.days)

    # 出力
    if args.format == "markdown":
        output = format_markdown(articles)
    else:
        output = format_text(articles)

    if output:
        print(output)


if __name__ == "__main__":
    main()
