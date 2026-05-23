---
slug: solo-time-tracking-discipline
tier: solo
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
content_id: "ae36e7f0c639cce6"
summary: Single-source-of-truth time-tracking habit + Friday reconciliation script that collapses invoicing from 2h to 15min and surfaces billable %, write-offs, gaps.
complexity: medium
produces: report
est_tokens: 4500
tags: [time-tracking, freelance, habit, invoicing, automation]
---

# Solo Time Tracking Discipline

## Summary

**One-sentence:** Single-source-of-truth tracker + 3-rule capture habit + Friday-16:00 reconciliation script that emits a weekly TimeReport and invoice draft for a solo operator.

**One-paragraph:** Earned Value Management assumes a tracking system exists; solos start with three (Toggl + a notes file + memory) and reconcile by guessing on Friday afternoon. This methodology forces one source-of-truth tool (Timing for macOS auto-track, Toggl elsewhere; Wakatime is signal not source), a 3-rule capture habit (start at session boundary, label with project+task from a closed taxonomy, stop before context switch), a write-off taxonomy (SALES / ADMIN / LEARNING / UNBILLABLE-REWORK / BREAK), and a Friday-reconciliation script that produces a TimeReport with billable_pct_actual + invoice draft.

**Ефективно для:**

- Solo billing hourly across ≥2 client projects.
- Solo who missed ≥30 min on a recent invoice or routinely rounds down.
- Calibrating billable_pct for the rate-floor calculator.
- Surfacing which write-off category eats the most non-billable time.

## Applies If (ALL must hold)

- Operator bills hourly or has any time-based reporting to clients.
- Operator has missed ≥30min on an invoice in the last 90 days OR multi-project drift exists.
- Operator works on ≥2 client projects in parallel.
- Operator owns a single primary computer (multi-device adds drift class).

## Skip If (ANY kills it)

- Operator is on flat-rate retainer and clients don't see time — overhead exceeds value.
- Operator is value-based pricing with no time component.
- Operator already runs a clean Toggl + invoicing pipeline.
- Pre-product solo with no clients — wait until billable work exists.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Active projects + billing rate | table | operator |
| Tracking tool installed (Timing / Toggl / Clockify) | app | operator |
| Labels taxonomy (project + task closed lists) | YAML | operator |
| Friday-16:00 calendar block | calendar | operator |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[solo-rate-floor-calculator]] | billable_pct_actual feeds the rate-floor recalibration. |
| [[reporting-dashboards]] | Weekly invoice draft can flow into a leadership digest. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: single source, capture-at-boundary, label discipline, write-off taxonomy, Friday cadence | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for TimeReport + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 6 modes: multi-tool drift, retro-track fabrication, inference hallucination, write-off creep, Friday drift, round-down loss | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure: capture → reconcile → label gaps → write-off classify → emit invoice draft | ~800 |
| `content/05-examples.xml` | essential | Worked example: 24h tracked week with 4 projects → invoice | ~700 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gap_detection_from_raw_track` | haiku | Pattern match against calendar. |
| `label_inference_for_blocks` | sonnet | Bounded judgement for ambiguous blocks. |
| `write_off_classification` | sonnet | Sales/admin/learning categorisation. |
| `invoice_draft_assembly` | sonnet | Aggregate by project per rate. |

## Templates

| File | Purpose |
|------|---------|
| `templates/time-report.json` | TimeReport output skeleton |
| `templates/invoice-lines.csv` | Invoice line-items export |
| `templates/labels-taxonomy.yaml` | Project/task closed label list |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-solo-time-tracking-discipline.py` | Validate TimeReport against 02-output-contract schema | Friday end-of-week before invoice send |

## Related

- [[solo-rate-floor-calculator]]
- [[solo-context-switch-protocol]]
- [[solo-burnout-tripwires]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes by source-of-truth count, capture-at-boundary state, label completeness, write-off mix, and Friday-cadence observance onto a rule from `content/01-core-rules.xml`. Walk it before every Friday reconciliation.
