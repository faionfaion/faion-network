---
slug: agency-pipeline-hygiene-15min
tier: pro
group: pm
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: 15-minute Monday pipeline hygiene — 5-item checklist forcing every opp to have stage, close date, next step + owner, with loss/source tagging for closed deals.
content_id: "e402b2deab859e92"
complexity: medium
produces: checklist
est_tokens: 3500
tags: [agency, pipeline, sales, checklist, weekly]
---
# Agency Pipeline Hygiene 15min

## Summary

**One-sentence:** 15-minute Monday pipeline hygiene — 5-item checklist forcing every opp to have stage, close date, next step + owner, with loss/source tagging for closed deals.

**One-paragraph:** Pipelines rot when nobody enforces hygiene: opps without close dates accumulate, lost opps lack reasons, sources untagged. This methodology pins a 15-minute Monday checklist (5 items) plus a ledger row appended weekly. Output: a clean CRM state and a trend ledger that surfaces sales-cycle drift. Designed for founders who hate 'doing sales' but need a usable pipeline.

**Ефективно для:**

- Agency founders running their own sales pipeline.
- Agencies with >5 active opps where one bad week of hygiene loses signal.
- Sales-led growth without dedicated SDR/AE.
- Owners using a CRM (Notion / HubSpot / Pipedrive) with stage-date fields.

## Applies If (ALL must hold)

- Owner controls the CRM.
- Pipeline has stage + close-date fields.
- Monday slot is calendar-protected.
- ≥5 opps actively in the funnel.

## Skip If (ANY kills it)

- Agency with dedicated sales team — different cadence applies.
- Bookings-driven (inbound-only) model — pipeline hygiene mismatch.
- Owner has no CRM yet — adopt CRM first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Prior-period output | MD / CSV | agency |
| Current pipeline / roadmap | list | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `stakeholder-engagement` | Engagement of partners / sponsors anchors the artefact. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules — 15-min cap, 5 items, hot-opp next-step, loss enum, source enum | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for the agency-pipeline-hygiene-15min artefact | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 700 |
| `content/06-decision-tree.xml` | essential | Decision tree mapping artefact state to a rule | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-artefact` | haiku | Template fill from prior-period output. |
| `fill-evidence` | sonnet | Select correct evidence per row. |
| `synthesise-decisions` | opus | Cross-period synthesis for corrective decisions. |

## Templates

| File | Purpose |
|------|---------|
| `templates/monday-checklist.md` | 5-item pipeline hygiene checklist. |
| `templates/ledger.md` | Weekly pipeline ledger row. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-agency-pipeline-hygiene-15min.py` | Schema-validate artefact JSON. | Pre-commit + before review. |

## Related

- [[agency-pnl-tracker-template]]
- [[agency-annual-plan-template]]
- [[agency-cash-flow-friday-routine]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals from the agency-pipeline-hygiene-15min input (precondition checks, scale thresholds, evidence presence) to a concrete action, with each leaf referencing a rule id from `01-core-rules.xml`. Consult it whenever the methodology could branch based on context.
