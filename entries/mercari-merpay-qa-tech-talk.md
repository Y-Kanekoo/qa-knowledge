---
title: "メルペイQAメンバーが明かした「全員品質」のリアルと本音｜merpay QA Tech Talk レポート"
company: "Mercari"
url: "https://engineering.mercari.com/blog/entry/20211109-99b2098e05/"
published_at: "2021-11-10"
content_type: "blog"
qa_domains:
  - "org-design"
  - "test-strategy"
tags:
  - "microservices-qa"
  - "test-automation"
  - "cypress"
  - "team-quality"
  - "autonomous-team"
language: "ja"
added_at: "2026-03-03"
industry: "ecommerce"
difficulty: "intermediate"
deprecated: false
---

## 概要

メルペイのQAエンジニア4名が2021年9月のイベントで各チームの取り組みを語ったレポート記事。マイクロサービス構成のため「チームごとにQAの立ち位置が大きく異なる」という前提のもと、決済基盤・スマート払い・管理画面の各チームが異なるアプローチでQAを実践している実態を紹介している。「全員品質」というミッションのもと、自動化範囲の判断やツール選定をチームが自律的に行う組織文化が共通している。

## 何が学べるか

- QA1名：エンジニア13名という比率の決済基盤チームで、バックエンド領域の自動化を軸に機能テストをカバーする少人数QA運用のアプローチ
- 20名以上のQAが複数マイクロサービスの並行開発を支える大規模チームで、小チーム単位に分割して管理する体制設計
- 仕様検討段階からQAが参加して「テスト設計の精度向上」に注力する上流シフトの実践例
- Cypress（フロントエンド）とScenariogoを主流ツールとした自動化の住み分けと、「メンテナンス性を最優先に自動化対象を戦略的に決定する」判断基準
- 自動化ノウハウの横展開とD&I（多様性推進）を今後の課題として掲げる、QA組織の中長期的な成長戦略

## 関連エントリ
