from pathlib import Path

from dayi_core.parsers.nuxt_state import extract_detail_api_path, extract_nuxt_script


def test_extract_nuxt_script_finds_window_nuxt_block():
    html = Path("tests/fixtures/medical_detail_sample.html").read_text(encoding="utf-8")
    script = extract_nuxt_script(html)
    assert "window.__NUXT__" in script
    assert "detailApi" in script


def test_extract_detail_api_path_returns_medical_api_path():
    html = Path("tests/fixtures/medical_detail_sample.html").read_text(encoding="utf-8")
    api_path = extract_detail_api_path(html)
    assert api_path == "/api/medical/detail"
