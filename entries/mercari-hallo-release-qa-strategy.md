---
title: "メルカリ ハロ リリースのQA戦略"
company: "Mercari"
url: "https://engineering.mercari.com/blog/entry/20240603-mercarihallo-releaseqastrategy/"
published_at: "2024-06-06"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "shift-left"
tags:
  - "qa-planning"
  - "acceptance-criteria"
  - "cross-team-qa"
  - "iso-29119"
  - "vendor-management"
language: "ja"
added_at: "2026-03-03"
industry: "ecommerce"
difficulty: "intermediate"
deprecated: false
---

## 概要

メルカリの新サービス「メルカリ ハロ」（事業者と働き手を結ぶプラットフォーム）のローンチに向けたQA戦略を解説した記事。複数カンパニーが関わる大規模プロジェクトで、社員・アルムナイ業務委託・外部ベンダーの3層構造でQAエンジニアをアサインし、ISO/IEC/IEEE 29119 Part3を参照してテスト計画書・完了報告書を整備した実践例を紹介している。

## 何が学べるか

- 社員・アルムナイ（元社員）業務委託・外部ベンダーという3層のQAアサイン構造で組織規模と開発複雑さに対応する設計
- JIRA・Confluence・TestRail・Google Spreadsheetsを組み合わせ、成果物をクラウド上に集約して社内全員が参照できる透明性管理の手法
- ISO/IEC/IEEE 29119 Part3を参照したテスト計画書・テスト完了報告書の標準化によりプロセスの一貫性を確保する方法
- ストーリーチケットにAcceptance Criteriaを直接記載し、エンジニアのセルフチェックとQAレビューの効率を向上させるシフトレフトの実践
- メルペイなど他カンパニーとの定期的なミーティングとドキュメント共有によりシステム統合テストを円滑に進めるカンパニー間QA連携

## 関連エントリ

