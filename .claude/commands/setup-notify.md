# Discord Webhook通知の設定 + RSS巡回日次化

check_rss.py に Discord Webhook 通知機能を追加し、GitHub Actions の RSS巡回を日次化する。

## 引数

`$ARGUMENTS` = サブコマンド

- `discord <WEBHOOK_URL>` — Discord Webhook を設定して通知機能を追加
- `status` — 現在の通知設定状況を表示

## 実行手順

### サブコマンド: discord

#### 1. Webhook URL の検証

指定された Webhook URL が Discord の形式（`https://discord.com/api/webhooks/...`）であることを確認。

#### 2. check_rss.py への Discord 通知機能追加

check_rss.py に以下の機能を追加（Edit ツールで既存コードを修正）:

- `--notify discord` 引数の追加
- Discord Webhook にリッチEmbed形式で新着記事を送信する関数:
  ```python
  def send_discord_notification(webhook_url: str, articles: list[dict]) -> None:
      """Discord Webhook にリッチEmbed形式で新着記事を通知する。"""
      # 各記事をEmbed形式で送信
      # フィールド: タイトル、企業名、URL、公開日、QAキーワード
  ```
- 環境変数 `DISCORD_WEBHOOK_URL` からも読み込み可能にする

#### 3. GitHub Actions ワークフローの更新

`.github/workflows/check-rss.yml` を Edit で更新:

- cron を `'0 0 * * *'`（日次、UTC 0:00 = JST 9:00）に変更
- `DISCORD_WEBHOOK_URL` シークレットの参照を追加
- check_rss.py の実行コマンドに `--notify discord` を追加

#### 4. GitHub Secrets の設定

```bash
gh secret set DISCORD_WEBHOOK_URL --body "<WEBHOOK_URL>"
```

#### 5. テスト送信

テスト用のメッセージを Discord に送信して疎通確認:

```bash
curl -H "Content-Type: application/json" \
  -d '{"embeds":[{"title":"QA Knowledge 通知テスト","description":"Discord Webhook の設定が完了しました。","color":5814783}]}' \
  "<WEBHOOK_URL>"
```

成功したら設定完了を表示。

### サブコマンド: status

以下を確認して表示:

1. check_rss.py に `--notify` オプションが存在するか
2. `.github/workflows/check-rss.yml` の cron 設定（日次/週次）
3. `gh secret list` で DISCORD_WEBHOOK_URL が設定済みか
4. 直近の check-rss ワークフロー実行結果

```
## 通知設定状況

| 項目 | 状態 |
|------|------|
| Discord通知機能 | 有効/未設定 |
| RSS巡回頻度 | 日次/週次 |
| Webhook Secret | 設定済み/未設定 |
| 直近の実行 | YYYY-MM-DD (成功/失敗) |
```
