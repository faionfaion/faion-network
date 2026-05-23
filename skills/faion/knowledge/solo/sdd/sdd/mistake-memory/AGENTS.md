---
slug: mistake-memory
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a mistake-memory config (severity + Five Whys \u22653 levels + concrete prevention + pre-task injection) so failures get documented immediately and recurring mistakes auto-promote to CI rules."
content_id: "483a34b280aac178"
complexity: medium
produces: config
est_tokens: 3500
tags: [learning, mistakes, quality-gates, prevention, memory]
---

# Mistake Memory

## Summary

**One-sentence:** Produces a mistake-memory config (severity + Five Whys ≥3 levels + concrete prevention + pre-task injection) so failures get documented immediately and recurring mistakes auto-promote to CI rules.

**Ефективно для:** Solo devs who keep stepping on the same bug every six weeks because the mistakes file is a graveyard, not a guardrail.

**One-paragraph:** Mistakes recur when not documented or when documentation lacks Five-Whys depth. This methodology pins each entry to .aidocs/memory/mistakes.md immediately after failure, requires severity + Five Whys root-cause chain (≥3 levels) + ONE concrete prevention step. Relevant warnings are injected into agent context before similar tasks. Second occurrence triggers automatic CI rule creation. Output is consumed by code-review-cycle and pattern-memory.

## Applies If (ALL must hold)

- Repo has .aidocs/memory/ directory.
- Operator runs SDD loops where pre-task context matters.
- Mistakes recur frequently enough to justify the writeback overhead.
- CI pipeline available for auto-rule creation on second occurrence.

## Skip If (ANY kills it)

- One-shot scripts with no future runs.
- Throwaway experiments where mistakes don't propagate.
- Pre-product phase with no production exposure.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| .aidocs/memory/mistakes.md | markdown | repo |
| Five Whys protocol | spec | team |
| session-start hook | tool config | operator |
| CI auto-rule scaffolding | yaml | engineer |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/pattern-memory` | Sibling — pattern memory captures successes; mistake memory captures failures. |
| `solo/sdd/sdd/engagement-pattern-memory` | Sibling — per-engagement variant for freelancers. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
| `content/04-procedure.xml` | essential | 4 step procedure | ~700 |
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
| `templates/mistake-memory.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/mistake-memory.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-mistake-memory.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[pattern-memory]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[engagement-pattern-memory]] — related methodology.
- [[daily-ship-rubric]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
