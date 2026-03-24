---
title: "Implementing health checks"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/implementing-health-checks/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "reliability"
  - "observability"
tags:
  - "health-check"
  - "monitoring"
  - "fault-detection"
  - "load-balancing"
  - "distributed-systems"
  - "resilience"
  - "false-positive"
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

サーバーの障害を自動検出・対応するためのヘルスチェック実装について、Amazonでの実経験に基づいて解説したAWS Builders' Libraryの記事。「単一サーバーの障害がシステム全体に過度な悪影響を及ぼすリスク」と「ヘルスチェックの過剰反応がシステム全体停止を引き起こすリスク」のバランスを取る設計原則を示している。バグのあるサーバーがエラーページを高速に返すことでロードバランサーからトラフィックを集中させてしまう「ブラックホール」問題など、現場で遭遇する具体的な障害パターンを豊富に紹介している。

## 何が学べるか

- ヘルスチェックにおける誤検知（false positive）の防止戦略と、「単一の不健康なサーバーからはトラフィックを遮断しつつ、全体的な障害時は許容する」という設計原則
- 独立した障害（ディスク故障、クロックスキュー、メモリリーク）と相関障害（依存関係の停止）を区別して対応するヘルスチェック設計
- バグのあるサーバーがエラーページを高速返却することでトラフィックを集中させる「ブラックホール」問題のメカニズムと防止策
- ヘルスチェックの深さ（shallow vs. deep）のトレードオフと、依存サービスの障害を自サービスの障害として報告するリスク
- 自動化システムがヘルスチェック結果に基づいてサーバーを切り離す際の安全なしきい値設定

## 関連エントリ

- [Amazon - Using load shedding to avoid overload](amazon-using-load-shedding-to-avoid-overload.md)
- [Amazon - Challenges with distributed systems](amazon-challenges-with-distributed-systems.md)
