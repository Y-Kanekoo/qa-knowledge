"""validate_frontmatter.py のユニットテスト。"""

from datetime import date
from pathlib import Path

from scripts.validate_frontmatter import find_entry_files, validate_file


def _write_md(path: Path, meta: dict) -> Path:
    """メタデータ辞書から frontmatter 付き MD ファイルを生成する。"""
    lines = ["---"]
    for key, value in meta.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        elif isinstance(value, date):
            lines.append(f"{key}: {value.isoformat()}")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        else:
            lines.append(f'{key}: "{value}"')
    lines.append("---")
    lines.append("")
    lines.append("本文")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _valid_meta() -> dict:
    """バリデーションを全てパスする正常なメタデータを返す。"""
    return {
        "title": "テスト自動化の実践ガイド",
        "company": "Example Inc.",
        "url": "https://example.com/blog/test-automation",
        "published_at": date(2024, 6, 15),
        "content_type": "blog",
        "qa_domains": ["test-automation"],
        "tags": ["selenium"],
        "language": "ja",
        "added_at": date(2024, 7, 1),
    }


# ==========================================================
# validate_file テスト
# ==========================================================


class TestValidateFile:
    """validate_file 関数のテスト。"""

    def test_全フィールド正常ならエラー0件(self, tmp_path: Path):
        md_file = _write_md(tmp_path / "valid.md", _valid_meta())
        errors = validate_file(md_file)
        assert errors == []

    def test_必須フィールド_title_欠如でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        del meta["title"]
        md_file = _write_md(tmp_path / "no-title.md", meta)
        errors = validate_file(md_file)
        assert any("title" in e for e in errors)

    def test_必須フィールド_url_欠如でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        del meta["url"]
        md_file = _write_md(tmp_path / "no-url.md", meta)
        errors = validate_file(md_file)
        assert any("url" in e for e in errors)

    def test_不正な_url_でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        meta["url"] = "http://example.com/not-https"
        md_file = _write_md(tmp_path / "bad-url.md", meta)
        errors = validate_file(md_file)
        assert any("https://" in e for e in errors)

    def test_不正な_content_type_でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        meta["content_type"] = "invalid_type"
        md_file = _write_md(tmp_path / "bad-content-type.md", meta)
        errors = validate_file(md_file)
        assert any("content_type" in e for e in errors)

    def test_不正な_qa_domain_でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        meta["qa_domains"] = ["nonexistent-domain"]
        md_file = _write_md(tmp_path / "bad-domain.md", meta)
        errors = validate_file(md_file)
        assert any("qa_domains" in e for e in errors)

    def test_不正なタグ形式でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        meta["tags"] = ["UPPER_CASE"]
        md_file = _write_md(tmp_path / "bad-tag.md", meta)
        errors = validate_file(md_file)
        assert any("tags" in e for e in errors)

    def test_不正な日付形式でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        meta["published_at"] = "not-a-date"
        md_file = _write_md(tmp_path / "bad-date.md", meta)
        errors = validate_file(md_file)
        assert any("published_at" in e for e in errors)

    def test_必須フィールド_company_欠如でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        del meta["company"]
        md_file = _write_md(tmp_path / "no-company.md", meta)
        errors = validate_file(md_file)
        assert any("company" in e for e in errors)

    def test_必須フィールド_language_が不正でエラー(self, tmp_path: Path):
        meta = _valid_meta()
        meta["language"] = "fr"
        md_file = _write_md(tmp_path / "bad-lang.md", meta)
        errors = validate_file(md_file)
        assert any("language" in e for e in errors)


# ==========================================================
# find_entry_files テスト
# ==========================================================


class TestFindEntryFiles:
    """find_entry_files 関数のテスト。"""

    def test_template_md_を除外する(self, tmp_entries_dir: Path):
        """_template.md がリストに含まれないこと。"""
        files = find_entry_files(tmp_entries_dir)
        filenames = [f.name for f in files]
        assert "_template.md" not in filenames
        assert len(filenames) >= 1
