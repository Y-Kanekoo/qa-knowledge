#!/usr/bin/env python3
"""URLからWebページのメタデータを取得し、エントリの骨格ファイルを生成するスクリプト。

HTMLの<title>タグとmetaタグから自動抽出できる情報（タイトル・公開日）を埋め込んだ
テンプレートを entries/ に出力する。概要や知見は手動で記入する。
"""

import argparse
import json
import os
import re
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup

# published_at を推定するためのmetaタグ属性（優先度順）
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
        help="出力先ファイルパスをカスタマイズ（デフォルト: entries/{company}-{slug}.md）",
    )
    return parser.parse_args()


def fetch_html(url: str) -> str:
    """URLからHTMLを取得する。"""
    print(f"URLを取得中: {url}")
    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; qa-knowledge-scaffold/1.0)"
        })
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"エラー: URLの取得に失敗しました: {e}", file=sys.stderr)
        if isinstance(e, requests.exceptions.ConnectionError):
            print("  ネットワーク接続を確認してください", file=sys.stderr)
        elif isinstance(e, requests.exceptions.Timeout):
            print("  タイムアウトしました。サイトが遅延している可能性があります", file=sys.stderr)
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
    # 英数字とスペース・ハイフン以外を除去
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    # スペースをハイフンに変換
    slug = re.sub(r"[\s_]+", "-", slug)
    # 連続するハイフンを1つにまとめる
    slug = re.sub(r"-{2,}", "-", slug)
    # 先頭・末尾のハイフンを除去
    slug = slug.strip("-")
    # 長すぎる場合は切り詰め（末尾のハイフンは除去）
    if len(slug) > 60:
        slug = slug[:60].rstrip("-")
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
    published_at_value = f'"{published_at}"' if published_at else '""'

    return f"""---
title: "{title}"
company: "{company}"
url: "{url}"
published_at: {published_at_value}
content_type: ""
qa_domains: []
tags: []
language: "{language}"
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


def main() -> None:
    """メインエントリーポイント。"""
    args = parse_args()

    # プロジェクトルートの特定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    entries_dir = os.path.join(project_root, "entries")

    # HTMLの取得
    html = fetch_html(args.url)
    soup = BeautifulSoup(html, "html.parser")

    # メタデータの抽出
    title = extract_title(soup)
    published_at = extract_published_at(soup)
    language = detect_language(soup)
    company = args.company or ""

    print(f"タイトル: {title}")
    print(f"公開日: {published_at or '（取得できませんでした）'}")
    print(f"言語: {language}")

    # 出力先の決定
    if args.output:
        output_path = args.output
    elif company:
        output_path = generate_output_path(company, title or "untitled", entries_dir)
    else:
        slug = generate_slug(title or "untitled")
        output_path = os.path.join(entries_dir, f"{slug}.md")

    # ファイル出力
    content = format_output(title, args.url, published_at, language, company)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ 骨格ファイルを生成しました: {output_path}")
    print("  → content_type, qa_domains, tags, 概要, 何が学べるか を手動で記入してください")


if __name__ == "__main__":
    main()
