# Cross-Tool Migration Basics

## Summary

**One-sentence:** Spec for migrating project-management data between tools: pre-migration audit, field mapping, ETL execution, post-cutover validation.

**One-paragraph:** Spec for migrating project-management data between tools: pre-migration audit, field mapping, ETL execution, post-cutover validation. The methodology applies in pm-agile contexts where the preconditions in `Applies If` hold and none of the `Skip If` triggers fire. Decision routing lives in `content/06-decision-tree.xml`; testable rules with rationale live in `content/01-core-rules.xml`; the validator at `scripts/validate-tool-migration-basics.py` enforces the output contract.

**Ефективно для:**

- Migrating a single team from Jira → Linear / GitHub Projects / ClickUp.
- Consolidating ≤3 boards into one tool before a larger org-wide migration.
- Auditing whether a proposed migration is feasible without data loss.

## Applies If (ALL must hold)

- Source tool has a documented export API or CSV export.
- Target tool supports the source's field types (or you accept lossy mapping).
- <500 active issues and <5 custom fields — otherwise use tool-migration-process.

## Skip If (ANY kills it)

- Org-wide migration with >3 boards — use tool-migration-process.
- Source data quality is unknown — audit first.
- No business sponsor for the migration.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Source export | CSV/JSON via API | source tool admin |
| Target field schema | JSON | target tool admin |
| Field-mapping table | Markdown/YAML | PM + admin |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[tool-migration-process]] | for >3-board migrations, use the full process spec |

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
| `draft-field-map` | sonnet | Judgement on lossy mappings + default-on-miss. |
| `run-count-check` | haiku | Mechanical row-count diff. |

## Templates

| File | Purpose |
|------|---------|
| `templates/field-mapping.md.j2` | Field-mapping template with source × target × transform × default-on-miss |
| `templates/field-mapping.md` | Field-mapping template with source × target × transform × default-on-miss Generated from `templates/field-mapping.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/count-check.py` | Pre/post count-check script to verify no rows lost |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-tool-migration-basics.py` | Validate the spec artefact against the schema in `02-output-contract.xml` | CI on each artefact change; pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[tool-migration-process]]
- [[scrum-ceremonies]]
- [[change-control]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (preconditions, baseline presence, threshold pass/fail) to a concrete action; each leaf references a rule from `01-core-rules.xml`. Use it when in doubt about whether or how to apply this methodology to the case at hand.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/count-check.py`

```python
#!/usr/bin/env python3
"""count-check.py — compare source vs target issue counts after migration.

Exit 0 if drift is within threshold (default 1%), exit 1 otherwise.

Usage:
    JIRA_URL=https://myorg.atlassian.net JIRA_TOKEN=<token> \\
    LINEAR_TOKEN=<token> \\
        python3 count-check.py [--threshold 0.01]

Customize SOURCE_COUNT and TARGET_COUNT functions for your tool pair.
"""
from __future__ import annotations

import argparse
import os
import sys

import requests


def source_count() -> int:
    """Count all issues in the Jira source project."""
    base = os.environ["JIRA_URL"].rstrip("/")
    token = os.environ["JIRA_TOKEN"]
    r = requests.get(
        f"{base}/rest/api/3/search",
        params={"jql": "project = PROJ", "maxResults": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    r.raise_for_status()
    return r.json()["total"]


def target_count() -> int:
    """Count all issues in the Linear target team."""
    token = os.environ["LINEAR_TOKEN"]
    query = '{ issues(filter:{team:{key:{eq:"ABC"}}}) { totalCount } }'
    r = requests.post(
        "https://api.linear.app/graphql",
        json={"query": query},
        headers={"Authorization": token},
    )
    r.raise_for_status()
    return r.json()["data"]["issues"]["totalCount"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=0.01, help="Max allowed drift (default 1%%)")
    args = ap.parse_args()

    src = source_count()
    tgt = target_count()
    drift = abs(src - tgt) / max(src, 1)

    print(f"source={src}  target={tgt}  drift={drift:.2%}  threshold={args.threshold:.2%}")

    if drift > args.threshold:
        print(f"FAIL: drift {drift:.2%} exceeds threshold {args.threshold:.2%}")
        return 1

    print("PASS: counts within threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
