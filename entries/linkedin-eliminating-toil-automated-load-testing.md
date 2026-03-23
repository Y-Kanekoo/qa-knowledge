---
title: "Eliminating Toil with Fully Automated Load Testing"
company: "LinkedIn"
url: "https://engineering.linkedin.com/blog/2019/eliminating-toil-with-fully-automated-load-testing"
published_at: "2019-12-06"
content_type: "blog"
qa_domains:
  - "performance-test"
  - "test-automation"
  - "reliability"
  - "observability"
tags:
  - "load-testing"
  - "traffic-shifting"
  - "capacity-planning"
  - "toil-elimination"
  - "site-reliability"
  - "automated-ramping"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
deprecated: false
---

## 概要

LinkedInが負荷テストを手動運用から完全自動化へ移行した取り組みを解説した記事。合成トラフィックではなく、本番の実トラフィックをデータセンター間でリダイレクト（TrafficShift）することでQPS容量を計測する手法を採用しており、3段階のランピング（75%→90%→目標QPS）とウォーターマークベースのトラフィック制御により、毎日2〜3時間かかっていた手動テスト作業を自動化し、エンジニアの生産性向上とサイト信頼性の強化を実現している。

## 何が学べるか

- 本番トラフィックを活用した負荷テストの設計パターン（合成トラフィックとの比較と実トラフィックリダイレクトの利点）
- 3段階ランピングとウォーターマーク（高低QPS閾値）による安全な自動スケーリング手法
- 監視パイプラインの遅延を考慮した頻繁なデータサンプリングによる正確な判断の実現方法
- 負荷テスト自動化における一時停止・終了ポイントの設計（エンジニア介入の余地を残す自動化）
- トイル（手作業の繰り返し）を特定・排除し、SREチームの運用効率を向上させるアプローチ

## 関連エントリ

