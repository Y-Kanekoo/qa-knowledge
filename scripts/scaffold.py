#!/usr/bin/env python3
"""URLからWebページのメタデータを取得し、エントリの骨格ファイルを生成するスクリプト。

HTMLの<title>タグとmetaタグから自動抽出できる情報（タイトル・公開日）を埋め込んだ
テンプレートを drafts/ に出力する。概要や知見は手動で記入してから公開する。
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

try:
    from scripts._http import create_session
    from scripts._url import normalize_url
except ImportError:
    from _http import create_session
    from _url import normalize_url

# モジュールレベルのロガー
logger = logging.getLogger(__name__)

# published_at を推定するためのmetaタグ属性（優先度順）
VERSION = "1.0"

PUBLISHED_META_ATTRS: list[dict[str, str]] = [
    {"property": "article:published_time"},
    {"name": "article:published_time"},
    {"property": "og:article:published_time"},
    {"name": "datePublished"},
    {"name": "date"},
    {"property": "date"},
    {"name": "DC.date.issued"},
    {"itemprop": "datePublished"},
]

# 共通セッション
_session = create_session(timeout=30)  # HTML全文取得のため長めに設定


def parse_args() -> argparse.Namespace:
    """コマンドライン引数をパースする。"""
    parser = argparse.ArgumentParser(
        description="URLからWebページのメタデータを取得し、エントリの骨格ファイルを生成する。"
    )
    parser.add_argument("url", help="対象のURL")
    parser.add_argument(
        "--company",
        default=None,
        help="企業名を指定（HTMLから推定できない場合に使用）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="下書きの出力先を指定（デフォルト: drafts/{company}-{slug}-{URLハッシュ}.md）",
    )
    return parser.parse_args()


def fetch_html(url: str) -> str:
    """URLからHTMLを取得する。"""
    logger.info("URLを取得中: %s", url)
    try:
        response = _session.get(url, timeout=30, headers={
            "User-Agent": f"Mozilla/5.0 (compatible; qa-knowledge-scaffold/{VERSION})"
        })
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error("URLの取得に失敗しました: %s", e)
        if isinstance(e, requests.exceptions.ConnectionError):
            logger.error("  ネットワーク接続を確認してください")
        elif isinstance(e, requests.exceptions.Timeout):
            logger.error("  タイムアウトしました。サイトが遅延している可能性があります")
        sys.exit(1)


def extract_title(soup: BeautifulSoup) -> str:
    """HTMLからタイトルを抽出する。"""
    # og:title を優先
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"].strip()

    # <title> タグにフォールバック
    title_tag = soup.find("title")
    if title_tag and title_tag.string:
        return title_tag.string.strip()

    return ""


def extract_published_at(soup: BeautifulSoup) -> str:
    """HTMLのmetaタグから公開日を抽出する。見つからない場合は空文字を返す。"""
    for attrs in PUBLISHED_META_ATTRS:
        meta = soup.find("meta", attrs=attrs)
        if meta and meta.get("content"):
            content = meta["content"].strip()
            # ISO 8601形式から日付部分を抽出（YYYY-MM-DD）
            match = re.match(r"(\d{4}-\d{2}-\d{2})", content)
            if match:
                return match.group(1)

    # JSON-LD からの抽出を試みる
    for script_tag in soup.find_all("script", type="application/ld+json"):
        try:
            ld_data = json.loads(script_tag.string or "")
            items = ld_data if isinstance(ld_data, list) else [ld_data]
            for item in items:
                for key in ("datePublished", "dateCreated"):
                    if key in item:
                        match = re.match(r"(\d{4}-\d{2}-\d{2})", str(item[key]))
                        if match:
                            return match.group(1)
        except (json.JSONDecodeError, TypeError):
            continue

    return ""


def detect_language(soup: BeautifulSoup) -> str:
    """HTMLのlang属性から言語を推定する。"""
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        lang = html_tag["lang"].lower()
        if lang.startswith("ja"):
            return "ja"
    return "en"


def generate_slug(title: str) -> str:
    """タイトルからURLスラッグを生成する。"""
    # YAMLファイル名に使えるよう、まずASCII外の文字を全て除去する
    slug = re.sub(r"[^\x00-\x7F]+", "", title.lower())
    # ASCII内でも英数字とスペース・アンダースコア・ハイフン以外は除去
    slug = re.sub(r"[^a-z0-9\s_-]", "", slug)
    # スペースをハイフンに変換
    slug = re.sub(r"[\s_]+", "-", slug)
    # 連続するハイフンを1つにまとめる
    slug = re.sub(r"-{2,}", "-", slug)
    # 先頭・末尾のハイフンを除去
    slug = slug.strip("-")
    # 長すぎる場合は切り詰め（末尾のハイフンは除去）
    if len(slug) > 60:
        slug = slug[:60].rstrip("-")
    # 文字が残らない場合はフォールバックを使う
    if not slug:
        slug = "untitled"
    return slug


def generate_output_path(company: str, title: str, entries_dir: str) -> str:
    """ファイル名を自動生成する: {company}-{slug}.md"""
    company_slug = re.sub(r"[^a-z0-9]", "", company.lower())
    title_slug = generate_slug(title)
    filename = f"{company_slug}-{title_slug}.md"
    return os.path.join(entries_dir, filename)


def format_output(
    title: str,
    url: str,
    published_at: str,
    language: str,
    company: str,
) -> str:
    """抽出したメタデータをYAML frontmatter + Markdown骨格に整形する。"""
    today = date.today().isoformat()
    # JSONの文字列リテラルはYAMLでも有効。引用符・改行・backslashを安全に保存する。
    title, company, url, published_at, language = (
        json.dumps(value, ensure_ascii=False) for value in (title, company, url, published_at, language)
    )

    return f"""---
status: draft
title: {title}
company: {company}
url: {url}
published_at: {published_at}
content_type: ""
qa_domains: []
tags: []
language: {language}
added_at: "{today}"
industry: ""
difficulty: ""
deprecated: false
---

## 概要



## 何が学べるか

-

## 関連エントリ

"""


def draft_path(company: str, title: str, url: str, drafts_dir: Path) -> Path:
    """日本語タイトル同士でも衝突しない、URLごとに安定した下書き名。"""
    base = Path(generate_output_path(company, title, str(drafts_dir)))
    digest = hashlib.sha256(normalize_url(url).encode("utf-8")).hexdigest()[:12]
    return base.with_stem(f"{base.stem}-{digest}")


def save_draft(path: Path, content: str) -> None:
    """既存の下書き・編集内容を上書きしない。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(content)


def main() -> None:
    """メインエントリーポイント。"""
    args = parse_args()

    # ロギングの設定
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    # プロジェクトルートの特定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    drafts_dir = Path(project_root) / "drafts"

    # HTMLの取得
    html = fetch_html(args.url)
    soup = BeautifulSoup(html, "html.parser")

    # メタデータの抽出
    title = extract_title(soup)
    published_at = extract_published_at(soup)
    language = detect_language(soup)
    company = args.company or ""

    logger.info("タイトル: %s", title)
    logger.info("公開日: %s", published_at or "（取得できませんでした）")
    logger.info("言語: %s", language)

    # 出力先の決定
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = draft_path(company, title or "untitled", args.url, drafts_dir)

    if output_path.resolve().is_relative_to(Path(project_root) / "entries"):
        logger.error("骨格は entries/ に保存できません。drafts/ で補完してから promote_draft.py を使ってください")
        sys.exit(1)

    # ファイル出力
    content = format_output(title, normalize_url(args.url), published_at, language, company)

    save_draft(output_path, content)

    logger.info("骨格ファイルを生成しました: %s", output_path)
    logger.info("  → content_type, qa_domains, tags, 概要, 何が学べるか を手動で記入してください")


if __name__ == "__main__":
    main()
