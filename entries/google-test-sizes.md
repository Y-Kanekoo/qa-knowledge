---
title: "Test Sizes"
company: "Google"
url: "https://testing.googleblog.com/2010/12/test-sizes.html"
published_at: "2010-12-13"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "test-automation"
tags:
  - "test-classification"
  - "test-pyramid"
  - "unit-test"
  - "integration-test"
  - "test-isolation"
language: "en"
added_at: "2026-03-03"
industry: "tech"
difficulty: "beginner"
deprecated: false
---

## 概要

Googleが「ユニットテスト」「インテグレーションテスト」といった曖昧な呼称を避け、実行制約に基づく「Small / Medium / Large」というサイズ分類を採用している理由と定義を解説した記事。各サイズには実行時間の上限とネットワーク・ファイルシステム・外部サービスへのアクセス可否が明確に定められており、自動的なポリシー適用が可能な点が特徴的である。

## 何が学べるか

- Smallテスト（60秒以内）はネットワーク・DB・ファイルシステム・マルチスレッド・sleep禁止という厳格な分離制約を持つ
- Mediumテスト（300秒以内）はlocalhost通信・DB・ファイルシステム・マルチスレッドを許可し、層間の結合検証に使用する
- Largeテスト（900秒以上）はフルネットワーク・外部システムへのアクセスを許可し、エンドツーエンドの検証に用いる
- テストサイズに応じた制約をJavaセキュリティマネージャ等で自動強制し、違反を機械的に検出できる
- 「ユニットテスト」という用語の解釈の揺れを排除し、チーム間でテスト分類の共通言語を持つことでCIの並列実行と一貫したフィードバックが実現できる

## 関連エントリ

