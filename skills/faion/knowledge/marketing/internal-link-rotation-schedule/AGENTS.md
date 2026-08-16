# Internal Link Rotation Schedule

## Summary

**One-sentence:** Quarterly cluster-rotation schedule for internal-link audits — one cluster per fortnight, 60-min review window, deferred-fix tracking with a 30-day SLA.

**One-paragraph:** Topical-authority best practice tells operators to maintain internal-link integrity, but never prescribes a cadence — so audits never happen. This schedule rotates one cluster every 2 weeks (6 clusters per quarter), in a fixed 60-min window. Each cluster audit consumes the upstream [[internal-linking-strategy-graph]] output; deferred fixes carry a 30-day SLA; missed SLAs escalate into the next rotation slot. Output is the rotation calendar + per-cluster audit log + deferred-fix register.

**Ефективно для:**

- Solo operators who already produced a graph spec but never rotate audits.
- Sites with 3-10 clusters where rotating one per fortnight covers the whole site quarterly.
- Sustaining E-E-A-T signals without taking on a continuous-audit cost.
- Pairing with publishing cadence — audit lands in the off-publishing week.

## Applies If (ALL must hold)

- Operator has a current internal-link graph spec (from [[internal-linking-strategy-graph]]).
- 3-10 topic clusters defined on the site.
- 60-min reserved review slot bi-weekly is realistic for the operator.
- Deferred-fix tracker exists (issue tracker, file, or spreadsheet).

## Skip If (ANY kills it)

- No graph spec yet — produce one first via [[internal-linking-strategy-graph]].
- Site has &gt; 10 clusters — rotation per fortnight cannot cover; need a different cadence.
- Operator cannot commit a recurring 60-min slot — choose a single annual audit instead.
- Deferred fixes consistently slip 60+ days — the schedule is theatre; address the underlying cause first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Current graph spec (clusters + hubs) | YAML | [[internal-linking-strategy-graph]] |
| Calendar with bi-weekly 60-min slot | calendar entry | operator |
| Deferred-fix register | sheet / issue tracker | operator |
| Last quarter's audit logs (if any) | markdown | prior cycle |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[internal-linking-strategy-graph]] | Provides the graph spec the rotation audits against. |
| [[hook-bank-template]] | Anchor-text rewrites benefit from hook patterns. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: 1 cluster per fortnight, 60-min window, deferred-fix 30-day SLA, no skipping, rotation order fixed, end-of-quarter retrospective | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for rotation calendar + audit-log + deferred-fix register + valid/invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: schedule-slip, SLA-erosion, audit-theatre, missing-retrospective | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure: confirm graph spec → assign cluster order → run 60-min audit → log fixes → quarterly retro | 700 |
| `content/05-examples.xml` | essential | Worked example: 6-cluster site, Q3 rotation, observed SLA drift and recovery | 600 |
| `content/06-decision-tree.xml` | essential | Tree routing observables → rule id | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `confirm_graph_spec_freshness` | haiku | Date-arithmetic check. |
| `audit_60min_walkthrough` | sonnet | Per-cluster judgement bounded to 60 min. |
| `defer_or_fix_decision` | sonnet | Bounded prioritisation per SLA budget. |
| `quarterly_retro_summary` | sonnet | Narrate trends across 6 rotations. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rotation-calendar.yaml` | Quarterly calendar with bi-weekly slots |
| `templates/audit-log.md.j2` | Per-cluster 60-min audit log template |
| `templates/audit-log.md` | Per-cluster 60-min audit log template Generated from `templates/audit-log.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/_smoke-test.json` | Minimum viable rotation + audit-log bundle for validator self-test |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-internal-link-rotation-schedule.py` | Validate rotation calendar + audit log + register against 02-output-contract schema | Pre-commit / end of quarter |

## Related

- [[internal-linking-strategy-graph]]
- [[hook-bank-template]]
- [[in-issue-ad-format-library]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps graph-spec freshness, cluster count, calendar availability, and deferred-fix backlog to a rule from `01-core-rules.xml`, telling the agent whether to publish the rotation calendar, block on a missing prerequisite, or skip the schedule. Walk it at the start of every quarter; do not cache outcomes across quarters.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/rotation-calendar.yaml`

```yaml
quarter: 2026-Q3
rotation_calendar:
  - slot_n: 1
    scheduled_date: 2026-07-07
    cluster_id: REPLACE-cluster-1
    status: scheduled
  - slot_n: 2
    scheduled_date: 2026-07-21
    cluster_id: REPLACE-cluster-2
    status: scheduled
  - slot_n: 3
    scheduled_date: 2026-08-04
    cluster_id: REPLACE-cluster-3
    status: scheduled
  - slot_n: 4
    scheduled_date: 2026-08-18
    cluster_id: REPLACE-cluster-4
    status: scheduled
  - slot_n: 5
    scheduled_date: 2026-09-01
    cluster_id: REPLACE-cluster-5
    status: scheduled
  - slot_n: 6
    scheduled_date: 2026-09-15
    cluster_id: REPLACE-cluster-6
    status: scheduled
```

### `templates/_smoke-test.json`

```json
{
  "quarter": "2026-Q3",
  "rotation_calendar": [
    {
      "slot_n": 1,
      "scheduled_date": "2026-07-07",
      "cluster_id": "saas-pricing",
      "status": "scheduled"
    },
    {
      "slot_n": 2,
      "scheduled_date": "2026-07-21",
      "cluster_id": "stripe-ops",
      "status": "scheduled"
    },
    {
      "slot_n": 3,
      "scheduled_date": "2026-08-04",
      "cluster_id": "indie-launch",
      "status": "scheduled"
    }
  ],
  "audit_log": [
    {
      "slot_n": 1,
      "cluster_id": "saas-pricing",
      "started_at": "2026-07-07T09:00:00Z",
      "duration_minutes": 58,
      "fixes_shipped": 4,
      "fixes_deferred": 1
    }
  ],
  "deferred_fixes": [
    {
      "fix_id": "DF-001",
      "logged_at": "2026-07-07",
      "due_date": "2026-08-06",
      "cluster_id": "saas-pricing",
      "status": "open"
    }
  ],
  "retrospective": {}
}
```
