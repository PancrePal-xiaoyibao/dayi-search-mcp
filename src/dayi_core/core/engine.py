import re

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


def _normalize_text(value: str) -> str:
    return re.sub(r"[\s\W_]+", "", value or "", flags=re.UNICODE).lower()


def _score_candidate(keyword: str, title: str, introduction: str) -> float:
    kw = _normalize_text(keyword)
    text = _normalize_text(f"{title}{introduction}")
    if not kw or not text:
        return 0.0

    score = 0.0
    if kw in text:
        score += 100.0

    kw_chars = set(kw)
    text_chars = set(text)
    overlap = len(kw_chars & text_chars) / max(len(kw_chars), 1)
    score += overlap * 50.0

    if title:
        title_n = _normalize_text(title)
        overlap_title = len(set(title_n) & kw_chars) / max(len(kw_chars), 1)
        score += overlap_title * 30.0

    return score


def select_best_candidate(payload: dict, keyword: str, top_k: int = 3) -> dict:
    items = payload.get("list") or []
    if not items:
        raise ValueError("No search candidates found")
    scored = []
    for raw in items[: max(1, top_k)]:
        candidate = dict(raw)
        candidate["title"] = strip_html(candidate.get("title", ""))
        candidate["introduction"] = strip_html(candidate.get("introduction", ""))
        score = _score_candidate(keyword, candidate["title"], candidate["introduction"])
        scored.append((score, candidate))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]


def select_first_candidate(payload: dict) -> dict:
    # 兼容旧调用（如 fixture 流程），仍保留“取首条”行为。
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
    candidate = select_best_candidate(payload, keyword=keyword, top_k=3)
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
