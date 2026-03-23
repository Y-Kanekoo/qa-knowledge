---
title: "Closing the Visual Testing Gap on Android with Screenshot Tests"
company: "Mercari"
url: "https://engineering.mercari.com/en/blog/entry/20231224-closing-the-visual-testing-gap-on-android-with-screenshot-tests/"
published_at: "2023-12-16"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "mobile-cross-browser"
  - "ci-cd"
tags:
  - "visual-regression-testing"
  - "screenshot-testing"
  - "android-testing"
  - "paparazzi"
  - "reg-suit"
  - "jetpack-compose"
  - "design-system"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

MercariのAndroidチームが、UIコンポーネントの視覚的リグレッションを自動検出するためにスクリーンショットテストを導入した事例を解説した記事。Paparazziフレームワークを採用し、reg-suitによるCI/CDパイプラインでの差分レポート生成を組み合わせることで、手動テストでは見落としがちなUI変更を効率的に検知する仕組みを構築している。Jetpack Composeベースのデザインシステムコンポーネントを対象に約9ヶ月運用し、リファクタリングの信頼性向上やPRレビューの効率化といった効果を報告している。

## 何が学べるか

- Androidスクリーンショットテストフレームワーク（Paparazzi vs Shot）の選定基準と、実行速度・開発体験を重視した意思決定プロセス
- Paparazzi + reg-suitを組み合わせたCI/CDパイプライン構成（スクリーンショット生成→集約→差分レポート生成）の実装パターン
- ライト/ダークモード同時キャプチャなど、カスタムラッパーによるテスト記述の簡素化アプローチ
- デザインシステムコンポーネントからスクリーンショットテストを段階的に導入し、フィーチャー画面へ拡大していく展開戦略
- ビジュアルテストフレームワークのエコシステム変化（Roborazzi等の登場）を踏まえた定期的な再評価の重要性

## 関連エントリ

- [Airbnb - Better Android Testing at Airbnb — Part 3: Interaction Testing](airbnb-better-android-testing-at-airbnb-part-3-interaction.md)
