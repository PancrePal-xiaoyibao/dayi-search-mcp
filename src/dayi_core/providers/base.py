from typing import Protocol

from dayi_core.core.models import build_base_result
from dayi_core.parsers.html_fields import extract_intro, extract_item_fields, extract_title
from dayi_core.parsers.nuxt_state import extract_detail_api_path, extract_nuxt_script


class DetailProvider(Protocol):
    type_name: str

    def parse_detail_html(self, *, detail_url: str, html: str, keyword: str) -> dict:
        ...


class GenericDetailProvider:
    type_name = "generic"

    def parse_detail_html(self, *, detail_url: str, html: str, keyword: str) -> dict:
        detail_api = extract_detail_api_path(html)
        result = build_base_result(
            keyword=keyword,
            query_type=self.type_name,
            detail_url=detail_url,
            detail_api=detail_api,
        )
        title = extract_title(html, keyword)
        intro = extract_intro(html)
        fields = extract_item_fields(html)
        result["search"]["selected_name"] = title
        result["record"]["title"] = title
        result["record"]["overview"] = {"introduction": intro}
        result["record"]["attributes"] = fields
        result["raw"]["detail_html"] = html
        try:
            result["raw"]["nuxt_script"] = extract_nuxt_script(html)
        except Exception:
            result["raw"]["nuxt_script"] = None
        return result
