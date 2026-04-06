import argparse
from pathlib import Path

from dayi_core.core.engine import query_detail_from_html
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
