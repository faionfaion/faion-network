# Continuous Discovery Habits

## Summary

**One-sentence:** Weekly customer-discovery cadence where the Product Trio (PM, Design, Tech) maintains an Opportunity Solution Tree with verbatim-quote provenance and agent-assisted triage / coding / synthesis.

**One-paragraph:** Weekly customer-discovery cadence (≥1 interview/week) where the Product Trio maintains an Opportunity Solution Tree (OST). Every roadmap item traces to a verbatim quote with participant-id + interview-date; opportunities are problem-shaped (never 'build X'); the tree is pruned monthly. Agents automate mechanical work — feedback triage, transcript coding, weekly tree-diff synthesis — under explicit token budgets. Output: tree-as-YAML + weekly discovery readout + roadmap-input delta.

**Ефективно для:**

- PM-owned продукт із потребою захищеного weekly cadence (≥1 інтерв'ю/тиждень).
- Roadmap, що дрейфує в feature-list — leadership не пояснює outcome за пунктами.
- Product Trio, який тільки формується і шукає shared artefact для синхронізації.
- Quarterly planning synthesis — агенти зводять 60-80 інтерв'ю в свіжий OST.

## Applies If (ALL must hold)

- PM owns one product area and needs a defensible weekly cadence (one interview/week minimum).
- Roadmaps drifting to feature-list mode — leadership cannot articulate what outcome each item serves.
- Product Trio is forming and needs a shared artifact to triangulate on.
- Quarterly planning prep — agents synthesize 60-80 interviews into a refreshed OST that becomes input to roadmap, OKRs, and discovery sprints.
- Solo PM at a startup wants an LLM to triage support tickets, NPS verbatims, sales-call recordings into the OST as candidate opportunities for trio review.

## Skip If (ANY kills it)

- Pre-PMF zero-to-one with founder-led customer development — use customer-development methodology.
- Regulated domains where weekly outside-customer interviews require legal review per touchpoint.
- B2B with fewer than 20 logo accounts and a 12-month sales cycle — weekly interviews are not sustainable.
- Mature growth-stage where experimentation-at-scale has displaced qualitative discovery as the primary loop.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Outcome metric | string + movability check | PM / leadership |
| Customer roster | table {segment, recency, plan_tier, churn_status} | CRM / billing |
| Transcript store | text/audio per interview | Zoom / Otter / Granola |
| OST current state | YAML | previous week's commit |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[stakeholder-management]] | Trio decision-rights + sponsor cadence inform the OST review meeting. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules + skip-this-methodology covering provenance, cadence, prune, trio-prep | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for OST node + weekly readout + valid/invalid + forbidden | 900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: outcome → interview → code → synthesize → trio decide | 800 |
| `content/06-decision-tree.xml` | essential | Apply / skip routing on observable signals → rule from 01-core-rules.xml | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feedback-triage` | haiku | High-volume taxonomy categorisation. |
| `interview-prep` | sonnet | Structured authoring with past-behaviour anchoring. |
| `ost-synthesizer` | opus | Cross-corpus reasoning over coded quotes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ost.yaml` | OST-as-YAML skeleton with outcome → opportunity → solution → assumption-test fields. |
| `templates/weekly-discovery.md.j2` | Weekly discovery readout template with shipped / coded / tree-diff / next-week sections. |
| `templates/weekly-discovery.md` | Weekly discovery readout template with shipped / coded / tree-diff / next-week sections. Generated from `templates/weekly-discovery.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/ost-apply.py` | Apply a tree-diff (JSON-patch / YAML-diff) to the current OST file. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-continuous-discovery-habits.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[stakeholder-management]]
- [[product-analytics]]
- [[experimentation-at-scale]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ost.yaml`

```yaml
# Opportunity Solution Tree (OST)
# Source of truth for continuous discovery. Edit via PR; agents emit diffs only.
# Run scripts/ost-apply.py to apply agent-proposed diffs.

outcome:
  id: outcome_YYYY_QN_<slug>
  metric: <measurable_metric_name>      # e.g., pct_new_signups_completing_first_value_action
  baseline: 0.00
  target: 0.00
  owner: pm@team.com
  frozen_since: "YYYY-MM-DD"

opportunities:
  - id: opp_<slug>
    statement: "<customer need/pain in customer's own words — no 'build X' phrases>"
    evidence:
      - quote_id: q_YYYY-MM-DD_p000   # participant-id + interview-date
        verbatim: "<exact quote>"
        participant_segment: <segment>
        interview_date: "YYYY-MM-DD"
    parent: outcome_YYYY_QN_<slug>
    last_evidence_date: "YYYY-MM-DD"
    status: active                      # active | parked | shipped | invalidated
    solutions:
      - id: sol_<slug>
        assumption_tests:
          - type: desirability           # desirability | viability | feasibility | usability | ethical
            method: prototype_test
            owner: ux
          - type: feasibility
            method: spike
            owner: tech_lead
        decision: not_started           # not_started | testing | win | kill

# OST diff format (for agent output):
# diffs:
#   add:
#     - id: opp_new
#       statement: "..."
#       evidence: [...]
#       parent: outcome_...
#   update:
#     - id: opp_existing
#       last_evidence_date: "YYYY-MM-DD"
#   park:
#     - opp_stale_no_evidence
#   archive:
#     - opp_old_180d
```

### `templates/ost-apply.py`

```python
"""

#!/usr/bin/env python3
"""
ost-apply.py — apply OST diffs emitted by agents.
Usage: python ost-apply.py <ost.yaml> <diff.yaml>
The diff format is the schema defined in ost.yaml under 'diffs:'.
PM reviews the diff file before running this script.
Operations: add (new opportunity), update (patch fields), park (set status=parked),
            archive (remove from active tree).
"""
import sys, yaml, copy
from pathlib import Path


def apply_diff(ost: dict, diff: dict) -> dict:
    out = copy.deepcopy(ost)
    by_id = {o["id"]: o for o in out.get("opportunities", [])}

    for op in diff.get("add", []):
        if op["id"] in by_id:
            raise SystemExit(f"add: id already exists: {op['id']}")
        out["opportunities"].append(op)
        by_id[op["id"]] = op

    for op in diff.get("update", []):
        if op["id"] not in by_id:
            raise SystemExit(f"update: missing opportunity: {op['id']}")
        by_id[op["id"]].update(op)

    for op_id in diff.get("park", []):
        if op_id not in by_id:
            raise SystemExit(f"park: missing opportunity: {op_id}")
        by_id[op_id]["status"] = "parked"

    for op_id in diff.get("archive", []):
        out["opportunities"] = [
            o for o in out["opportunities"] if o["id"] != op_id
        ]

    return out


if __name__ == "__main__":
    ost_path = Path(sys.argv[1])
    diff_path = Path(sys.argv[2])
    ost = yaml.safe_load(ost_path.read_text())
    diff = yaml.safe_load(diff_path.read_text())
    result = apply_diff(ost, diff.get("diffs", diff))
    ost_path.write_text(yaml.safe_dump(result, sort_keys=False, allow_unicode=True))
    print(f"Applied diff from {diff_path} to {ost_path}")
```
