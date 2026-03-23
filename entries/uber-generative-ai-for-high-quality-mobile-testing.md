---
title: "DragonCrawl: Generative AI for High-Quality Mobile Testing"
company: "Uber"
url: "https://www.uber.com/blog/generative-ai-for-high-quality-mobile-testing/"
published_at: "2024-04-23"
content_type: "blog"
qa_domains:
  - "ai-testing"
  - "test-automation"
  - "mobile-cross-browser"
tags:
  - "generative-ai"
  - "mobile-testing"
  - "llm"
  - "autonomous-testing"
  - "test-maintenance"
  - "e2e-testing"
  - "nlp"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
deprecated: false
---

## 概要

UberのDeveloper Platformチームが開発した「DragonCrawl」は、大規模言語モデル（LLM）を活用してモバイルアプリのテストを自動化するシステムである。従来の自動テストスクリプトはUI変更のたびに壊れやすくエンジニアが30〜40%の時間をメンテナンスに費やしていた課題を解決し、50以上の言語・89都市にわたるテストをコード修正なしで実行可能にした。2023年10月の本番投入以降、99%以上の実行成功率を達成し、3か月間で10件の高優先度バグをブロックしながら数千時間の開発工数を削減している。

## 何が学べるか

- 画面のテキスト表現とテスト目標を自然言語でLLMに与え、UIインタラクションを自律的に決定させるゴール指向型テスト設計の手法
- MPNet（110Mパラメータ）を選定しPrecision@1で0.9723を達成した、モバイルテストに適したモデルサイズとレイテンシのトレードオフ判断
- LLMのハルシネーション対策として、モデルサイズ制約・エミュレータによるグラウンドトゥルース検証・プロンプトフィードバックとバックトラッキングを組み合わせた3層防御アプローチ
- アプリ再起動による自律的リカバリや、一時的な障害に対する粘り強い再試行など、従来のスクリプトベーステストでは実現困難な適応的テスト実行の事例
- 85/89都市・3種のAndroidデバイス・3種のOSバージョンでコード修正なしに動作し、メンテナンスコストをゼロにした実績と、その背後にあるアーキテクチャ設計

## 関連エントリ

- [Meta - Automated Unit Test Improvement using Large Language Models at Meta](meta-automated-unit-test-improvement-llm.md)
- [SHIFT - AIテストエージェント](shift-ai-testing-agent.md)
- [LY Corporation - QAエンジニアが生成AIを利用して品質管理の生産性を向上させる方法](ly-corporation-qa-generative-ai-productivity.md)
