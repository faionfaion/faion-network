"""Design review pipeline: reads a component spec file, returns structured JSON feedback.

Requires: ANTHROPIC_API_KEY env var.
Usage: python design-review.py component-spec.md
"""
import json
import os
import sys

import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

RUBRIC = """
Review this component spec for:
1. Accessibility (WCAG AA contrast, keyboard nav, aria roles)
2. Token consistency (no hardcoded values)
3. State completeness (empty, loading, error)
4. Responsive behavior (320px / 768px / 1440px)

Return JSON: {"passed": [], "failed": [{"criterion": "", "detail": "", "suggestion": ""}]}
Strip all markdown code fences. Return raw JSON only.
"""


def review_component(spec: str) -> dict:
    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"{RUBRIC}\n\nComponent spec:\n{spec}"}],
    )
    text = resp.content[0].text
    # Strip markdown fences if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


if __name__ == "__main__":
    spec = open(sys.argv[1]).read()
    result = review_component(spec)
    failed = result.get("failed", [])
    print(f"Issues found: {len(failed)}")
    for f in failed:
        print(f"  [{f['criterion']}] {f['detail']} → {f['suggestion']}")
