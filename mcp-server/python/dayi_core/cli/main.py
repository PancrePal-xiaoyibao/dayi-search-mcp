import argparse
import json
from pathlib import Path

from dayi_core.core.engine import build_detail_url, query_by_keyword, query_detail_from_html, select_first_candidate
from dayi_core.core.fetcher import fetch_html
from dayi_core.exporters.console import render_summary
from dayi_core.exporters.json_exporter import dump_json


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="dayi")
    subparsers = parser.add_subparsers(dest="command", required=True)

    detail = subparsers.add_parser("detail")
    detail.add_argument("--type", required=True)
    detail.add_argument("--url", required=True)
    detail.add_argument("--keyword", required=False)
    detail.add_argument("--json", dest="json_path")
    detail.add_argument("--fixture-path")

    query = subparsers.add_parser("query")
    query.add_argument("--type", required=True)
    query.add_argument("--keyword", required=True)
    query.add_argument("--json", dest="json_path")
    query.add_argument("--search-fixture-path")
    query.add_argument("--detail-fixture-path")
    return parser


def render_detail_command(*, query_type: str, keyword: str, detail_url: str, fixture_path: str | None = None, json_path: str | None = None) -> str:
    html = Path(fixture_path).read_text(encoding="utf-8") if fixture_path else fetch_html(detail_url)
    result = query_detail_from_html(
        query_type=query_type,
        detail_url=detail_url,
        html=html,
        keyword=keyword,
    )
    if json_path:
        dump_json(result, json_path)
    return render_summary(result)


def render_query_command(*, query_type: str, keyword: str, search_fixture_path: str | None = None, detail_fixture_path: str | None = None, json_path: str | None = None) -> str:
    if search_fixture_path:
        payload = json.loads(Path(search_fixture_path).read_text(encoding="utf-8"))
        candidate = select_first_candidate(payload)
        detail_url = build_detail_url(candidate)
        html = Path(detail_fixture_path).read_text(encoding="utf-8") if detail_fixture_path else fetch_html(detail_url)
        result = query_detail_from_html(
            query_type=query_type,
            detail_url=detail_url,
            html=html,
            keyword=keyword,
        )
        result["search"]["search_url"] = "fixture://search"
        result["search"]["strategy"] = "fixture"
        result["search"]["selected_id"] = candidate["id"]
        result["search"]["selected_name"] = candidate["title"]
        result["search"]["candidates"] = payload.get("list", [])
    else:
        result = query_by_keyword(keyword=keyword, query_type=query_type)
    if json_path:
        dump_json(result, json_path)
    return render_summary(result)


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "detail":
        output = render_detail_command(
            query_type=args.type,
            keyword=args.keyword or "",
            detail_url=args.url,
            fixture_path=args.fixture_path,
            json_path=args.json_path,
        )
        print(output)
    elif args.command == "query":
        output = render_query_command(
            query_type=args.type,
            keyword=args.keyword,
            search_fixture_path=args.search_fixture_path,
            detail_fixture_path=args.detail_fixture_path,
            json_path=args.json_path,
        )
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
