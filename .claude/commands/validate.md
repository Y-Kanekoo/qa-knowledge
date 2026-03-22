# Frontmatter検証 + 修正提案

エントリの YAML frontmatter を検証し、エラーがあれば具体的な修正方法を提案する。

## 引数

`$ARGUMENTS` = `[ファイルパス]`（省略時は全エントリを検証）

## 実行手順

### ステップ1: バリデーション実行

```bash
.venv/bin/python scripts/validate_frontmatter.py $ARGUMENTS
```

### ステップ2: 結果分析

- エラーがない場合: 「全エントリのバリデーションに合格しました」と表示して終了
- エラーがある場合: 各エラーについて以下を表示:
  - エラー内容
  - 該当ファイルと行
  - 具体的な修正方法の提案

### ステップ3: 修正適用（エラーがある場合）

ユーザーに修正を適用してよいか確認し、承認を得てから Edit ツールで修正する。

### 許可値リファレンス

**content_type**: blog, conference_talk, slide_deck, oss_config, handbook, case_study, book_excerpt, podcast, video

**qa_domains**: test-strategy, test-automation, ci-cd, reliability, quality-metrics, org-design, ai-testing, security-test, performance-test, mobile-cross-browser, shift-left, observability

**language**: en, ja

**tags**: ケバブケース（小文字英数字とハイフンのみ、例: flaky-tests）

**日付**: ISO 8601形式（YYYY-MM-DD）

**url**: https:// で始まること
