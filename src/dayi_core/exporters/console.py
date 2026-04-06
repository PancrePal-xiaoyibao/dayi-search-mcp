def render_summary(result: dict) -> str:
    title = result["record"]["title"] or ""
    intro = result["record"].get("overview", {}).get("introduction", "")
    return f"标题: {title}\n概述: {intro}"
