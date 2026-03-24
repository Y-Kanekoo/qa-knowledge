---
title: "ソフトウェアアーキテクチャに基づいた自動テスト戦略と実装ガイドライン"
company: "freee"
url: "https://developers.freee.co.jp/entry/testing-strategy-based-on-software-architecture"
published_at: "2025-06-16"
content_type: "blog"
qa_domains: [test-strategy, test-automation, shift-left]
tags: [test-architecture, test-pyramid, playwright, unit-test, integration-test, e2e, microservices, clean-architecture]
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "advanced"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [playwright]
deprecated: false
---

## 概要

freeeの経費精算領域のテックリードが、ソフトウェアアーキテクチャの各層に対応した5段階のテスト戦略とその実装ガイドラインを体系的に解説している。Thoughtworksのマイクロサービステスティングアプローチを応用し、Unit・Integration・Backend E2E（In-Process / Out-Process）・Browser E2Eの各層について、速度・保守性・忠実度のトレードオフを明示した上で、フロントエンド・バックエンドそれぞれのアプリケーション層ごとのテスト方針を定めている。

## 何が学べるか

- アーキテクチャ層（Domain / Usecase / Repository / Client / Gateway）ごとに最適なテスト手法を選択する考え方
- 5段階テストレイヤー（Unit〜Browser E2E）の速度・保守性・忠実度のトレードオフ評価
- Backend E2Eを In-Process と Out-Process に分離し、モック注入の柔軟性と本番忠実度を両立する設計
- Playwrightでアクセシビリティベースのセレクタを用いたBrowser E2Eテストの実装方針
- 過剰テストを避けつつコスト効率の高いテスト配置を実現するガイドラインの策定方法

## 関連エントリ

