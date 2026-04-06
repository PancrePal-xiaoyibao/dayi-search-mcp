from dayi_core.providers.medical import MedicalDetailProvider


PROVIDERS = {
    "medical": MedicalDetailProvider(),
}


def query_detail_from_html(*, query_type: str, detail_url: str, html: str, keyword: str) -> dict:
    provider = PROVIDERS[query_type]
    return provider.parse_detail_html(detail_url=detail_url, html=html, keyword=keyword)
