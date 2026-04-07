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


def test_medical_provider_maps_detail_and_notice_sections():
    html = """
    <html><body>
      <h1>测试药物</h1>
      <script>window.__NUXT__={detailApi:"\\u002Fapi\\u002Fmedical\\u002Fdetail"}</script>
      <div id="component" class="item-container"><span class="item-content">成分A</span></div>
      <div id="character" class="item-container"><span class="item-content">白色粉末</span></div>
      <div id="indication" class="item-container"><span class="item-content">适应症A</span></div>
      <div id="dosage" class="item-container"><span class="item-content">每日一次</span></div>
      <div id="specification" class="item-container"><span class="item-content">100mg</span></div>
      <div id="storage" class="item-container"><span class="item-content">阴凉保存</span></div>
      <div id="validity" class="item-container"><span class="item-content">24个月</span></div>
      <div id="standard" class="item-container"><span class="item-content">国药标准</span></div>
      <div id="adverseReaction" class="item-container"><span class="item-content">恶心</span></div>
      <div id="taboo" class="item-container"><span class="item-content">禁用于孕妇</span></div>
      <div id="interaction" class="item-container"><span class="item-content">避免联用药X</span></div>
      <div id="notice" class="item-container"><span class="item-content">监测肝功能</span></div>
    </body></html>
    """
    provider = MedicalDetailProvider()
    result = provider.parse_detail_html(
        detail_url="https://m.dayi.org.cn/drug/999",
        html=html,
        keyword="测试药物",
    )
    detail = result["record"]["sections"]["药品详情"]
    notice = result["record"]["sections"]["注意事项"]
    assert detail["成分"] == "成分A"
    assert detail["执行标准"] == "国药标准"
    assert notice["不良反应"] == "恶心"
    assert notice["药物相互作用"] == "避免联用药X"


def test_medical_provider_fixture_has_non_empty_notice_fields():
    html = Path("tests/fixtures/medical_detail_sample.html").read_text(encoding="utf-8")
    provider = MedicalDetailProvider()
    result = provider.parse_detail_html(
        detail_url="https://m.dayi.org.cn/drug/1156140",
        html=html,
        keyword="替吉奥",
    )
    detail = result["record"]["sections"]["药品详情"]
    notice = result["record"]["sections"]["注意事项"]
    assert detail["成分"]
    assert detail["用法用量"]
    assert notice["不良反应"]
    assert notice["禁忌"]
