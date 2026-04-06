from pathlib import Path

from dayi_core.providers.medical import MedicalDetailProvider


def test_medical_provider_maps_title_and_detail_api():
    html = Path("tests/fixtures/medical_detail_sample.html").read_text(encoding="utf-8")
    provider = MedicalDetailProvider()
    result = provider.parse_detail_html(
        detail_url="https://m.dayi.org.cn/drug/1156140",
        html=html,
        keyword="替吉奥",
    )
    assert result["query_type"] == "medical"
    assert result["detail"]["detail_api"] == "/api/medical/detail"
    assert result["record"]["title"] == "替吉奥"


def test_medical_provider_extracts_intro_and_basic_fields():
    html = Path("tests/fixtures/medical_detail_sample.html").read_text(encoding="utf-8")
    provider = MedicalDetailProvider()
    result = provider.parse_detail_html(
        detail_url="https://m.dayi.org.cn/drug/1156140",
        html=html,
        keyword="替吉奥",
    )
    assert "抗肿瘤药" in result["record"]["overview"]["basic_info"]["药品类型"]
    assert "局部晚期或转移性胃癌" in result["record"]["overview"]["introduction"]
