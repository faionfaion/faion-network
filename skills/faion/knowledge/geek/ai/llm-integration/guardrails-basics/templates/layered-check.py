# Layered guardrail check: fast-to-slow ordering
# Requires: PromptInjectionDetector and a moderator with .moderate(text) -> dict

def check_input(text: str, detector, moderator, max_len: int = 4000) -> dict:
    """Run layered input checks from fastest to slowest.

    Returns {"safe": True} or {"safe": False, "reason": str, ...}
    Never raises — callers get a structured dict in all cases.
    """
    if len(text) > max_len:
        return {"safe": False, "reason": "length_exceeded"}
    is_injection, _ = detector.detect(text)
    if is_injection:
        return {"safe": False, "reason": "prompt_injection"}
    try:
        mod = moderator.moderate(text)
        if mod.get("is_flagged"):
            return {
                "safe": False,
                "reason": "moderation",
                "categories": mod.get("flagged_categories", []),
            }
    except Exception as exc:
        # Moderation API failure → log and fail open (or closed per policy)
        return {"safe": False, "reason": f"moderation_error: {exc}"}
    return {"safe": True}
