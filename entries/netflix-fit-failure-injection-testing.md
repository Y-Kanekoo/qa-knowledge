---
title: "FIT: Failure Injection Testing"
company: "Netflix"
url: "https://netflixtechblog.com/fit-failure-injection-testing-35d8e2a9bb2"
published_at: "2014-10-29"
content_type: "blog"
qa_domains:
  - "reliability"
  - "test-strategy"
tags:
  - "chaos-engineering"
  - "failure-injection"
  - "resilience"
  - "microservices"
  - "production-testing"
language: "en"
added_at: "2026-03-03"
industry: "media"
difficulty: "advanced"
deprecated: false
---

## 概要

NetflixがChaos Monkeyを超えた精度の高い障害注入テストプラットフォーム「FIT（Failure Injection Testing）」を解説したテックブログ記事。Zuulを活用してリクエスト単位で障害スコープを制御し、特定のテストアカウントから始めて段階的に本番トラフィックへ拡大するアプローチにより、安全かつ制御された形でプロダクション環境での耐障害性検証を実現している。

## 何が学べるか

- 障害注入をZuulのメタデータとして伝播させる設計により、マイクロサービス全体を貫くリクエストパスの全注入ポイントを自動的に特定できる仕組みを学べる
- 特定テストアカウント→本番の数%→100%という段階的な障害スコープ拡大戦略により、ビジネスリスクを最小化しながら本番同等の耐障害性を検証する手法が参考になる
- Hystrix・Ribbon・EVCache・Astyanaxといったビルディングブロックコンポーネントを障害注入ポイントとして活用することで、依存サービス障害時のフォールバック動作を体系的に検証できる
- 「大規模カオス実験と個別テストのギャップを埋めるセルフサービスな中間ツール」としてFITを位置づけることで、チーム自律的に耐障害性検証を行う組織文化の構築方法が学べる

## 関連エントリ

- netflix-chaosmonkey.md
