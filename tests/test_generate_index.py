"""generate_index.py のユニットテスト。"""

from datetime import date, datetime

from scripts.generate_index import (
    EntryMeta,
    _format_date,
    generate_by_company,
    generate_by_domain,
    generate_by_tag,
    generate_index_md,
)


def _make_entry(
    filename: str = "example-entry.md",
    title: str = "テスト記事",
    company: str = "Example Inc.",
    url: str = "https://example.com/test",
    published_at: str = "2024-06-15",
    content_type: str = "blog",
    qa_domains: list[str] | None = None,
    tags: list[str] | None = None,
    added_at: str = "2024-07-01",
) -> EntryMeta:
    """テスト用の EntryMeta 辞書を生成する。"""
    return EntryMeta(
        filename=filename,
        title=title,
        company=company,
        url=url,
        published_at=published_at,
        content_type=content_type,
        qa_domains=qa_domains if qa_domains is not None else ["test-automation"],
        tags=tags if tags is not None else ["selenium"],
        added_at=added_at,
    )


# ==========================================================
# _format_date テスト（4ケース）
# ==========================================================


class TestFormatDate:
    """日付フォーマットテスト。"""

    def test_文字列をそのまま返す(self):
        result = _format_date("2024-06-15")
        assert result == "2024-06-15"

    def test_date_オブジェクトを変換する(self):
        result = _format_date(date(2024, 6, 15))
        assert result == "2024-06-15"

    def test_datetime_オブジェクトを変換する(self):
        result = _format_date(datetime(2024, 6, 15, 10, 30, 0))
        assert result == "2024-06-15"

    def test_none_の場合は空文字を返す(self):
        result = _format_date(None)
        assert result == ""


# ==========================================================
# generate_by_company テスト（1ケース）
# ==========================================================


class TestGenerateByCompany:
    """会社別インデックス生成テスト。"""

    def test_エントリありの場合は会社名とテーブルを含む(self):
        entries = [
            _make_entry(
                filename="a.md", title="記事A", company="Alpha",
                published_at="2024-01-01",
            ),
            _make_entry(
                filename="b.md", title="記事B", company="Alpha",
                published_at="2024-06-01",
            ),
            _make_entry(filename="c.md", title="記事C", company="Beta"),
        ]
        result = generate_by_company(entries)

        # 会社名のセクションが存在する
        assert "## Alpha" in result
        assert "## Beta" in result
        # Alpha 内で新しい記事が先に来る（降順ソート）
        pos_b = result.index("記事B")
        pos_a = result.index("記事A")
        assert pos_b < pos_a


# ==========================================================
# generate_by_domain テスト（1ケース）
# ==========================================================


class TestGenerateByDomain:
    """QA領域別インデックス生成テスト。"""

    def test_複数ドメインに所属するエントリが各セクションに表示される(self):
        entries = [
            _make_entry(
                filename="multi.md",
                title="複合領域記事",
                qa_domains=["test-automation", "ci-cd"],
            ),
        ]
        result = generate_by_domain(entries)

        # 両方の領域セクションが存在する
        assert "## test-automation" in result
        assert "## ci-cd" in result
        # 各セクションに記事が含まれる
        # test-automation セクション内に記事リンクがある
        assert result.count("複合領域記事") == 2


# ==========================================================
# generate_by_tag テスト（1ケース）
# ==========================================================


class TestGenerateByTag:
    """タグ別インデックス生成テスト。"""

    def test_エントリ数が多いタグが先に表示される(self):
        entries = [
            _make_entry(filename="a.md", tags=["selenium", "pytest"]),
            _make_entry(filename="b.md", tags=["selenium"]),
            _make_entry(filename="c.md", tags=["pytest", "ci"]),
        ]
        result = generate_by_tag(entries)

        # selenium(2件) と pytest(2件) が ci(1件) より先に出る
        pos_selenium = result.index("## selenium")
        pos_ci = result.index("## ci")
        assert pos_selenium < pos_ci


# ==========================================================
# generate_index_md テスト（3ケース）
# ==========================================================


class TestGenerateIndexMd:
    """トップページ生成テスト。"""

    def test_統計情報を含む(self):
        entries = [
            _make_entry(company="Alpha", qa_domains=["test-automation"]),
            _make_entry(
                filename="b.md", company="Beta",
                qa_domains=["ci-cd", "reliability"],
            ),
        ]
        result = generate_index_md(entries)

        # 総エントリ数
        assert "| 総エントリ数 | 2 |" in result
        # 収録企業数
        assert "| 収録企業数 | 2 |" in result
        # QA領域数（test-automation, ci-cd, reliability = 3）
        assert "| QA領域数 | 3 |" in result

    def test_最近追加されたエントリを含む(self):
        entries = [
            _make_entry(
                filename="recent.md", title="最新記事", added_at="2024-12-01",
            ),
        ]
        result = generate_index_md(entries)
        assert "最新記事" in result

    def test_エントリなしの場合はプレースホルダーを表示する(self):
        result = generate_index_md([])
        assert "エントリ追加後に自動更新されます" in result
        assert "| 総エントリ数 | 0 |" in result
