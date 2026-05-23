---
slug: value-proposition-design
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a value-proposition-canvas spec (customer profile jobs/pains/gains + value map relievers/creators + alignment-gap list) so positioning is anchored on evidence, not adjective stacking."
content_id: "572024187cf4be1c"
complexity: medium
produces: spec
est_tokens: 4100
tags: [value-proposition, positioning, canvas, customer-research, product-market-fit]
---

# Value Proposition Design

## Summary

**One-sentence:** Produces a value-proposition-canvas spec (customer profile jobs/pains/gains + value map relievers/creators + alignment-gap list) so positioning is anchored on evidence, not adjective stacking.

**Ефективно для:** Solo founders whose pitch deck still describes 'faster, easier, better' instead of named customer jobs.

**One-paragraph:** Value propositions written without explicit customer-jobs anchoring drift to adjective stacking. This methodology pins each value-prop draft to Osterwalder's two-sided canvas: customer profile (jobs / pains / gains) on one side, value map (products / pain-relievers / gain-creators) on the other, with an explicit alignment-gap list for every mismatch. Output is consumed by launch-comms-kit and positioning iterations.

## Applies If (ALL must hold)

- Pre-launch positioning needs grounding in customer language.
- Pivoting positioning after low conversion or message rejection.
- Adjacent-segment expansion needs a fresh value map.
- Pitch deck or landing page draft missing customer-job anchor.

## Skip If (ANY kills it)

- When no customer interviews are accessible — canvas without evidence is fiction.
- Commodity products competing on price only.
- Internal tools with one captive user base.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| customer interview transcripts | files | user-interviews output |
| current product feature list | array | PM |
| competitor positioning grid | spec | researcher |
| draft value-prop statement (if any) | string | founder |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Upstream — interview data feeds the customer profile. |
| `solo/research/researcher/jobs-to-be-done` | Upstream — JTBD output feeds the 'jobs' field. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~600 |
| `content/06-decision-tree.xml` | essential | Run-or-skip gate + branching to rule-id conclusions | ~300 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| `draft_artefact` | haiku | Template fill from prereqs. |
| `audit_against_rules` | sonnet | Bounded judgement: do outputs satisfy 01-core-rules? |
| `final_sign_off` | opus | Synthesis at the gate before downstream handoff. |

## Templates

| File | Purpose |
|---|---|
| `templates/value-proposition-design.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/value-proposition-design.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-value-proposition-design.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[user-interviews]] — related methodology.
- [[problem-validation-2026]] — related methodology.
- [[jobs-to-be-done]] — related methodology.
- [[use-case-mapping]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
