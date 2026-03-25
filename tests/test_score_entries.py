"""score_entries.py のユニットテスト。"""

from pathlib import Path

from scripts.score_entries import score_entry


def _create_entry(tmp_path: Path, content: str) -> Path:
    """テスト用エントリファイルを作成する。"""
    filepath = tmp_path / "test-entry.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


class TestScoreEntry:
    """score_entry() のテスト。"""

    def test_全フィールド記入で満点になる(self, tmp_path):
        content = """\
---
title: "テスト記事"
company: "Example"
url: "https://example.com/test"
published_at: "2024-01-01"
content_type: "blog"
qa_domains:
  - "test-automation"
tags:
  - "test"
  - "automation"
  - "ci-cd"
  - "flaky-tests"
  - "e2e"
language: "ja"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
---

## 概要

これはテスト記事の概要です。100文字以上の詳細な概要を記述します。テスト自動化に関する記事で、具体的な手法やツールの使い方を解説しています。定量的なデータも含まれており、実践的な内容が充実しています。CI/CDパイプラインとの統合方法についても詳細に触れられています。

## 何が学べるか

- テスト自動化の基本的なアプローチ
- CI/CDパイプラインへの統合方法
- フレイキーテストの対策手法
- E2Eテストの効率的な設計パターン
- テストカバレッジの改善戦略

## 関連エントリ

- [Google - Test Sizes](google-test-sizes.md)
"""
        result = score_entry(_create_entry(tmp_path, content))
        assert result["score"] == 10

    def test_最低限のエントリで低スコアになる(self, tmp_path):
        content = """\
---
title: "最小エントリ"
company: "Example"
url: "https://example.com/min"
published_at: "2024-01-01"
content_type: "blog"
qa_domains:
  - "test-automation"
tags:
  - "test"
language: "en"
added_at: "2026-03-24"
industry: ""
difficulty: ""
---

## 概要

短い概要。

## 何が学べるか

- 1点のみ
"""
        result = score_entry(_create_entry(tmp_path, content))
        assert result["score"] <= 4

    def test_概要100文字以上で2点加算される(self, tmp_path):
        long_summary = "あ" * 100
        content = f"""\
---
title: "概要テスト"
company: "Example"
url: "https://example.com/summary"
published_at: "2024-01-01"
content_type: "blog"
qa_domains:
  - "test-automation"
tags: []
language: "en"
added_at: "2026-03-24"
---

## 概要

{long_summary}

## 何が学べるか

-
"""
        result = score_entry(_create_entry(tmp_path, content))
        # 概要100字以上で+2
        assert any("概要" in d and "+2" in d for d in result["details"])

    def test_タグ5個以上で2点加算される(self, tmp_path):
        content = """\
---
title: "タグテスト"
company: "Example"
url: "https://example.com/tags"
published_at: "2024-01-01"
content_type: "blog"
qa_domains:
  - "test-automation"
tags:
  - "a"
  - "b"
  - "c"
  - "d"
  - "e"
language: "en"
added_at: "2026-03-24"
---

## 概要

概要テスト。

## 何が学べるか

-
"""
        result = score_entry(_create_entry(tmp_path, content))
        assert any("タグ" in d and "+2" in d for d in result["details"])

    def test_関連エントリリンクで2点加算される(self, tmp_path):
        content = """\
---
title: "関連テスト"
company: "Example"
url: "https://example.com/related"
published_at: "2024-01-01"
content_type: "blog"
qa_domains:
  - "test-automation"
tags: []
language: "en"
added_at: "2026-03-24"
---

## 概要

概要テスト。

## 何が学べるか

-

## 関連エントリ

- [Google - Test Sizes](google-test-sizes.md)
"""
        result = score_entry(_create_entry(tmp_path, content))
        assert any("関連エントリ" in d and "+2" in d for d in result["details"])
