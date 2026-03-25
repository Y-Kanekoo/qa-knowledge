---
title: "テスト自動化の理論と技術と戦略：LINE Developer Meetup Tokyo #39 - Testing & Engineering"
company: "LINE"
url: "https://engineering.linecorp.com/ja/blog/test-automation-techniques-strategies-line-developer-meetup-tokyo-39/"
published_at: "2018-07-08"
content_type: "blog"
qa_domains:
  - "test-automation"
tags:
  - "test-pyramid"
  - "ci-cd"
  - "agile-testing"
  - "qa-strategy"
  - "mttr"
language: "ja"
added_at: "2026-03-03"
industry: "tech"
difficulty: "beginner"
deprecated: false
---

## 概要

LINE株式会社が開催したDeveloper Meetup Tokyo #39のレポート記事。テスト自動化とアジャイル開発の融合をテーマに、学術理論・技術実装・戦略立案の3つの視点から実践的な知見を共有している。QAの役割をプロダクト開発ライフサイクル全体に広げる考え方と、テスト施策をビジネスKPIに紐付けて評価するアプローチを紹介している。

## 何が学べるか

- 「3回以上繰り返し実行するテストは自動化すべき」という具体的な自動化判断基準
- テスト施策を「売上・利益・従業員満足度」の3つのビジネスKPIで評価する考え方
- テストピラミッド戦略：実行速度の速い単体テストでカバレッジを積み上げ、時間コストの高いE2Eテストを削減する設計方針
- GitHubへのプッシュをトリガーにした自動テスト実行によりMTTR（平均修復時間）を短縮するCI/CD統合パターン
- QAエンジニアが「品質保証」の枠を超えてプロダクト開発ライフサイクル全体に貢献するロール拡張の考え方

## 関連エントリ


- [Ariga - Testing Data Migrations](atlasgo-testing-data-migrations.md)
- [Cybozu - 自動テストのガイドライン策定によるテスト改善への取り組み](cybozu-automated-test-guidelines.md)
- [DeNA - Pocochaで実践するAgile Testing](dena-pococha-agile-testing.md)
