import json
from pathlib import Path


def dump_json(data: dict, path: str) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
