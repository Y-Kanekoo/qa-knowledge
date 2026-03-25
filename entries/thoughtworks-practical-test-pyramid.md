---
title: "The Practical Test Pyramid"
company: "ThoughtWorks"
url: "https://martinfowler.com/articles/practical-test-pyramid.html"
published_at: "2018-02-26"
content_type: "article"
qa_domains:
  - "test-strategy"
  - "test-automation"
  - "ci-cd"
tags:
  - "test-pyramid"
  - "unit-test"
  - "integration-test"
  - "contract-test"
  - "end-to-end-test"
  - "acceptance-test"
  - "exploratory-testing"
  - "consumer-driven-contract"
  - "microservices"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

Mike Cohnが提唱したテストピラミッドの概念を基に、ユニットテスト・インテグレーションテスト・コントラクトテスト・UIテスト・E2Eテスト・受け入れテスト・探索的テストの各レイヤーを、Spring Bootアプリケーションの具体的なコード例とともに実践的に解説した記事。テストをピラミッドの下層に寄せることで高速なフィードバックループを実現し、上層のテストは重要なユーザージャーニーに限定すべきという原則を、ツールの使い方まで含めて体系的に示している。

## 何が学べるか

- テストピラミッドの各レイヤー（Unit / Integration / Contract / UI / E2E）の役割と適切なテスト数のバランス
- Consumer-Driven Contract（CDC）テストによるマイクロサービス間のインターフェース検証手法（Pactを使用）
- 「solitary」テストと「sociable」テストの違い、およびモックとスタブの使い分け指針
- E2Eテストを最小限に抑えつつ十分な信頼性を確保するためのテスト設計戦略
- テストコードをプロダクションコードと同等の品質で管理し、CIパイプラインに速度順で組み込む実践方法

## 関連エントリ

- [Google - Test Sizes](google-test-sizes.md)
- [Shopify - Spark Joy by Running Fewer Tests](shopify-spark-joy-fewer-tests.md)
- [Microsoft - Shift Left: Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
