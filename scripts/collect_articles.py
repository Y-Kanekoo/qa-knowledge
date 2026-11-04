#!/usr/bin/env python3
"""RSSのJSON出力を下書きとして保存する。公開記事やインデックスは変更しない。"""

import argparse
import json
import subprocess
from pathlib import Path

import frontmatter

try:
    from scripts._url import normalize_url
    from scripts.check_rss import load_existing_urls
    from scripts.scaffold import draft_path, format_output, save_draft
    from scripts.validate_frontmatter import validate_metadata
except ImportError:
    from _url import normalize_url
    from check_rss import load_existing_urls
    from scaffold import draft_path, format_output, save_draft
    from validate_frontmatter import validate_metadata


def restore_pending_drafts(ref: str, root: Path) -> None:
    """収集ブランチの下書きだけを復元。mainの下書き・公開済みURLを優先する。"""
    files = (
        subprocess.check_output(
            ["git", "ls-tree", "-rz", "--name-only", ref, "--", "drafts/"],
            cwd=root,
        )
        .decode("utf-8")
        .split("\0")
    )
    published = load_existing_urls((root / "entries",))
    for filename in filter(None, files):
        relative = Path(filename)
        if relative.parent != Path("drafts") or relative.suffix != ".md":
            raise ValueError("収集ブランチのdrafts/にはMarkdownファイルだけを保存してください")
        target = root / relative
        if target.exists():
            continue
        content = subprocess.check_output(["git", "show", f"{ref}:{filename}"], cwd=root).decode("utf-8")
        metadata = frontmatter.loads(content).metadata
        if validate_metadata(metadata, draft=True):
            raise ValueError(f"既存の下書きの保存形式が不正です: {filename}")
        if normalize_url(metadata["url"]) not in published:
            save_draft(target, content)


def collect_articles(articles: list[dict], root: Path) -> list[Path]:
    """フィードのメタデータを保存。全入力を検証してから書き込み、既存ファイルは保持する。"""
    if not isinstance(articles, list):
        raise ValueError("RSS入力は記事オブジェクトのJSON配列である必要があります")
    seen = load_existing_urls((root / "entries", root / "drafts"))
    pending: list[tuple[Path, str]] = []
    for article in articles:
        if not isinstance(article, dict):
            raise ValueError("RSS記事はオブジェクトである必要があります")
        for field in ("url", "title", "company", "published", "language"):
            if not isinstance(article.get(field), str):
                raise ValueError(f"RSS記事の {field} は文字列である必要があります")
        url = normalize_url(article["url"])
        if not article["url"].startswith(("https://", "http://")) or not url.split("/", 3)[2]:
            raise ValueError("RSS記事のURLが不正です")
        if url in seen:
            continue
        content = format_output(article["title"], url, article["published"], article["language"], article["company"])
        errors = validate_metadata(frontmatter.loads(content).metadata, draft=True)
        if errors:
            raise ValueError(f"下書きのメタデータが不正です: {errors}")
        path = draft_path(article["company"], article["title"], url, root / "drafts")
        if path.exists():
            raise FileExistsError(f"既存の下書きは上書きしません: {path}")
        pending.append((path, content))
        seen.add(url)
    for path, content in pending:
        save_draft(path, content)
    return [path for path, _ in pending]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input", type=Path)
    source.add_argument("--restore-ref", help="既存収集ブランチの下書きを保持するためのGit ref")
    parser.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    if args.restore_ref:
        restore_pending_drafts(args.restore_ref, root)
        return
    articles = json.loads(args.input.read_text(encoding="utf-8"))
    added = collect_articles(articles, root)
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as stream:
            stream.write(f"added_count={len(added)}\nhas_changes={str(bool(added)).lower()}\n")
    print(f"下書き保存: {len(added)}件（公開記事追加: 0件）")


if __name__ == "__main__":
    main()
