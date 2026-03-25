---
title: "Automated Accessibility Testing at Slack"
company: "Slack"
url: "https://slack.engineering/automated-accessibility-testing-at-slack/"
published_at: "2025-01-07"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "test-strategy"
  - "ci-cd"
  - "shift-left"
tags:
  - "accessibility"
  - "a11y"
  - "axe-core"
  - "playwright"
  - "wcag"
  - "e2e-testing"
  - "developer-experience"
language: "en"
added_at: "2026-03-24"
industry: "saas"
difficulty: "intermediate"
deprecated: false
---

## 概要

SlackがPlaywright E2Eテストにaxe-coreを組み込み、アクセシビリティテストを自動化した実践事例を紹介した記事。WCAG 2.1 Level A/AAに準拠するための自動チェックをCI/CDパイプライン（Buildkite）に統合し、違反検出からJiraチケット自動作成までのワークフローを構築している。自動テストは手動テストや障害当事者によるレビューを補完する位置付けであり、開発者体験を重視したカスタムPlaywrightフィクスチャによる低摩擦な導入アプローチが特徴的である。

## 何が学べるか

- PlaywrightのE2Eテストにaxe-coreを統合してアクセシビリティチェックを自動化する具体的な実装手法と、Locatorオブジェクト設計に起因するフレームワーク統合の技術的課題への対処法
- `A11Y_ENABLE`フラグによるオンデマンド実行・日次スケジュール実行・CI統合の3モード運用と、非ブロッキングから段階的に導入する戦略
- 違反検出からSlackワークフロー経由でのJiraチケット自動作成まで、トリアージと追跡を効率化するレポーティングパイプラインの設計
- 自動テストの限界を認識した上で、外部の専門手動テスターや障害当事者の早期関与と組み合わせる包括的なアクセシビリティテスト戦略
- カスタムPlaywrightフィクスチャによる開発者向けAPIの簡素化と、重複チェック排除やcriticalレベルフィルタリングによるノイズ低減の工夫

## 関連エントリ


- [Uber - Simplifying Developer Testing Through SLATE](uber-simplifying-developer-testing-slate.md)
- [Uber - Shifting E2E Testing Left at Uber](uber-shifting-e2e-testing-left.md)
- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
