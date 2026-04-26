"""
reprompt-lint.py — validate VUI re-prompt ladder YAML files.

Checks per intent:
  - At least 3 rungs (rung 1, rung 2, rung 3)
  - Rung 2 contains at least 2 example phrases ("try" or "example" keyword)
  - Rung 3 contains an escalation path (agent|help|menu|instead|press|transfer)
  - No banned blame language in any rung

Usage: python reprompt-lint.py reprompts.yaml
Exit code: 0 = clean, 1 = violations found

Expected YAML format:
  welcome_intent:
    - "I didn't catch that. What's the city?"
    - "I'm having trouble. Try saying 'New York' or 'Chicago'."
    - "Let me try another way. Say 'agent' or press 1."
"""
import re
import sys
import yaml

BANNED = [
    r"\bwrong\b",
    r"\binvalid\b",
    r"\byou said\b",
    r"didn'?t work",
    r"i'?m sorry.*i'?m sorry",  # stacked apology
]

ESCALATION_KEYWORDS = ["agent", "help", "menu", "instead", "press", "transfer", "human"]
EXAMPLE_KEYWORDS = ["try", "example", "like", "such as"]


def check(prompts: dict) -> list:
    issues = []
    for intent, rungs in prompts.items():
        if not isinstance(rungs, list):
            issues.append(f"{intent}: expected list of rungs, got {type(rungs).__name__}")
            continue
        if len(rungs) < 3:
            issues.append(f"{intent}: needs 3 rungs, has {len(rungs)}")

        # Rung 2 must have example phrases
        if len(rungs) >= 2:
            rung2 = rungs[1].lower()
            if not any(kw in rung2 for kw in EXAMPLE_KEYWORDS):
                issues.append(f"{intent} rung2: missing example phrase (try/like/such as)")

        # Rung 3 must have escalation
        if len(rungs) >= 3:
            rung3 = rungs[2].lower()
            if not any(kw in rung3 for kw in ESCALATION_KEYWORDS):
                issues.append(f"{intent} rung3: missing escalation ({'/'.join(ESCALATION_KEYWORDS)})")

        # Blame language check in all rungs
        for i, rung in enumerate(rungs):
            for pat in BANNED:
                if re.search(pat, rung, re.IGNORECASE):
                    issues.append(f"{intent} rung{i+1}: banned pattern '{pat}' in: {rung[:80]}")

    return issues


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    with open(sys.argv[1]) as f:
        data = yaml.safe_load(f)

    issues = check(data)
    for issue in issues:
        print(issue)

    sys.exit(1 if issues else 0)
