---
title: "Testing for Reliability | Google SRE Book Chapter 17"
company: "Google"
url: "https://sre.google/sre-book/testing-reliability/"
published_at: "2016-04-01"
content_type: "book_excerpt"
qa_domains:
  - "reliability"
  - "test-strategy"
tags:
  - "sre"
  - "reliability-testing"
  - "canary-testing"
  - "mttr"
  - "testing-in-production"
language: "en"
added_at: "2026-03-03"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

Google SREブック第17章「Testing for Reliability」の全文。SREエンジニアがシステムの信頼性を定量化するために古典的なソフトウェアテスト技術を大規模環境でどう適用するかを体系的に解説している。ユニットテストから統合テスト、本番環境でのカナリアテストまでの階層的アプローチ、およびMTTR（平均修復時間）との関係性を論じている。

## 何が学べるか

- ユニットテスト・統合テスト・システムテスト（スモーク・パフォーマンス・回帰）を層状に組み合わせ、本番到達前にバグを検出して「ゼロMTTR」を実現するテスト戦略
- 本番環境での設定テスト・ストレステスト・カナリアテストを組み合わせ、ステージング環境では発見できない構成問題を本番プローブで検出する手法
- Fuzzing・Chaos Monkey・Jepsenなど統計的テスト手法の「反復可能性が必ずしも保証されない」という限界とその対処
- バージョン管理システム・継続的ビルドシステム・定量的なテストカバレッジ目標の設定という、テスト文化確立に必要な基盤の整備手順
- 「テスト成功は確実な信頼性を保証しない」という前提のもと、テスト結果と信頼性指標を組み合わせて判断する姿勢

## 関連エントリ
