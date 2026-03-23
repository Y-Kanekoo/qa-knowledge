---
title: "Automated Testing on Devices"
company: "Netflix"
url: "https://netflixtechblog.com/automated-testing-on-devices-fc5a39f47e24"
published_at: "2016-08-01"
content_type: "blog"
qa_domains:
  - "mobile-cross-browser"
  - "test-automation"
  - "test-strategy"
tags:
  - "device-testing"
  - "test-infrastructure"
  - "microservices"
  - "test-framework"
  - "device-management"
  - "ci-integration"
  - "cross-platform"
language: "en"
added_at: "2026-03-24"
industry: "media"
difficulty: "intermediate"
speaker: ""
conference: ""
video_url: ""
slide_url: ""
related_tools: []
deprecated: false
---

## 概要

Netflix SDK チームが、多種多様なデバイス（ゲームコンソール、モバイル、スマートTV等）上でNetflixアプリケーションの品質を保証するために構築した自動テスト基盤について解説したテックブログ記事。テストフレームワークと自動化サービスを明確に分離するプラグアンドプレイ設計を採用し、Device Service・Test Service・Network Manipulation・File Service・Maze Runner（テストオーケストレーター）といった独立したマイクロサービス群で構成されるスケーラブルなテストインフラを実現している。

## 何が学べるか

- テストフレームワークと自動化サービスを分離する設計原則により、テストの可読性・保守性・デバッグ容易性を高めながら、手動実行とCI実行の両方に対応する柔軟なアーキテクチャの構築方法が学べる
- RESTful APIによる統一的なデバイス抽象化レイヤー（Device Service + Device Handler パターン）を用いて、異なるデバイスタイプを同一インターフェースで管理するアプローチが参考になる
- Maze Runnerによるテストオーケストレーション（デバイス確保・ビルドインストール・テスト実行・結果収集・クラッシュ検知の自動化）の設計パターンが理解できる
- TPL（Test Portability Layer）という抽象化レイヤーにより、テストコードを自動化サービスの実装詳細から切り離し、異なる環境間でのテストの移植性を確保する手法が学べる
- ネットワーク操作サービス（帯域変動・DNS操作）を独立サービスとして提供し、実環境に近い条件でのストリーミング再生品質テストを実現する方法がわかる

## 関連エントリ

- [Netflix - FIT: Failure Injection Testing](netflix-fit-failure-injection-testing.md)
- [Netflix - Chaos Monkey](netflix-chaosmonkey.md)
