from dayi_core.core.fetcher import fetch_html, fetch_search_results
from dayi_core.parsers.html_fields import strip_html
from dayi_core.providers.disease import DiseaseDetailProvider
from dayi_core.providers.doctor import DoctorDetailProvider
from dayi_core.providers.medical import MedicalDetailProvider
from dayi_core.providers.symptom import SymptomDetailProvider


PROVIDERS = {
    "medical": MedicalDetailProvider(),
    "disease": DiseaseDetailProvider(),
    "doctor": DoctorDetailProvider(),
    "symptom": SymptomDetailProvider(),
}
DETAIL_PATHS = {
    "medical": "drug",
    "disease": "disease",
    "doctor": "doctor",
    "symptom": "symptom",
}


def select_first_candidate(payload: dict) -> dict:
    items = payload.get("list") or []
    if not items:
        raise ValueError("No search candidates found")
    candidate = dict(items[0])
    candidate["title"] = strip_html(candidate.get("title", ""))
    candidate["introduction"] = strip_html(candidate.get("introduction", ""))
    return candidate


def build_detail_url(candidate: dict) -> str:
    query_type = candidate["type"]
    path = DETAIL_PATHS[query_type]
    return f"https://m.dayi.org.cn/{path}/{candidate['id']}"


def query_detail_from_html(*, query_type: str, detail_url: str, html: str, keyword: str) -> dict:
    provider = PROVIDERS[query_type]
    return provider.parse_detail_html(detail_url=detail_url, html=html, keyword=keyword)


def query_by_keyword(*, keyword: str, query_type: str) -> dict:
    payload = fetch_search_results(keyword=keyword, query_type=query_type)
    candidate = select_first_candidate(payload)
    detail_url = build_detail_url(candidate)
    html = fetch_html(detail_url)
    result = query_detail_from_html(
        query_type=query_type,
        detail_url=detail_url,
        html=html,
        keyword=keyword,
    )
    result["search"]["search_url"] = "https://server.dayi.org.cn/api/search"
    result["search"]["strategy"] = "api"
    result["search"]["selected_id"] = candidate["id"]
    result["search"]["selected_name"] = candidate["title"]
    result["search"]["candidates"] = payload.get("list", [])
    result["raw"]["search_payload"] = payload
    return result
