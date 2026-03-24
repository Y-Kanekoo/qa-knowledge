---
title: "Inside look: How GitLab's Test Platform team validates AI features"
company: "GitLab"
url: "https://about.gitlab.com/blog/2024/06/03/inside-look-how-gitlabs-test-platform-team-validates-ai-features"
published_at: "2024-06-03"
content_type: "blog"
qa_domains:
  - "ai-testing"
  - "test-strategy"
  - "quality-metrics"
tags:
  - "ai-validation"
  - "non-deterministic-testing"
  - "performance-testing"
  - "code-suggestions"
  - "gitlab-duo"
  - "continuous-analysis"
language: "en"
added_at: "2026-03-24"
industry: "tech"
difficulty: "advanced"
speaker: "Mark Lapierre, Vincy Wilson"
deprecated: false
---

## 概要

GitLabのテストプラットフォームチームが、AI機能（GitLab Duo Code Suggestions等）の非決定論的な出力をどのようにバリデーションしているかを解説した記事。AI継続分析ツール、パフォーマンス検証、機能テストの三層構造でAI品質を担保するアプローチを紹介している。IDEレベルでの自動データ収集やAIゲートウェイへの模擬応答設定など、AI特有のテスト課題に対する具体的な解決策を示している。

## 何が学べるか

- AI機能の「非決定論的性質」（同一入力で異なる出力）に対応するテスト戦略の設計方法
- IDEレベルでコードプロンプト入力・提案記録・レイテンシー測定を行うAI継続分析ツールの構築アプローチ
- AIゲートウェイに模擬応答を設定して第三者AI提供者への依存を排除するパフォーマンス検証手法
- 複数地域（米国・欧州・アジア）からのTTFB測定によるグローバルなパフォーマンスベースライン確立
- 実AI応答と模擬応答の両方でE2Eテストを実施し、探索的テストとドッグフーディングを組み合わせる多層的バリデーション

## 関連エントリ

- [GitLab - An inside look at software testing](gitlab-inside-look-software-testing.md)
- [Meta - Automated Unit Test Improvement with LLM](meta-automated-unit-test-improvement-llm.md)
