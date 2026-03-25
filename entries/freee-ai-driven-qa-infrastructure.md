---
title: "AI駆動QA基盤の紹介"
company: "freee"
url: "https://developers.freee.co.jp/entry/ai-driven-qa-infrastructure"
published_at: "2025-12-22"
content_type: "blog"
qa_domains: [ai-testing, test-strategy, test-automation]
tags: [ai-agent, claude-code, roo-code, zephyr-scale, generative-ai, test-process]
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "advanced"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [claude-code, roo-code, zephyr-scale]
deprecated: false
---

## 概要

freeeのAI駆動QA基盤チームが構築した、生成AIエージェント（Claude Code・Roo Code）にQAプロセスを実行させるための基盤を紹介している。標準テストプロセスをYAMLベースのタスク定義に分解し、リスク分析からテスト設計・自動テスト実装までをAIが遂行できるアーキテクチャを解説している。現時点ではAI出力の品質は中堅QAエンジニアに及ばず人間のレビューが必須だが、プロセスの標準化とAI活用の実践的な知見が得られる。

## 何が学べるか

- 生成AIエージェントをQAプロセスに組み込むためのアーキテクチャ設計（リポジトリ構成、タスク定義のYAML化）
- QAプロセスを「入力・機能・出力」に分解してAIのハルシネーションリスクを低減するアプローチ
- スプレッドシートからMarkdownベースのワークフローへ移行することでAIとの親和性を高める手法
- AI駆動QAの現時点での限界と、人間によるレビューの必要性に関する実践的な評価
- 標準テストプロセスの整備がAI活用の前提条件であるという組織的な学び

## 関連エントリ


- [DeNA - AIと開発プロセスの改善チャレンジ](dena-swet-ai-development-process.md)
- [freee - freeeの自動テストの全体構成](freee-automated-test-structure.md)
- [freee - テストアーキテクチャの実践](freee-test-architecture-practice.md)
