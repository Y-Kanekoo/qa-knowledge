"""テスト共通フィクスチャ。"""

import sys
from datetime import date
from pathlib import Path

import pytest

# プロジェクトルートを sys.path に追加して scripts/ からインポート可能にする
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --- 共通フィクスチャ ---


@pytest.fixture()
def sample_entry_meta() -> dict:
    """正常な frontmatter 付き MD ファイルの内容を返すフィクスチャ。"""
    return {
        "title": "テスト自動化の実践ガイド",
        "company": "Example Inc.",
        "url": "https://example.com/blog/test-automation",
        "published_at": date(2024, 6, 15),
        "content_type": "blog",
        "qa_domains": ["test-automation", "ci-cd"],
        "tags": ["selenium", "pytest"],
        "language": "ja",
        "added_at": date(2024, 7, 1),
    }


def _build_md_content(meta: dict) -> str:
    """メタデータ辞書から frontmatter 付き Markdown 文字列を生成する。"""
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, date):
            lines.append(f"{key}: {value.isoformat()}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f'{key}: "{value}"')
    lines.append("---")
    lines.append("")
    lines.append("## 概要")
    lines.append("")
    lines.append("テスト用の本文です。")
    return "\n".join(lines)


@pytest.fixture()
def tmp_entries_dir(tmp_path: Path, sample_entry_meta: dict) -> Path:
    """一時 entries/ ディレクトリにサンプル MD ファイルを作成して返すフィクスチャ。"""
    entries_dir = tmp_path / "entries"
    entries_dir.mkdir()

    # サンプルエントリファイルを作成
    md_content = _build_md_content(sample_entry_meta)
    (entries_dir / "example-test-automation.md").write_text(md_content, encoding="utf-8")

    # テンプレートファイル（除外対象）も作成
    (entries_dir / "_template.md").write_text("---\ntitle: template\n---\n", encoding="utf-8")

    return entries_dir
