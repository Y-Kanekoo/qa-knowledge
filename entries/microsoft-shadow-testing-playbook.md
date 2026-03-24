---
title: "Shadow Testing - Engineering Fundamentals Playbook"
company: "Microsoft"
url: "https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/"
published_at: "2024-09-17"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "reliability"
  - "observability"
tags:
  - "shadow-testing"
  - "testing-in-production"
  - "dark-launching"
  - "traffic-mirroring"
  - "deployment-safety"
language: "en"
added_at: "2026-03-24"
industry: "general"
difficulty: "intermediate"
related_tools:
  - "diffy"
  - "envoy"
  - "keploy"
deprecated: false
---

## 概要

MicrosoftのEngineering Fundamentals Playbookに掲載されたシャドウテスト（シャドウデプロイメント）のガイド。現行バージョンと候補バージョンを並行デプロイし、本番トラフィックを複製して候補環境にも送信するが、候補のレスポンスはユーザーに返さず比較用に収集するという手法を解説している。Diffy（Twitter/Airbnb/Baidu/ByteDanceが使用）をはじめとするツール群も紹介し、本番環境への影響ゼロで新機能のスケーリング挙動やインフラ検証を行う方法を示している。

## 何が学べるか

- シャドウテストの基本アーキテクチャ：現行・候補バージョンの並行デプロイとトラフィック複製・レスポンス比較の仕組み
- ユーザーへの影響ゼロで本番トラフィックパターンを用いた新バージョン検証を実現する手法
- Diffy・Envoy・McRouter・Scientist・Keployなどシャドウテスト向けツールの特徴と使い分け
- 本番環境移行・インフラ検証・スケーリングテストなどシャドウテストが有効なユースケースの判断基準
- 合成テストシナリオの作成が不要になるメリットと、本番規模での実データ検証の利点

## 関連エントリ

- [Google - SRE Book: Testing for Reliability](google-sre-book-testing-reliability.md)
