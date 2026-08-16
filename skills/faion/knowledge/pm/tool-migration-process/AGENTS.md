# Cross-Tool PM Migration — Process

## Summary

**One-sentence:** Six-phase execution playbook for org-scale PM-tool migrations (Planning → Preparation → Pilot → Full Migration → Cutover → Stabilisation) with ETL engine, rollback, comms plan.

**One-paragraph:** Six-phase execution playbook for org-scale PM-tool migrations (Planning → Preparation → Pilot → Full Migration → Cutover → Stabilisation) with ETL engine, rollback, comms plan. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-tool-migration-process.py` enforces the output contract.

**Ефективно для:**

- Org-wide migration of ≥4 boards or ≥500 active issues.
- Programs requiring formal rollback strategy and change-management comms plan.
- Migrations spanning multiple business units with non-uniform field schemas.

## Applies If (ALL must hold)

- Migration scope includes ≥4 boards or ≥500 issues.
- Business sponsor + dedicated migration owner are named.
- Change-management comms plan can be authored before cutover.

## Skip If (ANY kills it)

- Single team, <500 issues — use tool-migration-basics.
- No sponsor or budget for full 6-phase execution.
- Source tool will sunset within 30 days — emergency path needed instead.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Migration sponsor | named person | exec |
| Migration owner | named PM | PMO |
| Source/target schema audit | Markdown | tool admins |
| Pilot cohort definition | list of boards/teams | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[tool-migration-basics]] | single-team mechanics are the building block |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (incl. skip rule) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix triplets | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output/decision-gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-phases` | sonnet | Judgement on phase ordering + pilot cohort selection. |
| `run-etl` | haiku | Mechanical batch ETL with checkpointing. |
| `draft-comms` | sonnet | Change-management copy per phase. |

## Templates

| File | Purpose |
|------|---------|
| `templates/migration-plan.md.j2` | Six-phase migration plan template with gate criteria per phase |
| `templates/migration-plan.md` | Six-phase migration plan template with gate criteria per phase Generated from `templates/migration-plan.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/load_resume.py` | ETL load + resume script with checkpointing |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-migration-process.py` | Validate the playbook-step artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

- [[tool-migration-basics]]
- [[change-control]]
- [[communications-management]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/load_resume.py`

```python
#!/usr/bin/env python3
"""Load JSONL of target-shaped issues; resumes from .checkpoint on rerun.

Usage:
    cat transformed.jsonl | TARGET_API_URL=https://... TARGET_TOKEN=tok_... python load_resume.py

Input:  JSONL on stdin; each record must have a `_source_id` field.
Output: prints OK <source_id> -> <target_id> per successful record.
        Writes completed source IDs to .load_checkpoint.
        Exits non-zero on unrecoverable error.
"""
import json
import os
import sys
import time

import requests

CHECKPOINT = ".load_checkpoint"
done = set(open(CHECKPOINT).read().split()) if os.path.exists(CHECKPOINT) else set()
URL = os.environ["TARGET_API_URL"]
TOK = os.environ["TARGET_TOKEN"]

with open(CHECKPOINT, "a") as ck:
    for line in sys.stdin:
        rec = json.loads(line)
        sid = rec["_source_id"]
        if sid in done:
            continue
        for attempt in range(5):
            r = requests.post(URL, json=rec, headers={"Authorization": TOK})
            if r.status_code < 300:
                break
            if r.status_code == 429:
                time.sleep(2**attempt)
                continue
            sys.exit(f"FAIL {sid}: {r.status_code} {r.text[:200]}")
        ck.write(sid + "\n")
        ck.flush()
        print(f"OK {sid} -> {r.json()['id']}")
```
