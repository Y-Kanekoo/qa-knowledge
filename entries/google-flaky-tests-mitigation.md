---
title: "Flaky Tests at Google and How We Mitigate Them"
company: "Google"
url: "https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html"
published_at: "2016-05-27"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "ci-cd"
tags:
  - "flaky-tests"
  - "test-reliability"
  - "ci-infrastructure"
  - "test-quarantine"
  - "non-determinism"
language: "en"
added_at: "2026-03-03"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

Googleの大規模テストインフラにおけるフレーキーテスト（同一コードで結果が変わる不安定なテスト）の実態と、その軽減策を解説した記事。全テスト実行の約1.5%がフレーキーな結果を報告し、テスト全体の約16%が何らかのフレーキー性を持つという具体的なスケールの問題が示されている。開発者がテスト失敗を無視する文化が生まれるリスクを指摘し、組織的な検出・隔離・修正のサイクルを構築する重要性を説いている。

## 何が学べるか

- Googleにおけるフレーキーテストの規模感：テスト実行の1.5%がフレーキー、全テストの16%が何らかのフレーキー性を保有、CIのpass→fail遷移の84%がフレーキーテスト起因
- フレーキーの主な原因：非決定的な動作への依存、並行処理の競合、サードパーティコードの不安定性、インフラ起因の問題
- テスト再実行の自動化により一時的なフレーキー失敗を吸収し、3回連続失敗を報告条件にする閾値設計
- フレーキー性が高いテストをクリティカルパスから自動的に隔離（quarantine）するツールの仕組み
- フレーキーテストを放置すると「テスト失敗を無視する文化」が生まれ品質ゲートとしての機能が損なわれるという組織的リスク

## 関連エントリ


- [Meta - Predictive Test Selection: A More Efficient Way to](meta-predictive-test-selection.md)
- [Microsoft - Shift Left to Make Testing Fast and Reliable](microsoft-shift-left-make-testing-fast-reliable.md)
- [Uber - Shifting E2E Testing Left at Uber](uber-shifting-e2e-testing-left.md)
