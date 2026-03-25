"""URL正規化の共通モジュール。"""

from urllib.parse import parse_qs, urlencode, urlparse


def normalize_url(url: str) -> str:
    """URLを正規化する（スキーム・www・トラッキングパラメータ対応）。

    - http → https に統一
    - www. を除去
    - 末尾スラッシュを除去
    - UTM/fbclid/gclid 等のトラッキングパラメータを除去
    """
    parsed = urlparse(url)
    scheme = "https"
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = parsed.path.rstrip("/")
    # UTM等のトラッキングパラメータを除去
    params = parse_qs(parsed.query, keep_blank_values=True)
    clean_params = {k: v for k, v in params.items()
                    if not k.lower().startswith(("utm_", "fbclid", "gclid"))}
    query = urlencode(clean_params, doseq=True) if clean_params else ""
    normalized = f"{scheme}://{netloc}{path}"
    if query:
        normalized += f"?{query}"
    return normalized
