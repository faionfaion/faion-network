---
slug: freelancer-positioning-content-calendar
tier: solo
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a 12-month topic rotation matrix tying weekly content slots to niche pillars sourced from real client work — kills the 'what do I post' decision and stabilises the positioning signal.
content_id: "2332d1c9f98c1809"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["freelancer", "positioning", "content-calendar", "marketing", "solo"]
---
# Freelancer Positioning Content Calendar

## Summary

**One-sentence:** Generates a 12-month topic rotation matrix tying weekly content slots to niche pillars sourced from real client work — kills the 'what do I post' decision and stabilises the positioning signal.

**One-paragraph:** Freelancer Positioning Content Calendar produces a spec artefact with named owner, evidence anchors, and explicit gates so the practice survives review. The artefact is the contract — the methodology exists to keep that contract honest. Output: a validated spec ready for downstream automation or human sign-off.

**Ефективно для:**

- Independent freelancer with a defined niche who needs a 12-month topic calendar that turns client work into weekly content without daily decision fatigue.

## Applies If (ALL must hold)

- Freelancer has a declared niche (≥1 pillar identified)
- Active client work that can be the source of stories / case studies
- Commitment to ≥1 published asset per week for the next 12 months

## Skip If (ANY kills it)

- No declared niche yet — run positioning-diff-log first
- No active client work — calendar will starve
- Pure-product founder (not service) — use content-marketing for SaaS instead

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| List of 3-5 positioning pillars | doc | positioning artefact |
| Active client engagement log | table | CRM or notes |
| Publishing channel(s) | list | marketing inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `positioning-diff-log` | Pillars must already exist; this calendar consumes them. |
| `audience-to-customer-funnel` | Content feeds the awareness stage of the funnel. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-pillars-3-to-5, r2-week-mapped-to-pillar, r3-source-from-real-work, r4-publish-cadence-weekly-min, r5-named-owner, r6-quarterly-review | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-freelancer-positioning-content-calendar` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-freelancer-positioning-content-calendar` | haiku | Schema check + threshold checks; deterministic. |
| `review-freelancer-positioning-content-calendar` | opus | Cross-cycle synthesis; high-stakes change to copy / pricing / lifecycle. |

## Templates

| File | Purpose |
|------|---------|
| `templates/freelancer-positioning-content-calendar.json` | JSON skeleton conforming to the output contract schema. |
| `templates/freelancer-positioning-content-calendar.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-freelancer-positioning-content-calendar.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + monthly review. |

## Related

- [[positioning-diff-log]]
- [[audience-to-customer-funnel]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
