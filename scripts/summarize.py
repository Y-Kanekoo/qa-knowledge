#!/usr/bin/env python3
"""URLからWebページを取得し、Claude APIで解析してエントリのドラフト（YAML frontmatter + Markdown本文）を自動生成するスクリプト。"""

import argparse
import json
import os
import re
import sys
from datetime import date

import anthropic
import requests
from bs4 import BeautifulSoup

# --- 許可値定義（validate_frontmatter.py と同期） ---

ALLOWED_CONTENT_TYPES: list[str] = [
    "blog",
    "conference_talk",
    "slide_deck",
    "oss_config",
    "handbook",
    "case_study",
    "book_excerpt",
    "podcast",
    "video",
]

ALLOWED_QA_DOMAINS: list[str] = [
    "test-strategy",
    "test-automation",
    "ci-cd",
    "reliability",
    "quality-metrics",
    "org-design",
    "ai-testing",
    "security-test",
    "performance-test",
    "mobile-cross-browser",
    "shift-left",
    "observability",
]

ALLOWED_INDUSTRIES: list[str] = [
    "tech",
    "finance",
    "ecommerce",
    "media",
    "gaming",
    "saas",
    "other",
]

ALLOWED_DIFFICULTIES: list[str] = [
    "beginner",
    "intermediate",
    "advanced",
]

# メインコンテンツを探すためのセレクタ（優先度順）
CONTENT_SELECTORS: list[str] = [
    "article",
    "main",
    ".post-content",
    ".entry-content",
    ".article-content",
    ".content",
    '[role="main"]',
]

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
        description="URLからWebページを取得し、Claude APIでエントリのドラフトを自動生成する。"
    )
    parser.add_argument("url", help="解析対象のURL")
    parser.add_argument(
        "--company",
        default=None,
        help="企業名を明示的に指定（推定が難しい場合）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="出力先ファイルパスをカスタマイズ（デフォルト: entries/{company}-{slug}.md）",
    )
    return parser.parse_args()


def fetch_html(url: str) -> str:
    """URLからHTMLを取得する。タイムアウト30秒。"""
    print(f"URLを取得中: {url}")
    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "Mozilla/5.0 (compatible; qa-knowledge-summarizer/1.0)"
        })
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"エラー: URLの取得に失敗しました: {e}", file=sys.stderr)
        sys.exit(1)


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
            # 単一オブジェクトまたはリストに対応
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


def extract_body_text(html: str) -> tuple[str, BeautifulSoup]:
    """HTMLから本文テキストを抽出する。BeautifulSoupオブジェクトも返す。"""
    soup = BeautifulSoup(html, "html.parser")

    # 不要なタグを除去
    for tag_name in ["script", "style", "nav", "footer", "header"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # メインコンテンツを優先的に抽出
    content_element = None
    for selector in CONTENT_SELECTORS:
        content_element = soup.select_one(selector)
        if content_element:
            break

    # メインコンテンツが見つからない場合はbody全体を使用
    if content_element is None:
        content_element = soup.find("body")

    if content_element is None:
        # bodyも見つからない場合はHTML全体のテキストを使用
        text = soup.get_text(separator="\n", strip=True)
    else:
        text = content_element.get_text(separator="\n", strip=True)

    # 連続する空行を1つにまとめる
    text = re.sub(r"\n{3,}", "\n\n", text)

    print(f"本文を抽出しました（{len(text)}文字）")
    return text, soup


def build_system_prompt() -> str:
    """Claude APIに送るシステムプロンプトを構築する。"""
    return f"""あなたはQAエンジニアリングの知識ベースのキュレーターです。
与えられたWebページの本文テキストを解析し、以下のフィールドをJSON形式で出力してください。

## 出力フィールド

- title: 記事のタイトル（原文のまま）
- company: 記事を公開した企業名（英語表記）
- content_type: 以下の許可値から1つ選択
  許可値: {json.dumps(ALLOWED_CONTENT_TYPES)}
- qa_domains: 以下の許可値リストから1つ以上選択
  許可値: {json.dumps(ALLOWED_QA_DOMAINS)}
- tags: 記事の内容を表すタグを3〜7個生成。小文字ケバブケース（英数字とハイフンのみ）で記述
- language: 元記事の言語（"en" または "ja"）
- industry: 企業の業種。以下の許可値から1つ選択
  許可値: {json.dumps(ALLOWED_INDUSTRIES)}
- difficulty: 記事の難易度。以下の許可値から1つ選択
  許可値: {json.dumps(ALLOWED_DIFFICULTIES)}
- summary: 記事の概要を2〜3文で記述。必ず日本語で記述すること
- learnings: 「何が学べるか」を3〜5点の箇条書きで記述。必ず日本語で記述すること。
  重要: 抽象的な感想ではなく、記事に書かれた具体的な手法・定量データ・実践的知見を抽出すること

## 出力形式

以下のJSON形式のみを出力してください。説明文やマークダウンのコードブロックは不要です。

{{
  "title": "...",
  "company": "...",
  "content_type": "...",
  "qa_domains": ["..."],
  "tags": ["..."],
  "language": "...",
  "industry": "...",
  "difficulty": "...",
  "summary": "...",
  "learnings": ["...", "..."]
}}"""


def call_claude_api(body_text: str, api_key: str) -> dict:
    """Claude APIを呼び出して解析結果を取得する。"""
    client = anthropic.Anthropic(api_key=api_key)

    # 本文が長すぎる場合は先頭部分に制限（トークン制限対策）
    max_chars = 50000
    truncated_text = body_text[:max_chars]
    if len(body_text) > max_chars:
        truncated_text += "\n\n（以下省略）"

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=build_system_prompt(),
            messages=[
                {
                    "role": "user",
                    "content": f"以下のWebページの本文テキストを解析してください。\n\n{truncated_text}",
                }
            ],
        )
    except anthropic.APIError as e:
        print(f"エラー: Claude APIの呼び出しに失敗しました: {e}", file=sys.stderr)
        sys.exit(1)

    # レスポンスからテキストを取得
    response_text = message.content[0].text

    # JSONをパース（コードブロックで囲まれている場合も対応）
    json_text = response_text.strip()
    # ```json ... ``` の形式を除去
    json_match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", json_text, re.DOTALL)
    if json_match:
        json_text = json_match.group(1).strip()

    try:
        result = json.loads(json_text)
    except json.JSONDecodeError:
        print(
            "エラー: AIのレスポンスをJSONとしてパースできませんでした。"
            "以下のレスポンス全文を確認し、リトライしてください。",
            file=sys.stderr,
        )
        print(f"\n--- レスポンス全文 ---\n{response_text}\n---", file=sys.stderr)
        sys.exit(1)

    print("AIによる解析が完了しました")
    return result


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
    # 長すぎる場合は切り詰め
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
    analysis: dict,
    url: str,
    published_at: str,
    company_override: str | None,
) -> str:
    """解析結果をYAML frontmatter + Markdown本文に整形する。"""
    # 企業名: CLI引数で指定されていればそちらを優先
    company = company_override if company_override else analysis.get("company", "")

    # YAML frontmatterの構築
    # リスト項目を手動でフォーマット（PyYAMLの出力形式を制御するため）
    qa_domains_yaml = "\n".join(f'  - "{d}"' for d in analysis.get("qa_domains", []))
    tags_yaml = "\n".join(f'  - "{t}"' for t in analysis.get("tags", []))

    today = date.today().isoformat()

    # published_at のクォート処理（日付文字列が空の場合は空文字をクォート）
    published_at_value = f'"{published_at}"' if published_at else '""'

    frontmatter = f"""---
title: "{analysis.get("title", "")}"
company: "{company}"
url: "{url}"
published_at: {published_at_value}
content_type: "{analysis.get("content_type", "")}"
qa_domains:
{qa_domains_yaml}
tags:
{tags_yaml}
language: "{analysis.get("language", "")}"
added_at: "{today}"
industry: "{analysis.get("industry", "")}"
difficulty: "{analysis.get("difficulty", "")}"
deprecated: false
---"""

    # Markdown本文の構築
    summary = analysis.get("summary", "")
    learnings = analysis.get("learnings", [])
    learnings_md = "\n".join(f"- {item}" for item in learnings)

    body = f"""
## 概要

{summary}

## 何が学べるか

{learnings_md}

## 関連エントリ

"""

    return frontmatter + "\n" + body


def main() -> None:
    """メインエントリーポイント。"""
    args = parse_args()

    # APIキーの確認
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "環境変数 ANTHROPIC_API_KEY が設定されていません",
            file=sys.stderr,
        )
        sys.exit(1)

    # プロジェクトルートの特定
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    entries_dir = os.path.join(project_root, "entries")

    # 1. HTMLの取得
    html = fetch_html(args.url)

    # 2. 本文テキストの抽出
    body_text, soup = extract_body_text(html)

    # 3. 公開日の抽出
    published_at = extract_published_at(soup)

    # 4. Claude APIで解析
    analysis = call_claude_api(body_text, api_key)

    # 5. 出力ファイルの生成
    company = args.company if args.company else analysis.get("company", "unknown")
    if args.output:
        output_path = args.output
    else:
        output_path = generate_output_path(company, analysis.get("title", "untitled"), entries_dir)

    # 6. Markdownファイルの出力
    content = format_output(analysis, args.url, published_at, args.company)

    # 出力先ディレクトリが存在することを確認
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ ドラフトを生成しました: {output_path}")


if __name__ == "__main__":
    main()
