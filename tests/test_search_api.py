import json
from pathlib import Path

from dayi_core.core.engine import select_first_candidate


def test_select_first_candidate_from_search_response():
    payload = json.loads(Path("tests/fixtures/search_medical_sample.json").read_text(encoding="utf-8"))
    candidate = select_first_candidate(payload)
    assert candidate["id"] == 1156140
    assert candidate["type"] == "medical"
    assert "替吉奥" in candidate["title"]
