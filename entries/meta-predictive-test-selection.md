---
title: "Predictive Test Selection: A More Efficient Way to Ensure Reliability of Code Changes"
company: "Meta"
url: "https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/"
published_at: "2018-11-21"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "ci-cd"
  - "shift-left"
  - "ai-testing"
  - "quality-metrics"
  - "reliability"
tags:
  - "predictive-test-selection"
  - "machine-learning"
  - "regression-testing"
  - "gradient-boosted-decision-tree"
  - "test-optimization"
  - "flaky-tests"
  - "test-infrastructure"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
deprecated: false
---

## 概要

Metaが開発した機械学習ベースの予測的テスト選択（Predictive Test Selection）について解説した記事。従来のビルド依存関係に基づくリグレッションテストでは、コード変更に対して推移的に依存する全テストの約4分の1を実行する必要があったが、勾配ブースティング決定木モデルを用いて「そのテストがリグレッションを発見する確率」を予測することで、依存テストの3分の1のみの実行で99.9%以上のリグレッションを検出可能にした。これによりテストインフラの効率を1年で2倍に向上させた。

## 何が学べるか

- 機械学習（勾配ブースティング決定木）を活用したテスト選択の仕組みと、従来の依存関係ベースの手法との違い
- テストインフラのスケーラビリティ課題に対して、確率的アプローチで効率とリグレッション検出率を両立する方法
- フレイキーテストの影響を学習時のリトライ戦略で軽減するテクニック
- モデルの自動再学習により、コードベースの進化に追従し続ける運用設計
- テスト選択の精度（95%以上の正答率）と安全性（99.9%以上のリグレッション検出率）を両立する閾値設計の考え方

## 関連エントリ


- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
- [Uber - Shifting E2E Testing Left at Uber](uber-shifting-e2e-testing-left.md)
- [Netflix - Fixing Performance Regressions Before They Happen](netflix-fixing-performance-regressions.md)
