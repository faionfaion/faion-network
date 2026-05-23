---
slug: roadmap-design
tier: solo
group: product
domain: product
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Design an outcome-based roadmap with Now/Next/Later horizons, explicit confidence per item, and quarterly review cadence so the roadmap becomes a steering tool instead of a wishlist.
content_id: "00bde11348cb1c2d"
complexity: medium
produces: spec
est_tokens: 4200
tags: ["roadmap", "now-next-later", "outcomes", "planning", "confidence"]
---
# Roadmap Design

## Summary

**One-sentence:** Design an outcome-based roadmap with Now/Next/Later horizons, explicit confidence per item, and quarterly review cadence so the roadmap becomes a steering tool instead of a wishlist.

**One-paragraph:** Replaces feature lists with outcome statements per horizon. Now items carry committed scope + owner; Next items carry hypotheses + dependencies; Later items carry bets + open questions. Confidence labels (high/medium/low) prevent the document from being read as a contract.

**Ефективно для:**

- Solo founder or small-team PM whose roadmap doc drifts every 2 weeks; needs a structure that holds shape under reprioritisation without lying about commitments.

## Applies If (ALL must hold)

- Multi-stakeholder product where alignment beats individual feature scope.
- Quarterly planning cadence exists or is being established.
- Roadmap will be shared externally or with non-PM stakeholders.

## Skip If (ANY kills it)

- Single-developer 1-week scope where a plain task list is sufficient.
- Pre-product phase where there are no users to align with.
- Stable maintenance product with no strategic direction.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Strategic outcomes / OKRs | markdown | Strategy doc |
| Confidence rubric | table | PM doc |
| Audience list for the roadmap (internal/external) | list | CRM / team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/product/product-planning/okr-setting` | Outcomes anchor the roadmap horizons. |
| `solo/product/product-operations/feature-prioritization-rice` | Within-horizon ranking when items contend. |

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
| `draft-roadmap-design` | sonnet | Per-instance judgement on the artefact; bounded inputs. |
| `validate-roadmap-design` | haiku | Schema check + threshold checks; deterministic. |
| `review-roadmap-design` | opus | Cross-cycle synthesis; high-stakes change to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/roadmap-design.json` | JSON skeleton conforming to the output contract schema. |
| `templates/roadmap-design.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-roadmap-design.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[okr-setting]]
- [[feature-prioritization-rice]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
