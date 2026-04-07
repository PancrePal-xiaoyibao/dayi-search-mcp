import re


TITLE_RE = re.compile(r"<h1[^>]*>(?P<title>[^<]+)</h1>")
INTRO_RE = re.compile(r'<div class="item-content _long-field-content"[^>]*><p>(?P<intro>.*?)</p></div>')
ITEM_RE = re.compile(
    r'<div id="(?P<field_id>[^"]+)" class="item-container".*?<span class="item-content"[^>]*>\s*(?P<value>.*?)\s*</span>',
    re.DOTALL,
)
LONG_ITEM_RE = re.compile(
    r'<div id="_(?P<field_id>[^"]+)" class="public-container".*?<div class="item-content _long-field-content"[^>]*>(?P<value>.*?)</div>',
    re.DOTALL,
)


def extract_title(html: str, fallback: str = "") -> str:
    match = TITLE_RE.search(html)
    return match.group("title") if match else fallback


def extract_intro(html: str) -> str:
    match = INTRO_RE.search(html)
    return match.group("intro") if match else ""


def extract_item_fields(html: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in ITEM_RE.finditer(html):
        value = re.sub(r"\s+", "", match.group("value"))
        fields[match.group("field_id")] = value
    return fields


def _clean_long_text(value: str) -> str:
    value = re.sub(r"</p>\s*<p[^>]*>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("&nbsp;", " ").replace("&ge;", "≥").replace("&lt;", "<")
    value = re.sub(r"[ \t\r\f\v]+", " ", value)
    value = re.sub(r"\n{2,}", "\n", value)
    return value.strip()


def extract_long_item_fields(html: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for match in LONG_ITEM_RE.finditer(html):
        fields[match.group("field_id")] = _clean_long_text(match.group("value"))
    return fields


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", "", text)
