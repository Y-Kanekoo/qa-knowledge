#!/usr/bin/env python3
"""既存記事とナビゲーション文書だけを MkDocs の入力へ配置する。"""

import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SITE_DOCS_DIR = ".site-docs"
SITE_DOCS_MARKER = ".gitkeep"

# nav の参照先と、従来の docs_dir にあった非 nav 文書を保持する。
STATIC_PAGES = (
    "index.md",
    "indexes/by-company.md",
    "indexes/by-domain.md",
    "indexes/by-tag.md",
    "indexes/by-date.md",
    "docs/regression-test-automation-guide.md",
    "docs/book-report-software-testing-basics.md",
    "docs/book-report-test-technique-drill.md",
    "docs/schema.md",
    "docs/review-report.md",
)


def prepare_site_docs(project_root: Path = PROJECT_ROOT) -> list[Path]:
    """限定した Markdown を元の相対配置のまま複製する。"""
    static_pages = [Path(name) for name in STATIC_PAGES]
    entries = sorted(
        path.relative_to(project_root)
        for path in (project_root / "entries").glob("*.md")
        if path.name != "_template.md"
    )
    if not entries:
        raise ValueError("公開対象の記事がありません")

    pages = static_pages + entries
    for relative_path in pages:
        source = project_root / relative_path
        if source.is_symlink() or not source.is_file():
            raise ValueError(f"公開用文書を確認できません: {relative_path}")

    target_root = project_root / SITE_DOCS_DIR
    if target_root.is_symlink():
        raise ValueError("公開用文書の配置先がシンボリックリンクです")
    if target_root.exists():
        marker = target_root / SITE_DOCS_MARKER
        if marker.is_symlink():
            raise ValueError("公開用文書の目印がシンボリックリンクです")
        marker_bytes = marker.read_bytes() if marker.is_file() else None
        existing = list(target_root.rglob("*"))
        existing_files = {path.relative_to(target_root) for path in existing if path.is_file() and path != marker}
        if any(path.is_symlink() for path in existing) or existing_files != set(pages):
            shutil.rmtree(target_root)
            if marker_bytes is not None:
                target_root.mkdir()
                marker.write_bytes(marker_bytes)

    for relative_path in pages:
        target = target_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        source = project_root / relative_path
        if not target.exists() or target.read_bytes() != source.read_bytes():
            shutil.copyfile(source, target)
    return pages


if __name__ == "__main__":
    print(f"公開用文書を準備しました: {len(prepare_site_docs())}件")
