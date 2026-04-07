from dayi_core.providers.base import GenericDetailProvider


class MedicalDetailProvider(GenericDetailProvider):
    type_name = "medical"

    @staticmethod
    def _pick(fields: dict, *aliases: str) -> str:
        for key in aliases:
            value = fields.get(key)
            if value:
                return value
        return ""

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
        result["record"]["sections"]["药品详情"] = {
            "成分": self._pick(fields, "component", "ingredient"),
            "性状": self._pick(fields, "character", "property"),
            "适应症": self._pick(fields, "indication"),
            "用法用量": self._pick(fields, "dosage", "usage", "dosageAndAdministration"),
            "规格": self._pick(fields, "specification", "spec"),
            "贮藏方法": self._pick(fields, "storage", "storeMethod"),
            "有效期": self._pick(fields, "validity", "expiryDate", "effectivePeriod"),
            "执行标准": self._pick(fields, "standard", "executionStandard"),
        }
        result["record"]["sections"]["注意事项"] = {
            "不良反应": self._pick(fields, "adverseReaction", "adverseReactions"),
            "禁忌": self._pick(fields, "taboo", "contraindication", "contraindications"),
            "药物相互作用": self._pick(fields, "interaction", "drugInteraction"),
            "注意事项": self._pick(fields, "notice", "precautions"),
        }
        return result
