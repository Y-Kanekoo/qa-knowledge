# QA Knowledge プロジェクト設定

## プロジェクト概要
テック企業のQA事例・ナレッジを構造化して収集するリポジトリ（103件、22社以上）。

## カスタムコマンド（14種）

| コマンド | 用途 |
|---------|------|
| `/add-entry <URL>` | AI自動補完でエントリ作成 |
| `/validate [ファイル]` | Frontmatter検証+修正提案 |
| `/update-indexes` | インデックス再生成 |
| `/qa-check [--fix]` | ruff+pytest+validate+mkdocs一括チェック |
| `/stats [--detail]` | 統計・QAドメインカバレッジ分析 |
| `/discover [--days N]` | RSS巡回で新着記事発見 |
| `/search-web <キーワード>` | Web検索でQA記事発見 |
| `/check-health` | リンク・CI・脆弱性の総合チェック |
| `/deploy-preview` | MkDocsビルド+プレビュー |
| `/find-entry <クエリ>` | 自然言語でエントリ検索 |
| `/summarize <トピック>` | トピック横断の知見要約 |
| `/compare <ファイル1> <ファイル2>` | エントリ比較分析 |
| `/manage-feeds` | RSSフィード管理 |
| `/setup-notify` | Discord通知設定 |

## 自動化ワークフロー

| ワークフロー | 頻度 | 内容 |
|-------------|------|------|
| check-rss.yml | 日次 | RSS巡回 → Discord通知 + Issue |
| collect-articles.yml | 日次 | scaffold.py で骨格PR自動作成 |
| ci.yml | push/PR | ruff + pytest |
| validate.yml | entries変更時 | Frontmatter検証 |
| generate-index.yml | main push | インデックス自動再生成 |
| deploy-docs.yml | main push | GitHub Pages デプロイ |
| check-links.yml | 月次 | URL死活確認 |

## スクリプト

| スクリプト | 用途 |
|-----------|------|
| `scripts/scaffold.py` | URL → エントリ骨格生成 |
| `scripts/validate_frontmatter.py` | Frontmatter検証 |
| `scripts/generate_index.py` | インデックス自動生成 |
| `scripts/check_links.py` | リンク死活確認 |
| `scripts/check_rss.py` | RSS巡回 + Discord通知 |
| `scripts/score_entries.py` | エントリ品質スコアリング |
| `scripts/_url.py` | URL正規化（共通モジュール） |
| `scripts/_http.py` | HTTPセッション（共通モジュール） |

## エントリ追加の標準手順

1. `/add-entry <URL> --company <企業名>` でエントリ作成（推奨）
2. または `python scripts/scaffold.py <URL> --company <企業名>` で骨格生成 → 手動記入
3. `python scripts/validate_frontmatter.py` で検証
4. `python scripts/generate_index.py` でインデックス更新

## Frontmatter スキーマ（主要フィールド）

- **content_type**: blog, article, conference_talk, slide_deck, oss_config, handbook, case_study, book_excerpt, podcast, video
- **qa_domains**: test-strategy, test-automation, ci-cd, reliability, quality-metrics, org-design, ai-testing, security-test, performance-test, mobile-cross-browser, shift-left, observability
- **tags**: ケバブケース（小文字英数字とハイフン）、`-testing` サフィックスで統一（例: `e2e-testing`, `unit-testing`）
- **language**: en, ja

## 品質基準

- `validate_frontmatter.py` で全エントリがエラーなし
- `ruff check .` がパス
- `pytest` が全テストパス
- エントリ品質スコア 7点以上（`score_entries.py`）

## 技術スタック

- Python 3.12+ / MkDocs Material / GitHub Pages
- ruff（Lint）/ pytest + pytest-cov（テスト）
- feedparser / python-frontmatter / requests / beautifulsoup4
