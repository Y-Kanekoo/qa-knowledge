---
schema_version: 1
generated_at: 2026-03-05T05:46:19+09:00
commit_hash: 6db7fc145e36f5ce67703fb03db183e455a34054
file_count: 50
stack: Python (pyyaml, mkdocs-material, requests, bs4, python-frontmatter, feedparser)
stage: アルファ
total_issues: 25
critical: 1
high: 6
medium: 11
low: 7
---

# プロジェクトレビューレポート

## 概要

| 項目 | 値 |
|------|-----|
| 対象コミット | `6db7fc1` |
| ファイル数 | 50 |
| スタック | Python |
| 段階 | アルファ |
| 指摘数 | 25件（Critical: 1 / High: 6 / Medium: 11 / Low: 7） |

## エグゼクティブサマリ

QAナレッジ収集リポジトリとして基本的なアーキテクチャは適切に構成されている。frontmatter バリデーション、インデックス自動生成、MkDocs デプロイ、RSS監視、リンクチェックの5本のCI/CDワークフローが稼働中。最大の課題は**テストゼロ**で品質ゲートが存在しないこと。外部API通信を行う3スクリプトが本番稼働中にもかかわらず、リグレッション検出手段がない。依存パッケージのバージョン固定も不足しており、再現性に懸念がある。

## 指摘サマリ

| 象限 | 件数 | 概要 |
|------|------|------|
| [1] 今すぐやる | 2 | 例外処理の厳密化 |
| [2] 計画的に対応 | 5 | テスト導入、CI品質ゲート、依存固定 |
| [3] 手が空いたら | 11 | エラーハンドリング改善、ドキュメント充実、設定バリデーション |
| [4] 余裕があれば | 7 | ログ統一、User-Agent管理、ドキュメント冗長解消、入力バリデーション |

---

## [1] 今すぐやる（Critical/High × small）

### C-001 | High | エラーハンドリング | `scripts/check_rss.py:45`
- **問題**: `load_existing_urls()` で `except Exception:` により全例外を握りつぶし。エラー情報が完全に喪失
- **対応**: 特定の例外型（`yaml.YAMLError`, `IOError`）に絞り、stderr にログ出力
- **修正案**:
```diff
  try:
      post = frontmatter.load(md_file)
      url = post.metadata.get("url", "")
      if url:
          urls.add(normalize_url(url))
- except Exception:
+ except (yaml.YAMLError, IOError) as e:
+     print(f"警告: {md_file.name} の読み込みに失敗: {e}", file=sys.stderr)
      continue
```
- **工数**: small | **根拠**: エラー情報喪失で問題診断が困難

### C-002 | High | 障害耐性 | `scripts/check_links.py:64-68`
- **問題**: HEAD リクエスト失敗時、ステータス `>= 400` で一律 GET フォールバック。404でもGETリトライする無駄
- **対応**: 405 (Method Not Allowed) に限定してフォールバック
- **修正案**:
```diff
- if response.status_code >= 400:
+ if response.status_code == 405:
```
- **工数**: small | **根拠**: 5xxや404でのGET再実行は不要なネットワーク負荷

---

## [2] 計画的に対応（Critical/High × medium/large）

### T-001 | Critical | テスト | プロジェクト全体
- **問題**: テストゼロ。外部API通信スクリプト3本が本番稼働中にリグレッション検出手段なし
- **対応**: pytest 導入、モック依存の単体テスト実装、CI統合
- **工数**: large | **根拠**: 5スクリプトが GitHub Actions で稼働中。品質保証の基盤が欠落

### T-002 | High | 依存 | `requirements.txt`
- **問題**: 全6パッケージがフローティングバージョン（`>=X.Y`）。再現性なし
- **対応**: `==X.Y.Z` でピンロック、pip audit 導入
- **工数**: small | **根拠**: CI再実行毎に異なるバージョンが入る可能性

### T-003 | High | CI-CD | 全ワークフロー
- **問題**: テスト自動実行・lintチェックが一切ない。品質ゲートなし
- **対応**: CI に `pytest` と `ruff check .` ステップを追加
- **工数**: small | **根拠**: PR マージ時のコード品質を担保する仕組みが欠落

### C-003 | High | エラーハンドリング | `scripts/scaffold.py:59`
- **問題**: `requests.RequestException` で即 `sys.exit(1)`。ユーザーへの診断情報が不十分
- **対応**: ConnectionError / Timeout を区別し、具体的なエラーメッセージを表示
- **工数**: medium | **根拠**: ユーザー向けCLIツールとして、無情報な終了はUXを悪化させる

### D-002 | High | ドキュメント | `README.md`
- **問題**: 5本のワークフローのトリガー条件・スケジュールが未文書化
- **対応**: README に「## GitHub Actions ワークフロー」セクションを表形式で追加
- **工数**: medium | **根拠**: 保守者がワークフロー実行タイミングを把握するために必要

---

## [3] 手が空いたら（Medium/Low × small/medium）

### D-003 | High → Medium（統合） | ドキュメント | `README.md`
- **問題**: クイックスタートに `pip install -r requirements.txt` の前提条件未記載。Python バージョン要件も不明
- **対応**: 冒頭に環境要件（Python 3.12+、pip install）を明記
- **工数**: small

### C-004 | Medium | 可読性 | `scripts/check_rss.py:172`
- **問題**: 日付パース失敗時に `except ValueError: pass` で silent failure
- **対応**: dry-run 時にスキップログを出力
- **工数**: small

### C-005 | Medium | 可読性 | `scripts/validate_frontmatter.py:87-89`
- **問題**: `isinstance(published_at, date)` チェック後に `pass` のみ。意図が不明確
- **対応**: コメント追加または early return で意図を明確化
- **工数**: small

### C-006 | Medium | エッジケース | `scripts/scaffold.py:128-129`
- **問題**: スラッグ切り詰め後の末尾ハイフン除去で60字未満になる可能性
- **対応**: 長さ確認を再度実施
- **工数**: small

### T-004 | Medium | 設定 | `.env.example`
- **問題**: 環境変数設定例ファイルが存在しない
- **対応**: `.env.example` を作成し、タイムアウト値等のカスタマイズ可能な設定を記載
- **工数**: small

### T-005 | Medium | 運用 | `feeds.yml`
- **問題**: feeds.yml のスキーマバリデーション機構がない
- **対応**: validate_frontmatter.py に feeds.yml 検証を統合、またはスクリプト新規作成
- **工数**: small

### D-005 | Medium | ドキュメント | `docs/schema.md`
- **問題**: `industry` と `difficulty` が「推奨」だが実態は全エントリで記入済み。定義と実装の乖離
- **対応**: schema.md で「推奨」→「必須」に変更、またはバリデータの挙動を明記
- **工数**: small

### D-006 | Medium | ドキュメント | `entries/_template.md`
- **問題**: 本文セクション「概要」「何が学べるか」の記述例がない
- **対応**: テンプレートに最小限のサンプルを追加、または既存エントリへのリンクを記載
- **工数**: small

### T-006 | Medium | 依存 | HTTP通信全般
- **問題**: リトライ機構なし。check_links.py, check_rss.py, scaffold.py がネットワーク障害に弱い
- **対応**: `urllib3.util.Retry` または `tenacity` ライブラリ導入
- **工数**: small

### T-007 | Medium | CI-CD | ワークフロー全体
- **問題**: validate.yml, generate-index.yml にワークフロー失敗時の通知機構がない
- **対応**: 失敗時の GitHub Issue 自動作成を全ワークフローに統一
- **工数**: small

---

## [4] 余裕があれば（Medium/Low × large、Low全般）

### T-008 | Low | 運用 | ログ出力
- **問題**: スクリプト間でログ形式が不統一。`print()` 直接出力と `sys.stderr` 混在
- **対応**: `logging` モジュール導入、ログレベル統一
- **工数**: medium

### C-007 | Low | スタイル | `scripts/check_rss.py:277-279`
- **問題**: `main()` 末尾の `if ... : pass` はデッドコード
- **対応**: 削除
- **工数**: small

### C-008 | Low | セキュリティ（軽微） | `scripts/scaffold.py:54`
- **問題**: User-Agent バージョンが固定値
- **対応**: 定数化して管理
- **工数**: small

### D-007 | Low | ドキュメント | `README.md`
- **問題**: 特徴セクションに「リンク切れチェック」ワークフローが未記載
- **対応**: 「GitHub Actions による CI/CD（バリデーション、インデックス更新、デプロイ、リンク・RSS監視）」に更新
- **工数**: small

### D-008 | Low | ドキュメント | `README.md`, `CONTRIBUTING.md`
- **問題**: エントリ追加方法の記述が両ファイルで重複
- **対応**: README からは CONTRIBUTING.md への参照に簡素化
- **工数**: small

---

## 外部レビュー（Codex CLI）

Codex CLI（gpt-5.3-codex）による外部レビュー結果。Critical/High は検出なし。以下の3件を追加指摘として統合。

### X-001 | Medium | コード品質 | `scripts/check_rss.py:76-78`
- **問題**: ASCII キーワードを `\b...\b` で厳密マッチしているため、表記ゆれ（`integration-test`, `load-testing`, `e2eテスト`）を取りこぼす。Codex による実証テストで `integration-test strategy` が `integration test` にマッチしないことを確認
- **対応**: 英単語のみ（`[A-Za-z]+`）のキーワードにだけ単語境界を使い、記号・複合語を含むキーワードは `-_/` と空白を同一視する正規化後の部分一致に切り替え
- **工数**: small | **根拠**: RSS検出の主目的（新着QA記事の拾い上げ）に対し、Recall 低下を招く

### X-002 | Low | エッジケース | `scripts/check_rss.py:132,168-169`
- **問題**: 日付フィルタが `datetime` 比較のため、境界日に公開された記事が時刻差で除外される可能性
- **対応**: `date` 同士で比較する（`cutoff_date = (...).date()`, `pub_date.date() < cutoff_date`）
- **工数**: small

### X-003 | Low | 入力バリデーション | `scripts/check_rss.py:251`
- **問題**: `--days` に負数を受け付けるため、誤指定で「ほぼ全件除外」になる
- **対応**: argparse の型を非負整数バリデータにする（`value >= 0` を強制）
- **工数**: small

---

## ドキュメント状況

| 項目 | 状態 | 評価 |
|------|------|------|
| README.md | RSS監視セクション追加済み、リポジトリ構成更新済み | 良好（ワークフロー説明が不足） |
| CONTRIBUTING.md | エントリ追加手順、PR規約を記載 | 良好（記述例が不足） |
| docs/schema.md | frontmatter スキーマ定義 | 中程度（推奨/必須の曖昧さ） |
| entries/_template.md | テンプレート | 中程度（本文例なし） |
| mkdocs.yml | サイト設定 | 良好 |

## テスト状況

| 項目 | 状態 |
|------|------|
| テストフレームワーク | **未導入** |
| 単体テスト | **0件** |
| 結合テスト | **0件** |
| CI テスト実行 | **なし** |
| lint CI 実行 | **なし** |

### テスト優先実装リスト

| 優先度 | 対象 | テスト項目 | 工数 |
|--------|------|----------|------|
| 1 | check_rss.py | キーワードフィルタ、URL正規化、日付フィルタ | medium |
| 2 | validate_frontmatter.py | スキーマ検証、エラー報告 | small |
| 3 | check_links.py | ステータスコード判定、フォールバック | medium |
| 4 | scaffold.py | メタデータ抽出、スラッグ生成 | medium |
| 5 | generate_index.py | インデックス生成、メタデータマッピング | small |

## 運用準備状況（アルファ段階基準）

| 項目 | 状態 | 評価 |
|------|------|------|
| 基本エラーハンドリング | 実装済み（改善余地あり） | 中程度 |
| ログ出力 | print/stderr 混在 | 要改善 |
| CI/CD | 5本稼働中 | 良好（品質ゲート欠落） |
| シークレット管理 | ハードコードなし | 良好 |
| 依存管理 | フローティングバージョン | 要改善 |

---

## 推奨アクション（次の3ステップ）

1. **pytest 導入 + check_rss.py のユニットテスト作成**（T-001）
   - `matches_keywords()`, `normalize_url()`, `parse_published_date()` は純関数でテスト容易
   - CI に pytest ステップを追加（T-003）

2. **requirements.txt のバージョンピンロック化**（T-002）
   - `pip freeze > requirements.txt` でロック
   - Dependabot 設定で定期更新

3. **例外処理の厳密化**（C-001, C-002）
   - 広い `except Exception` を特定の例外型に絞り込み
   - エラーログ出力の追加

## 並列修正可能グループ

以下のグループは相互に独立しており、並列で修正可能:

- **グループA**: C-001, C-004, C-007（check_rss.py 内の修正）
- **グループB**: C-002（check_links.py の修正）
- **グループC**: C-003, C-006, C-008（scaffold.py の修正）
- **グループD**: D-002, D-003, D-007, D-008（README/ドキュメント修正）
- **グループE**: T-001, T-003（テスト・CI基盤構築）

## 次回注目ポイント

- テスト導入後のカバレッジ推移
- CI 品質ゲート追加後の PR ワークフロー
- 依存パッケージの脆弱性スキャン結果
- feeds.yml のフィード増加に伴うフィルタ精度（dry-run で197件検出 → 目標40〜80件）

---

## ナレッジ候補（/sync-knowledge用）

- C-001: Python の広い例外キャッチ（`except Exception`）アンチパターン → kb-python
- C-002: HTTP HEAD→GET フォールバック戦略の設計 → kb-patterns
- T-002: requirements.txt のバージョン管理戦略（フローティング vs ピンロック） → kb-python
- T-003: Python プロジェクトの CI 品質ゲート構成（pytest + ruff） → kb-python
