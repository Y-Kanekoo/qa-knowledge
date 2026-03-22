# MkDocsローカルビルド + プレビュー

インデックスを最新化し、MkDocsサイトをビルドしてローカルプレビューサーバーを起動する。

## 引数

なし

## 実行手順

### ステップ1: インデックス最新化

```bash
.venv/bin/python scripts/generate_index.py
```

### ステップ2: サイトビルド

```bash
.venv/bin/python -m mkdocs build --strict
```

エラーがあれば内容を表示して修正を提案する。ビルド成功時はそのまま次へ。

### ステップ3: プレビューサーバー起動

```bash
.venv/bin/python -m mkdocs serve
```

Bash の run_in_background: true で起動し、以下を案内:

```
プレビューサーバーを起動しました:
  URL: http://127.0.0.1:8000
  停止: Ctrl+C または次のコマンドで停止できます
```
