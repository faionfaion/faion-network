---
slug: daily-ship-rubric
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a daily-ship rubric (definition of 'shipped today' + 5 binary gates + named owner + 24h checkpoint) so solo SaaS builders exit the SDD spec \u2192 code \u2192 review loop with a real artefact every working day."
content_id: "813738fb0a7ac6b5"
complexity: light
produces: rubric
est_tokens: 2800
tags: [daily-ship, sdd, rubric, solo, ship-discipline]
---

# Daily Ship Rubric

## Summary

**One-sentence:** Produces a daily-ship rubric (definition of 'shipped today' + 5 binary gates + named owner + 24h checkpoint) so solo SaaS builders exit the SDD spec → code → review loop with a real artefact every working day.

**Ефективно для:** Solo SaaS builders whose 'today' keeps ending without a merged commit because the daily ship definition is fuzzy.

**One-paragraph:** What 'shipped today' means for a one-person SaaS is ambiguous; generic quality-gates miss the solo cadence. This methodology pins a daily binary rubric (spec written / code committed / tests green / deploy attempted / customer-visible change) with a 24h checkpoint and a named owner (the operator). Output is consumed by daily review cycles and reflexion learning.

## Applies If (ALL must hold)

- One-person SaaS with daily commit cadence as the goal.
- Operator runs the SDD spec → vibe-code → review loop daily.
- Output will be reviewed by the operator at end of day.
- Tier solo or higher.

## Skip If (ANY kills it)

- Multi-person team — generic quality-gates apply.
- Research/exploration days where no ship is expected.
- Calendar-blocked maintenance days where rubric overhead exceeds value.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| named operator | string | single human |
| backlog item under work | task id | backlog |
| deployment target reachable | url/host | infra |
| test suite that runs in <5 min | ci config | engineer |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/sdd-workflow-overview` | Parent — daily rubric is a checkpoint within the SDD loop. |
| `solo/sdd/sdd/pattern-memory` | Sibling — daily-ship outcomes feed pattern memory. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
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
| `templates/daily-ship-rubric.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/daily-ship-rubric.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-daily-ship-rubric.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[pattern-memory]] — related methodology.
- [[mistake-memory]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[engagement-pattern-memory]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
