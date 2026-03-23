---
title: "Better Android Testing at Airbnb — Part 3: Interaction Testing"
company: "Airbnb"
url: "https://medium.com/airbnb-engineering/better-android-testing-at-airbnb-1d1e91e489b4"
published_at: "2019-09-04"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "mobile-cross-browser"
tags:
  - "android-testing"
  - "interaction-testing"
  - "approval-testing"
  - "espresso"
  - "mvrx"
  - "screenshot-testing"
  - "flaky-tests"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
deprecated: false
---

## 概要

AirbnbのAndroidチームが開発した、UIインタラクション（クリック操作等）の正当性を自動検証するテストフレームワークについて解説した記事。スクリーンショットテストではカバーできないクリックハンドラやViewModel状態変更、ネットワークリクエスト発行などの非視覚的振る舞いを、Approval Testingの手法を用いて自動的に記録・検証する仕組みを紹介している。MvRx（Mavericks）とEspressoを組み合わせ、各画面のインタラクション結果をゴールデンファイルとして管理することで、従来のEspressoテストを手書きせずにリグレッション検知を実現している。

## 何が学べるか

- スクリーンショットテストとインタラクションテストを組み合わせて、UIの見た目と振る舞いの両方を自動検証するアプローチ
- Approval Testing手法をAndroidインタラクションテストに応用し、ゴールデンファイルの差分で変更を検知する設計パターン
- Activity/Fragmentレベルでのメソッドオーバーライドにより、startIntent・finish等のActivity結果を副作用なしに記録するテスト基盤の設計
- 非同期処理（Fragment遷移・View再描画）をブロックまたは待機してからビューをリセットする、フレーキーテスト防止のための同期制御手法
- contentDescriptionの検証によるアクセシビリティテストの自動化への応用

## 関連エントリ

- [Uber - DragonCrawl: Generative AI for High-Quality Mobile Testing](uber-generative-ai-for-high-quality-mobile-testing.md)
- [Google - Flaky Tests at Google and How We Mitigate Them](google-flaky-tests-mitigation.md)
- [LINE - テスト自動化の理論と技術と戦略](line-test-automation-techniques-strategies.md)
