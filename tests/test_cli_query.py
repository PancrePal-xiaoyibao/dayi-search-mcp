from pathlib import Path

from dayi_core.cli.main import build_parser, render_query_command


def test_build_parser_accepts_query_command():
    parser = build_parser()
    args = parser.parse_args([
        "query",
        "--type", "medical",
        "--keyword", "替吉奥",
    ])
    assert args.command == "query"
    assert args.type == "medical"
    assert args.keyword == "替吉奥"


def test_render_query_command_uses_search_fixture_and_detail_fixture(tmp_path):
    output = render_query_command(
        query_type="medical",
        keyword="替吉奥",
        search_fixture_path="tests/fixtures/search_medical_sample.json",
        detail_fixture_path="tests/fixtures/medical_detail_sample.html",
        json_path=str(tmp_path / "query.json"),
    )
    assert "替吉奥" in output
    assert (tmp_path / "query.json").exists()
