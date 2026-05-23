---
slug: backlog-hygiene-cron-checklist
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Weekly 15-minute backlog-grooming checklist for a solo PM: stale-item sweep, duplicate merge, priority re-rank, top-10 surfaced, no-list refreshed."
content_id: "12061425ab7d1c60"
complexity: medium
produces: checklist
est_tokens: 4000
tags: [backlog-hygiene-cron-checklist, product, solo, backlog, grooming]
---
# Backlog Hygiene Cron Checklist

## Summary

**One-sentence:** Weekly 15-minute backlog-grooming checklist for a solo PM: stale-item sweep, duplicate merge, priority re-rank, top-10 surfaced, no-list refreshed.

**One-paragraph:** Backlog rot is the silent killer of solo PM productivity: items pile up, duplicates accumulate, priorities decay, and grooming meetings explode from 30 minutes to 3 hours. This methodology pins a 15-minute weekly checklist: (a) close items idle >90 days with no recent comment, (b) merge duplicates, (c) re-rank the top 20, (d) publish the top 10 visible to stakeholders, (e) refresh the anti-roadmap. Run weekly, no exceptions.

**Ефективно для:**

- Solo PM whose backlog has crossed 200 open items.
- Operator who dreads quarterly grooming because the backlog is unmanageable.
- Tech-lead acting as PM with no dedicated grooming time.
- Indie founder who treats the backlog as 'every idea ever'.

## Applies If (ALL must hold)

- Backlog has ≥50 open items.
- PM owns the tracker (Linear / Jira / GitHub Issues).
- Weekly 15-min slot is available on the calendar.
- Top-10 visibility matters for stakeholder alignment.

## Skip If (ANY kills it)

- Backlog has ≤20 items — overhead exceeds benefit.
- PM does not have write access to the tracker.
- Team already runs a working weekly grooming with no rot symptoms.
- Backlog is contractually frozen (audit, compliance).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backlog tracker URL | url | Linear / Jira / GitHub |
| Anti-roadmap reference | doc / page | anti-roadmap-template output |
| Top-10 publication target | channel | team wiki or Slack |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/anti-roadmap-template` | no-list refresh step |
| `solo/product/product-manager` | parent operating context |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-backlog-hygiene-cron-checklist` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/backlog-hygiene-cron-checklist.md` | Markdown skeleton for the checklist artefact, matching content/02-output-contract.xml |
| `templates/backlog-hygiene-cron-checklist.schema.json` | JSON Schema seed + filled fixture for the checklist artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-backlog-hygiene-cron-checklist.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[anti-roadmap-template]]`
- `[[friction-to-backlog]]`
- `[[kill-or-keep-criteria]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
