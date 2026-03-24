---
title: "Using Playwright Test Shards in Combination with a Job Matrix to Improve Your CI Speed"
company: "Tim Deschryver"
url: "https://timdeschryver.dev/blog/using-playwright-test-shards-in-combination-with-a-job-matrix-to-improve-your-ci-speed"
published_at: "2022-09-07"
content_type: "blog"
qa_domains:
  - "test-automation"
  - "ci-cd"
tags:
  - "playwright"
  - "test-sharding"
  - "ci-optimization"
  - "github-actions"
  - "parallel-testing"
  - "large-scale-testing"
language: "en"
added_at: "2026-03-24"
industry: "general"
difficulty: "intermediate"
speaker: "Tim Deschryver"
related_tools:
  - "playwright"
  - "github-actions"
deprecated: false
---

## 概要

Tim Deschryverが、Playwrightのテストシャーディング機能とGitHub Actionsのジョブマトリックスを組み合わせてCI実行速度を大幅に改善する方法を解説した記事。`--shard=X/Y`オプションによるテスト分割の基本から、段階的な最適化（単一ジョブ→複数ジョブ→マトリックス→キャッシング層追加）までを具体的なワークフロー設定とともに示している。インストールジョブでの依存関係キャッシュ分離により各テストジョブの実行時間を削減するアプローチが実践的である。

## 何が学べるか

- Playwrightの`--shard=X/Y`オプションによるテストスイート分割と並列実行の基本的な仕組み
- GitHub Actionsのジョブマトリックスを活用したシャード並列化の段階的最適化アプローチ（単一→複数→マトリックス→キャッシュ）
- node_modulesとPlaywrightバイナリのキャッシュを独立インストールジョブに分離する実践的なCI設計
- 大規模テストスイート（1,200テスト等）をシャーディングで62分→16分に短縮した具体的な成果例
- 単一マシンのワーカー並列化では不十分な場合にシャーディングへ移行する判断基準

## 関連エントリ

- [SmartHR - E2Eテストを Playwright で作り直して開発プロセスに組み込む話](smarthr-e2e-test-playwright-migration.md)
- [freee - CI上のテスト実行速度を改善する](freee-improving-ci-testing-speed.md)
