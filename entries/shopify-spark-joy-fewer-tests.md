---
title: "Spark Joy by Running Fewer Tests"
company: "Shopify"
url: "https://shopify.engineering/spark-joy-by-running-fewer-tests"
published_at: "2020-06-11"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "test-strategy"
tags:
  - "test-selection"
  - "dynamic-analysis"
  - "monolith"
  - "ci-optimization"
  - "call-graph"
language: "en"
added_at: "2026-03-03"
industry: "ecommerce"
difficulty: "advanced"
deprecated: false
---

## 概要

15万件以上のテストを持つShopifyの大規模モノリシックリポジトリで、テストスイートの実行時間が30〜40分に達する問題を解決するために、変更コードに関連するテストのみを動的に選択するシステムを導入した事例を紹介した記事。Rubyの動的言語特性により静的解析や機械学習ではなく動的コール解析が最適解として採用されており、99.94%のテスト検出率を維持しながらコンピュートコストを25%削減している。

## 何が学べるか

- 動的分析によるテスト選択システムの仕組み：ファイルのコールグラフを記録してテストマッピングを生成し、変更ファイルに関連するテストのみを実行する手法
- 静的解析・機械学習・水平スケーリング・動的分析の4アプローチを比較評価した結果、Rubyのような動的言語では動的分析が最適であるという判断基準
- テスト検出率99.94%を達成しながら全テストの約60%のみを実行し、約40%のビルドで20%未満のテストしか実行しないという具体的な数値
- コンピュートコスト25%削減という定量的な成果と、20〜30%の年間成長率を抱えるテストスイートのスケーラビリティ問題への対応
- 全テスト成功をマージ必須条件にしている大規模モノリスにおいて、テスト選択によってDXを損なわずにビルド時間を短縮する設計思想

## 関連エントリ


- [Uber - Shifting E2E Testing Left at Uber](uber-shifting-e2e-testing-left.md)
- [Amazon - Going faster with continuous delivery](amazon-going-faster-with-continuous-delivery.md)
- [Ariga - Testing Data Migrations](atlasgo-testing-data-migrations.md)
