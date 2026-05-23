---
slug: reflexion-learning
tier: solo
group: sdd
domain: sdd
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Reflexion verbal reinforcement loop: after each SDD iteration the agent writes a structured episodic note (failure, root cause, corrective rule), appends it to memory, and the next iteration consumes it as a hard prompt constraint — no weight updates required.
content_id: "1fdb37776dcbcf80"
complexity: medium
produces: report
est_tokens: 3600
tags: [reflexion, verbal-rl, memory-architecture, sdd, pdca]
---
# Reflexion Learning

## Summary

**One-sentence:** Reflexion verbal reinforcement loop: after each SDD iteration the agent writes a structured episodic note (failure, root cause, corrective rule), appends it to memory, and the next iteration consumes it as a hard prompt constraint — no weight updates required.

**One-paragraph:** Reflexion verbal reinforcement loop: after each SDD iteration the agent writes a structured episodic note (failure, root cause, corrective rule), appends it to memory, and the next iteration consumes it as a hard prompt constraint — no weight updates required. The methodology pins the artefact: a JSON episode with fixed schema, indexed by attempt number, with explicit corrective_rule that the next attempt MUST honour.

**Ефективно для:**

- Long-running SDD loops where the same class of mistake repeats across attempts.
- Solo agents that lack a separate reward signal and need a textual proxy for feedback.
- Pipelines that must survive context resets — episodes are durable, model weights are not.
- Audit surface: every failed attempt has a written reason and a corrective rule.

## Applies If (ALL must hold)

- An iterative agent loop attempts the same task ≥2 times.
- Each attempt produces an evaluable signal (test pass/fail, validator output, reviewer note).
- There is somewhere durable to store episodes (filesystem, DB) across attempts.

## Skip If (ANY kills it)

- Single-shot task with no retry budget.
- No evaluable signal; reflexion needs ground truth to write episodes against.
- Memory store is volatile or wiped between attempts — episodes will not survive.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Attempt result | json | Validator / test runner |
| Memory store path | filesystem path | Pipeline config |
| Original task brief | markdown | Caller |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/sdd/sdd/quality-gates-confidence` | Provides the pass/fail signal Reflexion writes episodes against. |

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
| `draft-reflexion-learning` | sonnet | Per-instance judgement; bounded inputs. |
| `validate-reflexion-learning` | haiku | Schema check + threshold checks; deterministic. |
| `review-reflexion-learning` | opus | Cross-cycle synthesis; high-stakes changes to policy / cadence. |

## Templates

| File | Purpose |
|------|---------|
| `templates/reflexion-learning.json` | JSON skeleton conforming to the output contract schema. |
| `templates/reflexion-learning.md` | Markdown skeleton for human-readable artefact rendering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-reflexion-learning.py` | Validates a filled artefact JSON against the output-contract schema. | Pre-merge + scheduled review. |

## Related

- [[quality-gates-confidence]]
- [[sdd-workflow-overview]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable inputs to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip and which rule path applies.
