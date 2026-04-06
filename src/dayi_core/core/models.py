from datetime import datetime, timezone


def build_base_result(*, keyword: str, query_type: str, detail_url: str, detail_api: str | None) -> dict:
    return {
        "keyword": keyword,
        "query_type": query_type,
        "status": "ok",
        "search": {
            "search_url": None,
            "strategy": "detail_only",
            "selected_id": detail_url.rstrip("/").split("/")[-1],
            "selected_name": None,
            "confidence": 1.0,
            "candidates": [],
        },
        "detail": {
            "detail_url": detail_url,
            "source_type": "nuxt_state",
            "detail_api": detail_api,
            "dictionary": [],
        },
        "record": {
            "record_type": query_type,
            "title": None,
            "subtitle": None,
            "tags": [],
            "summary": "",
            "overview": {},
            "sections": {},
            "attributes": {},
            "audit": {},
        },
        "source_meta": {
            "site": "m.dayi.org.cn",
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "parser_version": "v1",
        },
        "raw": {
            "nuxt": None,
            "response_data": None,
        },
    }
