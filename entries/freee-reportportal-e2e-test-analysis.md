---
title: "E2Eテスト分析基盤としてReportPortalを導入しました"
company: "freee"
url: "https://developers.freee.co.jp/entry/freee-qa-advent-calendar2024-day7"
published_at: "2024-12-07"
content_type: "blog"
qa_domains: [test-automation, ci-cd, observability]
tags: [e2e, reportportal, playwright, flaky-test, test-reporting, eks, aws, slack]
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: [reportportal, playwright, jenkins, redash, aws-eks, opensearch, slack]
deprecated: false
---

## 概要

freeeのSEQチームが、E2Eテストの失敗分析を効率化するためにオープンソースのテストレポートツール「ReportPortal」を導入した事例を紹介している。従来はRedashとJenkinsを行き来しながらスクリーンショットを手動管理する非効率な運用だったが、ReportPortalにより失敗ログ・スクリーンショットの一元管理を実現し、月額約400ドルのコストでEKS上に構築した分析基盤の詳細を解説している。

## 何が学べるか

- E2Eテストの失敗原因調査を一元化するためのReportPortal導入プロセスとアーキテクチャ設計
- EKS + S3 + OpenSearch + Amazon MQを組み合わせたテスト分析基盤の構成と運用コスト
- Playwrightテストからログ・スクリーンショットを自動収集しSlack通知と連携する仕組み
- フレイキーテスト一覧やテスト実行時間のダッシュボード構築による可視化手法

## 関連エントリ

- [freee - 自動テストの全体構成](freee-automated-test-structure.md)
- [freee - CI/CDテスト速度の改善](freee-improving-ci-testing-speed.md)
