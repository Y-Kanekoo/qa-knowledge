---
title: "freeeの自動テストの全体構成"
company: "freee"
url: "https://developers.freee.co.jp/entry/automated-test-structure-2022"
published_at: "2022-08-08"
content_type: "blog"
qa_domains: [test-automation, test-strategy, ci-cd]
tags: [test-pyramid, e2e, unit-test, api-test, selenium, jenkins, circleci, browserstack]
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [circleci, jenkins, browserstack, rspec, jest, postman, capybara, mabl, allure, testrail]
deprecated: false
---

## 概要

freeeのSEQ（Software Engineer in Quality）チームが、全社横断で運用している自動テストの全体構成を解説している。ユニットテスト・APIテスト・E2Eテストの3層ピラミッドを基本とし、月間25,000〜35,000シナリオを実行するE2E基盤や、Redashによるテスト成功率モニタリング（目標93〜94%）など、大規模SaaSにおける自動テスト運用の実態が詳述されている。

## 何が学べるか

- 大規模SaaS企業における3層テストピラミッド（Unit / API / E2E）の具体的な構成と各層のツール選定
- テスト作成・メンテナンスの責任分担モデル（コードに最も近い人が担当する原則）
- E2Eテストの並列実行基盤（Jenkins Main/replica構成）とスケーラビリティ確保の手法
- テスト成功率のモニタリングとフレイキーテスト管理の運用プラクティス
- Slack・Allure・TestRail・Jenkinsを組み合わせたテスト結果の可視化戦略

## 関連エントリ


- [freee - ソフトウェアアーキテクチャに基づいた自動テスト戦略と実装ガイドライン](freee-testing-strategy-based-on-software-architecture.md)
- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
- [ThoughtWorks - The Practical Test Pyramid](thoughtworks-practical-test-pyramid.md)
