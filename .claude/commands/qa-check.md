# CI相当の全品質チェック一括実行

ruff（Lint）、pytest（テスト）、validate_frontmatter（スキーマ検証）、mkdocs build（サイトビルド）をローカルで一括実行し、CI 通過前に問題を検出する。

## 引数

`$ARGUMENTS` = `[--fix]`

- `--fix`: ruff の自動修正を有効化（省略時はチェックのみ）

## 実行手順

4つのチェックを順に実行し、最後にサマリテーブルを表示する。

### チェック1: Lint（ruff）

```bash
# --fix が指定された場合
.venv/bin/python -m ruff check --fix .

# チェックのみの場合
.venv/bin/python -m ruff check .
```

### チェック2: Frontmatter検証

```bash
.venv/bin/python scripts/validate_frontmatter.py
```

### チェック3: テスト

```bash
.venv/bin/python -m pytest tests/ -v --tb=short --cov=scripts --cov-report=term-missing
```

### チェック4: サイトビルド

```bash
.venv/bin/python -m mkdocs build --strict 2>&1 | tail -20
```

### サマリ表示

以下の形式でサマリテーブルを出力:

```
| チェック | 結果 | 詳細 |
|---------|------|------|
| Lint (ruff) | PASS/FAIL | エラー数 |
| Frontmatter | PASS/FAIL | エラーファイル数 |
| テスト | PASS/FAIL | passed/failed/skipped |
| サイトビルド | PASS/FAIL | 警告数 |
```

全チェック合格なら「全品質チェックに合格しました」と表示。
