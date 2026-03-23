---
title: "Leveling Up Fuzzing: Finding more vulnerabilities with AI"
company: "Google"
url: "https://security.googleblog.com/2024/11/leveling-up-fuzzing-finding-more.html"
published_at: "2024-11-20"
content_type: "blog"
qa_domains:
  - "security-test"
  - "ai-testing"
  - "test-automation"
tags:
  - "fuzzing"
  - "llm"
  - "vulnerability-detection"
  - "oss-fuzz"
  - "code-coverage"
  - "ai-assisted-testing"
  - "open-source-security"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
deprecated: false
---

## 概要

Google Open Source Security Teamが、LLM（大規模言語モデル）を活用してOSS-Fuzzのファジングターゲット生成を自動化し、272のC/C++プロジェクトで370,000行以上の新規コードカバレッジを達成した取り組みを報告している。この手法により26件の新規脆弱性が発見され、OpenSSLで約20年間潜在していた脆弱性（CVE-2024-9143）の検出にも成功した。

## 何が学べるか

- LLMを活用したファジングターゲットの自動生成手法と、開発者ワークフロー（草案作成・コンパイルエラー修正・実行テスト・クラッシュ分類）全体をAIでシミュレートするアプローチ
- OSS-Fuzzのインフラを活用した大規模OSSプロジェクトへのファジング適用と、プロジェクト固有のコンテキスト（関数定義・型定義・既存テスト）をプロンプトに組み込む手法
- コードカバレッジ向上がバグフリーを保証しない原則と、異なるフラグ・設定の組み合わせで多様なバグを検出する戦略
- 従来の人手によるファジングターゲット作成では発見できなかった長期潜在脆弱性をAIが検出できた実証事例
- セキュリティテストの自動化におけるAI活用の現状と今後の展望（脆弱性修正の自動化を含む）

## 関連エントリ

- [Meta - Automated Unit Test Improvement Using LLM](meta-automated-unit-test-improvement-llm.md)
- [Google - Scaling Security with AI: From Detection to Solution](google-scaling-security-with-ai-from-detection-to-solution.md)
- [Google - Mutation Testing](google-mutation-testing.md)
- [Shift AI - Testing Agent](shift-ai-testing-agent.md)
