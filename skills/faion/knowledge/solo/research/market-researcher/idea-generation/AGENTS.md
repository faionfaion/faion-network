---
slug: idea-generation
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Seven systematic frameworks (skills inventory, pain mining, job substitution, productized service, unbundling, market stacking, own problems) producing 20–50 scored candidate ideas for downstream niche-evaluation."
content_id: "89b8446cffd1d510"
complexity: medium
produces: report
est_tokens: 4700
tags: [ideation, frameworks, solopreneur, diverge-converge, scoring]
---
# Idea Generation for Solopreneurs

## Summary

**One-sentence:** Seven systematic frameworks (skills inventory, pain mining, job substitution, productized service, unbundling, market stacking, own problems) producing 20–50 scored candidate ideas for downstream niche-evaluation.

**One-paragraph:** Waiting for inspiration produces mode-collapsed output ('AI-powered X', 'task tracker for Y'). This methodology runs seven systematic frameworks in a single ideation session, generating 20–50 raw candidates and scoring the top 10 on a weighted 5-criterion matrix (market 20% / fit 25% / competition 15% / monetization 20% / speed-to-MVP 20%). Diverge-then-converge prevents premature convergence; scoring separation from generation prevents the same agent rationalising its own output.

**Ефективно для:**

- Solopreneur stuck on 'what to build' with skills inventory but no candidates.
- Operator refreshing a stale roadmap quarterly.
- Indie builder whose first three ideas all looked the same.
- Founder running an ideation week before a quarterly planning cycle.

## Applies If (ALL must hold)

- Operator has skills + constraints stated explicitly.
- Need 20–50 raw candidates for downstream niche-evaluation scoring.
- Operator can dedicate ≥2 focused hours to the session.
- There is a downstream scoring step (niche-evaluation or similar).

## Skip If (ANY kills it)

- Operator already has a validated idea with paying customers — skip to pricing-research.
- Generating without skills/constraints input — produces ungrounded lists.
- Scientific or novelty-driven domain — LLMs converge on consensus; use literature-driven discovery.
- Refresh cadence still fresh (last session <14 days).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Skills inventory | list of 8–15 named skills with depth | operator self-assessment |
| Constraints | hours/week, budget, segment, geography | operator brief |
| Pain log | md / Notion | personal observation + audience signals |
| Last ideation session (if any) | md / capture template | research repo |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/research/market-researcher/niche-evaluation` | downstream scoring rubric for top candidates |
| `solo/research/researcher/idea-generation` | sibling researcher-tier ideation; share scoring matrix |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source + skip-this-methodology fallback | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom / root-cause / fix | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~800 |
| `content/05-examples.xml` | essential | One end-to-end worked example | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches → conclusion(ref=rule-id) | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-skip-vs-apply` | sonnet | Decision-tree application requires judgement. |
| `draft-idea-generation` | sonnet | Output drafting needs structure + light judgement. |
| `validate-output` | haiku | Schema validation is mechanical. |

## Templates

| File | Purpose |
|------|---------|
| `templates/idea-generation.md` | Markdown skeleton for the report artefact, matching content/02-output-contract.xml |
| `templates/idea-generation.schema.json` | JSON Schema seed + filled fixture for the report artefact |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-idea-generation.py` | Validate output against the schema in `content/02-output-contract.xml` | CI on each artefact change; pre-commit; `--self-test` in unit run |

## Related

- `[[niche-evaluation]]`
- `[[idea-generation-methods]]`
- `[[pain-point-research]]`

## Decision tree

See `content/06-decision-tree.xml`. The tree starts from a concrete observable signal (applies_if + skip_if check, then the next observable input), routes each branch to a `<conclusion ref="rule-id">` resolved against `content/01-core-rules.xml`. Use it whenever you are unsure whether this methodology applies — the tree always terminates either on an applicable rule or on `skip-this-methodology`.
