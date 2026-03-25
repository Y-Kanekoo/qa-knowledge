---
title: "Challenges with distributed systems"
company: "Amazon"
url: "https://aws.amazon.com/builders-library/challenges-with-distributed-systems/"
published_at: "2019-09-01"
content_type: "blog"
qa_domains:
  - "test-strategy"
  - "reliability"
tags:
  - "distributed-systems"
  - "failure-modes"
  - "network-testing"
  - "fault-injection"
  - "non-determinism"
  - "partial-failure"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
speaker: "Jacob Gabrielson"
conference: ""
video_url: ""
slide_url: ""
related_tools: []
deprecated: false
---

## 概要

Amazonの分散システム開発で直面するテスト上の課題を体系的に解説した記事。単一マシンのプログラミングとは根本的に異なる、独立した障害とノンデターミニズムという2つの本質的な困難に焦点を当てている。ネットワークリクエスト/リプライの各ステップで発生しうる「8つの障害モード」を定義し、1つのメソッド呼び出しが8つの異なる障害シナリオに展開されることを示すことで、分散システムのテストに求められる網羅性の高さを明確にしている。

## 何が学べるか

- 分散システムにおけるリクエスト/リプライサイクルの「8つの障害モード」（メッセージ送信失敗、ネットワーク配送失敗、バリデーション失敗、状態更新失敗など）の体系的理解
- サーバーとネットワークが運命を共有しない（share fate しない）ため、ネットワーク障害のすべての側面をテストする必要がある理由
- 部分的障害（partial failure）と結果不明状態（unknown outcome）に対するテスト設計の考え方
- 単一マシンでの正常動作が分散環境では保証されないことを前提としたテスト戦略の構築方法
- 障害モードの組み合わせ爆発に対処するための、系統的なテストアプローチの必要性

## 関連エントリ

- [Amazon - Ensuring rollback safety during deployments](amazon-ensuring-rollback-safety-during-deployments.md)
