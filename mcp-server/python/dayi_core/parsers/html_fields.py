import re


TITLE_RE = re.compile(r"<h1[^>]*>(?P<title>[^<]+)</h1>")
INTRO_RE = re.compile(r'<div class="item-content _long-field-content"[^>]*><p>(?P<intro>.*?)</p></div>')
ITEM_RE = re.compile(
    r'<div id="(?P<field_id>[^"]+)" class="item-container".*?<span class="item-content"[^>]*>\s*(?P<value>.*?)\s*</span>',
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


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", "", text)
