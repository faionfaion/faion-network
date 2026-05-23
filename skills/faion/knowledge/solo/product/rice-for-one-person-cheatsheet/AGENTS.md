---
slug: rice-for-one-person-cheatsheet
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: RICE reweighted for solo SaaS: Reach in absolute small-number users (80 is signal), Effort in dev-days for one person, Confidence collapsed to 3 levels, and WIP-1 framing — the top of the list is the ONLY bet of the week.
content_id: "3c12d266af805e7f"
complexity: light
produces: rubric
est_tokens: 2900
tags: [product, solo, rice, prioritization, wip-1, sunday-roadmap]
---
# Rice For One Person Cheatsheet

## Summary

**One-sentence:** RICE reweighted for solo SaaS: Reach in absolute small-number users (80 is signal), Effort in dev-days for one person, Confidence collapsed to 3 levels, and WIP-1 framing — the top of the list is the ONLY bet of the week.

**One-paragraph:** RICE reweighted for solo SaaS: Reach in absolute small-number users (80 is signal), Effort in dev-days for one person, Confidence collapsed to 3 levels, and WIP-1 framing — the top of the list is the ONLY bet of the week. The methodology pins the artefact: a fixed shape, a named owner, evidence anchors, and a published review cadence. It is loaded when the role named in the trigger starts the block and produces a committed artefact reviewed against outcomes at the next iteration.

**Ефективно для:**

- Operators who run Rice For One Person Cheatsheet on a recurring cadence and need a reviewable operating tool.
- Solo founders who need a defensible artefact for stakeholder pressure.
- Teams syncing outcome work across PM, design, and engineering.
- Audit / review surface: every artefact has an owner, evidence anchors, and a decay date.

## Applies If (ALL must hold)

- Solo SaaS operator running a Sunday roadmap ritual.
- Active user base ≥10 but <10k (solo scale).
- One operator wears all four roles (PM, design, eng, support).
- Confidence judgements span discovery / metrics / gut at different fidelity.

## Skip If (ANY kills it)

- Team of ≥3 — use full RICE.
- Reach ≥10k — solo cheat sheet undercounts.
- Multi-stream operator with formal product board — use OKR cascade.
- Pre-launch — no reach to ground on.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Backlog of candidate bets | list | Linear / Notion |
| Active-user count (small-N) | integer | Analytics |
| Effort estimate per bet (dev-days) | number | Self |
| Confidence level (3pt) | high/med/low | Evidence |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-operations/feature-prioritization-rice` | Parent RICE; this is the solo-reweighted variant. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-rice-for-one-person-cheatsheet` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-rice-for-one-person-cheatsheet` | haiku | Schema check + threshold checks; deterministic. |
| `review-rice-for-one-person-cheatsheet` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/rice-for-one-person-cheatsheet.json` | JSON skeleton conforming to the output contract schema. |
| `templates/rice-for-one-person-cheatsheet.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rice-for-one-person-cheatsheet.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[feature-prioritization-rice]]
- [[rfc-lite-pm-template]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
