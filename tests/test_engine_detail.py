from pathlib import Path

from dayi_core.core.engine import query_detail_from_html


def test_query_detail_from_html_returns_normalized_result():
    html = Path("tests/fixtures/medical_detail_sample.html").read_text(encoding="utf-8")
    result = query_detail_from_html(
        query_type="medical",
        detail_url="https://m.dayi.org.cn/drug/1156140",
        html=html,
        keyword="替吉奥",
    )
    assert result["record"]["title"] == "替吉奥"
    assert result["detail"]["source_type"] == "nuxt_state"
