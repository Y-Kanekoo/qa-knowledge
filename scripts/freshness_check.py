#!/usr/bin/env python3
"""entries/ ディレクトリ内の古いエントリを検出するスクリプト。"""

import argparse
import datetime
import logging
import pathlib
import sys

import frontmatter

logger = logging.getLogger(__name__)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """CLI引数を解析する。"""
    parser = argparse.ArgumentParser(
        description="published_at が指定年数以上前の entries/ エントリを検出する",
    )
    parser.add_argument(
        "--years",
        type=int,
        default=3,
        help="公開から何年以上経過したエントリを検出するか（デフォルト: 3）",
    )
    return parser.parse_args(argv)


def find_entry_files(entries_dir: pathlib.Path) -> list[pathlib.Path]:
    """entries/ ディレクトリ内の .md ファイルを取得する（_template.md を除外）。"""
    files = sorted(entries_dir.glob("*.md"))
    return [file_path for file_path in files if file_path.name != "_template.md"]


def parse_published_at(value: object, filepath: pathlib.Path) -> datetime.date | None:
    """published_at を date に正規化する。"""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError:
            logger.warning("published_at の形式が不正です: %s (%s)", filepath.name, value)
            return None

    logger.warning("published_at の型が不正です: %s (%r)", filepath.name, value)
    return None


def subtract_years(target_date: datetime.date, years: int) -> datetime.date:
    """指定日から年数を引いた日付を返す。"""
    try:
        return target_date.replace(year=target_date.year - years)
    except ValueError:
        # 2/29 を平年に移す場合は 2/28 とする
        return target_date.replace(month=2, day=28, year=target_date.year - years)


def calculate_elapsed_years(
    published_at: datetime.date,
    today: datetime.date,
) -> int:
    """公開日から今日までの経過年数を返す。"""
    years = today.year - published_at.year
    anniversary = subtract_years(today, years)
    if anniversary < published_at:
        years -= 1
    return years


def collect_stale_entries(
    entries_dir: pathlib.Path,
    years: int,
    today: datetime.date | None = None,
) -> list[dict[str, object]]:
    """指定年数以上前に公開されたエントリを収集する。"""
    if today is None:
        today = datetime.date.today()

    cutoff_date = subtract_years(today, years)
    stale_entries: list[dict[str, object]] = []

    for filepath in find_entry_files(entries_dir):
        try:
            post = frontmatter.load(filepath)
        except Exception as exc:
            logger.warning("frontmatter の読み込みに失敗しました: %s (%s)", filepath.name, exc)
            continue

        metadata = post.metadata
        if metadata.get("deprecated", False):
            continue

        published_at = parse_published_at(metadata.get("published_at"), filepath)
        if published_at is None or published_at > cutoff_date:
            continue

        stale_entries.append(
            {
                "filename": filepath.name,
                "title": str(metadata.get("title", "")),
                "company": str(metadata.get("company", "")),
                "published_at": published_at.isoformat(),
                "elapsed_years": calculate_elapsed_years(published_at, today),
            }
        )

    stale_entries.sort(key=lambda entry: (entry["published_at"], entry["filename"]))
    return stale_entries


def format_table(rows: list[dict[str, object]]) -> str:
    """Markdownテーブル形式で結果を整形する。"""
    if not rows:
        return "該当するエントリはありません。"

    lines = [
        "| ファイル名 | タイトル | 企業 | 公開日 | 経過年数 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        title = str(row["title"]).replace("|", "\\|")
        company = str(row["company"]).replace("|", "\\|")
        lines.append(
            f"| {row['filename']} | {title} | {company} | {row['published_at']} | {row['elapsed_years']} |"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """メインエントリーポイント。"""
    args = parse_args(argv)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    if args.years < 0:
        logger.error("--years は 0 以上で指定してください: %s", args.years)
        return 1

    script_dir = pathlib.Path(__file__).resolve().parent
    entries_dir = script_dir.parent / "entries"

    if not entries_dir.is_dir():
        logger.error("entries/ ディレクトリが見つかりません: %s", entries_dir)
        return 1

    rows = collect_stale_entries(entries_dir=entries_dir, years=args.years)
    print(format_table(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
