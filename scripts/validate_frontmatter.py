#!/usr/bin/env python3
"""entries/ ディレクトリ内の .md ファイルの YAML frontmatter をバリデーションするスクリプト。"""

import re
import sys
from datetime import date
from pathlib import Path

import frontmatter

# --- 許可値定義 ---

ALLOWED_CONTENT_TYPES: set[str] = {
    "blog",
    "conference_talk",
    "slide_deck",
    "oss_config",
    "handbook",
    "case_study",
    "book_excerpt",
    "podcast",
    "video",
}

ALLOWED_QA_DOMAINS: set[str] = {
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
}

ALLOWED_LANGUAGES: set[str] = {"en", "ja"}

# ケバブケースの正規表現（小文字英数字とハイフンのみ）
KEBAB_CASE_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def validate_file(filepath: Path) -> list[str]:
    """単一ファイルの frontmatter をバリデーションし、エラーメッセージのリストを返す。"""
    errors: list[str] = []

    try:
        post = frontmatter.load(filepath)
    except Exception as e:
        errors.append(f"frontmatter の読み込みに失敗しました: {e}")
        return errors

    metadata = post.metadata

    # --- 必須フィールドの存在チェックと型・値の検証 ---

    # title: string（空でない）
    title = metadata.get("title")
    if title is None:
        errors.append("必須フィールド 'title' がありません")
    elif not isinstance(title, str) or not title.strip():
        errors.append("'title' は空でない文字列である必要があります")

    # company: string（空でない）
    company = metadata.get("company")
    if company is None:
        errors.append("必須フィールド 'company' がありません")
    elif not isinstance(company, str) or not company.strip():
        errors.append("'company' は空でない文字列である必要があります")

    # url: string（https:// で始まる）
    url = metadata.get("url")
    if url is None:
        errors.append("必須フィールド 'url' がありません")
    elif not isinstance(url, str) or not url.strip():
        errors.append("'url' は空でない文字列である必要があります")
    elif not url.startswith("https://"):
        errors.append(f"'url' は https:// で始まる必要があります: {url}")

    # published_at: date（ISO 8601形式 YYYY-MM-DD）
    published_at = metadata.get("published_at")
    if published_at is None:
        errors.append("必須フィールド 'published_at' がありません")
    elif isinstance(published_at, date):
        # python-frontmatter が自動的に date オブジェクトに変換する場合がある
        # date 型は有効なのでバリデーションOK（何もしない）
        pass
    elif isinstance(published_at, str):
        if not _is_valid_date(published_at):
            errors.append(
                f"'published_at' は YYYY-MM-DD 形式の日付である必要があります: {published_at}"
            )
    else:
        errors.append(
            f"'published_at' は YYYY-MM-DD 形式の日付である必要があります: {published_at}"
        )

    # content_type: string（許可値リストに含まれる）
    content_type = metadata.get("content_type")
    if content_type is None:
        errors.append("必須フィールド 'content_type' がありません")
    elif not isinstance(content_type, str) or not content_type.strip():
        errors.append("'content_type' は空でない文字列である必要があります")
    elif content_type not in ALLOWED_CONTENT_TYPES:
        errors.append(
            f"'content_type' の値が不正です: '{content_type}' "
            f"(許可値: {', '.join(sorted(ALLOWED_CONTENT_TYPES))})"
        )

    # qa_domains: list[string]（1つ以上、各値が許可値リストに含まれる）
    qa_domains = metadata.get("qa_domains")
    if qa_domains is None:
        errors.append("必須フィールド 'qa_domains' がありません")
    elif not isinstance(qa_domains, list) or len(qa_domains) == 0:
        errors.append("'qa_domains' は1つ以上の要素を持つリストである必要があります")
    else:
        for domain in qa_domains:
            if domain not in ALLOWED_QA_DOMAINS:
                errors.append(
                    f"'qa_domains' に不正な値が含まれています: '{domain}' "
                    f"(許可値: {', '.join(sorted(ALLOWED_QA_DOMAINS))})"
                )

    # tags: list[string]（1つ以上、各値が小文字ケバブケース）
    tags = metadata.get("tags")
    if tags is None:
        errors.append("必須フィールド 'tags' がありません")
    elif not isinstance(tags, list) or len(tags) == 0:
        errors.append("'tags' は1つ以上の要素を持つリストである必要があります")
    else:
        for tag in tags:
            if not isinstance(tag, str) or not KEBAB_CASE_RE.match(tag):
                errors.append(
                    f"'tags' の値はケバブケース（小文字英数字とハイフンのみ）である必要があります: '{tag}'"
                )

    # language: string（"en" or "ja"）
    language = metadata.get("language")
    if language is None:
        errors.append("必須フィールド 'language' がありません")
    elif language not in ALLOWED_LANGUAGES:
        errors.append(
            f"'language' の値が不正です: '{language}' (許可値: {', '.join(sorted(ALLOWED_LANGUAGES))})"
        )

    # added_at: date（ISO 8601形式 YYYY-MM-DD）
    added_at = metadata.get("added_at")
    if added_at is None:
        errors.append("必須フィールド 'added_at' がありません")
    elif isinstance(added_at, date):
        # date 型は有効なのでバリデーションOK（何もしない）
        pass
    elif isinstance(added_at, str):
        if not _is_valid_date(added_at):
            errors.append(
                f"'added_at' は YYYY-MM-DD 形式の日付である必要があります: {added_at}"
            )
    else:
        errors.append(
            f"'added_at' は YYYY-MM-DD 形式の日付である必要があります: {added_at}"
        )

    return errors


def _is_valid_date(value: str) -> bool:
    """文字列が YYYY-MM-DD 形式の有効な日付かどうかを判定する。"""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return False
    try:
        year, month, day = value.split("-")
        date(int(year), int(month), int(day))
        return True
    except ValueError:
        return False


def find_entry_files(entries_dir: Path) -> list[Path]:
    """entries/ ディレクトリ内の .md ファイルを取得する（_template.md を除外）。"""
    files = sorted(entries_dir.glob("*.md"))
    return [f for f in files if f.name != "_template.md"]


def check_duplicate_urls(files: list[Path]) -> dict[Path, list[str]]:
    """複数ファイル間での URL 重複をチェックする。"""
    url_to_files: dict[str, list[Path]] = {}
    errors_by_file: dict[Path, list[str]] = {}

    for filepath in files:
        try:
            post = frontmatter.load(filepath)
        except Exception:
            # ファイル読み込みエラーは validate_file 側で報告するのでここではスキップ
            continue

        url = post.metadata.get("url")
        if isinstance(url, str) and url.strip():
            url_to_files.setdefault(url, []).append(filepath)

    # 重複している URL を報告
    for url, filepaths in url_to_files.items():
        if len(filepaths) > 1:
            filenames = [f.name for f in filepaths]
            for filepath in filepaths:
                msg = (
                    f"URL が重複しています: {url} "
                    f"(重複ファイル: {', '.join(filenames)})"
                )
                errors_by_file.setdefault(filepath, []).append(msg)

    return errors_by_file


def main() -> int:
    """メインエントリーポイント。"""
    # プロジェクトルートを基準に entries/ ディレクトリを特定
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent
    entries_dir = project_root / "entries"

    if not entries_dir.is_dir():
        print(f"エラー: entries/ ディレクトリが見つかりません: {entries_dir}", file=sys.stderr)
        return 1

    # CLI引数の処理: 指定ファイルのみ or 全エントリ
    if len(sys.argv) > 1:
        # 指定されたファイルのみ検証
        target_files: list[Path] = []
        for arg in sys.argv[1:]:
            filepath = Path(arg).resolve()
            if not filepath.exists():
                print(f"エラー: ファイルが見つかりません: {arg}", file=sys.stderr)
                return 1
            target_files.append(filepath)
        # 重複URLチェック用に全エントリファイルも取得
        all_files = find_entry_files(entries_dir)
    else:
        # 全エントリを検証
        target_files = find_entry_files(entries_dir)
        all_files = target_files

    if not target_files:
        print("検証対象のエントリファイルがありません。", file=sys.stderr)
        return 0

    # 各ファイルのバリデーション
    has_errors = False
    file_errors: dict[Path, list[str]] = {}

    for filepath in target_files:
        errors = validate_file(filepath)
        if errors:
            file_errors[filepath] = errors

    # 重複URLチェック（全エントリファイル対象）
    duplicate_errors = check_duplicate_urls(all_files)
    for filepath in target_files:
        if filepath in duplicate_errors:
            file_errors.setdefault(filepath, []).extend(duplicate_errors[filepath])

    # エラー出力
    for filepath, errors in file_errors.items():
        relative_path = filepath.relative_to(project_root)
        for error in errors:
            print(f"{relative_path}: {error}", file=sys.stderr)
        has_errors = True

    if has_errors:
        return 1

    print(f"\u2713 {len(target_files)}件のエントリを検証しました。エラーはありません。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
