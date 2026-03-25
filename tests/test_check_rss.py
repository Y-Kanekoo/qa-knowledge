"""check_rss.py のユニットテスト。"""

import json
import time
from unittest.mock import MagicMock, patch

import requests

from scripts._url import normalize_url
from scripts.check_rss import (
    check_feeds,
    format_markdown,
    format_text,
    matches_keywords,
    parse_published_date,
    send_discord_notification,
)

# ==========================================================
# normalize_url（5ケース）
# ==========================================================


class TestNormalizeUrl:
    """URLの正規化テスト。"""

    def test_utm_パラメータを除去する(self):
        url = "https://example.com/post?utm_source=twitter&utm_medium=social"
        result = normalize_url(url)
        assert result == "https://example.com/post"

    def test_www_を除去する(self):
        url = "https://www.example.com/post"
        result = normalize_url(url)
        assert result == "https://example.com/post"

    def test_http_を_https_に変換する(self):
        url = "http://example.com/post"
        result = normalize_url(url)
        assert result == "https://example.com/post"

    def test_末尾スラッシュを除去する(self):
        url = "https://example.com/post/"
        result = normalize_url(url)
        assert result == "https://example.com/post"

    def test_非トラッキングパラメータを保持する(self):
        url = "https://example.com/search?q=testing&page=2&utm_campaign=launch"
        result = normalize_url(url)
        # utm_campaign は除去されるが q と page は残る
        assert "q=testing" in result
        assert "page=2" in result
        assert "utm_campaign" not in result


# ==========================================================
# matches_keywords（5ケース）
# ==========================================================


class TestMatchesKeywords:
    """キーワードマッチングテスト。"""

    def test_contest_に_test_がマッチしない_単語境界(self):
        """英語キーワードは単語境界で検索されること。"""
        result = matches_keywords("contest results announced", ["test"])
        assert result is False

    def test_日本語キーワードは部分一致する(self):
        result = matches_keywords("品質保証チームの取り組み", ["品質保証"])
        assert result is True

    def test_大文字小文字を無視する(self):
        result = matches_keywords("End-to-End Testing Best Practices", ["testing"])
        assert result is True

    def test_複合キーワード_integration_test_にマッチする(self):
        result = matches_keywords("Our integration test strategy", ["integration-test"])
        assert result is True

    def test_cicd_キーワードにマッチする(self):
        result = matches_keywords("How we improved our CI/CD pipeline", ["ci/cd"])
        assert result is True


# ==========================================================
# parse_published_date（3ケース）
# ==========================================================


class TestParsePublishedDate:
    """公開日パーステスト。"""

    def test_struct_time_から日付を抽出する(self):
        """published_parsed (time.struct_time) から日付文字列を取得する。"""
        entry = {
            "published_parsed": time.strptime("2024-03-15", "%Y-%m-%d"),
        }
        result = parse_published_date(entry)
        assert result == "2024-03-15"

    def test_文字列から日付部分を抽出する(self):
        """published フィールドの文字列から YYYY-MM-DD を抽出する。"""
        entry = {
            "published": "Fri, 15 Mar 2024-03-15T10:00:00Z",
        }
        result = parse_published_date(entry)
        assert result == "2024-03-15"

    def test_日付情報なしの場合は空文字を返す(self):
        entry = {"title": "No date entry"}
        result = parse_published_date(entry)
        assert result == ""


# ==========================================================
# format_text / format_markdown（3ケース）
# ==========================================================


class TestFormatText:
    """テキスト出力テスト。"""

    def test_記事ありの場合はタイトルとURLを含む(self):
        articles = [
            {
                "blog": "Tech Blog",
                "company": "Example",
                "title": "Testing Guide",
                "url": "https://example.com/testing",
                "published": "2024-03-15",
                "language": "en",
            }
        ]
        result = format_text(articles)
        assert "新着QA関連記事: 1件" in result
        assert "Testing Guide" in result
        assert "https://example.com/testing" in result

    def test_記事なしの場合はメッセージを返す(self):
        result = format_text([])
        assert result == "新着QA関連記事はありません。"


class TestFormatMarkdown:
    """Markdown出力テスト。"""

    def test_記事ありの場合はテーブルを含む(self):
        articles = [
            {
                "blog": "Tech Blog",
                "company": "Example",
                "title": "Testing Guide",
                "url": "https://example.com/testing",
                "published": "2024-03-15",
                "language": "en",
            }
        ]
        result = format_markdown(articles)
        assert "## 新着QA関連記事が見つかりました" in result
        assert "| Tech Blog |" in result
        assert "[Testing Guide](https://example.com/testing)" in result

    def test_記事なしの場合は空文字を返す(self):
        result = format_markdown([])
        assert result == ""


# ==========================================================
# check_feeds 統合テスト（4ケース）
# ==========================================================


class TestCheckFeeds:
    """check_feeds() の統合テスト。"""

    @patch("scripts.check_rss.feedparser.parse")
    def test_新着QA記事を検出する(self, mock_parse):
        """キーワードに一致する新着記事を検出する。"""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = lambda k, d="": {
            "title": "テスト自動化の最新手法",
            "link": "https://example.com/test-automation",
            "summary": "テスト自動化に関する記事",
        }.get(k, d)
        mock_entry.__contains__ = lambda self_inner, k: k in {"title", "link", "summary"}

        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.entries = [mock_entry]
        mock_parse.return_value = mock_result

        config = {
            "feeds": [{"name": "Test Blog", "url": "https://example.com/feed", "company": "Example", "language": "ja"}],
            "keywords": ["テスト"],
        }
        results = check_feeds(config, existing_urls=set(), dry_run=False, days_limit=0)
        assert len(results) >= 1
        assert any("test-automation" in r["url"] for r in results)

    @patch("scripts.check_rss.feedparser.parse")
    def test_既存URLは除外する(self, mock_parse):
        """existing_urls に含まれるURLの記事はスキップされる。"""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = lambda k, d="": {
            "title": "テスト記事",
            "link": "https://example.com/existing",
            "summary": "テスト",
        }.get(k, d)

        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.entries = [mock_entry]
        mock_parse.return_value = mock_result

        config = {
            "feeds": [{"name": "Test Blog", "url": "https://example.com/feed", "company": "Example", "language": "ja"}],
            "keywords": ["テスト"],
        }
        results = check_feeds(config, existing_urls={"https://example.com/existing"}, dry_run=False, days_limit=0)
        assert len(results) == 0

    @patch("scripts.check_rss.feedparser.parse")
    def test_キーワード不一致は除外する(self, mock_parse):
        """キーワードに一致しない記事は結果に含まれない。"""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = lambda k, d="": {
            "title": "料理レシピ特集",
            "link": "https://example.com/cooking",
            "summary": "美味しい料理の作り方",
        }.get(k, d)
        mock_entry.__contains__ = lambda self_inner, k: k in {"title", "link", "summary"}

        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.entries = [mock_entry]
        mock_parse.return_value = mock_result

        config = {
            "feeds": [{"name": "Blog", "url": "https://example.com/feed", "company": "Example", "language": "ja"}],
            "keywords": ["テスト", "test"],
        }
        results = check_feeds(config, existing_urls=set(), dry_run=False, days_limit=0)
        assert len(results) == 0

    @patch("scripts.check_rss.feedparser.parse")
    def test_skip_keyword_filterでキーワードフィルタをスキップ(self, mock_parse):
        """skip_keyword_filter: true の場合、キーワード不一致でも記事が含まれる。"""
        mock_entry = MagicMock()
        mock_entry.get.side_effect = lambda k, d="": {
            "title": "全く関係ない記事",
            "link": "https://example.com/unrelated",
            "summary": "キーワードに一致しない内容",
        }.get(k, d)

        mock_result = MagicMock()
        mock_result.bozo = False
        mock_result.entries = [mock_entry]
        mock_parse.return_value = mock_result

        config = {
            "feeds": [{
                "name": "Blog", "url": "https://example.com/feed",
                "company": "Example", "language": "ja",
                "skip_keyword_filter": True,
            }],
            "keywords": ["テスト"],
        }
        results = check_feeds(config, existing_urls=set(), dry_run=False, days_limit=0)
        assert len(results) >= 1


# ==========================================================
# send_discord_notification（4ケース）
# ==========================================================


class TestSendDiscordNotification:
    """Discord通知テスト。"""

    SAMPLE_ARTICLES = [
        {
            "blog": "Google Testing Blog",
            "company": "Google",
            "title": "テスト自動化の最新手法",
            "url": "https://testing.googleblog.com/2026/03/test-automation.html",
            "published": "2026-03-15",
            "language": "en",
        }
    ]

    @patch("scripts.check_rss.requests.post")
    def test_記事ありの場合にWebhookを送信する(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        result = send_discord_notification("https://discord.com/api/webhooks/test", self.SAMPLE_ARTICLES)
        assert result is True
        mock_post.assert_called_once()

        # 送信ペイロードの検証
        call_kwargs = mock_post.call_args
        payload = json.loads(call_kwargs.kwargs["data"] if "data" in call_kwargs.kwargs else call_kwargs[1]["data"])
        assert len(payload["embeds"]) == 1
        assert payload["embeds"][0]["title"] == "テスト自動化の最新手法"

    @patch("scripts.check_rss.requests.post")
    def test_記事なしの場合は送信しない(self, mock_post):
        result = send_discord_notification("https://discord.com/api/webhooks/test", [])
        assert result is True
        mock_post.assert_not_called()

    @patch("scripts.check_rss.requests.post")
    def test_送信失敗時にFalseを返す(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError("接続エラー")

        result = send_discord_notification("https://discord.com/api/webhooks/test", self.SAMPLE_ARTICLES)
        assert result is False

    @patch("scripts.check_rss.requests.post")
    def test_11件以上の場合にバッチ分割する(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        # 11件の記事を生成
        articles = [
            {**self.SAMPLE_ARTICLES[0], "title": f"記事{i}", "url": f"https://example.com/{i}"}
            for i in range(11)
        ]
        result = send_discord_notification("https://discord.com/api/webhooks/test", articles)
        assert result is True
        assert mock_post.call_count == 2  # 10件 + 1件 の2バッチ
