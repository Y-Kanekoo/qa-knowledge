---
title: "Avoiding fallback in distributed systems"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "reliability"
  - "test-strategy"
tags:
  - "fallback"
  - "distributed-systems"
  - "resilience"
  - "retry"
  - "failover"
  - "failure-modes"
  - "code-reliability"
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

分散システムにおけるフォールバック戦略がなぜ危険であり、Amazonではほとんど使用されないかを解説したAWS Builders' Libraryの記事。リトライ・プロアクティブリトライ・フェイルオーバー・フォールバックの4つの障害対処戦略を区別し、フォールバックロジックは本番環境の障害状態を正確にシミュレートすることが困難なためテストが極めて難しいという課題を指摘している。プライマリコードの信頼性向上にエンジニアリングリソースを投資する方が、使用頻度の低いフォールバック戦略よりも成功確率が高いというAmazonの設計方針を示している。

## 何が学べるか

- フォールバックロジックが「テスト困難」である理由（本番の障害状態の正確なシミュレーションが困難、メモリ不足状態の再現の難しさなど）
- リトライ・プロアクティブリトライ・フェイルオーバー・フォールバックの4つの障害対処戦略の特性と使い分け
- 「使用頻度の低いコードパスほどバグが潜みやすい」という原則に基づく、フォールバックよりプライマリコードの信頼性に投資する設計判断
- スタートアップ時のヒープメモリ事前割り当てなど、エラー状態でも追加リソース確保に依存しないアーキテクチャ設計
- フォールバックが引き起こすモーダル動作（通常時と障害時で異なる挙動）のテスト・運用上のリスク

## 関連エントリ

- [Amazon - Challenges with distributed systems](amazon-challenges-with-distributed-systems.md)
- [Amazon - Timeouts, retries and backoff with jitter](amazon-timeouts-retries-backoff-with-jitter.md)
