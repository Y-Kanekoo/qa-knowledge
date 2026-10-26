#!/usr/bin/env python3
"""下書きの保存形式を検証する。公開記事の必須値を捏造して補完しない。"""

from pathlib import Path

try:
    from scripts.validate_frontmatter import check_duplicate_urls, find_entry_files, validate_file
except ImportError:
    from validate_frontmatter import check_duplicate_urls, find_entry_files, validate_file


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    drafts = find_entry_files(root / "drafts")
    errors = {path: problems for path in drafts if (problems := validate_file(path, draft=True))}
    # 下書き同士と公開記事との重複も検出する。
    errors.update(check_duplicate_urls(drafts + find_entry_files(root / "entries")))
    for path, problems in errors.items():
        for problem in problems:
            print(f"[ERROR] {path.relative_to(root)}: {problem}")
    if errors:
        return 1
    print(f"✓ {len(drafts)}件の下書きを検証しました（公開記事には含めません）。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
