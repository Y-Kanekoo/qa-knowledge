---
title: "Example Error Budget Policy | Google SRE Workbook Appendix B"
company: "Google"
url: "https://sre.google/workbook/error-budget-policy/"
published_at: "2018-08-01"
content_type: "book_excerpt"
qa_domains:
  - "reliability"
  - "quality-metrics"
tags:
  - "slo"
  - "error-budget"
  - "sre"
  - "postmortem"
  - "release-policy"
language: "en"
added_at: "2026-03-03"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

Google SREワークブック付録Bに掲載されている、エラーバジェットポリシーの具体的な実装例。架空のゲームサービス（Example Game Service）を対象に、SLOとエラーバジェットの定義から、バジェット超過時のリリース停止ルール、ポストモーテムの実施条件までを実践的なポリシー文書として記載している。顧客をSLO違反から保護しつつ、信頼性と機能開発のバランスを取るインセンティブ設計が核心。

## 何が学べるか

- エラーバジェットを「1 - SLO」で計算する具体的な算出方法（99.9% SLOの場合、4週間・100万リクエストで約1,000エラーの余裕）
- 4週間でエラーバジェットを超過した際に「P0問題またはセキュリティ修正以外の変更を全停止」するリリース停止ルールの実装例
- 単一インシデントが4週間のエラーバジェットの20%以上を消費した場合にポストモーテムを義務付け、根本原因に対するP0アクション項目を求める品質管理プロセス
- バックエンド（日次更新）とクライアント（週次更新）で異なる更新頻度に対応したエラーバジェットポリシーの設計方法
- 「信頼性と機能開発のバランスにインセンティブを与える」というエラーバジェットの組織的な活用目的

## 関連エントリ

- [Grafana Labs - Observability Survey 2024](grafana-labs-observability-survey-2024.md)
- [GitLab - Flaky tests management and processes | The GitLab ](gitlab-flaky-tests-management.md)
- [Google - Testing for Reliability | Google SRE Book Chapter ](google-sre-book-testing-reliability.md)
