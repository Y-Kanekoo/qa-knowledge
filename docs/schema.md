# フロントマタースキーマ定義

各エントリの `.md` ファイルは YAML フロントマターで構造化メタデータを持つ。

## 必須フィールド

| フィールド | 型 | 説明 | 例 |
|-----------|------|------|------|
| `title` | string | エントリのタイトル | `"Hermetic Servers"` |
| `company` | string | 企業名 | `"Google"` |
| `url` | string | 元コンテンツのURL（HTTPS） | `"https://..."` |
| `published_at` | date | 元コンテンツの公開日（ISO 8601） | `"2024-03-15"` |
| `content_type` | string | コンテンツ種別（下記の許可値） | `"blog"` |
| `qa_domains` | list[string] | QA領域（1つ以上、下記の許可値） | `["test-automation"]` |
| `tags` | list[string] | 自由キーワード（小文字ケバブケース） | `["flaky-tests"]` |
| `language` | string | コンテンツの言語 | `"en"` or `"ja"` |
| `added_at` | date | リポジトリへの追加日（ISO 8601） | `"2026-03-10"` |

## 推奨フィールド

| フィールド | 型 | 説明 | 許可値 |
|-----------|------|------|--------|
| `industry` | string | 企業の業種 | `tech`, `finance`, `ecommerce`, `media`, `gaming`, `saas`, `other` |
| `difficulty` | string | 内容の難易度 | `beginner`, `intermediate`, `advanced` |

## オプションフィールド

| フィールド | 型 | 説明 |
|-----------|------|------|
| `speaker` | string | カンファレンス発表者名 |
| `conference` | string | カンファレンス名 |
| `video_url` | string | 動画URL |
| `slide_url` | string | スライドURL |
| `related_tools` | list[string] | 関連ツール名 |
| `deprecated` | bool | リンク切れ・陳腐化フラグ（デフォルト: false） |

## content_type 許可値

| コード | 種別 |
|--------|------|
| `blog` | テックブログ記事 |
| `conference_talk` | カンファレンス発表 |
| `slide_deck` | スライドのみ公開 |
| `oss_config` | OSS設定・実装例 |
| `handbook` | 社内ハンドブック公開 |
| `case_study` | ケーススタディ・ポストモーテム |
| `book_excerpt` | 書籍・SREドキュメント |
| `podcast` | ポッドキャスト |
| `video` | 動画 |

## qa_domains 許可値

| コード | 説明 |
|--------|------|
| `test-strategy` | テスト戦略・全体設計・テストピラミッド |
| `test-automation` | E2E/UI/APIテスト自動化 |
| `ci-cd` | CI/CDパイプラインとの統合 |
| `reliability` | SRE・カオスエンジニアリング |
| `quality-metrics` | 品質メトリクス・DORA・ダッシュボード |
| `org-design` | QA組織体制・役割設計・文化 |
| `ai-testing` | AI/LLMを使ったテスト / AI対象のテスト |
| `security-test` | セキュリティ・コンプライアンス |
| `performance-test` | パフォーマンス・負荷テスト |
| `mobile-cross-browser` | モバイル・クロスブラウザ |
| `shift-left` | シフトレフト・開発プロセス組み込み |
| `observability` | 監視・オブザーバビリティ活用のQA |
