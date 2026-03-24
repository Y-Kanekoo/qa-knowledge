---
title: "自動テストのガイドライン策定によるテスト改善への取り組み"
company: "Cybozu"
url: "https://blog.cybozu.io/entry/2025/07/16/113000"
published_at: "2025-07-16"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "test-automation"
tags:
  - "test-pyramid"
  - "test-guideline"
  - "ui-testing"
  - "unit-testing"
  - "e2e-testing"
  - "kintone"
  - "test-stability"
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "intermediate"
speaker: "堀越"
deprecated: false
---

## 概要

kintone開発チームが数千ケースに及ぶUIテストの不安定さと実行時間の課題に対し、テストピラミッドに基づく自動テストガイドラインを策定した取り組みの報告。E2E-ui、E2E-api、Integration、Unit、VRTの6種類のテストを分類・体系化し、UIテストを94件から52件に約45%削減しながらテスト品質を維持した成果を紹介している。

## 何が学べるか

- テストピラミッドの概念を実際のプロダクト（kintone）に適用する際の具体的な分類方法（E2E-ui、E2E-api、Integration、Unit、VRT）
- UIテスト94件→52件（約45%削減）、実行時間約5分短縮という定量的な改善成果
- テストガイドライン策定により、QAが自律的にテスト実装・修正を進められるようになった組織的効果
- UI操作起因の不安定テストを削減し、テストスイート全体の安定性を向上させるアプローチ
- 新機能開発時にもガイドラインに沿って適切なテスト分類を選択できるようになった波及効果

## 関連エントリ

- [Cybozu - QAエンジニアリレーブログ](cybozu-qa-engineer-relay-blog.md)
- [Cybozu - SETからプラットフォームQAへ](cybozu-set-to-platform-qa.md)
