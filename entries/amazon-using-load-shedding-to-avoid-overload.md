---
title: "Using load shedding to avoid overload"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "reliability"
  - "performance-test"
  - "observability"
tags:
  - "load-shedding"
  - "overload-protection"
  - "load-testing"
  - "chaos-engineering"
  - "distributed-systems"
  - "resilience"
  - "monitoring"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
speaker: "David Yanacek"
conference: ""
video_url: ""
slide_url: ""
related_tools: []
deprecated: false
---

## 概要

Amazonにおけるオーバーロード回避のための負荷シェディング戦略を解説したAWS Builders' Libraryの記事。「負荷テストを破断点を超えて実施していなければ、サービスは最悪の方法で失敗すると想定すべき」という原則のもと、固定フリート負荷テスト、Chaos Monkey、段階的フリート削減テストなど、限界を超えたテスト手法を具体的に提示している。受け入れるリクエストには低レイテンシーを維持しつつ、超過トラフィックのみを拒否する負荷シェディングの設計原則と、偽陽性率ゼロを目標とした監視の重要性を説いている。

## 何が学べるか

- 「破断点を超えた負荷テスト」の必要性と、固定フリート負荷テスト・Chaos Monkey・段階的フリート削減テストという3つの具体的テスト手法
- タイムアウト時の無駄な処理削減やリトライの連鎖的増幅防止による、正のフィードバックループの遮断メカニズム
- クライアント側の可用性とサーバー側の測定値の両方を追跡することの重要性と、失敗リクエストのレイテンシーをメトリクスから除外すべき理由
- 偽陽性率（容量があるにもかかわらずリクエストを拒否する割合）をゼロに保つ負荷シェディングの品質基準
- 自動スケーリング・負荷シェディング・継続的テストを組み合わせた段階的な保護層によるシステム可用性の維持

## 関連エントリ

- [Amazon - Timeouts, retries and backoff with jitter](amazon-timeouts-retries-backoff-with-jitter.md)
- [Amazon - Challenges with distributed systems](amazon-challenges-with-distributed-systems.md)
