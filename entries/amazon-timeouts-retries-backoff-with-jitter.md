---
title: "Timeouts, retries and backoff with jitter"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "reliability"
  - "test-strategy"
  - "performance-test"
tags:
  - "timeout"
  - "retry"
  - "exponential-backoff"
  - "jitter"
  - "distributed-systems"
  - "resilience"
  - "latency"
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

分散システムにおけるタイムアウト、リトライ、エクスポネンシャルバックオフ、ジッターという4つの耐障害性構築ツールを体系的に解説したAWS Builders' Libraryの記事。リトライは「利己的」であり下流サービスに追加負荷をかけるという視点から、トークンバケットによるローカルリトライ制限や、ジッターによるリトライストームの防止など、信頼性を損なわないリトライ戦略の設計原則を示している。

## 何が学べるか

- 接続タイムアウトとリクエストタイムアウトの両方を適切に設定する方法と、p99.9パーセンタイルのレイテンシーメトリクスを基準としたタイムアウト値の決定手法
- リトライが「利己的」に下流サービスへ負荷を増幅させるメカニズムと、トークンバケットによるローカルリトライ制限で負荷増幅を防ぐ設計パターン
- エクスポネンシャルバックオフにジッター（ランダム遅延）を組み合わせることで、クライアント群が同時にリトライするバースト現象（thundering herd）を防止する手法
- DNS・TLSハンドシェイクを含む包括的なタイムアウトカバレッジの必要性と、低すぎるタイムアウト設定が引き起こすリトライ増幅の悪循環

## 関連エントリ

- [Amazon - Using load shedding to avoid overload](amazon-using-load-shedding-to-avoid-overload.md)
- [Amazon - Challenges with distributed systems](amazon-challenges-with-distributed-systems.md)
