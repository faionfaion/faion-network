---
slug: agency-acquisition-prep
tier: pro
group: product
domain: product-operations
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Concrete operating checklist covering agency acquisition prep — the small set of items a practitioner runs every cycle so nothing high-leverage gets skipped.
content_id: "1335c93c60356c4f"
tags: [agency, checklist, product]
---
# Agency Acquisition Prep

## Summary

**One-sentence:** Concrete operating checklist covering agency acquisition prep — the small set of items a practitioner runs every cycle so nothing high-leverage gets skipped.

**One-paragraph:** Concrete operating checklist covering agency acquisition prep — the small set of items a practitioner runs every cycle so nothing high-leverage gets skipped. There is no exit methodology anywhere in the corpus. For pro-tier buyers ($35/mo, 1–3 person, $100K/mo), exit is real and 3–5 years out. Methodology should cover: founder-dependency reduction, deal lane choice, buyer outreach, basic LOI hygiene, due-diligence prep. Without it, the corpus implicitly tells founders to run forever.

## Applies If (ALL must hold)

- You operate the recurring activity addressed by agency acquisition prep at least once per cycle (weekly, sprint, quarter, or annual).
- You have authority to act on each item — checklist items without owners or budget are deferred.
- Skipped items must be auditable: a written reason replaces the action.
- Time-box: full pass completes within the cycle window (e.g., 30-90 min for weekly, 1-2 days for annual).

## Skip If (ANY kills it)

- One-off events with no recurrence — checklist value is in the rhythm.
- Activities without a named owner — items will not be done, only ticked.
- Teams running a more granular checklist already — adding a meta-layer creates conflict.

## Prerequisites

- Calendar slot dedicated to the cycle (recurring meeting / focus block).
- Read-access to the source systems each item inspects (analytics, billing, repo).
- Last cycle's output filed where current cycle can compare year-over-year.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-operations/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `checklist_dry_run` | haiku | Template walk, no judgment needed |
| `anomaly_flag` | sonnet | Compare current cycle vs prior, flag deltas |
| `decision_synthesis` | opus | Consolidate flags into a corrective-action list |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/product/product-operations/`
- peer methodologies: see siblings under `pro/product/product-operations/`
- external: industry references cited inline in `content/01-core-rules.xml`
