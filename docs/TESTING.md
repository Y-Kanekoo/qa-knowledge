# テスト（qa-knowledge）

development-hub のテスト標準（https://github.com/Y-Kanekoo/development-hub/blob/main/docs/testing-standard.md）に従います。段階は static → unit → api → e2e の順で、前の段階が失敗したら止めます。

## 段階とコマンド

依存パッケージは `requirements.txt` で管理します。以下は `.local-ci.yml` の実行内容です。

| 段階 | コマンド・状態 |
| --- | --- |
| static | `uv run --no-project ruff check .` / `uv run --no-project ruff format --check .` / `uv run --no-project python scripts/scan_secrets.py`。`mypy` は未導入のためスキップ |
| unit | `uv run --no-project pytest --ignore=tests/api`（`tests/` 直下のテスト） |
| api | `uv run --no-project pytest tests/api`（外部通信は `fake_server` で代替） |
| e2e | Playwright の設定がないためスキップ |

まとめて実行: `local-ci run .`（段階の絞り込み: `--stage static,unit`）。

GitHub Actions の `ci.yml` は別構成で、`ruff check .`、`pytest -v --tb=short --cov=scripts --cov-report=term-missing`、公開記事と下書きの検証を実行します。

## カバレッジ

- 現在、カバレッジの下限は設定していません。
- GitHub Actions の CI では `scripts/` のカバレッジを計測します。`.local-ci.yml` の unit 段階では計測しません。

## スキップの記録

スキップは `.local-ci.yml` の `skip: true` と `skip_reason` に加えて、この表にも書きます。テストコードに `skip` を追加しません。

| 段階 | 理由 | 解除条件 | 記録日 |
| --- | --- | --- | --- |
| static（mypy） | mypy が未導入 | 対象を絞って導入する | 導入時点の記録なし |
| e2e | Playwright の設定がない | UI と Playwright 設定を用意する | 導入時点の記録なし |

## 弱体化の確認（レビュー時）

- [ ] `git diff origin/main -- tests .local-ci.yml .github/workflows/ci.yml` でテスト削除・skip 追加・段階削除がないことを確認
- [ ] 期待値を緩めていない（完全一致を部分一致や存在確認にしていない）
- [ ] カバレッジの除外・`.local-ci.yml` の skip・段階の削除を追加していない（追加したなら理由をこの文書に記録）
- [ ] 外部通信はモックかローカルのフェイクだけ
