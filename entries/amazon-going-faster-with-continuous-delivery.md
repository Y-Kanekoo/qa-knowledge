---
title: "Going faster with continuous delivery"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/going-faster-with-continuous-delivery/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "ci-cd"
  - "test-automation"
  - "test-strategy"
tags:
  - "continuous-delivery"
  - "canary-deployment"
  - "synthetic-monitoring"
  - "automated-rollback"
  - "deployment-pipeline"
  - "code-coverage"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: []
deprecated: false
---

## 概要

Amazonが全社的に採用している継続的デリバリーの実践と、その中核をなすテスト戦略を解説した記事。「可用性を最優先、次に速度、そして開発者の利便性」という優先順位のもと、ユニットテスト・統合テスト・pre-productionテスト・本番カナリアデプロイ・合成モニタリングという多層的な品質保証アプローチを採用している。3,000件の正常データポイントを確認してからデプロイを進めるカナリア基準など、データ駆動のデプロイ判断が特徴的である。

## 何が学べるか

- ユニットテスト（スタイルチェック・カバレッジ・複雑度分析を含む）から統合テスト（障害注入・ブラウザ自動化を含む）までの多層テスト設計
- pre-production環境で本番データストアや依存APIとの接続を検証し、本番構成との差異を最小化するテスト環境戦略
- カナリアデプロイで「3,000件の正常データポイント、異常データポイント0件」を達成してから次段階に進むというデータ駆動のデプロイ基準
- 全公開APIに対して毎分以上の頻度で合成トラフィックを生成し、継続的にシステムヘルスを監視する合成モニタリング
- メトリクスベースのデプロイゲートと自動ロールバック機構の組み合わせによる本番品質の担保

## 関連エントリ

- [Amazon - Automating safe, hands-off deployments](amazon-automating-safe-hands-off-deployments.md)
- [Amazon - Ensuring rollback safety during deployments](amazon-ensuring-rollback-safety-during-deployments.md)
