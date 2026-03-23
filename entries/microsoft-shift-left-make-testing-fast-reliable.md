---
title: "Shift Left to Make Testing Fast and Reliable"
company: "Microsoft"
url: "https://learn.microsoft.com/en-us/devops/develop/shift-left-make-testing-fast-reliable"
published_at: "2022-08-18"
content_type: "handbook"
qa_domains:
  - shift-left
  - test-strategy
  - test-automation
  - ci-cd
  - reliability
  - quality-metrics
tags:
  - unit-testing
  - test-taxonomy
  - test-pyramid
  - functional-testing
  - test-reliability
  - testability
  - continuous-integration
  - devops
language: "en"
added_at: "2026-03-24"
industry: "technology"
difficulty: "beginner"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools:
  - "Azure DevOps"
deprecated: false
---

## 概要

MicrosoftのDevOpsチームが提唱するシフトレフト戦略について、テストをL0〜L4の4段階に分類するテスト分類体系と、ユニットテストを中心に据えた品質向上アプローチを解説している。6万件のユニットテストを6分以内に並列実行する実践例や、レガシーテストスイートを2年半かけてモダンなユニットテストへ移行したケーススタディを通じて、テストの高速化・信頼性向上の具体的な方法論を示している。

## 何が学べるか

- テストをL0（高速ユニットテスト）からL4（本番統合テスト）まで分類するDevOpsテスト分類体系の設計方法
- シフトレフト戦略の実践：テストをパイプラインの早い段階に移動し、PRマージ前に大半のテストを完了させるアプローチ
- テスト信頼性の確保原則：UIテストの抑制、機能テストの独立性担保、パブリックAPIのみを使ったテスト設計
- レガシーテストスイートからモダンユニットテストへの段階的移行の進め方（27,000件のレガシーテストを2年半で置換した事例）
- テスト品質をプロダクトコードと同等に扱い、テスタビリティを設計段階から組み込む組織文化の構築

## 関連エントリ

- [Google - Test Sizes](google-test-sizes.md)
- [Google - Flaky Tests at Google and How We Mitigate Them](google-flaky-tests-mitigation.md)
- [Shopify - Spark Joy by Running Fewer Tests](shopify-spark-joy-fewer-tests.md)
