---
title: "Honeycomb + Tracetest: Observability-Driven Development"
company: "Honeycomb"
url: "https://www.honeycomb.io/blog/honeycomb-tracetest-observability-driven-development"
published_at: "2023-08-24"
content_type: "blog"
qa_domains:
  - "observability"
  - "test-automation"
  - "ci-cd"
tags:
  - "distributed-tracing"
  - "opentelemetry"
  - "tracetest"
  - "microservices"
  - "trace-based-testing"
  - "integration-testing"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

HoneycombとTracetestを組み合わせ、分散トレースデータを活用した統合テスト（トレースベーステスト）を実現する手法を解説する技術ガイド。OpenTelemetry Collectorを介してトレースデータを収集し、APIレスポンスだけでなくマイクロサービス内部の処理に対してもアサーションを定義できるObservability-Driven Development（ODD）のアプローチを、実装手順とともに紹介している。

## 何が学べるか

- トレースベーステストの概念と、従来のAPIテストとの違い（レスポンスだけでなく内部のトレースデータにもアサーションを定義できる利点）
- HoneycombとTracetestの統合セットアップ手順（OpenTelemetry Collectorの構成を含む）
- Observability-Driven Development（ODD）の実践方法：本番のトレースデータから問題を発見し、それをテストケースに落とし込む反復的な改善サイクル
- 分散マイクロサービス環境でのエンドツーエンドなテスト戦略の設計指針
- トレースベーステストをCI/CDパイプラインに組み込み、デプロイ前の品質ゲートとして活用する方法

## 関連エントリ


- [Uber - Shifting E2E Testing Left at Uber](uber-shifting-e2e-testing-left.md)
- [Uber - Simplifying Developer Testing Through SLATE](uber-simplifying-developer-testing-slate.md)
- [freee - E2Eテスト分析基盤としてReportPortalを導入しました](freee-reportportal-e2e-test-analysis.md)
