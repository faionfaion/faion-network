---
slug: founder-led-qualification-rubric
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Yes/no qualification rubric for founder-led sales — 5 binary checks (budget, authority, need, timeline, fit) gate every proposal cycle and prevent overqualification.
content_id: "founder-qual-1"
complexity: medium
produces: rubric
est_tokens: 3000
tags: [sales, qualification, bant, founder-led, rubric]
---
# Founder Led Qualification Rubric

## Summary

**One-sentence:** Yes/no qualification rubric for founder-led sales — 5 binary checks (budget, authority, need, timeline, fit) gate every proposal cycle and prevent overqualification.

**One-paragraph:** Founders without sales background overqualify, spending weeks on prospects who never close. This rubric forces 5 binary yes/no checks before proposal effort begins: budget confirmed (numeric), authority (decision-maker contacted), need (specific pain articulated), timeline (start date ≤ 90d), fit (ICP match). Core rules: every check is binary with evidence cited; 3+ no's auto-disqualifies; ambiguous checks default to no; results feed pipeline + kill-rule; weekly review batch-applies the rubric.

**Ефективно для:**

- Founder-led sales — overqualification protection.
- Pipeline reviewer — uniform qualification across deals.
- Inbound triage — 60-second decision before deeper effort.
- Agency lead — same rubric applied across multiple prospects.

## Applies If (ALL must hold)

- Founder or team-of-one runs sales without a dedicated SDR/AE.
- ≥3 new prospects/week reach the proposal-readiness stage.
- Authority to disqualify deals exists at the rubric runner's level.
- An ICP doc exists or can be drafted (1-page).

## Skip If (ANY kills it)

- Mature sales team with their own qualification framework (MEDDIC, BANT formal).
- Tiny inbound volume (&lt;1/week) — manual qualification fine.
- Sales cycle &gt;12 months where 90-day timeline check is too tight.
- No ICP defined — fix ICP first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| ICP doc (1 page) | doc | growth team |
| Inbound queue with discovery notes | CRM / table | CRM |
| Budget threshold + ACV target | spec | founder |
| Disqualification log (prior quarter) | report | own ops |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[founder-deal-kill-rule]] | Downstream — disqualifies feed kill batch. |
| [[freelance-pilot-pricing]] | Pilot pricing covers the 'no budget yet' bucket. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: five-binary-checks, evidence-per-check, three-no-auto-disqualify, ambiguous-defaults-no, weekly-batch-application | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for rubric + valid/invalid | 800 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure | 600 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `apply-checks` | sonnet | Per-check evidence judgment. |
| `log-batch` | haiku | Template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/qualification-rubric.json` | JSON example of one qualification run |
| `templates/rubric-card.md` | Markdown skeleton for one qualification card |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-founder-led-qualification-rubric.py` | Validate one rubric JSON against the schema | After draft, before publish |

## Related

- [[founder-deal-kill-rule]]
- [[freelance-pilot-pricing]]
- [[proposal-from-discovery-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree routes observable signals to one of the rules in `01-core-rules.xml`. Use it before producing the output — picking the wrong branch is the most common failure.
