"""scaffold.py のユニットテスト。"""

from bs4 import BeautifulSoup

from scripts.scaffold import (
    detect_language,
    extract_published_at,
    extract_title,
    format_output,
    generate_slug,
)


def _make_soup(html: str) -> BeautifulSoup:
    """HTML文字列から BeautifulSoup オブジェクトを生成する。"""
    return BeautifulSoup(html, "html.parser")


# ==========================================================
# extract_title（3ケース）
# ==========================================================


class TestExtractTitle:
    """タイトル抽出テスト。"""

    def test_og_title_を優先する(self):
        html = """
        <html>
        <head>
            <meta property="og:title" content="OGタイトル" />
            <title>通常タイトル</title>
        </head>
        <body></body>
        </html>
        """
        soup = _make_soup(html)
        result = extract_title(soup)
        assert result == "OGタイトル"

    def test_og_title_がない場合は_title_要素にフォールバック(self):
        html = """
        <html>
        <head><title>フォールバックタイトル</title></head>
        <body></body>
        </html>
        """
        soup = _make_soup(html)
        result = extract_title(soup)
        assert result == "フォールバックタイトル"

    def test_タイトルなしの場合は空文字を返す(self):
        html = "<html><head></head><body></body></html>"
        soup = _make_soup(html)
        result = extract_title(soup)
        assert result == ""


# ==========================================================
# extract_published_at（3ケース）
# ==========================================================


class TestExtractPublishedAt:
    """公開日抽出テスト。"""

    def test_meta_タグから日付を抽出する(self):
        html = """
        <html>
        <head>
            <meta property="article:published_time" content="2024-06-15T10:00:00Z" />
        </head>
        <body></body>
        </html>
        """
        soup = _make_soup(html)
        result = extract_published_at(soup)
        assert result == "2024-06-15"

    def test_json_ld_から日付を抽出する(self):
        html = """
        <html>
        <head>
            <script type="application/ld+json">
            {"@type": "Article", "datePublished": "2024-08-20T09:00:00Z"}
            </script>
        </head>
        <body></body>
        </html>
        """
        soup = _make_soup(html)
        result = extract_published_at(soup)
        assert result == "2024-08-20"

    def test_日付情報なしの場合は空文字を返す(self):
        html = "<html><head></head><body></body></html>"
        soup = _make_soup(html)
        result = extract_published_at(soup)
        assert result == ""


# ==========================================================
# detect_language（2ケース）
# ==========================================================


class TestDetectLanguage:
    """言語推定テスト。"""

    def test_html_lang_属性から日本語を検出する(self):
        html = '<html lang="ja"><head></head><body></body></html>'
        soup = _make_soup(html)
        result = detect_language(soup)
        assert result == "ja"

    def test_lang_属性なしの場合は_en_を返す(self):
        html = "<html><head></head><body></body></html>"
        soup = _make_soup(html)
        result = detect_language(soup)
        assert result == "en"


# ==========================================================
# generate_slug（3ケース）
# ==========================================================


class TestGenerateSlug:
    """スラッグ生成テスト。"""

    def test_通常のタイトルからスラッグを生成する(self):
        result = generate_slug("Testing Best Practices")
        assert result == "testing-best-practices"

    def test_長い文字列を60文字に切り詰める(self):
        long_title = "a" * 100
        result = generate_slug(long_title)
        assert len(result) <= 60

    def test_特殊文字を除去する(self):
        result = generate_slug("Hello! World? (2024)")
        # 特殊文字(!, ?, 括弧)は除去される
        assert "!" not in result
        assert "?" not in result
        assert "(" not in result
        assert ")" not in result
        # 単語部分は残る
        assert "hello" in result
        assert "world" in result
        assert "2024" in result


# ==========================================================
# format_output（1ケース）
# ==========================================================


class TestFormatOutput:
    """出力フォーマットテスト。"""

    def test_yaml_frontmatter_構造を含む(self):
        result = format_output(
            title="テスト記事",
            url="https://example.com/test",
            published_at="2024-06-15",
            language="ja",
            company="Example Inc.",
        )
        # YAML frontmatter の開始・終了マーカーを確認
        assert result.startswith("---\n")
        assert "\n---\n" in result
        # 主要フィールドの存在を確認
        assert 'title: "テスト記事"' in result
        assert 'company: "Example Inc."' in result
        assert 'url: "https://example.com/test"' in result
        assert '"2024-06-15"' in result
        assert 'language: "ja"' in result
        # Markdown 骨格の存在を確認
        assert "## 概要" in result
        assert "## 何が学べるか" in result
