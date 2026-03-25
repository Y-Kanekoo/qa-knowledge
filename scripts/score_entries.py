#!/usr/bin/env python3
"""エントリの品質スコアを算出するスクリプト。

各エントリの概要・学び・タグ・推奨フィールド・関連エントリを評価し、
0-10点のスコアを出力する。
"""

import argparse
import logging
import re
import sys
from pathlib import Path

import frontmatter

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = PROJECT_ROOT / "entries"

# スコアリング基準
MAX_SCORE = 10


def score_entry(filepath: Path) -> dict:
    """単一エントリの品質スコアを算出する。"""
    post = frontmatter.load(filepath)
    metadata = post.metadata
    content = post.content

    score = 0
    details: list[str] = []

    # 1. 概要セクションの文字数（最大2点）
    summary_match = re.search(r"## 概要\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if summary_match:
        summary_text = summary_match.group(1).strip()
        # コメント行を除外
        summary_text = re.sub(r"<!--.*?-->", "", summary_text, flags=re.DOTALL).strip()
        summary_len = len(summary_text)
        if summary_len >= 100:
            score += 2
            details.append(f"概要: {summary_len}字 (+2)")
        elif summary_len >= 50:
            score += 1
            details.append(f"概要: {summary_len}字 (+1)")
        else:
            details.append(f"概要: {summary_len}字 (不足)")
    else:
        details.append("概要: セクションなし")

    # 2. 「何が学べるか」の箇条書き数（最大2点）
    learning_match = re.search(r"## 何が学べるか\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if learning_match:
        learning_text = learning_match.group(1).strip()
        learning_text = re.sub(r"<!--.*?-->", "", learning_text, flags=re.DOTALL).strip()
        bullet_count = len(re.findall(r"^- .+", learning_text, re.MULTILINE))
        if bullet_count >= 5:
            score += 2
            details.append(f"学び: {bullet_count}点 (+2)")
        elif bullet_count >= 3:
            score += 1
            details.append(f"学び: {bullet_count}点 (+1)")
        else:
            details.append(f"学び: {bullet_count}点 (不足)")
    else:
        details.append("学び: セクションなし")

    # 3. タグ数（最大2点）
    tags = metadata.get("tags", [])
    tag_count = len(tags) if isinstance(tags, list) else 0
    if tag_count >= 5:
        score += 2
        details.append(f"タグ: {tag_count}個 (+2)")
    elif tag_count >= 3:
        score += 1
        details.append(f"タグ: {tag_count}個 (+1)")
    else:
        details.append(f"タグ: {tag_count}個 (不足)")

    # 4. industry 記入（1点）
    industry = metadata.get("industry", "")
    if industry and industry != "":
        score += 1
        details.append(f"industry: {industry} (+1)")
    else:
        details.append("industry: 未記入")

    # 5. difficulty 記入（1点）
    difficulty = metadata.get("difficulty", "")
    if difficulty and difficulty != "":
        score += 1
        details.append(f"difficulty: {difficulty} (+1)")
    else:
        details.append("difficulty: 未記入")

    # 6. 関連エントリリンクあり（2点）
    related_match = re.search(r"## 関連エントリ\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if related_match:
        related_text = related_match.group(1).strip()
        related_text = re.sub(r"<!--.*?-->", "", related_text, flags=re.DOTALL).strip()
        link_count = len(re.findall(r"\[.+?\]\(.+?\)", related_text))
        if link_count >= 1:
            score += 2
            details.append(f"関連エントリ: {link_count}件 (+2)")
        else:
            details.append("関連エントリ: リンクなし")
    else:
        details.append("関連エントリ: セクションなし")

    return {
        "file": filepath.name,
        "title": metadata.get("title", ""),
        "company": metadata.get("company", ""),
        "score": min(score, MAX_SCORE),
        "max": MAX_SCORE,
        "details": details,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="エントリの品質スコアを算出する。")
    parser.add_argument(
        "--threshold", type=int, default=0,
        help="このスコア以下のエントリのみ表示（デフォルト: 0=全件表示）",
    )
    parser.add_argument(
        "--detail", action="store_true",
        help="各エントリのスコア詳細を表示する",
    )
    parser.add_argument(
        "--sort", choices=["score", "name"], default="score",
        help="ソート順（デフォルト: score=スコア昇順）",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s", stream=sys.stderr)

    if not ENTRIES_DIR.exists():
        logger.error("entries/ ディレクトリが見つかりません")
        sys.exit(1)

    results: list[dict] = []
    for md_file in sorted(ENTRIES_DIR.glob("*.md")):
        if md_file.name == "_template.md":
            continue
        try:
            result = score_entry(md_file)
            results.append(result)
        except Exception as e:
            logger.warning("%s のスコアリングに失敗: %s", md_file.name, e)

    if not results:
        print("エントリがありません。")
        return

    # ソート
    if args.sort == "score":
        results.sort(key=lambda r: r["score"])
    else:
        results.sort(key=lambda r: r["file"])

    # フィルタ
    if args.threshold > 0:
        results = [r for r in results if r["score"] <= args.threshold]

    # 統計
    total = len(results)
    avg_score = sum(r["score"] for r in results) / total if total else 0
    low_count = sum(1 for r in results if r["score"] <= 4)

    print(f"## 品質スコアレポート（{total}件）")
    print(f"平均スコア: {avg_score:.1f}/{MAX_SCORE}  低スコア（4以下）: {low_count}件")
    print()

    # テーブル表示
    print("| スコア | 企業 | タイトル | ファイル |")
    print("|--------|------|---------|---------|")
    for r in results:
        indicator = "⚠" if r["score"] <= 4 else "✓"
        print(f"| {indicator} {r['score']}/{r['max']} | {r['company']} | {r['title'][:40]} | {r['file']} |")

        if args.detail:
            for d in r["details"]:
                print(f"|  |  | {d} |  |")

    print()
    # スコア分布
    dist = {}
    for r in results:
        dist[r["score"]] = dist.get(r["score"], 0) + 1
    print("スコア分布:")
    for s in range(MAX_SCORE + 1):
        count = dist.get(s, 0)
        bar = "█" * count
        if count > 0:
            print(f"  {s:2d}点: {bar} ({count}件)")


if __name__ == "__main__":
    main()
