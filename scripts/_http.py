"""共通HTTPセッション設定モジュール。"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_session(timeout: int = 10, retries: int = 3) -> requests.Session:
    """リトライ付きHTTPセッションを作成する。"""
    session = requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
