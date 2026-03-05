"""check_links.py のユニットテスト。"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import requests

from scripts.check_links import check_url, load_entries


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
