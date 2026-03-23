---
title: "Fixing Performance Regressions Before They Happen"
company: "Netflix"
url: "https://netflixtechblog.com/fixing-performance-regressions-before-they-happen-eab2602b86fe"
published_at: "2022-01-24"
content_type: "blog"
qa_domains:
  - "performance-test"
  - "test-automation"
  - "ci-cd"
  - "quality-metrics"
  - "shift-left"
tags:
  - "performance-regression"
  - "anomaly-detection"
  - "changepoint-detection"
  - "statistical-testing"
  - "tv-app"
  - "e-divisive"
language: "en"
added_at: "2026-03-24"
industry: "entertainment"
difficulty: "advanced"
deprecated: false
---

## 概要

NetflixのTVUIチームが、パフォーマンス回帰をリリース前（多くの場合コミット前）に検出するために構築した自動化システムについて解説した記事。約50のパフォーマンステストをPR提出時とマージ時に自動実行し、異常検知（動的閾値による標準偏差ベースの検出）と変化点検出（e-divisiveアルゴリズム）の2つの統計的手法を組み合わせることで、静的閾値時代に90%だった誤検知率を10%まで削減した実践事例を紹介している。

## 何が学べるか

- 静的閾値から動的閾値（直近m回の平均±n標準偏差）への移行により、パフォーマンステストの誤検知率を90%から10%に大幅削減するアプローチ
- 異常検知（リアルタイムの回帰検出）と変化点検出（e-divisiveアルゴリズムによる事後的なトレンド分析）を組み合わせた多層的な検出戦略
- PRごと・マージごとに各テストを3回繰り返し実行し、デバイスノイズを除去して最小値を採用する実践的なテスト設計
- メモリ制約のあるTVデバイスなど低スペック環境でのパフォーマンステスト自動化における具体的な測定指標の選び方（メモリは最大値、応答性は中央値）
- CI/CDパイプラインにパフォーマンステストを統合し、シフトレフトでパフォーマンス回帰を早期発見するNetflixの組織的取り組み

## 関連エントリ

