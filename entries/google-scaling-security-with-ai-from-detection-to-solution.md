---
title: "Scaling security with AI:  from detection to solution"
company: "Google"
url: "https://security.googleblog.com/2024/01/scaling-security-with-ai-from-detection.html"
published_at: "2024-01-31"
content_type: "blog"
qa_domains:
  - "security-test"
  - "ai-testing"
  - "test-automation"
tags:
  - "llm"
  - "fuzzing"
  - "vulnerability-detection"
  - "automated-patching"
  - "oss-fuzz"
  - "open-source-security"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "intermediate"
deprecated: false
---

## 概要

GoogleのセキュリティチームがAI/LLMを活用してソフトウェアの脆弱性発見と修正を自動化・スケーリングする取り組みを紹介したブログ記事。OSS-Fuzzサービスと連携したLLMベースのファジング生成により300以上のC/C++プロジェクトでコードカバレッジを最大29%向上させ、cJSONやlibplistで未知の脆弱性を発見した実績、さらにLLMによる自動パッチ生成パイプラインで対象バグの15%を解決した成果が報告されている。

## 何が学べるか

- LLMを活用してプロジェクト固有のファジングコードを自動生成し、セキュリティテストのカバレッジを大幅に拡大する手法が学べる
- 300以上のOSSプロジェクトで最大29%のカバレッジ向上という定量的な成果から、AI駆動のセキュリティテストの有効性と限界を評価できる
- 脆弱性の「発見」だけでなく「修正」までをLLMで自動化するパイプライン設計により、検出から解決までのライフサイクル全体をAIで効率化するアプローチが参考になる
- oss-fuzz-genとしてオープンソース化されたフレームワークを通じて、自組織のセキュリティテストにLLMベースのファジングを導入する具体的な手段が得られる

## 関連エントリ

- [Automated Unit Test Improvement using Large Language Models at Meta](meta-automated-unit-test-improvement-llm.md) - LLMを活用したテスト自動化の産業規模での実践事例
- [CodeQL team uses AI to power vulnerability detection in code](github-codeql-team-uses-ai-to-power-vulnerability-detection-in-code.md) - AIによる脆弱性検出の別アプローチ
