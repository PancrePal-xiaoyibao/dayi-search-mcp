from dayi_core.providers.base import GenericDetailProvider


class MedicalDetailProvider(GenericDetailProvider):
    type_name = "medical"

    def parse_detail_html(self, *, detail_url: str, html: str, keyword: str) -> dict:
        result = super().parse_detail_html(detail_url=detail_url, html=html, keyword=keyword)
        fields = result["record"]["attributes"]
        result["record"]["overview"] = {
            "introduction": result["record"]["overview"].get("introduction", ""),
            "basic_info": {
                "中文名称": fields.get("comName"),
                "汉语拼音": fields.get("chinesePinyin"),
                "英文名称": fields.get("englishName"),
                "药品类型": fields.get("drugType"),
                "处方类型": fields.get("recipeType"),
                "医保类型": fields.get("healthType"),
                "参考价格": fields.get("price"),
                "给药途径": fields.get("routeAdministration"),
                "剂型": fields.get("dosageForm"),
            },
        }
        return result
