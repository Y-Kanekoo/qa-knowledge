"""RSS 設定の型誤りを外部通信前に検出する回帰テスト。"""

from copy import deepcopy
from unittest.mock import Mock

import pytest

from scripts import check_rss


def valid_config():
    return {
        "feeds": [{"name": "QA Blog", "company": "Example", "url": "https://example.com/feed"}],
        "keywords": ["testing", "品質保証"],
    }


@pytest.mark.parametrize("config", [None, [], "feeds", 42, True])
def test_root_must_be_mapping(config):
    assert check_rss.validate_feeds_config(config) == ["設定全体はマッピングで指定してください"]


@pytest.mark.parametrize("feed", [None, [], "feed", 42, True])
def test_feed_must_be_mapping(feed):
    config = valid_config()
    config["feeds"] = [feed]
    assert check_rss.validate_feeds_config(config) == ["feeds[0]: マッピングで指定してください"]


@pytest.mark.parametrize("field", ["name", "company", "url"])
@pytest.mark.parametrize("value", [None, "", "  ", 42, True, [], {}])
def test_required_fields_must_be_nonempty_strings(field, value):
    config = valid_config()
    config["feeds"][0][field] = value
    assert check_rss.validate_feeds_config(config) == [f"feeds[0]: '{field}' は空でない文字列で指定してください"]


@pytest.mark.parametrize(
    "url",
    [
        "http-not-a-url",
        "https://",
        "file:///feed.xml",
        "https://[",
        "https://example.com:bad/feed",
        "https://exa mple.com/feed",
        "https://example.com/\nfeed",
    ],
)
def test_url_must_have_http_scheme_and_host(url):
    config = valid_config()
    config["feeds"][0]["url"] = url
    assert check_rss.validate_feeds_config(config) == ["feeds[0]: url は有効な HTTP(S) URL で指定してください"]


@pytest.mark.parametrize("value", ["false", "true", 0, 1, None, [], {}])
def test_skip_keyword_filter_must_be_boolean(value):
    config = valid_config()
    config["feeds"][0]["skip_keyword_filter"] = value
    assert check_rss.validate_feeds_config(config) == ["feeds[0]: skip_keyword_filter は真偽値で指定してください"]


@pytest.mark.parametrize("keyword", [None, "", "  ", 42, True, [], {}])
def test_keywords_must_be_nonempty_strings(keyword):
    config = valid_config()
    config["keywords"] = ["testing", keyword]
    assert check_rss.validate_feeds_config(config) == ["keywords[1]: 空でない文字列で指定してください"]


@pytest.mark.parametrize("language", [None, "fr", 42, True, [], {}])
def test_language_must_be_supported(language):
    config = valid_config()
    config["feeds"][0]["language"] = language
    assert check_rss.validate_feeds_config(config) == ["feeds[0]: language は 'en' または 'ja' を指定してください"]


@pytest.mark.parametrize("skip_filter", [False, True])
@pytest.mark.parametrize(
    "url", ["http://example.com/feed.xml", "https://example.com:8443/feed.xml?q=qa", "HTTPS://example.com/feed"]
)
def test_valid_config_is_accepted_without_mutation(skip_filter, url):
    config = valid_config()
    config["feeds"][0].update(url=url, language="ja", skip_keyword_filter=skip_filter)
    original = deepcopy(config)
    assert check_rss.validate_feeds_config(config) == []
    assert config == original


def test_current_repository_config_remains_valid():
    assert check_rss.validate_feeds_config(check_rss.load_feeds_config()) == []


def test_invalid_values_are_not_echoed():
    config = valid_config()
    config["feeds"][0].update(url="invalid-private-value", language="private-language-value")
    errors = check_rss.validate_feeds_config(config)
    assert len(errors) == 2
    assert "private" not in "\n".join(errors)


@pytest.mark.parametrize(
    "config",
    [
        None,
        {"feeds": [None], "keywords": ["testing"]},
        {
            "feeds": [
                {"name": "QA", "company": "Example", "url": "https://example.com/feed", "skip_keyword_filter": "false"}
            ],
            "keywords": ["testing"],
        },
    ],
)
def test_main_stops_before_collection_notification_and_output(config, monkeypatch, tmp_path, capsys):
    output = tmp_path / "output.txt"
    output.write_text("existing\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["check_rss.py", "--notify", "discord", "--github-output", str(output)])
    monkeypatch.setattr(check_rss, "load_feeds_config", lambda: config)
    existing = Mock(side_effect=AssertionError("設定エラー時に記事を読まない"))
    fetch = Mock(side_effect=AssertionError("設定エラー時に取得しない"))
    notify = Mock(side_effect=AssertionError("設定エラー時に通知しない"))
    monkeypatch.setattr(check_rss, "load_existing_urls", existing)
    monkeypatch.setattr(check_rss, "check_feeds", fetch)
    monkeypatch.setattr(check_rss, "send_discord_notification", notify)
    assert check_rss.main() == 1
    captured = capsys.readouterr()
    assert "設定エラー:" in captured.err
    assert "RSS処理に失敗" not in captured.err
    assert captured.out == ""
    assert output.read_text(encoding="utf-8") == "existing\n"
    existing.assert_not_called()
    fetch.assert_not_called()
    notify.assert_not_called()
