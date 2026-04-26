# pretest_check.py — enforce pre-launch gates before any A/B test goes live
# Input: test card dict with required fields
# Output: (can_launch: bool, failures: list[str])

def can_launch(card: dict) -> tuple[bool, list[str]]:
    """Return (True, []) if all gates pass, else (False, [reason, ...])."""
    fails = []
    if not card.get("hypothesis_if_then_because"):
        fails.append("missing if/then/because hypothesis")
    if not card.get("primary_metric"):
        fails.append("no primary metric")
    if not card.get("mde_relative"):
        fails.append("no MDE (state as relative %, e.g. 0.10 for 10%)")
    if card.get("sample_per_variant", 0) < 1000:
        fails.append("sample_per_variant < 1000 — underpowered")
    if not card.get("guardrails"):
        fails.append("no guardrail metrics listed")
    if not card.get("end_date"):
        fails.append("no pre-committed end date")
    if card.get("overlaps_with_active_test"):
        fails.append("overlaps with an active test on the same surface")
    return (len(fails) == 0, fails)


# Example usage:
if __name__ == "__main__":
    card = {
        "hypothesis_if_then_because": "IF we change CTA copy THEN conversion increases 10% BECAUSE...",
        "primary_metric": "signup_conversion_rate",
        "mde_relative": 0.10,
        "sample_per_variant": 15000,
        "guardrails": ["bounce_rate", "d7_retention", "support_tickets"],
        "end_date": "2026-05-10",
        "overlaps_with_active_test": False,
    }
    ok, errors = can_launch(card)
    if ok:
        print("PASS — test may launch")
    else:
        print("FAIL:")
        for e in errors:
            print(f"  - {e}")
