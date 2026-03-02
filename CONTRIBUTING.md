# コントリビューションガイド

QA事例・ナレッジの追加を歓迎します。

## エントリの追加方法

### 1. 骨格ファイルの生成

```bash
python scripts/scaffold.py "https://example.com/blog/..." --company "CompanyName"
```

`entries/` にタイトル・公開日が自動入力された骨格ファイルが生成されます。

### 2. 内容の記入

以下のフィールドを手動で記入してください:

| フィールド | 説明 | 例 |
|-----------|------|------|
| `content_type` | コンテンツ種別 | `blog`, `conference_talk`, `handbook` 等 |
| `qa_domains` | QA領域（1つ以上） | `test-automation`, `ci-cd` 等 |
| `tags` | 自由キーワード（小文字ケバブケース） | `playwright`, `flaky-tests` 等 |
| `industry` | 企業の業種（推奨） | `tech`, `finance`, `ecommerce` 等 |
| `difficulty` | 難易度（推奨） | `beginner`, `intermediate`, `advanced` |

本文セクション:

- **概要**: 2〜3文で記事の内容を説明
- **何が学べるか**: 3〜5点の箇条書き。抽象的な感想ではなく、記事に書かれた具体的な手法・数値を記述

### 3. バリデーション

```bash
python scripts/validate_frontmatter.py
```

### 4. PR作成

- ブランチ名: `add/{company}-{slug}`
- 1つのPRに複数エントリを含めてOK

## 許可値一覧

`content_type` と `qa_domains` の許可値は [docs/schema.md](docs/schema.md) を参照してください。

## 品質基準

- 一次情報（公式ブログ・公式発表）を優先。転載・まとめ記事は収録しない
- 「何が学べるか」は具体的な手法・定量データを記述する
- URLは `https://` であること
