"""action_extractor.py — extract action items from markdown meeting notes.

Matches lines like:
  - [ ] Deploy to staging @alice by 2026-05-01
  * [ ] Review SOW @bob due 2026-05-03
  - [x] Done item @carol by 2026-04-28

Usage:
  notes = open("meeting-notes.md").read()
  for action in extract(notes):
      print(action)
"""

import re

ACTION_RE = re.compile(
    r"(?:^|\n)\s*[-*]\s*\[\s*(?P<done>[xX ])?\s*\]\s*(?P<text>.+?)"
    r"(?:\s+@(?P<owner>\w[\w.-]*))?"
    r"(?:\s+(?:by|due)\s+(?P<due>\d{4}-\d{2}-\d{2}))?\s*(?=\n|$)",
    re.IGNORECASE | re.MULTILINE,
)


def extract(notes: str) -> list[dict]:
    """Return list of action items; items without owner or due date are flagged."""
    results = []
    for m in ACTION_RE.finditer(notes):
        text = m.group("text").strip()
        if not text:
            continue
        item = {
            "text": text,
            "owner": m.group("owner"),
            "due": m.group("due"),
            "complete": m.group("done") in ("x", "X"),
            "warnings": [],
        }
        if not item["owner"]:
            item["warnings"].append("no owner — add @name")
        if not item["due"]:
            item["warnings"].append("no due date — add 'by YYYY-MM-DD'")
        results.append(item)
    return results
