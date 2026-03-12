"""check_links.py のユニットテスト。"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from scripts.check_links import check_url, load_entries, main, run_checks

# ==========================================================
# check_url テスト（4ケース）
# ==========================================================


class TestCheckUrl:
    """URLチェックのテスト（_session をモックする）。"""

    @patch("scripts.check_links._session")
    def test_200応答の場合は成功を返す(self, mock_session: MagicMock):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_session.head.return_value = mock_response

        entry = {"filename": "example.md", "url": "https://example.com"}
        result = check_url(entry)

        assert result["success"] is True
        assert result["status"] == "200 OK"

    @patch("scripts.check_links._session")
    def test_404応答の場合は失敗を返す(self, mock_session: MagicMock):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_session.head.return_value = mock_response

        entry = {"filename": "dead-link.md", "url": "https://example.com/gone"}
        result = check_url(entry)

        assert result["success"] is False
        assert "404" in result["status"]

    @patch("scripts.check_links._session")
    def test_405の場合は_get_にフォールバックして成功(self, mock_session: MagicMock):
        # HEAD が 405 を返す
        mock_head_response = MagicMock()
        mock_head_response.status_code = 405
        mock_session.head.return_value = mock_head_response

        # GET で 200 を返す
        mock_get_response = MagicMock()
        mock_get_response.status_code = 200
        mock_get_response.reason = "OK"
        mock_session.get.return_value = mock_get_response

        entry = {"filename": "head-blocked.md", "url": "https://example.com/api"}
        result = check_url(entry)

        assert result["success"] is True
        assert result["status"] == "200 OK"
        mock_session.get.assert_called_once()

    @patch("scripts.check_links._session")
    def test_タイムアウトの場合は失敗を返す(self, mock_session: MagicMock):
        mock_session.head.side_effect = requests.exceptions.Timeout("接続タイムアウト")

        entry = {"filename": "slow.md", "url": "https://slow.example.com"}
        result = check_url(entry)

        assert result["success"] is False
        assert "タイムアウト" in result["status"]


# ==========================================================
# load_entries テスト（3ケース）
# ==========================================================


def _write_entry_md(path: Path, url: str, deprecated: bool = False) -> None:
    """テスト用の entries/ MD ファイルを作成する。"""
    lines = ["---"]
    lines.append(f'url: "{url}"')
    if deprecated:
        lines.append("deprecated: true")
    lines.append("---")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


class TestLoadEntries:
    """エントリ読み込みのテスト。"""

    @patch("scripts.check_links.ENTRIES_DIR")
    def test_通常のエントリを読み込む(self, mock_dir: MagicMock, tmp_path: Path):
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()
        _write_entry_md(entries_dir / "test-entry.md", "https://example.com/test")
        mock_dir.__class__ = Path
        mock_dir.glob = entries_dir.glob

        result = load_entries()
        assert len(result) == 1
        assert result[0]["url"] == "https://example.com/test"
        assert result[0]["filename"] == "test-entry.md"

    @patch("scripts.check_links.ENTRIES_DIR")
    def test_deprecated_エントリをスキップする(self, mock_dir: MagicMock, tmp_path: Path):
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()
        _write_entry_md(
            entries_dir / "old-entry.md", "https://example.com/old", deprecated=True
        )
        _write_entry_md(entries_dir / "active-entry.md", "https://example.com/active")
        mock_dir.__class__ = Path
        mock_dir.glob = entries_dir.glob

        result = load_entries()
        # deprecated=true のエントリはスキップされる
        filenames = [r["filename"] for r in result]
        assert "old-entry.md" not in filenames
        assert "active-entry.md" in filenames

    @patch("scripts.check_links.ENTRIES_DIR")
    def test_template_md_をスキップする(self, mock_dir: MagicMock, tmp_path: Path):
        entries_dir = tmp_path / "entries"
        entries_dir.mkdir()
        _write_entry_md(entries_dir / "_template.md", "https://example.com/template")
        _write_entry_md(entries_dir / "real-entry.md", "https://example.com/real")
        mock_dir.__class__ = Path
        mock_dir.glob = entries_dir.glob

        result = load_entries()
        filenames = [r["filename"] for r in result]
        assert "_template.md" not in filenames
        assert "real-entry.md" in filenames


# ==========================================================
# run_checks 統合テスト（3ケース）
# ==========================================================


class TestRunChecks:
    """run_checks() の統合テスト。"""

    @patch("scripts.check_links._session")
    def test_複数エントリの結果をファイル名順で返す(self, mock_session):
        """2件のエントリを並列チェックし、ファイル名順にソートされた結果を返す。"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_session.head.return_value = mock_response

        entries = [
            {"filename": "b-entry.md", "url": "https://example.com/b"},
            {"filename": "a-entry.md", "url": "https://example.com/a"},
        ]
        results = run_checks(entries)
        assert len(results) == 2
        assert results[0]["filename"] == "a-entry.md"
        assert results[1]["filename"] == "b-entry.md"
        assert all(r["success"] for r in results)

    @patch("scripts.check_links._session")
    def test_成功と失敗が混在する場合(self, mock_session):
        """成功と失敗の両方を正しく記録する。"""
        ok_response = MagicMock()
        ok_response.status_code = 200
        ok_response.reason = "OK"

        import requests
        mock_session.head.side_effect = [
            ok_response,
            requests.exceptions.Timeout("タイムアウト"),
        ]

        entries = [
            {"filename": "a.md", "url": "https://example.com/a"},
            {"filename": "b.md", "url": "https://example.com/b"},
        ]
        results = run_checks(entries)
        assert len(results) == 2
        successes = [r for r in results if r["success"]]
        failures = [r for r in results if not r["success"]]
        assert len(successes) == 1
        assert len(failures) == 1

    @patch("scripts.check_links._session")
    def test_空リストの場合は空リストを返す(self, mock_session):
        """空のエントリリストを渡すと空リストを返す。"""
        results = run_checks([])
        assert results == []


# ==========================================================
# main() 統合テスト
# ==========================================================


class TestMain:
    """main() 関数の統合テスト。"""

    @patch("scripts.check_links.sys.argv", ["check_links.py"])
    @patch("scripts.check_links.load_entries", return_value=[])
    def test_エントリなしの場合は正常終了(self, mock_load):
        """チェック対象のエントリがない場合、exit code 0 で終了する。"""
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    @patch("scripts.check_links.sys.argv", ["check_links.py"])
    @patch("scripts.check_links.run_checks")
    @patch("scripts.check_links.load_entries")
    def test_全URL成功の場合は正常終了(self, mock_load, mock_run_checks):
        """全URLが成功の場合、exit code 0 で終了する。"""
        mock_load.return_value = [
            {"filename": "a.md", "url": "https://example.com/a"},
            {"filename": "b.md", "url": "https://example.com/b"},
        ]
        mock_run_checks.return_value = [
            {"filename": "a.md", "url": "https://example.com/a", "success": True, "status": "200 OK"},
            {"filename": "b.md", "url": "https://example.com/b", "success": True, "status": "200 OK"},
        ]

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    @patch("scripts.check_links.sys.argv", ["check_links.py"])
    @patch("scripts.check_links.run_checks")
    @patch("scripts.check_links.load_entries")
    def test_一部失敗の場合はエラー終了(self, mock_load, mock_run_checks):
        """一部のURLが失敗の場合、exit code 1 で終了する。"""
        mock_load.return_value = [
            {"filename": "a.md", "url": "https://example.com/a"},
            {"filename": "b.md", "url": "https://example.com/b"},
        ]
        mock_run_checks.return_value = [
            {"filename": "a.md", "url": "https://example.com/a", "success": True, "status": "200 OK"},
            {"filename": "b.md", "url": "https://example.com/b", "success": False, "status": "404 Not Found"},
        ]

        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
