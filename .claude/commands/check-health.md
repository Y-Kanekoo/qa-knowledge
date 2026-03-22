# プロジェクト健全性チェック

リンク死活・CI実行状態・依存脆弱性・deprecatedエントリを統合ダッシュボードで表示する。

## 引数

`$ARGUMENTS` = `[--links | --ci | --deps]`

- `--links`: リンクチェックのみ
- `--ci`: CI状態確認のみ
- `--deps`: 依存脆弱性チェックのみ
- 省略時: 全チェックを実行

## 実行手順

### チェック1: リンク死活確認

```bash
.venv/bin/python scripts/check_links.py
```

リンク切れがあればURL・ステータスコード・エントリファイル名を表示。

### チェック2: CI実行状態

```bash
gh run list --limit 10 --json name,status,conclusion,createdAt
```

直近10回のワークフロー実行結果を表示。失敗があれば詳細を確認:

```bash
gh run view <run-id> --log-failed
```

### チェック3: 依存脆弱性

```bash
.venv/bin/python -m pip audit 2>&1 || echo "pip-audit が未インストールです"
```

脆弱性があれば影響パッケージと推奨バージョンを表示。

### チェック4: deprecatedエントリ棚卸し

entries/ 内の全ファイルから `deprecated: true` のエントリを検出して一覧表示。

### ダッシュボード表示

全チェック結果を以下の形式でサマリ表示:

```
## プロジェクト健全性ダッシュボード

| 項目 | 状態 | 詳細 |
|------|------|------|
| リンク | OK / NG(N件) | リンク切れ数 |
| CI | OK / NG | 直近の失敗ワークフロー |
| 依存 | OK / NG(N件) | 脆弱性数 |
| deprecated | N件 | 対象エントリ数 |
```
