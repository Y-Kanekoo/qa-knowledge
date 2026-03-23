---
title: "Introducing Ballast: An Adaptive Load Test Framework"
company: "Uber"
url: "https://www.uber.com/blog/introducing-ballast-an-adaptive-load-test-framework/"
published_at: "2022-03-01"
content_type: "blog"
qa_domains:
  - "performance-test"
  - "test-automation"
  - "reliability"
tags:
  - "load-testing"
  - "adaptive-testing"
  - "pid-controller"
  - "traffic-replay"
  - "bpf"
  - "capacity-planning"
  - "microservices"
  - "golden-signals"
language: "en"
added_at: "2026-03-24"
industry: "mobility"
difficulty: "advanced"
deprecated: false
---

## 概要

Uberのマップ基盤チームが開発した適応型負荷テストフレームワーク「Ballast」を紹介する記事。BPF（Berkeley Packet Filter）による本番トラフィックのキャプチャと、PID制御アルゴリズムによるRPS（秒間リクエスト数）の自動調整を組み合わせることで、手動での負荷テスト作成・実行の課題を解消し、本番に近いトラフィックパターンでの再現性の高い負荷テストを実現している。マイクロサービスの急増に伴い従来の手動アプローチがスケールしなくなった背景から、6つのコンポーネント（Load Generator、Traffic Capture、Golden Signals、PID Controller、Scheduler、Watchdog）で構成されるアーキテクチャを解説している。

## 何が学べるか

- BPFを活用した本番トラフィックのキャプチャとリプレイにより、手動でテストシナリオを作成する負担を排除し、本番に忠実な負荷パターンを再現するアプローチ
- PID制御アルゴリズムを用いて、ターゲットSLO（例: CPU使用率80%）と実測値の差分に基づきRPSを動的に調整する適応型負荷制御の仕組み
- レイテンシ・可用性・スループット・リソース利用率の4つのゴールデンシグナルを基準にしたサービスの限界容量の自動検出手法
- ホリデーピーク時の容量推定やカナリアデプロイメントの品質検証など、大規模マイクロサービス環境での実践的な活用パターン
- HTTP 1.1/2.0やTChannelなど複数プロトコルに対応した、スケーラブルな負荷テスト基盤の設計思想

## 関連エントリ

- [Grafana Labs - Understanding Grafana k6](grafana-labs-understanding-grafana-k6-load-testing.md)
- [Netflix - Fixing Performance Regressions](netflix-fixing-performance-regressions.md)
