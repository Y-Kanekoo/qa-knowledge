# QA Knowledge — 他社QA事例・ナレッジ集

[![コード品質チェック](https://github.com/Y-Kanekoo/qa-knowledge/actions/workflows/ci.yml/badge.svg)](https://github.com/Y-Kanekoo/qa-knowledge/actions/workflows/ci.yml)

テック企業のQA（品質保証）事例・ナレッジを構造化して収集するリポジトリ。

各エントリには元記事へのリンクだけでなく、**「何が学べるか」** を具体的に記述し、単なるリンク集を超えた実用的なナレッジベースを目指す。

## 規模

- **103件**のエントリ、**22社**以上の企業事例を収録
- **全12 QAドメイン**をカバー（テスト戦略、テスト自動化、CI/CD、信頼性、品質メトリクス、QA組織設計、AIテスト、セキュリティテスト、パフォーマンステスト、モバイルテスト、シフトレフト、オブザーバビリティ）
- 日本語 39件 / 英語 64件

## 特徴

- YAML frontmatter による構造化メタデータ（企業名、QA領域、タグ、難易度等）
- 会社別・QA領域別・タグ別・追加日順の自動生成インデックス
- MkDocs Material による全文検索対応の静的サイト
- GitHub Actions による CI/CD（バリデーション、インデックス自動更新、サイトデプロイ、リンク・RSS監視）
- RSSフィード日次巡回による新着QA記事の自動検出（Discord通知 + GitHub Issue）
- Claude Code カスタムコマンド14種によるワークフロー自動化
- [ドキュメントサイト](https://y-kanekoo.github.io/qa-knowledge/)（GitHub Pages）

## 収録対象

テックブログ、カンファレンス発表、OSS設定例、ハンドブック等、公開されているQA事例を幅広く収録する。

**QA領域**: テスト戦略、テスト自動化、CI/CD、SRE/カオスエンジニアリング、品質メトリクス、QA組織設計、AI/LLMテスト、セキュリティテスト、パフォーマンステスト、モバイルテスト、シフトレフト、オブザーバビリティ

## クイックスタート

### 環境要件

- Python 3.12 以上
- 依存パッケージ: `pip install -r requirements.txt`

### エントリを追加する

詳細は [CONTRIBUTING.md](CONTRIBUTING.md) を参照。

### ローカルでサイトをプレビュー

```bash
pip install -r requirements.txt
mkdocs serve
# http://127.0.0.1:8000 で確認
```

## RSS監視（自動・日次）

毎日 GitHub Actions が RSS フィードを巡回し、未収録のQA関連記事を検出する。

- **通知先**: Discord Webhook（リッチEmbed形式）+ GitHub Issue
- 監視対象: `feeds.yml` で定義（Google, Netflix, Spotify, Mercari, LY Corporation, Cybozu, DeNA 等14フィード）
- QAキーワードでフィルタリング（汎用ブログからQA記事のみ抽出）
- 手動実行: Actions タブ → 「新着QA記事チェック（日次）」→ Run workflow

### フィードの追加

`feeds.yml` に追記する:

```yaml
- name: ブログ名
  company: 企業名
  url: https://example.com/feed.xml
  language: en  # or ja
  skip_keyword_filter: false  # QA専門ブログの場合は true
```

## リポジトリ構成

```
qa-knowledge/
├── entries/           # エントリ（1記事1ファイル、フラット配置）
├── indexes/           # 自動生成インデックス（by-company, by-domain, by-tag, by-date）
├── scripts/
│   ├── scaffold.py            # エントリ骨格生成（URLからメタデータ自動抽出）
│   ├── validate_frontmatter.py # frontmatterバリデーション
│   ├── generate_index.py       # インデックス自動生成
│   ├── check_links.py          # リンク切れチェック
│   └── check_rss.py            # RSSフィード巡回（新着QA記事の自動検出）
├── docs/              # スキーマ定義等のドキュメント
├── .github/workflows/ # CI/CD（バリデーション、インデックス生成、サイトデプロイ、リンクチェック）
├── mkdocs.yml         # MkDocs Material 設定
└── index.md           # サイトトップページ（自動生成）
```

## GitHub Actions ワークフロー

| ワークフロー | トリガー | 概要 |
|-------------|---------|------|
| フロントマター検証 | `entries/` への push | frontmatter スキーマの自動検証 |
| インデックス自動生成 | main への push（`entries/` 変更時） | by-company, by-domain 等のインデックスを再生成 |
| ドキュメントサイトのデプロイ | main への push | MkDocs Material サイトを GitHub Pages にデプロイ |
| リンク切れチェック（月次） | 月次スケジュール / 手動 | 全エントリのURLが有効か確認し、問題があれば Issue 作成 |
| 新着QA記事チェック（日次） | 日次スケジュール / 手動 | RSS 巡回、未収録記事を Discord + Issue で通知 |

## スキーマ

各エントリの frontmatter スキーマは [docs/schema.md](docs/schema.md) を参照。

## ライセンス

[CC BY 4.0](LICENSE)
