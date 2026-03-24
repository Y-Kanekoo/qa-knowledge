---
title: "Pocochaで実践するAgile Testing"
company: "DeNA"
url: "https://engineering.dena.com/blog/2023/03/pococha-agile-testing/"
published_at: "2023-03-15"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "test-automation"
  - "shift-left"
tags:
  - "agile-testing"
  - "bdd"
  - "gherkin"
  - "example-mapping"
  - "unit-testing"
  - "metrics"
  - "pococha"
language: "ja"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
speaker: "片山大輝"
deprecated: false
---

## 概要

DeNAのライブコミュニケーションアプリ「Pococha」における、開発終盤テスト集約型から「常にテストし続ける」アジャイルテスト体制への転換を詳述した記事。実例マッピング、Gherkin記法によるシナリオ記述、ユニットテスト必須化の3つのプラクティスを中心に、SWETグループの支援を得ながらチーム全員で品質に責任を持つ体制を構築した過程を紹介している。

## 何が学べるか

- 実例マッピング（Example Mapping）をPdM・PO・QA・開発者が参加して実施し、要件を具体化するBDDプラクティスの導入方法
- Gherkin記法とBRIEFの原則（簡潔性・ビジネス言語使用・実データ利用）に基づくシナリオ記述の実践
- ユニットテスト必須化に際してSWETグループがモブプログラミングで支援し、テスト作成ガイドを整備するアプローチ
- JIRA APIからBigQueryへデータ蓄積しDataStudioでダッシュボード化する、ベロシティ・変更失敗率等のメトリクス管理基盤
- モバイルアプリ開発でのUIテスト自動化の困難さと、BDD「生きたドキュメント」実現を見送った判断の背景

## 関連エントリ

- [DeNA - SWETって一体何者!?](dena-what-is-swet.md)
- [DeNA - 品質管理部門が挑むAI化戦略](dena-qa-ai-strategy.md)
