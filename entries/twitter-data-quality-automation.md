---
title: "Data Quality Automation at Twitter"
company: "Twitter"
url: "https://blog.x.com/engineering/en_us/topics/infrastructure/2022/data-quality-automation-at-twitter"
published_at: "2022-09-15"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "quality-metrics"
  - "observability"
  - "ci-cd"
  - "reliability"
tags:
  - "data-quality"
  - "great-expectations"
  - "apache-airflow"
  - "gcp"
  - "bigquery"
  - "dataflow"
  - "yaml-config"
  - "monitoring"
  - "alerting"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

Twitterが広告・分析・MLプロダクトで使用する数千のデータセットの品質を自動検証するために構築した「Data Quality Platform（DQP）」について解説した記事。Apache Airflow、Great Expectations、GCPサービス（BigQuery・Dataflow・Pub/Sub）を組み合わせたconfig駆動・ワークフローベースのプラットフォームにより、月間1,000万クエリ以上の品質検証を自動化し、新機能リリース時の検証工数を20%削減した事例を紹介している。

## 何が学べるか

- YAML設定ファイルによるconfig駆動のデータ品質ルール定義と、Apache Airflowによるオーケストレーションを組み合わせたスケーラブルな自動検証パイプラインの設計手法
- データの鮮度（freshness）、完全性（completeness）、正確性（accuracy）、一貫性（consistency）の4軸でデータ品質を定量的に測定・監視するアプローチ
- Great Expectationsなどのオープンソースライブラリを活用し、上流・下流データセット間の乖離をアライメントメトリクスで追跡する仕組み
- 400以上の社内顧客データセットに対する品質可視化と、Pub/Sub・Dataflowを用いたリアルタイム品質メトリクス収集・アラートの実装パターン
- エクサバイト規模のデータに対して品質保証を自動化することで、手動検証の属人化・工数負荷を解消した組織的な取り組み

## 関連エントリ

