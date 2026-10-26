# コントリビューションガイド

QA事例・ナレッジの追加を歓迎します。

## エントリの追加方法

### 推奨: Claude Code カスタムコマンド

Claude Code を使っている場合、`/add-entry` コマンドで骨格生成からメタデータ・概要・学びの自動補完まで一括で実行できます:

```
/add-entry https://example.com/blog/... --company CompanyName
```

### 手動での追加

#### 1. 骨格ファイルの生成

```bash
python scripts/scaffold.py "https://example.com/blog/..." --company "CompanyName"
```

`drafts/` に `status: draft` の骨格が生成されます。下書きのままコミット・マージして保存できます。
公開日が取得できなければ空欄のまま保存し、分類・要約を仮の値で埋めて公開しないでください。
下書きは公開インデックス・記事数・サイト検索に含まれません。

#### 2. 内容の記入

以下のフィールドを手動で記入してください:

| フィールド | 説明 | 例 |
|-----------|------|------|
| `content_type` | コンテンツ種別 | `blog`, `conference_talk`, `handbook` 等 |
| `qa_domains` | QA領域（1つ以上） | `test-automation`, `ci-cd` 等 |
| `tags` | 自由キーワード（小文字ケバブケース） | `playwright`, `flaky-tests` 等 |
| `industry` | 企業の業種（推奨） | `tech`, `finance`, `ecommerce` 等 |
| `difficulty` | 難易度（推奨） | `beginner`, `intermediate`, `advanced` |

本文セクション:

- **概要**: 2〜3文で記事の内容を説明
- **何が学べるか**: 3〜5点の箇条書き。抽象的な感想ではなく、記事に書かれた具体的な手法・数値を記述

#### 3. 下書きの検証と公開記事への移行

```bash
# 保存形式の検証。未記入の分類や公開日は下書きのまま保持する
python scripts/validate_drafts.py

# 必須メタデータと「概要」「何が学べるか」を補完した後に実行
python scripts/promote_draft.py drafts/<file>.md

# 公開記事の検証 → 公開用インデックスの更新
python scripts/validate_frontmatter.py
python scripts/generate_index.py
```

公開前検証に失敗した下書きは削除されません。移行時に `added_at` を実際の収録日（UTC）へ更新します。
インデックスの「最終更新」は公開記事の `added_at` の最大値です。再生成した日や下書きの保存日ではありません。
同じURLの公開や既存ファイルの上書きは拒否します。概要の正確性・QAとの関連性・学びの具体性はレビューで確認してください。

#### 日次収集とIssue通知の対象期間

- 自動収集PR: `--days 3`。UTCの3日前以降（境界日を含む）。新規に保存した下書きが0件ならPRを作成・更新しません。
- Issue通知: `--days 365`。収集対象より広い期間の未収録記事を検出します。Issue #347の214件を3日分の期待件数として扱わないでください。
- 公開日不明の記事は両方で検出対象とし、下書きに保持します。`--days 0` は日付制限なしです。
- 両方とも公開済み・下書き保存済みの正規化URLを除外し、同一実行の重複URLも除外します。
- 処理間の受け渡しはJSON、Actionsの新着判定は記事数・真偽値で行います。人向けメッセージを部分一致で解析しません。
- 収集PRは `auto/collect-articles` に集約します。開いている同ブランチのPRから下書きを保持し、補完中の編集を上書きしません。マージ・却下済みのPRは復元しません。
- RSSの取得・解析警告はstderrに出します。フィードの取得失敗と新着0件は同義ではありません。設定・JSON・保存・検証の失敗はPR作成前にジョブを停止します。

#### 4. テスト・Lint の実行

PR を作成する前に、以下のチェックを実行してください:

```bash
# テスト実行
pytest

# コード品質チェック
ruff check .
```

#### 5. PR作成

- ブランチ名: `add/{company}-{slug}`
- 1つのPRに複数エントリを含めてOK

## 許可値一覧

`content_type` と `qa_domains` の許可値は [docs/schema.md](docs/schema.md) を参照してください。

## 品質基準

- 一次情報（公式ブログ・公式発表）を優先。転載・まとめ記事は収録しない
- 「何が学べるか」は具体的な手法・定量データを記述する
- URLは `https://` であること
