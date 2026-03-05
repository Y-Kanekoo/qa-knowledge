#!/usr/bin/env python3
"""entries/ ディレクトリ内の .md ファイルのURL死活確認スクリプト。

各エントリの frontmatter にある url フィールドに対して HTTP リクエストを送り、
リンク切れを検出する。
"""

import argparse
import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import frontmatter

try:
    from scripts._http import create_session
except ImportError:
    from _http import create_session

# モジュールレベルのロガー
logger = logging.getLogger(__name__)

# 定数
ENTRIES_DIR = Path(__file__).resolve().parent.parent / "entries"
USER_AGENT = "qa-knowledge-link-checker/1.0"
TIMEOUT_SECONDS = 10
MAX_WORKERS = 5

# モジュールレベルの共通セッション
_session = create_session(timeout=TIMEOUT_SECONDS)


def load_entries() -> list[dict]:
    """entries/ ディレクトリから対象の .md ファイルを読み込み、URLリストを返す。

    _template.md と deprecated: true のエントリはスキップする。
    """
    entries = []
    for md_path in sorted(ENTRIES_DIR.glob("*.md")):
        # テンプレートファイルはスキップ
        if md_path.name == "_template.md":
            continue

        post = frontmatter.load(md_path)
        metadata = post.metadata

        # deprecated なエントリはスキップ
        if metadata.get("deprecated", False):
            continue

        url = metadata.get("url", "")
        if not url:
            continue

        entries.append({
            "filename": md_path.name,
            "url": url,
        })

    return entries


def check_url(entry: dict) -> dict:
    """指定されたエントリのURLにリクエストを送り、結果を返す。

    HEAD リクエストを試み、405等で失敗した場合は GET にフォールバックする。
    """
    filename = entry["filename"]
    url = entry["url"]
    headers = {"User-Agent": USER_AGENT}

    try:
        # まず HEAD リクエストを試行
        response = _session.head(url, headers=headers, timeout=TIMEOUT_SECONDS, allow_redirects=True)

        # HEAD が 405 (Method Not Allowed) 等で失敗した場合は GET にフォールバック
        if response.status_code == 405:
            response = _session.get(url, headers=headers, timeout=TIMEOUT_SECONDS, allow_redirects=True)

        success = 200 <= response.status_code <= 399
        status_text = f"{response.status_code} {response.reason}"

        return {
            "filename": filename,
            "url": url,
            "success": success,
            "status": status_text,
        }

    except Exception as e:
        # タイムアウト・接続エラー等の個別ハンドリング
        import requests as _requests
        if isinstance(e, _requests.exceptions.Timeout):
            status = f"タイムアウト（{TIMEOUT_SECONDS}秒）"
        elif isinstance(e, _requests.exceptions.ConnectionError):
            status = "接続エラー"
        else:
            status = f"リクエストエラー: {e}"

        return {
            "filename": filename,
            "url": url,
            "success": False,
            "status": status,
        }


def run_checks(entries: list[dict]) -> list[dict]:
    """全エントリのURLチェックを並列実行する。"""
    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_entry = {
            executor.submit(check_url, entry): entry
            for entry in entries
        }

        for future in as_completed(future_to_entry):
            results.append(future.result())

    # ファイル名順にソートして返す
    results.sort(key=lambda r: r["filename"])
    return results


def print_normal_output(results: list[dict]) -> None:
    """通常モードの出力を表示する。"""
    total = len(results)
    success_count = sum(1 for r in results if r["success"])
    fail_count = total - success_count

    for result in results:
        mark = "✓" if result["success"] else "✗"
        print(f"{mark} {result['filename']} - {result['status']}")

    print()
    print(f"結果: {total}件中 {success_count}件成功、{fail_count}件失敗")


def print_github_output(results: list[dict]) -> None:
    """GitHub Actions 向けのマシン可読形式で失敗エントリを出力する。"""
    for result in results:
        if not result["success"]:
            print(f"{result['filename']}|{result['status']}|{result['url']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="entries/ 内の .md ファイルのURL死活確認",
    )
    parser.add_argument(
        "--github-output",
        action="store_true",
        help="GitHub Actions 向けのマシン可読形式で出力する",
    )
    args = parser.parse_args()

    # ロギングの設定
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    # エントリ読み込み
    entries = load_entries()

    if not entries:
        logger.info("チェック対象のエントリが見つかりませんでした。")
        sys.exit(0)

    logger.info("URLチェック開始: %d件", len(entries))

    # URLチェック実行
    results = run_checks(entries)

    # 結果出力
    if args.github_output:
        print_github_output(results)
    else:
        print_normal_output(results)

    # 失敗があれば exit code 1
    has_failures = any(not r["success"] for r in results)
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
