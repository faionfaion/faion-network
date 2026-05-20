---
slug: solo-time-tracking-discipline
tier: solo
group: pm
domain: project-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "ae36e7f0c639cce6"
summary: Habit-plus-tooling discipline so the solo's billable hours are captured at the moment of work and Friday reconciliation collapses from 2h to 15min.
tags: [time-tracking, freelance, habit, invoicing, automation]
---

# Solo Time Tracking Discipline

## Summary

**One-sentence:** Habit-plus-tooling discipline so the solo's billable hours are captured at the moment of work and Friday reconciliation collapses from 2h to 15min.

**One-paragraph:** Earned Value Management assumes a tracking system exists. Solos start with no system, end up with three (Toggl + a notes file + memory) and reconcile by guessing on Friday afternoon. This methodology forces a single-source-of-truth tool (Timing for macOS auto-track, Toggl Track elsewhere, Wakatime as supplement), a 3-rule capture habit (start at session boundary, label with project+task, stop before context switch), and a Friday-reconciliation script that produces an invoice draft. Output: weekly `TimeReport` with billable_hours, top tasks, write-offs, and an auto-drafted invoice line-items file.

## Applies If (ALL must hold)

- operator bills hourly or has any time-based reporting to clients
- operator has missed ≥ 30min on an invoice in the last 90 days
- operator works on ≥ 2 client projects in parallel
- operator owns a single primary computer (otherwise multi-device sync issues dominate)

## Skip If (ANY kills it)

- operator is on flat-rate retainer and clients don't see time — overhead exceeds value
- operator is value-based pricing with no time component
- operator already runs a clean Toggl + invoicing pipeline — this methodology is for the un-disciplined

## Prerequisites

- list of active projects with client name and billing rate
- chosen tracking tool installed (Timing / Toggl / Clockify / Wakatime)
- a calendar / time-blocking habit that the tool can integrate with
- 7 days of prior tracking data (or willingness to baseline for 1 week)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/pm/project-manager/solo-rate-floor-calculator` | Billable hours feeds the rate-floor input |
| `solo/marketing/conversion-optimizer/solo-lead-qualification-rubric` | Triage time spent on un-qualified leads (write-off bucket) |
| `pro/pm/project-manager/earned-value-management` | Conceptual parent — solos use this lite version |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: single source, capture-at-boundary, label-discipline, write-off-tag, reconciliation cadence | ~900 |
| `content/02-output-contract.xml` | essential | `TimeReport` and invoice-line-items schemas | ~700 |
| `content/03-failure-modes.xml` | essential | 6 modes: multi-tool drift, retro-tracking, untagged gaps, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `gap_detection_from_raw_track` | haiku | Pattern match against calendar |
| `label_inference_for_blocks` | sonnet | Bounded judgment for ambiguous blocks |
| `write_off_classification` | sonnet | Sales/admin/learning categorisation |
| `invoice_draft_assembly` | sonnet | Aggregate by project per rate |

## Templates

| File | Purpose |
|------|---------|
| `templates/time-report.json` | Output schema |
| `templates/invoice-lines.csv` | Invoice line-items export |
| `templates/labels-taxonomy.yaml` | Project/task label conventions |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/friday-reconcile.py` | Pulls weekly data, detects gaps, drafts invoice | Friday end-of-week |
| `scripts/gap-alert.py` | Detects untagged blocks &gt; 30min, prompts label | Daily 17:00 |

## Related

- parent skill: `solo/pm/project-manager/`
- peer methodologies: `solo-rate-floor-calculator`, `solo-lead-qualification-rubric`
- external: [Timing app for macOS](https://timingapp.com/) · [Toggl Track](https://toggl.com/track/) · [Wakatime](https://wakatime.com/) · [Cal Newport — Deep Work / time-block planning](https://www.calnewport.com/books/deep-work/)
