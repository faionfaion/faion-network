---
slug: outcome-based-roadmaps
tier: solo
group: product
domain: product
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces an outcome-based roadmap spec (≤3 outcomes per quarter + opportunities → solutions → confidence + No-Date-Promises rule + reviewer cadence)."
content_id: "9903ba7c3a7cfceb"
complexity: medium
produces: spec
est_tokens: 4200
tags: [roadmap, outcomes, product-management, no-dates]
---

# Outcome Based Roadmaps

## Summary

**One-sentence:** Produces an outcome-based roadmap spec (≤3 outcomes per quarter + opportunities → solutions → confidence + No-Date-Promises rule + reviewer cadence).

**Ефективно для:** Solopreneur PMs whose roadmap is a feature gantt with promised dates that miss by 200%, eroding stakeholder trust each cycle.

**One-paragraph:** Feature-gantt roadmaps lock the team to promised dates and lose the optionality that outcomes-first planning preserves. This methodology produces a roadmap built around outcomes (≤3 per quarter), with each outcome carrying opportunities → solutions → confidence levels and a No-Date-Promises rule (delivery windows by month-range, not exact dates). Output is consumed by stakeholder communication + OKR alignment + the launch-tier-decision-frame.

## Applies If (ALL must hold)

- Operator has quarter-bounded planning (≥1 quarter horizon).
- Stakeholders accept outcomes-first framing (not feature commitments).
- Operator can name 1-3 outcomes worth pursuing.
- Operator can publish a public roadmap surface.

## Skip If (ANY kills it)

- Operator forced to promise exact delivery dates (contracts) — use date-bound roadmap instead.
- No instrumented outcomes — outcome-based framing has nothing to anchor.
- Single-product operator with no stakeholders — roadmap is overkill, use OKRs alone.
- Pre-MVP — fix MVP scoping first.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| quarter dates | ISO range | calendar |
| candidate outcomes | array | founder |
| instrumented metrics per outcome | object | analytics |
| public roadmap surface URL | URL | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/product/product-manager/okr-setting` | Upstream — OKRs anchor outcomes. |
| `solo/product/product-manager/continuous-discovery` | Upstream — discovery feeds opportunities. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields, forbidden patterns, allowed transformations | ~800 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |
| `content/04-procedure.xml` | essential | 4 step-by-step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_roadmap_skeleton` | haiku | Template fill outcomes/opportunities. |
| `attach_confidence_per_solution` | sonnet | Bounded judgement on confidence per solution. |
| `stakeholder_comms_synthesis` | opus | Synthesis for stakeholder-facing comms. |

## Templates

| File | Purpose |
|---|---|
| `templates/outcome-based-roadmaps.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/outcome-based-roadmaps.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-outcome-based-roadmaps.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[okr-setting]] — related methodology.
- [[continuous-discovery]] — related methodology.
- [[feature-prioritization-rice]] — related methodology.
- [[outcome-based-roadmaps-advanced]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
