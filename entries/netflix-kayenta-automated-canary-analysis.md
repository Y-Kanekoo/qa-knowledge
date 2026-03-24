---
title: "Automated Canary Analysis at Netflix with Kayenta"
company: "Netflix"
url: "https://netflixtechblog.com/automated-canary-analysis-at-netflix-with-kayenta-3260bc7acc69"
published_at: "2018-05-29"
content_type: "blog"
qa_domains:
  - "ci-cd"
  - "reliability"
  - "observability"
tags:
  - "canary-release"
  - "canary-analysis"
  - "kayenta"
  - "spinnaker"
  - "statistical-testing"
  - "deployment-safety"
language: "en"
added_at: "2026-03-24"
industry: "media"
difficulty: "advanced"
related_tools:
  - "kayenta"
  - "spinnaker"
  - "prometheus"
  - "datadog"
deprecated: false
---

## 概要

NetflixとGoogleが共同開発したオープンソースの自動カナリー分析プラットフォーム「Kayenta」の設計と実装を紹介するNetflix Tech Blog記事。Kayentaはユーザー設定のメトリクスをソースから取得し、Mann-Whitney U検定による統計的テストを実行して、カナリーバージョンの0〜100のスコアを算出する。このスコアに基づき自動プロモーション・ロールバック・人間承認パスへの振り分けを行うことで、デプロイの安全性を大幅に向上させている。

## 何が学べるか

- Kayentaのアーキテクチャと、メトリクス取得→統計的比較→スコア算出→判定の自動カナリー分析パイプライン
- Mann-Whitney U検定の信頼区間を用いたカナリー・ベースライン間のメトリクス比較手法と、メトリクス重み付けによる集約スコアリング
- Spinnakerとの統合によるCI/CDパイプライン内でのカナリー分析ステージの組み込み方法
- Stackdriver・Prometheus・Datadog・Atlas等の複数メトリクスソースに対応した拡張可能な設計
- 「success（自動プロモーション）」「marginal（人間承認）」「failure（自動ロールバック）」の3段階判定による段階的リスク管理

## 関連エントリ

- [Amazon - Automating Safe, Hands-Off Deployments](amazon-automating-safe-hands-off-deployments.md)
- [Google - SRE Book: Testing for Reliability](google-sre-book-testing-reliability.md)
