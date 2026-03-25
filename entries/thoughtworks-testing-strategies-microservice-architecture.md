---
title: "Testing Strategies in a Microservice Architecture"
company: "ThoughtWorks"
url: "https://martinfowler.com/articles/microservice-testing/"
published_at: "2014-11-18"
content_type: "article"
qa_domains:
  - "test-strategy"
  - "test-automation"
  - "ci-cd"
tags:
  - "microservices"
  - "test-pyramid"
  - "unit-test"
  - "integration-test"
  - "component-test"
  - "contract-test"
  - "e2e-test"
  - "test-doubles"
  - "consumer-driven-contracts"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
speaker: "Toby Clemson"
deprecated: false
---

## 概要

マイクロサービスアーキテクチャにおけるテスト戦略を、ユニットテスト・統合テスト・コンポーネントテスト・契約テスト・エンドツーエンドテストの5層に体系化した基礎文献。各テスト層のスコープ・目的・テストダブルの使い分けを明確に定義し、テストピラミッドに基づくバランスの取れたテスト戦略の構築指針を提示している。分散システム特有のテスト課題に対して、どの粒度でどのような検証を行うべきかの判断基準を与える定番記事である。

## 何が学べるか

- ユニットテスト（単一クラス/関数）・統合テスト（外部コンポーネントとの通信経路）・コンポーネントテスト（サービス単体の振る舞い）・契約テスト（サービス間インターフェースの互換性）・E2Eテスト（システム全体の業務フロー）の5層それぞれの目的・スコープ・トレードオフを理解できる
- テストダブル（スタブ・モック・フェイク）を各テスト層でどう使い分けるか、特にコンポーネントテストでin-processとout-of-processの2つのアプローチがある点を学べる
- Consumer-Driven Contract Testingにより、サービス間の契約をプロバイダ側で自動検証し、統合の破壊を早期に検出する手法を理解できる
- E2Eテストの実行コスト・フレイキーさ・デバッグ困難性といった課題を踏まえ、テストピラミッドの下層を厚くしてE2Eを最小限に抑える戦略的判断の根拠を学べる
- マイクロサービス環境でのCI/CDパイプラインにおいて、各テスト層をどのステージで実行すべきかの設計指針が得られる

## 関連エントリ

- [Google - Test Sizes](google-test-sizes.md)
