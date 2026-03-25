---
title: "自動テスト速度改善 - 自動テストが品質のボトルネックとならないために"
company: "freee"
url: "https://developers.freee.co.jp/entry/improving-ci-testing-for-next-quality"
published_at: "2022-03-28"
content_type: "blog"
qa_domains: [ci-cd, test-automation, reliability]
tags: [ci-optimization, circleci, flaky-test, parallel-execution, test-speed, rspec]
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [circleci, rspec]
deprecated: false
---

## 概要

freee人事労務チームが、CIの自動テスト実行時間を30分から10分へ（1/3に）短縮した5つの具体的な改善施策を解説している。レガシーテストの削除、フレイキーテスト管理、変更ファイルに基づく条件付きテストスキップ、ファイルレベルの実行時間最適化、共通フック処理の見直しを通じて、16並列コンテナの総実行時間を272分から138分に削減し、MTTRの短縮とリリース速度の向上を実現した。

## 何が学べるか

- CIテスト実行時間を1/3に短縮する5つの具体的な最適化手法とその効果測定
- 並列実行のボトルネック特定と負荷分散の改善方法（33.8分→9.5分の事例）
- フレイキーテストをゼロに保つためのチーム運用ルール（全体リラン禁止、ジョブ単位リラン推奨）
- 変更ファイルに基づくフロントエンド/バックエンドの条件付きテストスキップの実装
- 共通フック処理（before/after）の最適化が2万件以上のテストに与える集約的コストインパクトの分析

## 関連エントリ


- [Amazon - Automating safe, hands-off deployments](amazon-automating-safe-hands-off-deployments.md)
- [freee - freeeの自動テストの全体構成](freee-automated-test-structure.md)
- [freee - E2Eテスト分析基盤としてReportPortalを導入しました](freee-reportportal-e2e-test-analysis.md)
