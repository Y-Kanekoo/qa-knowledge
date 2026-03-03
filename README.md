# QA Knowledge — 他社QA事例・ナレッジ集

テック企業のQA（品質保証）事例・ナレッジを構造化して収集するリポジトリ。

各エントリには元記事へのリンクだけでなく、**「何が学べるか」** を具体的に記述し、単なるリンク集を超えた実用的なナレッジベースを目指す。

## 特徴

- YAML frontmatter による構造化メタデータ（企業名、QA領域、タグ、難易度等）
- 会社別・QA領域別・タグ別・追加日順の自動生成インデックス
- MkDocs Material による全文検索対応の静的サイト
- GitHub Actions によるバリデーション・インデックス自動更新・サイトデプロイ
- RSSフィード監視による新着QA記事の自動検出（週次 → GitHub Issue通知）

## 収録対象

テックブログ、カンファレンス発表、OSS設定例、ハンドブック等、公開されているQA事例を幅広く収録する。

**QA領域**: テスト戦略、テスト自動化、CI/CD、SRE/カオスエンジニアリング、品質メトリクス、QA組織設計、AI/LLMテスト、セキュリティテスト、パフォーマンステスト、モバイルテスト、シフトレフト、オブザーバビリティ

## クイックスタート

### エントリを追加する

```bash
# 1. URLからエントリの骨格ファイルを生成
python scripts/scaffold.py "https://example.com/blog/..." --company "CompanyName"

# 2. 生成されたファイルを編集（content_type, qa_domains, tags, 概要, 何が学べるか を記入）
# 3. バリデーション
python scripts/validate_frontmatter.py

# 4. インデックスを再生成
python scripts/generate_index.py

# 5. コミット
```

### ローカルでサイトをプレビュー

```bash
pip install -r requirements.txt
mkdocs serve
# http://127.0.0.1:8000 で確認
```

## RSS監視（自動）

毎週月曜に GitHub Actions が RSS フィードを巡回し、
未収録のQA関連記事を GitHub Issue で通知する。

- 監視対象: `feeds.yml` で定義（Google Testing Blog, Netflix, Spotify, メルカリ 等）
- QAキーワードでフィルタリング（汎用ブログからQA記事のみ抽出）
- 手動実行: Actions タブ → 「新着QA記事チェック（週次）」→ Run workflow

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

## スキーマ

各エントリの frontmatter スキーマは [docs/schema.md](docs/schema.md) を参照。

## ライセンス

[CC BY 4.0](LICENSE)
