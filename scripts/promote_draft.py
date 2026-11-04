#!/usr/bin/env python3
"""補完済み下書きを検証してentries/に移す。公開インデックス生成は別工程。"""

import argparse
import re
from datetime import UTC, datetime
from pathlib import Path

import frontmatter

try:
    from scripts._url import normalize_url
    from scripts.check_rss import load_existing_urls
    from scripts.validate_frontmatter import validate_metadata
except ImportError:
    from _url import normalize_url
    from check_rss import load_existing_urls
    from validate_frontmatter import validate_metadata


def promote_draft(path: Path, root: Path) -> Path:
    path = path.resolve()
    if path.parent != (root / "drafts").resolve() or path.suffix != ".md":
        raise ValueError("drafts/ 直下のMarkdownファイルを指定してください")
    post = frontmatter.load(path)
    if post.get("status") != "draft":
        raise ValueError("status: draft の下書きだけを公開できます")
    post["status"] = "published"
    # 収集日ではなく、実際に公開記事へ移すUTC日付を記録する。
    post["added_at"] = datetime.now(tz=UTC).date().isoformat()
    errors = validate_metadata(post.metadata)
    for heading in ("概要", "何が学べるか"):
        section = re.search(rf"^## {heading}\s*\n(.*?)(?=^## |\Z)", post.content, re.M | re.S)
        if not section or not section[1].strip(" \n\r\t-*"):
            errors.append(f"本文の {heading} を記入してください")
    if errors:
        raise ValueError(f"公開前検証に失敗しました（下書きは保持します）: {errors}")
    existing = load_existing_urls((root / "entries",))
    if normalize_url(post["url"]) in existing:
        raise ValueError("同じURLの記事が公開済みです")
    target = root / "entries" / path.name
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        stream.write(frontmatter.dumps(post) + "\n")
    path.unlink()
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    args = parser.parse_args()
    print(promote_draft(args.draft, Path(__file__).resolve().parent.parent))


if __name__ == "__main__":
    main()
