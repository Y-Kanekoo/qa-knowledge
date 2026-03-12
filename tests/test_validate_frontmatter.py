"""validate_frontmatter.py のユニットテスト。"""

from datetime import date
from pathlib import Path
from unittest.mock import patch

from scripts.validate_frontmatter import find_entry_files, main, validate_file


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


# ==========================================================
# main() 統合テスト
# ==========================================================


class TestMain:
    """main() 関数の統合テスト。"""

    @staticmethod
    def _run_main_with_fake_root(tmp_path: Path) -> int:
        """tmp_path をプロジェクトルートとみなして main() を実行するヘルパー。

        main() は Path(__file__).resolve().parent.parent で entries/ を探すため、
        モジュールの __file__ を tmp_path/scripts/validate_frontmatter.py に差し替える。
        """
        import scripts.validate_frontmatter as mod

        fake_script = tmp_path / "scripts" / "validate_frontmatter.py"
        fake_script.parent.mkdir(parents=True, exist_ok=True)

        original_file = mod.__file__
        try:
            mod.__file__ = str(fake_script)
            with patch("scripts.validate_frontmatter.sys.argv", ["validate_frontmatter.py"]):
                return main()
        finally:
            mod.__file__ = original_file

    def test_エントリがバリデーション成功する場合は0を返す(self, tmp_path: Path):
        """正常なエントリのみの場合、main() は 0 を返す。"""
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()
        _write_md(entries_dir / "valid-entry.md", _valid_meta())

        result = self._run_main_with_fake_root(tmp_path)
        assert result == 0

    def test_エントリにエラーがある場合は1を返す(self, tmp_path: Path):
        """バリデーションエラーがあるエントリの場合、main() は 1 を返す。"""
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()
        # 必須フィールドが欠けたエントリ
        _write_md(entries_dir / "bad-entry.md", {"title": "Bad Entry"})

        result = self._run_main_with_fake_root(tmp_path)
        assert result == 1

    def test_entriesディレクトリが存在しない場合は1を返す(self, tmp_path: Path):
        """entries/ ディレクトリが存在しない場合、main() は 1 を返す。"""
        # entries/ ディレクトリは作成しない
        result = self._run_main_with_fake_root(tmp_path)
        assert result == 1
