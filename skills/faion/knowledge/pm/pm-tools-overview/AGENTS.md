# PM Tools Overview

## Summary

**One-sentence:** Overview report mapping team needs to the PM-tool market: MoSCoW requirements (Must/Should/Could/Won't), candidate list, fit-gap analysis, shortlist recommendation.

**One-paragraph:** PM Tools Overview defines the testable methodology that turns the recurring work named in this skill into a repeatable, auditable artefact. The methodology is grounded in 6 core rules (see `content/01-core-rules.xml`), a JSON-Schema output contract, 4 catalogued failure modes, a 5-step procedure, and a decision tree whose leaves all reference a rule id.

**Ефективно для:**

- Teams that do NOT yet have a PM tool and need a structured first selection.
- Coaches helping a portfolio map vague pain points into hard requirements before tool selection.
- Procurement / PMO that needs a fit-gap before triggering a deeper comparison (see pm-tools-comparison).
- Solopreneurs choosing their first tracker beyond a spreadsheet.

## Applies If (ALL must hold)

- Team can articulate 5-15 needs that a PM tool would address.
- At least one stakeholder can prioritise needs via MoSCoW.
- Time-box of 4-8h is available to compile the overview.
- Market scan can include 3-10 candidates without analysis paralysis.

## Skip If (ANY kills it)

- Team already has a working tool and only minor friction — patch the tool, don't re-select.
- Team has not done discovery on needs — overview without needs is shopping.
- Mandatory tool dictated by parent org or customer — write a single-choice ADR instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source-of-truth data | tool export / sheet / API | upstream system named in this methodology |
| Prior cycle's artefact (if any) | json / md | repo / wiki where artefacts persist |
| Named consumer | person / agent | engagement charter |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| `pro/pm/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies). |
| `pro/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft 2020-12) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure with input/action/output | 800 |
| `content/05-examples.xml` | essential | One end-to-end worked example with trace | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `pm-tools-overview_template_fill` | haiku | Bounded template fill, no judgement. |
| `pm-tools-overview_evidence_check` | sonnet | Bounded comparison + judgement on anchored evidence. |
| `pm-tools-overview_synthesis` | opus | Cross-input synthesis + final write-up. |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema (draft 2020-12) for the PM tools overview report artefact. |
| `templates/requirements-doc.md.j2` | Markdown skeleton for the MoSCoW requirements table. |
| `templates/requirements-doc.md` | Markdown skeleton for the MoSCoW requirements table. Generated from `templates/requirements-doc.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/poc-runner.py` | Reference script to scaffold PoC plans per shortlisted tool. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-pm-tools-overview.py` | Validate the artefact against the schema in `content/02-output-contract.xml`. | CI on each artefact change; pre-commit. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- parent skill: `pro/pm/` (see neighbouring methodologies).
- [[launch-raci-template]]
- [[reporting-basics]]
- external: industry references cited inline in `content/01-core-rules.xml`.

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input
preconditions, source-of-truth access, named-consumer presence) onto a concrete
verdict — apply the methodology, downgrade to draft, or skip — with each leaf
referencing a rule id from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://faion.net/schemas/pm-tools-overview.json",
  "type": "object",
  "required": [
    "report_id",
    "requirements",
    "candidates",
    "fit_gap",
    "shortlist",
    "decision_owner"
  ],
  "properties": {
    "report_id": {
      "type": "string"
    },
    "requirements": {
      "type": "array",
      "minItems": 5,
      "items": {
        "type": "object",
        "required": [
          "title",
          "moscow",
          "evidence"
        ],
        "properties": {
          "moscow": {
            "enum": [
              "Must",
              "Should",
              "Could",
              "Won't"
            ]
          },
          "evidence": {
            "type": "array",
            "minItems": 1
          }
        }
      }
    },
    "candidates": {
      "type": "array",
      "minItems": 3,
      "maxItems": 10,
      "items": {
        "type": "object",
        "required": [
          "name",
          "reason"
        ]
      }
    },
    "fit_gap": {
      "type": "object",
      "additionalProperties": {
        "type": "object"
      }
    },
    "shortlist": {
      "type": "array",
      "minItems": 2,
      "maxItems": 3
    },
    "decision_owner": {
      "type": "string"
    }
  }
}
```

### `templates/poc-runner.py`

```python
"""


"""poc_runner.py — minimal POC scenario harness for PM tool evaluation.

Vendor adapters live in adapters/<vendor>.py and implement:
    create_issue() -> str (issue ID)
    transition(issue_id: str) -> None
    search(query: str) -> list[dict]
    fire_webhook() -> None

Usage:
    python3 poc_runner.py --vendor jira --config config/jira.json
    python3 poc_runner.py --vendor linear --config config/linear.json
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import time


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vendor", required=True, help="e.g. jira, linear, gitlab")
    ap.add_argument("--config", required=True, help="JSON path with creds + project")
    args = ap.parse_args()

    cfg = json.load(open(args.config))
    adapter = importlib.import_module(f"adapters.{args.vendor}").Adapter(cfg)

    results: dict[str, dict] = {}
    for step in ("create_issue", "transition", "search", "fire_webhook"):
        t0 = time.perf_counter()
        try:
            getattr(adapter, step)()
            results[step] = {
                "ok": True,
                "ms": int((time.perf_counter() - t0) * 1000),
            }
        except Exception as exc:  # noqa: BLE001
            results[step] = {"ok": False, "error": str(exc)}

    json.dump({"vendor": args.vendor, "steps": results}, sys.stdout, indent=2)
    print()
    failed = [s for s, r in results.items() if not r["ok"]]
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
```
