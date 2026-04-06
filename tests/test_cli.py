from pathlib import Path

from dayi_core.cli.main import build_parser, render_detail_command


def test_build_parser_accepts_detail_url():
    parser = build_parser()
    args = parser.parse_args([
        "detail",
        "--type", "medical",
        "--url", "https://m.dayi.org.cn/drug/1156140",
    ])
    assert args.command == "detail"
    assert args.type == "medical"
    assert args.url == "https://m.dayi.org.cn/drug/1156140"


def test_render_detail_command_outputs_title_and_intro(tmp_path):
    fixture = Path("tests/fixtures/medical_detail_sample.html")
    output = render_detail_command(
        query_type="medical",
        keyword="替吉奥",
        detail_url="https://m.dayi.org.cn/drug/1156140",
        fixture_path=str(fixture),
        json_path=str(tmp_path / "out.json"),
    )
    assert "替吉奥" in output
    assert "局部晚期或转移性胃癌" in output
    assert (tmp_path / "out.json").exists()
