import codecs
import re

from dayi_core.core.exceptions import NuxtStateNotFoundError


NUXT_SCRIPT_RE = re.compile(r"<script>window\.__NUXT__=.*?</script>", re.DOTALL)
DETAIL_API_RE = re.compile(r'detailApi:"(?P<path>[^"]+)"')


def extract_nuxt_script(html: str) -> str:
    match = NUXT_SCRIPT_RE.search(html)
    if not match:
        raise NuxtStateNotFoundError("window.__NUXT__ script block not found")
    return match.group(0)


def extract_detail_api_path(html: str) -> str | None:
    script = extract_nuxt_script(html)
    match = DETAIL_API_RE.search(script)
    if not match:
        return None
    return codecs.decode(match.group("path"), "unicode_escape")
