---
title: "探索的テスト補助用テストケースの自動生成 ー 使用したLLMプロンプトもご紹介"
company: "SmartHR"
url: "https://tech.smarthr.jp/entry/2025/09/01/181905"
published_at: "2025-09-01"
content_type: "blog"
qa_domains:
  - "ai-testing"
  - "test-strategy"
tags:
  - "exploratory-testing"
  - "llm"
  - "test-generation"
  - "cline"
  - "mcp"
  - "prompt-engineering"
language: "ja"
added_at: "2026-03-24"
industry: "saas"
difficulty: "advanced"
deprecated: false
---

## 概要

SmartHRの勤怠管理機能チームのQAエンジニアが、AIアシスタントツールClineを活用して探索的テストの補助用テストケースを自動生成する手法を紹介している。MCPサーバー経由でPBI情報や仕様書を取得し、構造化されたプロンプトでテストチャーターを生成する仕組みを、実際に使用したプロンプト設計とともに詳細に解説している。生成結果は基本シナリオでは高精度であり、推測的な後半部分でも人間が見落としていた観点の発見に寄与している。

## 何が学べるか

- LLM（Cline）を使った探索的テストケース自動生成の具体的なプロンプト設計手法
- MCPサーバーを活用したGitHub・DocBaseからの情報取得によるコンテキスト構築方法
- 生成されたテストケースを「テストチャーター」として位置づけ、人間が柔軟に探索を拡張するAIとの協働モデル
- 明確な受入基準（MECE原則）を事前に整備しておくことがAI活用の前提条件であるという知見
- AI生成結果の精度特性（基本→複雑→組み合わせ→見落としの順で推測度が上がる）

## 関連エントリ
