---
title: "Getting Started With Property-Based Testing in Python With Hypothesis and Pytest"
company: "Semaphore"
url: "https://semaphore.io/blog/property-based-testing-python-hypothesis-pytest"
published_at: "2023-01-19"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "test-strategy"
tags:
  - "property-based-testing"
  - "hypothesis"
  - "pytest"
  - "python"
  - "test-generation"
  - "edge-case"
language: "en"
added_at: "2026-03-24"
industry: "general"
difficulty: "beginner"
related_tools:
  - "hypothesis"
  - "pytest"
deprecated: false
---

## 概要

PythonのHypothesisライブラリとpytestを組み合わせたProperty-Based Testingの実践入門記事。GCD関数やソート関数を題材に、プロパティの定義方法、Hypothesisデコレータの使い方、エッジケースの自動発見までを具体的なコード例とともに段階的に解説している。「Hypothesisは数十から数百のテストを自動生成できる一方、手動では数件しか書かないのが典型的」という生産性の観点も示している。

## 何が学べるか

- Hypothesis + pytestの環境構築から`@given`デコレータによるテストデータ自動生成の実装手順
- GCD関数の「結果が正・両入力を割り切る・それ以上大きい公約数がない」という3つのプロパティ定義の具体例
- ソート関数テストで「長さ同一かつソート済み」だけでは不十分な理由と、`collections.Counter`を用いた要素頻度検証の重要性
- ラウンドトリップ（`int(str(x)) == x`）やファジングなど、Property-Based Testingの代表的なユースケース
- 空リスト・負数・0・辞書キー欠損など、Hypothesisが自動発見する典型的なエッジケースパターン

## 関連エントリ

- [Increment - In Praise of Property-Based Testing](increment-property-based-testing.md)
