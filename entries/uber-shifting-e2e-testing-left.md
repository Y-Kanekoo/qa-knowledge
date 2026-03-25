---
title: "Shifting E2E Testing Left at Uber"
company: "Uber"
url: "https://www.uber.com/blog/shifting-e2e-testing-left/"
published_at: "2024-08-22"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "test-automation"
  - "ci-cd"
  - "reliability"
  - "shift-left"
  - "observability"
tags:
  - "e2e-testing"
  - "microservices"
  - "test-isolation"
  - "flaky-tests"
  - "test-selection"
  - "distributed-tracing"
  - "multi-tenancy"
  - "sandbox-testing"
  - "placebo-execution"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
related_tools:
  - "Cadence"
  - "Apache Kafka"
  - "Jaeger"
  - "OpenTelemetry"
  - "SPIFFE/SPIRE"
deprecated: false
---

## 概要

Uberが1,000以上のマイクロサービスを持つ大規模環境でE2Eテストを「シフトレフト」し、本番デプロイ前に欠陥を検出する仕組み（BITS: Backend Integration Testing Strategy）を構築した事例を解説した記事。分散トレーシングによるインテリジェントなテスト選択、マルチテナンシーによるテスト分離、プラセボ実行によるフレイキーテスト判別など、大規模マイクロサービス環境におけるE2Eテスト基盤の設計と運用を詳述している。この取り組みにより、2023年には1,000 diff あたりのインシデント数が71%減少した。

## 何が学べるか

- 大規模マイクロサービス環境でのE2Eテスト基盤の設計パターン（オンデマンドサンドボックス、ルーティングオーバーライド、ストレージ分離によるテスト隔離）
- 分散トレーシング（Jaeger/OpenTelemetry）を活用したエンドポイントカバレッジの自動追跡と、コード変更に基づくインテリジェントなテスト選択の実装方法
- プラセボ実行（本番ブランチとの並列実行による真理値表）を用いて、フレイキーテスト・壊れたテスト・実際の欠陥を自動判別するアプローチ
- テスト信頼性の定量管理（個別テスト90%以上のパス率、リトライによる99.9%達成、90%未満で自動隔離）と、その運用プロセス
- 設定変更（インシデントの約30%の原因）にもE2Eテストを適用することで、コード変更以外のリグレッションもカバーする戦略

## 関連エントリ

- [Uber - Simplifying Developer Testing Through SLATE](uber-simplifying-developer-testing-slate.md)
- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
- [Meta - Predictive Test Selection: A More Efficient Way to](meta-predictive-test-selection.md)
