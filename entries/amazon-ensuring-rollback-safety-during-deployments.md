---
title: "Ensuring rollback safety during deployments"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/ensuring-rollback-safety-during-deployments/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "reliability"
  - "ci-cd"
tags:
  - "rollback-safety"
  - "backward-compatibility"
  - "two-phase-deployment"
  - "protocol-testing"
  - "deployment-verification"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: []
deprecated: false
---

## 概要

Amazonが実践するデプロイのロールバック安全性を保証するためのテスト手法と設計原則を解説した記事。「不可逆な決定を避ける」を基本原則とし、すべてのリビジョンで後方互換性を計画・検証する。プロトコル変更（データ圧縮形式の変更やハートビートタイムアウトの変更など）がロールバック時に引き起こす障害パターンと、それを防ぐための2フェーズデプロイ戦略（Prepare→Activate）を具体例とともに解説している。

## 何が学べるか

- デプロイのロールバック安全性を事前に検証するためのテスト設計手法
- プロトコル変更（シリアライゼーション形式、タイムアウト値など）がローリングアップデート中に引き起こす互換性問題のパターン
- リスクの高い変更を「Prepare（新形式の読み取り対応）」と「Activate（新形式への書き込み切替）」の2段階に分割する安全なデプロイ戦略
- 標準的な機能テストだけでは検出できない、ローリングアップデート中のバージョン混在状態に起因する不具合を検証する方法
- 「すべてのデプロイの前にロールバックの準備を完了させる」という運用原則

## 関連エントリ

- [Amazon - Automating safe, hands-off deployments](amazon-automating-safe-hands-off-deployments.md)
- [Amazon - Going faster with continuous delivery](amazon-going-faster-with-continuous-delivery.md)
