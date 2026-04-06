from pathlib import Path

from dayi_core.providers.disease import DiseaseDetailProvider
from dayi_core.providers.doctor import DoctorDetailProvider
from dayi_core.providers.symptom import SymptomDetailProvider


def test_disease_provider_extracts_title_and_detail_api():
    html = Path("tests/fixtures/disease_detail_sample.html").read_text(encoding="utf-8")
    result = DiseaseDetailProvider().parse_detail_html(
        detail_url="https://m.dayi.org.cn/disease/1148126",
        html=html,
        keyword="胰腺癌",
    )
    assert result["query_type"] == "disease"
    assert result["record"]["title"] == "胰腺癌"
    assert result["detail"]["detail_api"] == "/api/disease/detail"


def test_doctor_provider_extracts_title_and_detail_api():
    html = Path("tests/fixtures/doctor_detail_sample.html").read_text(encoding="utf-8")
    result = DoctorDetailProvider().parse_detail_html(
        detail_url="https://m.dayi.org.cn/doctor/1137429",
        html=html,
        keyword="傅德良",
    )
    assert result["query_type"] == "doctor"
    assert result["record"]["title"] == "傅德良"
    assert result["detail"]["detail_api"] == "/api/doctor/detail"


def test_symptom_provider_extracts_title_and_detail_api():
    html = Path("tests/fixtures/symptom_detail_sample.html").read_text(encoding="utf-8")
    result = SymptomDetailProvider().parse_detail_html(
        detail_url="https://m.dayi.org.cn/symptom/1150773",
        html=html,
        keyword="尿淀粉酶升高",
    )
    assert result["query_type"] == "symptom"
    assert result["record"]["title"] == "尿淀粉酶升高"
    assert result["detail"]["detail_api"] == "/api/symptom/detail"
