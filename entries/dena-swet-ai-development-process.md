---
title: "AIと開発プロセスの改善チャレンジ"
company: "DeNA"
url: "https://engineering.dena.com/blog/2025/10/swet-ai-journey/"
published_at: "2025-10-01"
content_type: "blog"
qa_domains:
  - "ai-testing"
  - "test-automation"
  - "quality-metrics"
tags:
  - "ai-agent"
  - "software-metrics"
  - "mutation-testing"
  - "mobile-testing"
  - "code-review"
  - "traceability"
  - "swet"
language: "ja"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
speaker: "伊藤彰人"
deprecated: false
---

## 概要

DeNAのSWET（Software Engineer in Test）チームが、AI Agentの出力品質を高く保ちながら自律稼働させる仕組みの構築に取り組む4つの施策を解説した記事。ソフトウェアメトリクス活用によるAI生成コード品質向上、モバイルSmoke Test自動化、レビュー効率化、仕様トレーサビリティの確立を通じて、AI時代のテスト・開発プロセス改善を実践している。

## 何が学べるか

- テストカバレッジ・循環的複雑度・重複コード率・ミューテーションスコア等のソフトウェアメトリクスをAI生成コードの品質向上に活用する手法
- mobile-mcp等のツールを用いたAI AgentによるAndroid/iOSアプリのSmoke Test自動化アプローチ
- PR-Agent等のコードレビュー支援ツール導入によるレビュープロセスのAI効率化
- 「仕様ID」を活用して仕様・実装・テストの関連性を明確化し、AIが仕様を正確に認識できる環境を構築するトレーサビリティ戦略
- AI Agentの導入による「人間が修正・確認に時間を費やす」という新たな課題認識と、複数施策の相互作用管理

## 関連エントリ

- [DeNA - SWETって一体何者!?](dena-what-is-swet.md)
- [DeNA - 品質管理部門が挑むAI化戦略](dena-qa-ai-strategy.md)
