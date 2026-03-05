"""check_rss.py のユニットテスト。"""

import time

from scripts.check_rss import (
    format_markdown,
    format_text,
    matches_keywords,
    normalize_url,
    parse_published_date,
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
