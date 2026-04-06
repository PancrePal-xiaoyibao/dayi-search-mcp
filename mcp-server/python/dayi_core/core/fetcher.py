import json
import ssl
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}
JSON_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json,text/plain,*/*",
}
INSECURE_CONTEXT = ssl._create_unverified_context()
SEARCH_API_URL = "https://server.dayi.org.cn/api/search"


def fetch_html(url: str, *, timeout: int = 20) -> str:
    request = Request(url, headers=DEFAULT_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except URLError as exc:
        if not isinstance(exc.reason, ssl.SSLError):
            raise
        with urlopen(request, timeout=timeout, context=INSECURE_CONTEXT) as response:
            return response.read().decode("utf-8", errors="replace")


def fetch_json(url: str, *, params: dict[str, object] | None = None, timeout: int = 20, insecure: bool = False) -> dict:
    full_url = url if not params else f"{url}?{urlencode(params)}"
    request = Request(full_url, headers=JSON_HEADERS)
    kwargs = {"timeout": timeout}
    if insecure:
        kwargs["context"] = INSECURE_CONTEXT
    with urlopen(request, **kwargs) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def fetch_search_results(*, keyword: str, query_type: str, page_no: int = 1, page_size: int = 8) -> dict:
    return fetch_json(
        SEARCH_API_URL,
        params={"pageNo": page_no, "pageSize": page_size, "keyword": keyword, "type": query_type},
        insecure=True,
    )
