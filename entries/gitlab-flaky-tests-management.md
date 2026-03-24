---
title: "Flaky tests management and processes | The GitLab Handbook"
company: "GitLab"
url: "https://handbook.gitlab.com/handbook/engineering/infrastructure/engineering-productivity/flaky-tests-management-and-processes/"
published_at: "2024-01-01"
content_type: "handbook"
qa_domains:
  - "reliability"
  - "ci-cd"
  - "quality-metrics"
tags:
  - "flaky-tests"
  - "test-stability"
  - "pipeline-reliability"
  - "engineering-productivity"
  - "test-quarantine"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

GitLabのEngineering Productivityチームによるフレイキーテスト管理プロセスのハンドブック。フレイキーテストがmasterパイプライン障害の少なくとも30%を占めるという課題に対し、検出・分類・隔離・修正の体系的なプロセスを定義している。260,040件のテストのうち1.99%がフレイキーと特定されたデータに基づき、定量的な管理アプローチを採用している。

## 何が学べるか

- フレイキーテストの定義（不安定なテスト・テストインフラ・アプリケーション起因）と影響範囲の定量的把握
- masterパイプライン障害の30%以上がフレイキーテスト起因であるという実データに基づく優先度判断
- テストの隔離（quarantine）プロセスとパイプライン信頼性の維持方法
- 260,000件超のテストスイートにおけるフレイキー率1.99%という大規模プロジェクトでの管理指標
- フレイキーテストの検出から修正までの体系的なワークフロー

## 関連エントリ

- [Google - Flaky Tests Mitigation](google-flaky-tests-mitigation.md)
- [GitLab - Infrastructure and Quality Handbook](gitlab-infrastructure-quality-handbook.md)
