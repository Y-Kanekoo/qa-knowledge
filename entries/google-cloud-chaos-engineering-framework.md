---
title: "Google Cloud Introduces Chaos Engineering Framework and Recipes for Distributed Systems"
company: "Google"
url: "https://www.infoq.com/news/2025/11/google-chaos-engineering/"
published_at: "2025-11-12"
content_type: "blog"
qa_domains:
  - "reliability"
  - "test-strategy"
tags:
  - "chaos-engineering"
  - "fault-injection"
  - "distributed-systems"
  - "chaos-toolkit"
  - "gcp"
  - "resilience"
language: "en"
added_at: "2026-03-24"
industry: "cloud"
difficulty: "advanced"
related_tools:
  - "chaos-toolkit"
deprecated: false
---

## 概要

Google CloudのExpert Services Teamが公開したカオスエンジニアリングフレームワークとレシピ集を紹介するInfoQ記事。クラウドプロバイダのSLAと組み込み復旧機能だけではアプリケーションの障害耐性を保証できないことを前提に、定常状態仮説の確立・現実的条件の再現・本番環境での実施・自動化・影響範囲の評価という5つの基本原則と6つのベストプラクティスを提示している。OSSのChaos Toolkitを推奨ツールとし、Google Cloud向けのレシピ集もGitHubで公開している。

## 何が学べるか

- Google Cloudが提唱するカオスエンジニアリングの5つの基本原則と、Netflix以外の大規模クラウドプロバイダによる実装アプローチ
- 「コンテナポッド削除がユーザーログインに影響しない」等のテスト仮説策定と定常状態メトリクス（レイテンシー・スループット）の定義方法
- 非本番環境から本番環境への段階的拡張戦略と、直接的・間接的障害注入の使い分け
- OSSフレームワーク「Chaos Toolkit」のPythonベースの実装とGoogle Cloud向けレシピの活用方法
- CI/CDパイプラインへのカオス実験の自動化統合と、結果から実行可能な洞察を導出するプロセス

## 関連エントリ

- [Netflix - Chaos Monkey](netflix-chaosmonkey.md)
- [Netflix - FIT: Failure Injection Testing](netflix-fit-failure-injection-testing.md)
