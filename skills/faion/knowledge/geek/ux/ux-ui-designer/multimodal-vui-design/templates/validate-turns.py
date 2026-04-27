"""
Validate a multimodal dialogue tree JSON file for structural completeness.
Input: path to JSON file containing a list of dialogue turns.
Output: JSON list of issues with turn index, description, and severity.
Usage: python validate-turns.py dialogue.json
"""
import json
import sys


def validate_turns(turns: list) -> list:
    issues = []
    for i, turn in enumerate(turns):
        # Touch fallback required on every turn
        actions = turn.get("user_actions", {})
        if not actions.get("touch"):
            issues.append({
                "turn": i,
                "issue": "no touch fallback — voice-only state",
                "severity": "high",
            })

        # Visual overload check
        visual = turn.get("visual_state", {})
        items = visual.get("items", [])
        if len(items) > 5:
            issues.append({
                "turn": i,
                "issue": f"visual overload: {len(items)} items (max 5)",
                "severity": "medium",
            })

        # Destructive actions need confirmation
        if turn.get("destructive") and not turn.get("confirmation_required"):
            issues.append({
                "turn": i,
                "issue": "destructive action without confirmation_required",
                "severity": "high",
            })

        # Voice prompt length for smart displays
        voice_prompt = turn.get("voice_prompt", "")
        word_count = len(voice_prompt.split())
        if word_count > 15:
            issues.append({
                "turn": i,
                "issue": f"voice prompt too long: {word_count} words (max 15 for smart display)",
                "severity": "low",
            })

        # Silence fallback required
        if not turn.get("fallback"):
            issues.append({
                "turn": i,
                "issue": "missing silence fallback",
                "severity": "medium",
            })

    return issues


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate-turns.py <dialogue.json>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        data = json.load(f)

    turns = data if isinstance(data, list) else data.get("turns", [])
    issues = validate_turns(turns)

    if not issues:
        print("OK — no issues found.")
    else:
        print(f"Found {len(issues)} issue(s):")
        print(json.dumps(issues, indent=2))
        high_count = sum(1 for i in issues if i["severity"] == "high")
        if high_count > 0:
            sys.exit(1)
