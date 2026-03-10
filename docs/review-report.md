---
schema_version: 1
generated_at: 2026-03-06T01:24:46+09:00
commit_hash: f4e1251fba01a894019a12ce82ba7692968b12e0
previous_commit: 6db7fc145e36f5ce67703fb03db183e455a34054
file_count: 82
stack: Python (pyyaml, mkdocs-material, requests, bs4, python-frontmatter, feedparser)
stage: ベータ
total_issues: 4
critical: 0
high: 0
medium: 1
low: 3
---

# プロジェクトレビューレポート（差分レビュー）

## 概要

| 項目 | 値 |
|------|-----|
| 対象コミット | `f4e1251`（前回: `6db7fc1`） |
| ファイル数 | 82（前回: 50） |
| 変更ファイル | 22ファイル（7コミット） |
| スタック | Python |
| 段階 | ベータ（前回: アルファ → 昇格） |
| 指摘数 | 4件（Critical: 0 / High: 0 / Medium: 1 / Low: 3） |

## エグゼクティブサマリ

前回レビュー（`6db7fc1`）で指摘した **25件が全て対応済み**。テスト基盤（pytest 57テスト）、CI品質ゲート（ruff + pytest）、HTTPリトライ機構、loggingモジュール統一、依存パッケージのピンロック、ドキュメント整備が完了し、プロジェクト段階はアルファからベータに昇格した。残る指摘は軽微な4件のみで、Critical/High の問題はない。

## 前回指摘の対応状況

| 状態 | 件数 |
|------|------|
| 解決済み | 25/25 |
| 未解決 | 0 |
| 新規指摘 | 4 |

<details>
<summary>前回25件の対応詳細（クリックで展開）</summary>

| ID | 重大度 | 問題 | 対応コミット | 状態 |
|----|--------|------|-------------|------|
| C-001 | High | `except Exception:` による例外握りつぶし | `96162c9` | 解決 |
| C-002 | High | HEAD→GET フォールバック条件が広すぎ | `96162c9` | 解決 |
| T-001 | Critical | テストゼロ | `e20da53` | 解決（57テスト） |
| T-002 | High | 依存パッケージのフローティングバージョン | `665ad5e` | 解決（ピンロック） |
| T-003 | High | CI品質ゲートなし | `665ad5e` | 解決（pytest+ruff） |
| C-003 | High | scaffold.py のエラーメッセージ不足 | `96162c9` | 解決 |
| D-002 | High | ワークフロー説明の欠落 | `96162c9` | 解決 |
| D-003 | Medium | Python バージョン要件の未記載 | `96162c9` | 解決 |
| C-004 | Medium | 日付パース失敗時の silent failure | `96162c9` | 解決 |
| C-005 | Medium | pass 文の意図不明 | `a079120` | 解決（コメント追加） |
| C-006 | Medium | スラッグ切り詰めのエッジケース | `96162c9` | 解決 |
| T-004 | Medium | .env.example 未作成 | — | 対象外（環境変数未使用） |
| T-005 | Medium | feeds.yml バリデーション欠落 | `665ad5e` | 解決 |
| D-005 | Medium | schema.md の推奨/必須の曖昧さ | `f4e1251` | 解決 |
| D-006 | Medium | テンプレートに記述例なし | `f4e1251` | 解決 |
| T-006 | Medium | HTTP リトライ機構なし | `665ad5e` | 解決（_http.py） |
| T-007 | Medium | ワークフロー失敗通知なし | `665ad5e` | 解決 |
| T-008 | Low | ログ形式の不統一 | `665ad5e`, `dbe7305` | 解決（logging統一） |
| C-007 | Low | デッドコード | `96162c9` | 解決 |
| C-008 | Low | User-Agent バージョン管理 | `a079120` | 解決（VERSION定数） |
| D-007 | Low | README特徴セクションの不足 | `96162c9` | 解決 |
| D-008 | Low | README/CONTRIBUTING の重複 | `a079120` | 解決 |
| X-001 | Medium | キーワード表記ゆれ対応不足 | `6db7fc1` | 解決（柔軟区切りパターン） |
| X-002 | Low | 日付フィルタの境界問題 | `96162c9` | 解決（.date()比較） |
| X-003 | Low | --days 負数受付 | `96162c9` | 解決（positive_int） |

</details>

## 指摘サマリ

| 象限 | 件数 | 概要 |
|------|------|------|
| [1] 今すぐやる | 0 | — |
| [2] 計画的に対応 | 0 | — |
| [3] 手が空いたら | 1 | requests の動的インポート |
| [4] 余裕があれば | 3 | ドキュメント・テスト・設定の軽微な改善 |

---

## [3] 手が空いたら（Medium × small）

### C-009 | Medium | コード品質 | `scripts/check_links.py:91-93`, `scripts/scaffold.py:72-73`
- **問題**: `requests` をモジュールレベルでインポートせず、`except Exception as e:` ブロック内で `import requests as _requests` として動的インポートしている。`_http.create_session()` 経由で `requests` は間接的に利用されているが、例外型の参照のためだけに動的インポートするのはアンチパターン
- **対応**: `import requests` をモジュールレベルに追加し、`except Exception` を `except requests.exceptions.RequestException` に絞り込む
- **修正案**:
```diff
  # check_links.py
+ import requests
  ...
- except Exception as e:
-     import requests as _requests
-     if isinstance(e, _requests.exceptions.Timeout):
+ except requests.exceptions.RequestException as e:
+     if isinstance(e, requests.exceptions.Timeout):
```
- **工数**: small | **影響範囲**: check_links.py, scaffold.py | **根拠**: 動的インポートの失敗で元の例外がマスクされるリスク

---

## [4] 余裕があれば（Low）

### D-009 | Low | ドキュメント | `CONTRIBUTING.md`
- **問題**: PR前に実行すべき品質チェック（`pytest`, `ruff check .`）の手順が未記載
- **対応**: 「3. バリデーション」セクションに `pytest` と `ruff check .` の実行手順を追加
- **工数**: small

### T-009 | Low | テスト | テスト全体
- **問題**: 57テストは全て純関数の単体テスト。`check_feeds()`, `main()` 等の統合関数はテスト未実装
- **対応**: モック付き結合テストの段階的追加（`check_feeds()` → `check_url()` → `main()` の順）
- **工数**: medium | **根拠**: 現段階（ベータ）では単体テストで十分だが、次のステップとして有効

### C-010 | Low | 設定 | `scripts/check_links.py:28`, `scripts/scaffold.py:41`, `scripts/_http.py:8`
- **問題**: タイムアウト値がスクリプト間で異なる（check_links: 10秒、scaffold: 30秒、_http.pyデフォルト: 10秒）が、値の根拠がコード上に未記載
- **対応**: 各タイムアウト値にコメントで根拠を付記（check_links: 死活確認のため短め、scaffold: HTML全文取得のため長め）
- **工数**: small

---

## ドキュメント状況

| 項目 | 状態 | 評価 |
|------|------|------|
| README.md | RSS監視、ワークフロー表、環境要件、構成図 | 良好 |
| CONTRIBUTING.md | エントリ追加手順、PR規約 | 良好（テスト手順未記載: D-009） |
| docs/schema.md | スキーマ定義、推奨フィールド注記追加済み | 良好 |
| entries/_template.md | 記述例追加済み | 良好 |
| mkdocs.yml | サイト設定 | 良好 |

## テスト状況

| 項目 | 状態 |
|------|------|
| テストフレームワーク | pytest 導入済み（`pyproject.toml` 設定済み） |
| 単体テスト | **57件**（5スクリプト全てカバー） |
| 結合テスト | 未実装（T-009） |
| CI テスト実行 | `ci.yml` で `pytest -v --tb=short` |
| lint CI 実行 | `ci.yml` で `ruff check .` |

### テスト内訳

| 対象スクリプト | テスト数 | カバー範囲 |
|---------------|---------|-----------|
| check_rss.py | 16 | normalize_url, matches_keywords, parse_published_date, format_* |
| validate_frontmatter.py | 11 | validate_file, find_entry_files |
| scaffold.py | 12 | extract_title, extract_published_at, detect_language, generate_slug, format_output |
| check_links.py | 7 | check_url（モック）, load_entries |
| generate_index.py | 11 | _format_date, generate_by_*, generate_index_md |

## 運用準備状況（ベータ段階基準）

| 項目 | 状態 | 評価 |
|------|------|------|
| 基本エラーハンドリング | 例外型を絞り込み、エラーログ出力 | 良好 |
| ログ出力 | `logging` モジュール統一済み | 良好 |
| CI/CD | 6本稼働中 + 品質ゲート（pytest+ruff） | 良好 |
| シークレット管理 | ハードコードなし | 良好 |
| 依存管理 | `==X.Y.Z` ピンロック済み | 良好 |
| 障害耐性 | HTTPリトライ（_http.py）、feeds.ymlバリデーション | 良好 |
| ワークフロー通知 | 失敗時 GitHub Issue 自動作成 | 良好 |

---

## 推奨アクション（次の3ステップ）

1. **requests の動的インポート解消**（C-009）
   - check_links.py と scaffold.py の `import requests` をモジュールレベルに移動
   - `except Exception` を `except requests.exceptions.RequestException` に変更

2. **CONTRIBUTING.md にテスト・lint手順を追加**（D-009）
   - PR前チェックリストとして `pytest` と `ruff check .` を明記

3. **結合テストの段階的追加**（T-009）
   - `check_feeds()` のモック付き結合テストから開始
   - カバレッジ計測の導入検討

## 並列修正可能グループ

以下は相互に独立しており、並列で修正可能:

- **グループA**: C-009（check_links.py + scaffold.py のインポート修正）
- **グループB**: D-009（CONTRIBUTING.md の更新）
- **グループC**: T-009（結合テスト追加）

## 改善推移

| 指標 | 前回（`6db7fc1`） | 今回（`f4e1251`） | 変化 |
|------|-----------------|-----------------|------|
| 段階 | アルファ | ベータ | 昇格 |
| テスト数 | 0 | 57 | +57 |
| CI品質ゲート | なし | pytest + ruff | 導入 |
| ログ統一 | 未統一（print混在） | logging モジュール | 統一 |
| 依存固定 | フローティング | ピンロック | 改善 |
| HTTPリトライ | なし | urllib3.util.Retry | 導入 |
| 指摘数 | 25件（C:1/H:6/M:11/L:7） | 4件（M:1/L:3） | -21件 |
| ファイル数 | 50 | 82 | +32 |

## 次回注目ポイント

- 結合テスト導入後のカバレッジ推移
- Dependabot 設定による依存更新の自動化
- feeds.yml のフィード増加に伴うフィルタ精度の継続監視
