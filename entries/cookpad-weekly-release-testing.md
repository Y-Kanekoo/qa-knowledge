---
title: "毎週リリースを実現するテスト活動"
company: "Cookpad"
url: "https://techlife.cookpad.com/entry/2018/12/12/120000"
published_at: "2018-12-12"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "ci-cd"
  - "mobile-cross-browser"
tags:
  - "appium"
  - "mobile-testing"
  - "ios"
  - "weekly-release"
  - "parallel-execution"
  - "screenshot-testing"
language: "ja"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [appium, aws-s3]
deprecated: false
---

## 概要

クックパッドの品質向上グループが、iOSアプリの毎週リリースを実現するために行ったテスト活動を紹介した記事。Appiumによるシナリオテスト、手動テスト、探索的テストの3本柱で構成されるリリース前テストを、3〜4営業日から2日間に短縮した改善プロセスが詳述されている。CI専用マシンへの移行やシミュレータ並列実行により、テスト実行時間を3分の1に削減した成果が報告されている。

## 何が学べるか

- モバイルアプリの毎週リリースを支えるテスト戦略の3本柱（自動シナリオテスト・手動テスト・探索的テスト）の構成
- Appiumによる複数iOS端末・バージョン組み合わせでの自動テスト実行手法
- CI専用マシンと並列シミュレータ実行によるテスト時間短縮（実行時間3分の1）の具体策
- スクリーンショット比較のためのAWS S3集中管理とリファレンス画像更新の自動化
- テスト結果の環境横断可視化ツールによる障害分析（実バグか環境不安定かの判定）

## 関連エントリ


- [Mercari - Closing the Visual Testing Gap on Android with Scr](mercari-closing-visual-testing-gap-android-screenshot.md)
- [Airbnb - Better Android Testing at Airbnb — Part 3: Interac](airbnb-better-android-testing-at-airbnb-part-3-interaction.md)
- [freee - 自動テスト速度改善 - 自動テストが品質のボトルネックとならないために](freee-improving-ci-testing-speed.md)
