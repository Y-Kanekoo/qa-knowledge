---
title: "Simplifying Developer Testing Through SLATE"
company: "Uber"
url: "https://www.uber.com/blog/simplifying-developer-testing-through-slate/"
published_at: "2022-10-20"
content_type: "blog"
qa_domains:
  - test-strategy
  - test-automation
  - ci-cd
  - shift-left
  - reliability
  - observability
tags:
  - microservices
  - e2e-testing
  - ephemeral-environments
  - test-isolation
  - developer-experience
  - distributed-systems
language: "en"
added_at: "2026-03-24"
industry: "ride-hailing"
difficulty: "advanced"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools:
  - jaeger
  - kafka
  - cadence
deprecated: false
---

## 概要

Uberが開発したSLATE（Short-Lived Application Testing Environment）は、数千のマイクロサービスで構成される環境においてオンデマンドで短命なE2Eテスト環境を提供するインフラである。テナンシーベースのリクエストルーティングとデータ分離により、本番依存関係を活用しつつテスト安全性を確保し、従来のステージング環境の課題（フレイキーテスト・共有競合・高コスト）を解消するアプローチを解説している。

## 何が学べるか

- マイクロサービス環境における短命テスト環境（エフェメラル環境）の設計パターンと、ステージング環境を置き換えるアーキテクチャ判断の根拠
- Jaeger Baggageを活用したテナンシーベースのリクエストルーティングにより、本番トラフィックとテストトラフィックを安全に分離する手法
- Kafka・Cadenceワークフローなど非同期処理におけるテストデータ分離の具体的な実装戦略
- Cadenceベースのワーカーによる耐障害性のある環境ライフサイクル管理（ビルド・デプロイ・回収の自動化）と制御ループによる状態の整合性維持
- 開発者がモバイルアプリやスクリプトから直接テスト環境を利用できるセルフサービス型テストインフラの設計思想

## 関連エントリ


- [Uber - Shifting E2E Testing Left at Uber](uber-shifting-e2e-testing-left.md)
- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
- [Slack - Automated Accessibility Testing at Slack](slack-automated-accessibility-testing.md)
