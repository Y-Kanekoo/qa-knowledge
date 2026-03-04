#!/usr/bin/env python3
"""RSSフィードを巡回し、未収録のQA関連記事を検出するスクリプト。

feeds.yml に定義されたフィードを取得し、entries/ の既存URLと照合して
新着記事をリストアップする。GitHub Actions から週次実行される想定。
"""

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode

import feedparser
import frontmatter
import yaml

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEEDS_FILE = PROJECT_ROOT / "feeds.yml"
ENTRIES_DIR = PROJECT_ROOT / "entries"


def load_feeds_config() -> dict:
    """feeds.yml を読み込む。"""
    with open(FEEDS_FILE, encoding="utf-8") as f:
        return yaml.safe_load(f)


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
        except Exception:
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
            pattern = rf'\b{re.escape(kw)}\b'
            if re.search(pattern, text_lower):
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
    cutoff_date = datetime.now(tz=timezone.utc) - timedelta(days=days_limit)

    for feed_config in feeds:
        name = feed_config["name"]
        feed_url = feed_config["url"]
        company = feed_config["company"]
        language = feed_config.get("language", "en")
        skip_filter = feed_config.get("skip_keyword_filter", False)

        if dry_run:
            print(f"フィードを取得中: {name} ({feed_url})")

        try:
            parsed = feedparser.parse(feed_url)
        except Exception as e:
            print(f"警告: {name} の取得に失敗しました: {e}", file=sys.stderr)
            continue

        if parsed.bozo and not parsed.entries:
            print(f"警告: {name} のパースに問題があります: {parsed.bozo_exception}", file=sys.stderr)
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
                    pub_date = datetime.strptime(published, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                    if pub_date < cutoff_date:
                        continue
                except ValueError:
                    pass

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
            print(f"  → 新着QA記事: {feed_new_count}件")

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
        "--days", type=int, default=365,
        help="この日数以内の記事のみ対象（デフォルト: 365）",
    )
    args = parser.parse_args()

    # 設定と既存URLの読み込み
    config = load_feeds_config()
    existing_urls = load_existing_urls()

    if args.dry_run:
        print(f"既存エントリ: {len(existing_urls)}件")
        print()

    # フィード巡回
    articles = check_feeds(config, existing_urls, dry_run=args.dry_run, days_limit=args.days)

    # 出力
    if args.format == "markdown":
        output = format_markdown(articles)
    else:
        output = format_text(articles)

    if output:
        print(output)

    # 新着がなければ exit 0、あれば exit 0（Issueが必要かどうかは呼び出し側で判断）
    if args.format == "markdown" and not articles:
        # markdown形式で新着なしの場合は空出力（GitHub Actionsで判定に使用）
        pass


if __name__ == "__main__":
    main()
