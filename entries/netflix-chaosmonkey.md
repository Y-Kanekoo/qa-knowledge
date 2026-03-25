---
title: "Chaos Monkey - Resiliency Tool That Helps Applications Tolerate Random Instance Failures"
company: "Netflix"
url: "https://github.com/Netflix/chaosmonkey"
published_at: "2016-10-01"
content_type: "oss_config"
qa_domains:
  - "reliability"
tags:
  - "chaos-engineering"
  - "resilience"
  - "microservices"
  - "fault-injection"
  - "testing-in-production"
language: "en"
added_at: "2026-03-03"
industry: "media"
difficulty: "advanced"
deprecated: false
---

## 概要

Netflixが開発したChaos EngineeringツールのOSSリポジトリ。本番環境で動作するVMインスタンスやコンテナをランダムに停止させることで、システムの耐障害性を継続的に検証する。Principles of Chaos Engineeringに基づいており、エンジニアが障害を恐れずに設計する文化を醸成することを目的としている。Go言語で実装され、AWS・GCE・Kubernetes・Azureなど主要なクラウドプラットフォームに対応している。

## 何が学べるか

- 本番環境でインスタンスをランダムに停止させるChaos Monkey手法の実装原理と、Spinnaker（継続的デリバリープラットフォーム）との統合方法
- 「予測不可能なタイミングでの障害注入を繰り返すことでエンジニアが堅牢な設計を自然に意識するようになる」というChaos Engineeringの行動変容効果
- マルチクラウド環境（AWS、GCE、Kubernetes、Azure）に対応した障害注入の設定方法と段階的な適用戦略
- Principles of Chaos Engineeringに基づく「本番環境での継続的な耐性検証」という信頼性テストのアプローチ
- OSSとして公開された設定・アーキテクチャを参考に自社サービスのカオスエンジニアリング基盤を構築する際の参考実装

## 関連エントリ

- [Netflix - FIT: Failure Injection Testing](netflix-fit-failure-injection-testing.md)
- [Google - Google Cloud Introduces Chaos Engineering Framewor](google-cloud-chaos-engineering-framework.md)
- [Amazon - Using load shedding to avoid overload](amazon-using-load-shedding-to-avoid-overload.md)
