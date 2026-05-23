# purpose: Scoring script for a candidate study session against ECO domain weights
# consumes: see content/02-output-contract.xml inputs
# produces: artefact conforming to content/02-output-contract.xml
# depends-on: content/01-core-rules.xml
# token-budget-impact: ~200-1000 tokens when loaded as context

#!/usr/bin/env python3
"""score-session.py — weighted exam-style scoring per 2026 PMP ECO.

Usage: python score-session.py session.json
Input JSON: list of {domain: "people"|"process"|"business_environment", correct: true|false}
Output: weighted score and per-domain breakdown.

NOTE: This is a sanity check only. PMI scaled scoring is not public.
Do NOT use as a pass/fail oracle.
"""
from __future__ import annotations
import json
import pathlib
import sys

WEIGHTS = {"people": 0.33, "process": 0.41, "business_environment": 0.26}


def main(path: str) -> int:
    rows = json.loads(pathlib.Path(path).read_text())
    by_dom: dict[str, list[int]] = {k: [] for k in WEIGHTS}
    for r in rows:
        d = r["domain"].lower().replace(" ", "_")
        by_dom.setdefault(d, []).append(1 if r["correct"] else 0)
    weighted = 0.0
    for d, w in WEIGHTS.items():
        items = by_dom.get(d) or [0]
        weighted += w * (sum(items) / len(items))
    print(f"Weighted score: {weighted:.1%}")
    for d, items in by_dom.items():
        if items:
            pct = sum(items) / len(items)
            print(f"  {d}: {sum(items)}/{len(items)} ({pct:.0%})")
    # PMI passing band approximation — NOT authoritative
    return 0 if weighted >= 0.61 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
