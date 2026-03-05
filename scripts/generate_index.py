#!/usr/bin/env python3
"""
entries/ 内の .md ファイルを読み込み、各種インデックスと index.md を自動生成するスクリプト。

生成対象:
  - indexes/by-company.md （会社別）
  - indexes/by-domain.md  （QA領域別）
  - indexes/by-tag.md     （タグ別）
  - indexes/by-date.md    （追加日順）
  - index.md              （トップページ）
"""

from __future__ import annotations

import logging
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path
from typing import TypedDict

import frontmatter

logger = logging.getLogger(__name__)

# ---------- 定数 ----------

# プロジェクトルート（scripts/ の1つ上）
PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENTRIES_DIR = PROJECT_ROOT / "entries"
INDEXES_DIR = PROJECT_ROOT / "indexes"
INDEX_MD = PROJECT_ROOT / "index.md"

# テンプレートファイルは処理対象外
EXCLUDE_FILES = {"_template.md"}

# 自動生成コメント
AUTO_GENERATED_COMMENT = (
    "<!-- このファイルは generate_index.py によって自動生成されます。"
    "手動編集しないでください -->"
)

# index.md 用の自動更新コメント
INDEX_AUTO_COMMENT = "<!-- このファイルは generate_index.py によって自動更新されます -->"

# content_type の日本語表示名
CONTENT_TYPE_LABELS: dict[str, str] = {
    "blog": "テックブログ",
    "conference_talk": "カンファレンス発表",
    "slide_deck": "スライド",
    "oss_config": "OSS設定例",
    "handbook": "ハンドブック",
    "case_study": "ケーススタディ",
    "book_excerpt": "書籍",
    "podcast": "ポッドキャスト",
    "video": "動画",
}

# 最近追加されたエントリの最大表示件数
RECENT_ENTRIES_LIMIT = 10


# ---------- 型定義 ----------


class EntryMeta(TypedDict):
    """エントリのメタデータ（フロントマターから抽出）。"""

    filename: str
    title: str
    company: str
    url: str
    published_at: str
    content_type: str
    qa_domains: list[str]
    tags: list[str]
    added_at: str


# ---------- ユーティリティ ----------


def _format_date(value: str | date | datetime | None) -> str:
    """日付値を YYYY-MM-DD 文字列に変換する。"""
    if value is None:
        return ""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


def _content_type_label(content_type: str) -> str:
    """content_type コードを日本語表示名に変換する。"""
    return CONTENT_TYPE_LABELS.get(content_type, content_type)


def _index_link(filename: str) -> str:
    """indexes/ ディレクトリからの相対リンクを生成する。"""
    return f"../entries/{filename}"


def _root_link(filename: str) -> str:
    """プロジェクトルートからの相対リンクを生成する。"""
    return f"entries/{filename}"


# ---------- エントリ読み込み ----------


def load_entries() -> list[EntryMeta]:
    """entries/ 内の .md ファイルを読み込み、メタデータのリストを返す。"""
    entries: list[EntryMeta] = []

    if not ENTRIES_DIR.exists():
        return entries

    for md_file in sorted(ENTRIES_DIR.glob("*.md")):
        if md_file.name in EXCLUDE_FILES:
            continue

        post = frontmatter.load(md_file)
        meta = post.metadata

        entry: EntryMeta = {
            "filename": md_file.name,
            "title": meta.get("title", md_file.stem),
            "company": meta.get("company", ""),
            "url": meta.get("url", ""),
            "published_at": _format_date(meta.get("published_at")),
            "content_type": meta.get("content_type", ""),
            "qa_domains": meta.get("qa_domains", []) or [],
            "tags": meta.get("tags", []) or [],
            "added_at": _format_date(meta.get("added_at")),
        }
        entries.append(entry)

    return entries


# ---------- インデックス生成 ----------


def generate_by_company(entries: list[EntryMeta]) -> str:
    """会社別インデックスを生成する。"""
    lines: list[str] = [
        AUTO_GENERATED_COMMENT,
        "",
        "# 会社別インデックス",
        "",
    ]

    if not entries:
        lines.append("エントリがありません。")
        return "\n".join(lines) + "\n"

    # 会社名でグループ化
    by_company: dict[str, list[EntryMeta]] = defaultdict(list)
    for entry in entries:
        company = entry["company"] or "（不明）"
        by_company[company].append(entry)

    # 会社名でソート
    for company in sorted(by_company.keys()):
        group = by_company[company]
        lines.append(f"## {company}")
        lines.append("")
        lines.append("| タイトル | QA領域 | 公開日 | 種別 |")
        lines.append("|---------|--------|--------|------|")
        for entry in sorted(group, key=lambda e: e["published_at"], reverse=True):
            title_link = f"[{entry['title']}]({_index_link(entry['filename'])})"
            domains = ", ".join(entry["qa_domains"])
            published = entry["published_at"]
            content_type = _content_type_label(entry["content_type"])
            lines.append(f"| {title_link} | {domains} | {published} | {content_type} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def generate_by_domain(entries: list[EntryMeta]) -> str:
    """QA領域別インデックスを生成する。"""
    lines: list[str] = [
        AUTO_GENERATED_COMMENT,
        "",
        "# QA領域別インデックス",
        "",
    ]

    if not entries:
        lines.append("エントリがありません。")
        return "\n".join(lines) + "\n"

    # QA領域でグループ化（1エントリが複数の領域に出現可能）
    by_domain: dict[str, list[EntryMeta]] = defaultdict(list)
    for entry in entries:
        for domain in entry["qa_domains"]:
            by_domain[domain].append(entry)

    if not by_domain:
        lines.append("QA領域が設定されたエントリがありません。")
        return "\n".join(lines) + "\n"

    # 領域名でソート
    for domain in sorted(by_domain.keys()):
        group = by_domain[domain]
        lines.append(f"## {domain}")
        lines.append("")
        lines.append("| タイトル | 会社 | 公開日 |")
        lines.append("|---------|------|--------|")
        for entry in sorted(group, key=lambda e: e["published_at"], reverse=True):
            title_link = f"[{entry['title']}]({_index_link(entry['filename'])})"
            lines.append(f"| {title_link} | {entry['company']} | {entry['published_at']} |")
        lines.append("")

    return "\n".join(lines) + "\n"


def generate_by_tag(entries: list[EntryMeta]) -> str:
    """タグ別インデックスを生成する。"""
    lines: list[str] = [
        AUTO_GENERATED_COMMENT,
        "",
        "# タグ別インデックス",
        "",
    ]

    if not entries:
        lines.append("エントリがありません。")
        return "\n".join(lines) + "\n"

    # タグでグループ化（1エントリが複数のタグに出現可能）
    by_tag: dict[str, list[EntryMeta]] = defaultdict(list)
    for entry in entries:
        for tag in entry["tags"]:
            by_tag[tag].append(entry)

    if not by_tag:
        lines.append("タグが設定されたエントリがありません。")
        return "\n".join(lines) + "\n"

    # エントリ数が多いタグを先に表示（同数の場合はタグ名でソート）
    sorted_tags = sorted(by_tag.keys(), key=lambda t: (-len(by_tag[t]), t))

    for tag in sorted_tags:
        group = by_tag[tag]
        lines.append(f"## {tag} ({len(group)})")
        lines.append("")
        for entry in sorted(group, key=lambda e: e["published_at"], reverse=True):
            title_link = f"[{entry['title']}]({_index_link(entry['filename'])})"
            lines.append(f"- {title_link} — {entry['company']}")
        lines.append("")

    return "\n".join(lines) + "\n"


def generate_by_date(entries: list[EntryMeta]) -> str:
    """追加日順インデックスを生成する。"""
    lines: list[str] = [
        AUTO_GENERATED_COMMENT,
        "",
        "# 追加日順インデックス",
        "",
    ]

    if not entries:
        lines.append("エントリがありません。")
        return "\n".join(lines) + "\n"

    # added_at の降順でソート
    sorted_entries = sorted(entries, key=lambda e: e["added_at"], reverse=True)

    lines.append("| 追加日 | タイトル | 会社 | QA領域 |")
    lines.append("|--------|---------|------|--------|")
    for entry in sorted_entries:
        title_link = f"[{entry['title']}]({_index_link(entry['filename'])})"
        domains = ", ".join(entry["qa_domains"])
        lines.append(
            f"| {entry['added_at']} | {title_link} | {entry['company']} | {domains} |"
        )
    lines.append("")

    return "\n".join(lines) + "\n"


def generate_index_md(entries: list[EntryMeta]) -> str:
    """トップページ（index.md）を生成する。"""
    # 統計情報の計算
    total_entries = len(entries)
    companies = {e["company"] for e in entries if e["company"]}
    all_domains: set[str] = set()
    for entry in entries:
        all_domains.update(entry["qa_domains"])

    today = date.today().isoformat()
    last_updated = today if total_entries > 0 else "-"

    lines: list[str] = [
        INDEX_AUTO_COMMENT,
        "",
        "# QA Knowledge - 他社QA事例・ナレッジ集",
        "",
        "テック企業のQA（品質保証）事例・ナレッジを構造化して収集するリポジトリ。",
        "",
        "## 統計",
        "",
        "| 項目 | 数値 |",
        "|------|------|",
        f"| 総エントリ数 | {total_entries} |",
        f"| 収録企業数 | {len(companies)} |",
        f"| QA領域数 | {len(all_domains)} |",
        f"| 最終更新 | {last_updated} |",
        "",
        "## 最近追加されたエントリ",
        "",
    ]

    if not entries:
        lines.append("（エントリ追加後に自動更新されます）")
    else:
        # added_at の降順でソートし、上位N件を表示
        recent = sorted(entries, key=lambda e: e["added_at"], reverse=True)[
            :RECENT_ENTRIES_LIMIT
        ]
        lines.append("| 追加日 | タイトル | 会社 | QA領域 |")
        lines.append("|--------|---------|------|--------|")
        for entry in recent:
            title_link = f"[{entry['title']}]({_root_link(entry['filename'])})"
            domains = ", ".join(entry["qa_domains"])
            lines.append(
                f"| {entry['added_at']} | {title_link} | {entry['company']} | {domains} |"
            )

    lines.extend(
        [
            "",
            "## インデックス",
            "",
            "- [会社別](indexes/by-company.md)",
            "- [QA領域別](indexes/by-domain.md)",
            "- [タグ別](indexes/by-tag.md)",
            "- [追加日順](indexes/by-date.md)",
        ]
    )

    return "\n".join(lines) + "\n"


# ---------- ファイル書き出し ----------


def write_file(path: Path, content: str) -> None:
    """ファイルを書き出す。親ディレクトリが存在しない場合は作成する。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------- メイン ----------


def main() -> None:
    """エントリを読み込み、全インデックスファイルを生成する。"""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    entries = load_entries()

    # 各インデックスファイルを生成
    write_file(INDEXES_DIR / "by-company.md", generate_by_company(entries))
    write_file(INDEXES_DIR / "by-domain.md", generate_by_domain(entries))
    write_file(INDEXES_DIR / "by-tag.md", generate_by_tag(entries))
    write_file(INDEXES_DIR / "by-date.md", generate_by_date(entries))

    # トップページを生成
    write_file(INDEX_MD, generate_index_md(entries))

    print(f"✓ {len(entries)}件のエントリからインデックスを生成しました。")


if __name__ == "__main__":
    main()
