# RSS 通知の配信先別台帳（有効化待ち）

## 現在の状態

永続台帳、Discord / GitHub Issue 送信アダプター、CLI、workflow の切替経路を実装しています。
**フラグは既定で無効、RSS ジョブの権限は `contents: read` のままです。**
この変更だけを取り込んでも日跨ぎ重複は止まりません。変数未設定時は既存の通知経路が動きます。
実通知、台帳作成、権限・Secrets・変数の変更は行っていません。

新コードは既存の一時的な `GITHUB_TOKEN` を使います。新しい PAT や秘密値は不要です。
コードの実装・モック試験に実認証情報は必要ありません。実環境で有効化する際だけ下記の承認・準備が必要です。

## 実装したこと

- `scripts/_delivery_state.py`: 専用ブランチ上の既存 JSON ファイルを読み、blob SHA による比較更新で保存
- `scripts/_delivery.py`: 配信先の論理名と正規化 URL の SHA-256 ごとに予約・重複判定
- `scripts/_notification_senders.py`: provider の成功・明確な拒否・結果不明を分類
- `scripts/notify_rss.py`: 記事収集を保持し、Discord と Issue を独立処理して機械可読な結果を保存
- `check-rss.yml`: `RSS_DELIVERY_LEDGER_ENABLED` が文字列 `true` のときだけ新経路を実行。旧 Issue 作成 action は同時実行しない
- schedule と手動実行に固定 concurrency group を使い、中断による不明状態を減らす。正しさは比較更新でも保護

送信前は `pending`、確認済み成功後だけ `delivered`、確実な拒否は `retryable` です。
タイムアウト、5xx、リダイレクト、形式不正の成功応答などは `pending` を維持し、自動再送しません。
保存するのは URL ハッシュ、状態、試行 ID、時刻だけです。記事本文・Webhook・token・例外本文は保存しません。

Discord は最大10件ずつ、`wait=true` を指定し、HTTP 200 とメッセージ ID を確認します。
GitHub は HTTP 201 と Issue 番号を確認します。通常は最大500件の候補を1つの Issue にまとめます。
60,000文字を超える本文は送信せず拒否扱いにします。必要なら `--issue-batch-size 50` 等で分割できます。
前のバッチだけ成功した場合、その成功を保持して後続の失敗・未実行分だけを次回処理します。

参考: [Discord Execute Webhook](https://docs.discord.com/developers/resources/webhook#execute-webhook)、
[GitHub Create an issue](https://docs.github.com/en/rest/issues/issues#create-an-issue)、
[GitHub Create or update file contents](https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents)

## 有効化に必要な操作（未実施）

1. 専用ブランチ `rss-delivery-state` の `.state/rss-delivery.json` を一度だけ作成・確認する

   ```json
   {"schema_version": 1, "destinations": {}}
   ```

   過去の通知は空台帳には入りません。初回に既存候補が再通知され得るため、
   配信成功を確認できる履歴だけを配信先別に移行するか、初回の対象件数をレビューします。
   Issue の作成成功を Discord の送信成功の代用にはしません。
   運用後にファイルが消えても空台帳を自動作成してはいけません。

2. **承認後に限り** RSS ジョブの `permissions.contents` を `read` から `write` に変更する

   `issues: write` は既存権限です。台帳の保存先は上記の専用ブランチで、main に状態を書きません。
   現在の `contents: read` のままでは新規予約の PUT が拒否され、通知前に停止します。
   branch protection 等により書込みが拒否された場合も停止し、無記録の従来送信には戻しません。

3. **承認後に限り** リポジトリ変数 `RSS_DELIVERY_LEDGER_ENABLED=true` を設定する

   `DISCORD_WEBHOOK_URL` は既存 Secret を使用します。認証値はチャット・ファイルへコピーしません。
   workflow のコード接続は実装済みなので、追加実装は不要です。
   有効化後は Actions summary で配信先別の delivered / already_delivered / pending / rejected / not_attempted を確認します。
   このパッチでは変数を設定していません。実環境の送信・書込み確認も行っていません。

## 送信しない確認方法

リポジトリルートから実行します。以下は RSS の読取りと記事出力のみです。
state API、Discord、GitHub Issue API は呼びません。

```bash
python -m scripts.notify_rss --dry-run --format markdown --status-file rss_status.json
# --enabled と --dry-run が両方あっても送信しない
python -m scripts.notify_rss --enabled --dry-run --format markdown
# --enabled がなければ既定で通知無効
python -m scripts.notify_rss --format markdown
```

実通知は承認済みの有効化後に、workflow 内の `--enabled` 経路が行います。
`--state-branch` / `--state-path` / `--repository` で設定を確認できますが、通常は既定値を使います。
`--days` の既定は既存処理と同じ365日です。元の収集記事・知識データは削除しません。

## 失敗・中断時の扱い

- **予約保存失敗:** そのバッチは送っていません。権限・台帳を復旧してから再実行
- **送信後の結果保存失敗・中断:** `pending` のまま。通知先を確認するまで自動再送しない
- **明確な拒否:** `retryable`。次回実行で再試行。現在の実行では後続バッチを停止
- **片方の通知先の失敗:** もう一方は独立して自身の予約・送信を続行。全体ジョブは失敗を明示
- **未確認状態の解決:** URL ハッシュと送信先を照合し、成功が確認できた場合のみ `delivered`、未送信が確実な場合のみ `retryable` に管理者が修正
- **ファイル消失・破損:** 既知の正常な台帳を復旧して、失われた期間の結果を照合。空台帳からの再開は重複の原因になる

`pending` に自動期限はありません。送信先と台帳は単一トランザクションではないため、exactly-once は保証しません。
論理名は `discord:qa-rss` と `github:qa-rss-issues`。Webhook を単に再発行しても履歴を破棄しません。
変数を無効に戻すと既存の台帳なし通知に戻り、日跨ぎ重複が再発する点に注意してください。
Actions cache や短期 artifact は消失し得るため、この台帳の代用にはしません。
