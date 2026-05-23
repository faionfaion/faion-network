---
slug: validation-paralysis-breaker
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a forced-decision validation record (72h budget + ship-or-park verdict + named risk + falsification trigger) so indie hackers exit validation loops in days, not months."
content_id: "ac558cf0a0d5aa33"
complexity: light
produces: decision-record
est_tokens: 2800
tags: [validation-paralysis, forced-decision, indie, ship-discipline]
---

# Validation Paralysis Breaker

## Summary

**One-sentence:** Produces a forced-decision validation record (72h budget + ship-or-park verdict + named risk + falsification trigger) so indie hackers exit validation loops in days, not months.

**Ефективно для:** Indie hackers stuck in eternal validation who keep running 'one more interview' instead of shipping a paying-user test.

**One-paragraph:** The indie-hacker validation paralysis anti-pattern: endless interviews, surveys, and 'just one more landing page' before any user pays. This methodology pins a hard 72-hour validation budget, a named falsification trigger, and a forced ship-or-park verdict at budget end. Output is a decision-record consumed by mvp-scoping and launch-tier-decision-frame.

## Applies If (ALL must hold)

- Operator has been 'validating' for >2 weeks without a paying-user test.
- Hypothesis is testable inside a 3-week tweet-to-launch sprint.
- Operator can write a falsification trigger up-front.
- Tier solo or higher.

## Skip If (ANY kills it)

- Hypothesis requires multi-party / regulated launch.
- Operator hasn't yet articulated a hypothesis — use problem-validation-2026 first.
- Already-paying users exist for an adjacent product — use feature-discovery.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| one-line hypothesis | string | founder |
| falsification trigger statement | string | founder |
| 72h budget start | datetime | operator |
| named risk and mitigation | string | founder |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/problem-validation-2026` | Upstream — provides the hypothesis under test. |
| `solo/product/mvp-scoping` | Downstream — ship verdict triggers MVP scoping. |

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
| `templates/validation-paralysis-breaker.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/validation-paralysis-breaker.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-validation-paralysis-breaker.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[problem-validation-2026]] — related methodology.
- [[mvp-scoping]] — related methodology.
- [[single-interview-fast-loop-template]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
