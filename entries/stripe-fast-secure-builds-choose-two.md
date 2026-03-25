---
title: "Fast builds, secure builds. Choose two."
company: "Stripe"
url: "https://stripe.dev/blog/fast-secure-builds-choose-two"
published_at: "2022-05-04"
content_type: "blog"
qa_domains:
  - "ci-cd"
  - "security-test"
  - "performance-test"
  - "reliability"
tags:
  - "build-system"
  - "bazel"
  - "firecracker"
  - "remote-execution"
  - "sandboxing"
  - "cache-poisoning"
  - "developer-productivity"
  - "microvm"
language: "en"
added_at: "2026-03-24"
industry: "fintech"
difficulty: "advanced"
speaker: "Sushain Cherivirala"
conference: ""
video_url: ""
slide_url: ""
related_tools:
  - "bazel"
  - "firecracker"
  - "gvisor"
  - "containerd"
  - "squashfs"
deprecated: false
---

## 概要

Stripeが数万のテストスイートを支えるCIビルドシステムにおいて、高速性とセキュリティの両立をどのように実現したかを解説した記事。キャッシュポイズニングによる悪意あるコード注入リスクに対処するため、BazelのRemote Execution APIとFirecracker microVMを組み合わせたサンドボックス実行基盤を構築し、Java・Rubyなど数十万アクションを伴う大規模ビルドでもサブ5分の実行速度を維持している。LVMスナップショット、TreeCache、アクションマージング、SquashFSバンドリングなど複数の最適化技術を積み重ねることで、セキュリティ隔離のオーバーヘッドを最小化したアプローチを紹介している。

## 何が学べるか

- CIビルドシステムにおけるキャッシュポイズニング攻撃のリスクと、それに対するFirecracker microVMによるサンドボックス隔離の設計手法
- Bazel Remote Execution APIを活用し、言語固有のカスタマイズを最小限に抑えながら複数言語（Java・Ruby等）の大規模ビルドを統合管理するアーキテクチャ
- LVMのcopy-on-writeスナップショットとOverlayFSを組み合わせた、VM内での高速なファイルシステム提供パターン
- TreeCache（ディレクトリ構造キャッシュ）やアクションマージング（重複アクションの結果再利用）など、リモート実行環境特有のパフォーマンス最適化手法
- セキュリティとビルド速度のトレードオフを段階的に解消していく、大規模フィンテック企業のCI基盤進化の実例

## 関連エントリ

- [Amazon - Automating safe, hands-off deployments](amazon-automating-safe-hands-off-deployments.md)
- [Amazon - Ensuring rollback safety during deployments](amazon-ensuring-rollback-safety-during-deployments.md)
- [Amazon - Timeouts, retries and backoff with jitter](amazon-timeouts-retries-backoff-with-jitter.md)
