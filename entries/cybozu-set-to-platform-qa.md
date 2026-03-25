---
title: "SETからPlatform QAへ：DevOps推進のための組織再編"
company: "Cybozu"
url: "https://blog.cybozu.io/entry/2024/08/16/121627"
published_at: "2024-08-16"
content_type: "blog"
qa_domains:
  - "org-design"
tags:
  - "platform-engineering"
  - "devops"
  - "kubernetes"
  - "org-restructuring"
  - "platform-quality"
language: "ja"
added_at: "2026-03-03"
industry: "saas"
difficulty: "intermediate"
deprecated: false
---

## 概要

サイボウズのクラウドプラットフォームがKubernetesベースの「Neco」へ移行完了（2021年）した後、従来のSET（Software Engineer in Test）チームをPDX（Platform Developer Experience）とPQM（Platform Quality Management）の2チームに分割した組織再編の記録。開発と運用の分離による遅延という課題に対し、DevOpsアプローチへの転換と認知負荷の削減を目的とした再編の背景・目的・各チームの役割を詳細に説明している。

## 何が学べるか

- 旧来の「開発と運用の分離」体制がKubernetesへの移行後に引き起こした課題（製品関連の問題発生時の対応遅延）と、それを解決するための組織分割の判断プロセス
- PDX（Platform Developer Experience）がPlatform Engineering原則を適用してドキュメント・オンボーディング・ベストプラクティスを提供することで、製品チームの認知負荷を削減するアプローチ
- PQM（Platform Quality Management）がミドルウェアのQAを担いつつ、直接テスト支援から全体的な品質管理へとシフトする役割変化
- 「品質保証は製品が正しく機能することの保証を超え、チームの運用負荷を下げることも含む」という拡張されたQA哲学
- 技術プラットフォーム刷新に伴うチームトポロジーの見直しと、新しい組織構造が定着するまでのプロセス

## 関連エントリ

- [Cybozu - アジャイル型QAの心構え](cybozu-agile-qa-mindset.md)
- [Cybozu - リレーブログ企画：サイボウズ QAエンジニアの取り組み紹介](cybozu-qa-engineer-relay-blog.md)
- [Cybozu - リレーブログ企画：自動テストをQAが実装可能にする取り組み「QAムキムキ化」](cybozu-qa-mukimuki-automation.md)
