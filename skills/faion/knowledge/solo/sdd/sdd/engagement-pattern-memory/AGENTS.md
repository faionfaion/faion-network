---
slug: engagement-pattern-memory
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a per-engagement memory file (repo conventions + reviewer preferences + deploy quirks + recurring traps + glossary + resolved questions) so freelancers juggling multiple clients don't re-learn each one every session."
content_id: "6cb3b0a1171bfa13"
complexity: light
produces: config
est_tokens: 2800
tags: [memory, freelance, client-engagement, pattern-memory, repo-conventions]
---

# Engagement Pattern Memory

## Summary

**One-sentence:** Produces a per-engagement memory file (repo conventions + reviewer preferences + deploy quirks + recurring traps + glossary + resolved questions) so freelancers juggling multiple clients don't re-learn each one every session.

**Ефективно для:** Freelancers with 2-3 active clients who keep spending the first hour of every session re-learning what they already knew last week.

**One-paragraph:** Generic pattern-memory leaks one client's conventions into another. This methodology pins a per-engagement memory file (one per active client / repo) updated after each session with structured sections (repo conventions, reviewer preferences, deploy quirks, recurring traps, glossary, resolved questions). Files are versioned, indexed, and surfaced to the LLM agent on session start. Output is consumed by daily-ship-rubric and pattern-memory.

## Applies If (ALL must hold)

- Contractor / freelancer with ≥2 active engagements.
- Each engagement has distinct repo conventions or reviewer preferences.
- Operator uses an LLM agent where pre-session context matters.
- Memory write discipline is realistic (10-15 min at session end).

## Skip If (ANY kills it)

- Single-client operator — generic pattern-memory suffices.
- Engagements with identical conventions — no separation value.
- Operator already maintains per-client docs elsewhere with no LLM gap.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| list of active engagements | array | operator |
| memory file location convention | path | operator |
| session-start hook | tool config | operator |
| session-end discipline | habit | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/pattern-memory` | Parent — engagement memory is a per-client variant. |
| `solo/sdd/sdd/mistake-memory` | Sibling — engagement-scoped mistakes feed back into client memory. |

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
| `templates/engagement-pattern-memory.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/engagement-pattern-memory.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-engagement-pattern-memory.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[pattern-memory]] — related methodology.
- [[mistake-memory]] — related methodology.
- [[daily-ship-rubric]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
