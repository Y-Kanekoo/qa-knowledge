---
title: "PACT Contract Testing – Because Not Everything Needs Full Integration Tests"
company: "Microsoft"
url: "https://devblogs.microsoft.com/ise/pact-contract-testing-because-not-everything-needs-full-integration-tests/"
published_at: "2025-06-19"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "test-automation"
  - "ci-cd"
tags:
  - "contract-testing"
  - "pact"
  - "consumer-driven-contracts"
  - "microservices"
  - "integration-testing"
  - "spring-boot"
  - "java"
  - "kafka"
  - "pact-broker"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
speaker: "Adam Dougal"
deprecated: false
---

## 概要

マイクロサービス環境において、完全な統合テストが現実的でないケースに対し、Pactを用いたコンシューマ駆動契約テスト（Consumer-Driven Contract Testing）を導入するアプローチを解説している。製造業向け自然言語検索エンジンのPoCプロジェクトを題材に、異なるチームが管理する複数の下流システムとの連携を、ユニットテストに近い速度と手軽さで検証する方法を具体的なJava/Spring Bootコード例とともに示している。

## 何が学べるか

- コンシューマ駆動契約テストの基本概念（コンシューマがAPI契約を定義し、プロバイダがその契約に準拠しているかを検証する仕組み）を理解できる
- Pactのコンシューマ側テスト（`@Pact`アノテーションによる契約定義）とプロバイダ側テスト（`@TestTemplate`による契約検証）の実装方法を学べる
- ユニットテスト・契約テスト・統合テストそれぞれの速度・セットアップ複雑度・カバレッジのトレードオフを比較し、契約テストが中間層として有効である根拠を理解できる
- Pact Brokerによる契約ファイルの集中管理や、Kafkaメッセージブローカーとの契約テストなど、実運用に向けた拡張ポイントを把握できる
- 異なる技術成熟度のチームが混在する環境で、完全な統合テスト環境の構築が困難な場合の現実的なテスト戦略の選択肢を学べる

## 関連エントリ

- [ThoughtWorks - Testing Strategies in a Microservice Architecture](thoughtworks-testing-strategies-microservice-architecture.md)
- [ThoughtWorks - Practical Test Pyramid](thoughtworks-practical-test-pyramid.md)
