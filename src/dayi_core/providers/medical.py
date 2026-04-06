import re

from dayi_core.core.models import build_base_result
from dayi_core.parsers.nuxt_state import extract_detail_api_path


TITLE_RE = re.compile(r"<h1[^>]*>(?P<title>[^<]+)</h1>")
INTRO_RE = re.compile(r'<div class="item-content _long-field-content"[^>]*><p>(?P<intro>.*?)</p></div>')
FIELD_RE_TEMPLATE = r'<div id="{field_id}" class="item-container".*?<span class="item-content"[^>]*>\s*(?P<value>.*?)\s*</span>'


class MedicalDetailProvider:
    type_name = "medical"

    def _extract_field(self, html: str, field_id: str) -> str | None:
        pattern = re.compile(FIELD_RE_TEMPLATE.format(field_id=field_id), re.DOTALL)
        match = pattern.search(html)
        if not match:
            return None
        return re.sub(r"\s+", "", match.group("value"))

    def parse_detail_html(self, *, detail_url: str, html: str, keyword: str) -> dict:
        detail_api = extract_detail_api_path(html)
        result = build_base_result(
            keyword=keyword,
            query_type=self.type_name,
            detail_url=detail_url,
            detail_api=detail_api,
        )
        match = TITLE_RE.search(html)
        title = match.group("title") if match else keyword
        intro_match = INTRO_RE.search(html)
        intro = intro_match.group("intro") if intro_match else ""

        result["search"]["selected_name"] = title
        result["record"]["title"] = title
        result["record"]["overview"] = {
            "introduction": intro,
            "basic_info": {
                "中文名称": self._extract_field(html, "comName"),
                "汉语拼音": self._extract_field(html, "chinesePinyin"),
                "英文名称": self._extract_field(html, "englishName"),
                "药品类型": self._extract_field(html, "drugType"),
                "处方类型": self._extract_field(html, "recipeType"),
                "医保类型": self._extract_field(html, "healthType"),
                "参考价格": self._extract_field(html, "price"),
                "给药途径": self._extract_field(html, "routeAdministration"),
                "剂型": self._extract_field(html, "dosageForm"),
            },
        }
        return result
