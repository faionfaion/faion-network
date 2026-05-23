---
slug: pattern-memory
tier: solo
group: sdd
domain: sdd
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a pattern-memory config (confidence-graduated entries + \u22652 distinct contexts to capture + CLAUDE.md sync at \u22650.8 confidence) so LLM agents apply consistent proven solutions across tasks and projects."
content_id: "e4bad7eff73a0048"
complexity: medium
produces: config
est_tokens: 3500
tags: [pattern-memory, learning, reflexion, agent-memory, knowledge-capture]
---

# Pattern Memory

## Summary

**One-sentence:** Produces a pattern-memory config (confidence-graduated entries + ≥2 distinct contexts to capture + CLAUDE.md sync at ≥0.8 confidence) so LLM agents apply consistent proven solutions across tasks and projects.

**Ефективно для:** Solo devs whose LLM agents keep re-inventing the same regex / retry / migration pattern in different ways because no memory layer carries the win forward.

**One-paragraph:** Patterns evaporate when not captured. This methodology pins .aidocs/memory/patterns.md with a confidence score (0.5 initial → 0.9+ proven), graduated by successful uses. Capture rule: solution works in ≥2 distinct contexts; obvious best-practices and one-off fixes rejected. High-confidence patterns (≥0.8) sync to CLAUDE.md for immediate availability in new sessions. Output is consumed by code-review-cycle and engagement-pattern-memory.

## Applies If (ALL must hold)

- Repo has .aidocs/memory/ directory.
- Operator uses an LLM agent with session-start context.
- Solutions recur across distinct contexts within the codebase.
- Confidence-graduation discipline is realistic at session end.

## Skip If (ANY kills it)

- One-shot scripts with no future reuse.
- Obvious best-practices already enforced by linter.
- Patterns that have worked exactly once — wait for the second context.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| .aidocs/memory/patterns.md | markdown | repo |
| CLAUDE.md sync target | markdown | repo |
| confidence-graduation rule | spec | team |
| session-start hook | tool config | operator |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/sdd/sdd/mistake-memory` | Sibling — mistake memory captures failures; pattern memory captures successes. |
| `solo/sdd/sdd/engagement-pattern-memory` | Variant — per-client scoping for freelancers. |

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
| `templates/pattern-memory.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/pattern-memory.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-pattern-memory.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[mistake-memory]] — related methodology.
- [[engagement-pattern-memory]] — related methodology.
- [[code-review-cycle]] — related methodology.
- [[daily-ship-rubric]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
