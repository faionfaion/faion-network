---
slug: micro-mvps
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Ship a Micro-MVP (≤5 dev-days, 1 risk tested, 1 segment, hard kill threshold) per cycle to learn-or-die rather than build-and-hope.
content_id: "a6b66c6dd95e0167"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["micro-mvp", "ship-fast", "learning", "kill-threshold", "solo"]
---
# Micro-MVPs

## Summary

**One-sentence:** Ship a Micro-MVP (≤5 dev-days, 1 risk tested, 1 segment, hard kill threshold) per cycle to learn-or-die rather than build-and-hope.

**One-paragraph:** A Micro-MVP is the shippable unit of solo-founder learning: 5 days max, one segment, one assumption tested, one kill threshold. The methodology turns 'we'll iterate' (vague) into 'we'll ship 8 of these per quarter' (concrete). Failure modes are baked in: each Micro-MVP carries its kill criterion.

**Ефективно для:**

- Solo founder whose last 3 'iterations' took 6+ weeks each with no learning at the end — needs a forcing function for 1-week cycles with a binary learn/no-learn outcome.

## Applies If (ALL must hold)

- Discovery output points to 1+ riskiest assumption.
- ≤5 dev-days available for the test.
- Audience segment of ≥10 reachable users exists.

## Skip If (ANY kills it)

- Compliance / contractual scope blocks 5-day cuts.
- Risk requires production-grade infrastructure to test.
- Founder cannot recruit ≥10 testers in the segment.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Riskiest assumption + segment | markdown | Discovery / continuous-discovery |
| ≤5 dev-day capacity | estimate | Plan |
| Test recruit list (≥10) | csv | CRM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/micro-mvp-cut-rubric` | Rubric that cuts scope down. |
| `solo/product/product-manager/product-discovery` | Source of the riskiest assumption. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 testable rules + skip + run rules | 800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | Step-by-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes observable inputs to a rule id in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-micro-mvps` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-micro-mvps` | haiku | Schema check + threshold checks; deterministic. |
| `review-micro-mvps` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/micro-mvps.json` | JSON skeleton conforming to the output contract schema. |
| `templates/micro-mvps.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-micro-mvps.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[micro-mvp-cut-rubric]]
- [[product-discovery]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
