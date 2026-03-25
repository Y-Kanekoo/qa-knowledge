---
title: "フロントエンドテストの正解って？FAANSにおけるテスト戦略の振り返りとこれから"
company: "ZOZO"
url: "https://techblog.zozo.com/entry/2024-faans-web-test"
published_at: "2025-01-21"
content_type: "blog"
qa_domains: [test-strategy, test-automation, ci-cd, quality-metrics]
tags: [frontend-testing, storybook, chromatic, visual-regression, testing-trophy, msw]
language: "ja"
added_at: "2026-03-24"
industry: "ecommerce"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [Storybook, Chromatic, MSW, SonarQube]
deprecated: false
---

## 概要

ZOZOの社内システムFAANSにおけるフロントエンドテスト戦略を、立ち上げ期・急成長期・現在の3フェーズに分けて振り返り、テスト戦略の進化過程を解説した記事。Storybookのplay関数とChromaticによるビジュアルリグレッションテストを中核に据えた「テスティングトロフィー」型の戦略を構築し、「アプリケーション品質」と「開発品質」を明確に区別する品質観を示している。

## 何が学べるか

- 開発フェーズに応じたテスト戦略の段階的な進化のさせ方（速度優先→信頼性構築→計測と最適化）
- Storybook play関数 + Chromaticを活用したインテグレーションテスト中心のフロントエンドテスト構成
- 「アプリケーション品質」（QAチーム責務）と「開発品質」（開発チーム責務）の区分の考え方
- フレイキーテストへの具体的対処法（タイムアウト延長、バージョンアップ、シャード分割）
- ビジュアルリグレッションテストのコスト管理（PRラベルによるChromatic実行制御、turboSnap活用）

## 関連エントリ


- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
- [Amazon - Going faster with continuous delivery](amazon-going-faster-with-continuous-delivery.md)
- [freee - freeeの自動テストの全体構成](freee-automated-test-structure.md)
