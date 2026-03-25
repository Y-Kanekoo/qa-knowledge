---
title: "Load Testing for 2022 Wrapped"
company: "Spotify"
url: "https://engineering.atspotify.com/2023/03/load-testing-for-2022-wrapped"
published_at: "2023-03-31"
content_type: "blog"
qa_domains:
  - "performance-test"
  - "test-strategy"
  - "reliability"
  - "observability"
tags:
  - "load-testing"
  - "thundering-herd"
  - "moshpit"
  - "backstage"
  - "kubernetes"
  - "grafana"
  - "grpc"
  - "horizontal-scaling"
  - "capacity-planning"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

Spotifyの年末恒例キャンペーン「Wrapped 2022」において、150万人以上のユーザーがローンチ直後の数時間に一斉アクセスする「thundering herd問題」に対処するための負荷テスト戦略を解説した記事。社内Backstageプラグイン「Moshpit」を活用し、HTTP/gRPCベースで段階的に負荷を増加させるテスト手法と、複数リージョン・複数上流サービスを含めた包括的なキャパシティプランニングの実践について述べている。結果として、重大な技術的障害なくキャンペーンをローンチすることに成功した。

## 何が学べるか

- 大規模イベント（数千万ユーザー同時アクセス）に備えた負荷テストの計画・実行プロセスの全体像
- 社内負荷テストツール（Moshpit）の設計思想と、Backstageプラグインとして開発者が利用しやすい形で提供するアプローチ
- テストペイロードに社内従業員データを活用する戦略と、キャッシュ動作を正しく再現するためのフラグ除去などの現実的な工夫
- 上流サービスのレートリミッターやKubernetesリソース（クォータ、オートスケーリング設定）を含めた、依存サービスまで考慮した包括的な負荷テスト設計
- Grafanaダッシュボードでレイテンシ・パケットロス率・HPA挙動・CPU/メモリ使用率を横断監視する可観測性の実践

## 関連エントリ

- [LinkedIn - Eliminating Toil with Fully Automated Load Testing](linkedin-eliminating-toil-automated-load-testing.md)
- [Amazon - Using load shedding to avoid overload](amazon-using-load-shedding-to-avoid-overload.md)
- [Amazon - Timeouts, retries and backoff with jitter](amazon-timeouts-retries-backoff-with-jitter.md)
