# エントリ追加（AI自動補完付き）

URLからQAナレッジエントリを作成する。scaffold.py で骨格を生成し、AIが元記事を読んでメタデータ・概要・学びを自動補完する。

## 引数

`$ARGUMENTS` = `<URL> [--company <企業名>]`

- URL: 対象記事のURL（必須）
- --company: 企業名（scaffold.py が推定できない場合に指定）

## 実行手順

### ステップ1: 骨格生成

```bash
.venv/bin/python scripts/scaffold.py $ARGUMENTS
```

生成されたファイルパスを記録する。エラーが出た場合はエラー内容を表示して終了。

### ステップ2: 元記事の取得

WebFetch ツールで元記事のURLにアクセスし、記事の全文を取得する。

### ステップ3: メタデータ推定

記事の内容に基づき、以下のフィールドを推定して埋める：

**content_type**（以下から1つ選択）:
blog, conference_talk, slide_deck, oss_config, handbook, case_study, book_excerpt, podcast, video

**qa_domains**（以下から1つ以上選択）:
test-strategy, test-automation, ci-cd, reliability, quality-metrics, org-design, ai-testing, security-test, performance-test, mobile-cross-browser, shift-left, observability

**tags**（ケバブケースで3-7個）:
記事の主要トピックを表すキーワード。小文字英数字とハイフンのみ（例: flaky-tests, contract-testing）

**industry**（以下から1つ選択）:
tech, finance, ecommerce, media, gaming, saas, other

**difficulty**（以下から1つ選択）:
beginner, intermediate, advanced

**language**: 記事の言語（en または ja）

### ステップ4: 概要と学びの生成

記事の内容に基づき：

- **概要**（`## 概要` セクション）: 2-3文でこの記事の内容を要約。具体的な技術・手法名を含める
- **何が学べるか**（`## 何が学べるか` セクション）: 3-5点の箇条書き。具体的な手法・定量データ・実践的な知見を記述

### ステップ5: 関連エントリのリンク

entries/ 内の既存エントリの frontmatter を確認し、同じ qa_domains や tags を持つエントリがあれば `## 関連エントリ` セクションにリンクを追加する。

### ステップ6: ファイル更新

Edit ツールで生成ファイルを更新する。

### ステップ7: バリデーション

```bash
.venv/bin/python scripts/validate_frontmatter.py
```

エラーがあれば修正する。

### ステップ8: 結果表示

完成したエントリの全内容をプレビュー表示する。
