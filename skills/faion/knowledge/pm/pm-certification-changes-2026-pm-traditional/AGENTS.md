# PM Certification Exam Changes 2026

## Summary

**One-sentence:** Diff report of 2026 PMP ECO vs prior: People 42→33%, Process 50→41%, Business Environment 8→26%; lists added/removed/reweighted tasks per domain.

**One-paragraph:** Diff report of 2026 PMP ECO vs prior: People 42→33%, Process 50→41%, Business Environment 8→26%; lists added/removed/reweighted tasks per domain. The methodology applies in pm-traditional contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-pm-certification-changes-2026.py` enforces the output contract.

**Ефективно для:**

- Briefing existing PMP candidates on what changes 2026-07-01.
- Updating training collateral with a single source of truth on diffs.
- Producing study-plan reallocation guidance.
- Communicating curriculum re-design rationale to stakeholders.

## Applies If (ALL must hold)

- Diff is authored against the 2026 ECO PDF as primary source.
- Prior ECO is available for line-by-line comparison.
- Output will be consumed by training providers / candidates.

## Skip If (ANY kills it)

- Non-PMP certification.
- Diff already published by an authoritative source the team trusts.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| 2026 ECO PDF | PDF | PMI |
| Prior ECO PDF | PDF | PMI archive |
| Diff tooling or manual comparison checklist | spec | PM author |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[pm-certification-alignment-2026]] | downstream methodology that consumes this diff |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/05-examples.xml` | optional | End-to-end worked example | 700 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `extract-diffs` | sonnet | Judgement: which task is renamed vs added vs removed. |
| `compute-weight-delta` | haiku | Mechanical % deltas. |
| `draft-candidate-brief` | sonnet | Narrative for candidate-facing brief. |

## Templates

| File | Purpose |
|------|---------|
| `templates/score-session.py` | Scoring script for a candidate study session against ECO domain weights |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Related

- [[pm-certification-alignment-2026]]
- [[communications-management]]
- [[lessons-learned]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/score-session.py`

```python
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
```
