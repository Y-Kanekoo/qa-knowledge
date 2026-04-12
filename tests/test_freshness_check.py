"""freshness_check.py のユニットテスト。"""

import datetime
from pathlib import Path

from scripts.freshness_check import collect_stale_entries


def _write_entry(
    path: Path,
    *,
    title: str,
    company: str,
    published_at: str,
    deprecated: bool = False,
) -> Path:
    """テスト用の frontmatter 付き Markdown ファイルを作成する。"""
    lines = [
        "---",
        f'title: "{title}"',
        f'company: "{company}"',
        'url: "https://example.com/article"',
        f'published_at: "{published_at}"',
        'content_type: "blog"',
        "qa_domains:",
        "  - test-automation",
        "tags:",
        "  - pytest",
        'language: "ja"',
        'added_at: "2026-04-13"',
        f"deprecated: {'true' if deprecated else 'false'}",
        "---",
        "",
        "本文",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def test_3年以上前のエントリを検出する(tmp_path: Path):
    entries_dir = tmp_path / "entries"
    entries_dir.mkdir()
    _write_entry(
        entries_dir / "old-entry.md",
        title="古い記事",
        company="Example Inc.",
        published_at="2020-04-13",
    )

    rows = collect_stale_entries(
        entries_dir=entries_dir,
        years=3,
        today=datetime.date(2026, 4, 13),
    )

    assert len(rows) == 1
    assert rows[0]["filename"] == "old-entry.md"
    assert rows[0]["elapsed_years"] == 6


def test_deprecated_エントリをスキップする(tmp_path: Path):
    entries_dir = tmp_path / "entries"
    entries_dir.mkdir()
    _write_entry(
        entries_dir / "deprecated-entry.md",
        title="古い非推奨記事",
        company="Example Inc.",
        published_at="2020-04-13",
        deprecated=True,
    )

    rows = collect_stale_entries(
        entries_dir=entries_dir,
        years=3,
        today=datetime.date(2026, 4, 13),
    )

    assert rows == []


def test_3年未満のエントリはリストに含まれない(tmp_path: Path):
    entries_dir = tmp_path / "entries"
    entries_dir.mkdir()
    _write_entry(
        entries_dir / "recent-entry.md",
        title="比較的新しい記事",
        company="Example Inc.",
        published_at="2024-04-14",
    )

    rows = collect_stale_entries(
        entries_dir=entries_dir,
        years=3,
        today=datetime.date(2026, 4, 13),
    )

    assert rows == []
