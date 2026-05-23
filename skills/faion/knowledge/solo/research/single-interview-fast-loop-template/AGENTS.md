---
slug: single-interview-fast-loop-template
tier: solo
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Produces a single-interview fast-loop spec (30-min prep + 60-min interview + 60-min synthesis inside 36h, anchored to one decision) so single-shot interviews compound into evidence instead of evaporating."
content_id: "ab841df023411c5b"
complexity: light
produces: spec
est_tokens: 3400
tags: [single-interview, fast-loop, research, solo, synthesis]
---

# Single Interview Fast Loop Template

## Summary

**One-sentence:** Produces a single-interview fast-loop spec (30-min prep + 60-min interview + 60-min synthesis inside 36h, anchored to one decision) so single-shot interviews compound into evidence instead of evaporating.

**Ефективно для:** Solo PMs and founders who keep landing one-off interview slots that should produce evidence but instead get lost in the inbox.

**One-paragraph:** Existing interview playbooks assume batch studies. PMs and solo founders increasingly run one interview when the opportunity appears — a churned customer, a discovery call, a power user with 30 free minutes. This methodology pins a tight prep (one hypothesis + 5 must-asks + one decision the interview informs) and a hard 24-hour synthesis deadline so the learning lands while context is hot. Output is consumed by problem-validation-2026 and the broader user-interviews insight ledger.

## Applies If (ALL must hold)

- Exactly one interview opportunity (no batch study).
- There is a specific decision or hypothesis this interview should inform.
- Interviewer can commit 30 min prep + 60 min interview + 60 min synthesis inside ~36 hours.
- Tier solo or higher.

## Skip If (ANY kills it)

- Batch study (≥4 interviews planned) — use user-interviews instead.
- No decision attached — the interview is small-talk, not research.
- Synthesis cannot land inside 36h — the loop's compounding value dies.

## Prerequisites

| Artefact | Format | Source |
|---|---|---|
| one hypothesis or decision | string | PM |
| 5 must-ask questions | list | researcher |
| interview slot confirmed | calendar | operator |
| synthesis template ready | markdown | researcher |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `solo/research/researcher/user-interviews` | Parent — single loop is a degenerate case of the batch loop. |
| `solo/research/researcher/problem-validation-2026` | Downstream — single-loop insights feed the evidence ledger. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema fields + forbidden patterns + transformations + valid/invalid examples | ~800 |
| `content/03-failure-modes.xml` | essential | 3 failure modes with detector + repair | ~800 |
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
| `templates/single-interview-fast-loop-template.json` | JSON Schema for the output contract (machine-validatable). |
| `templates/single-interview-fast-loop-template.md` | Markdown skeleton with the required fields. |
| `templates/_smoke-test.json` | Minimum viable filled-in fixture passing the schema. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-single-interview-fast-loop-template.py` | Enforce the output contract from `content/02-output-contract.xml`. | After the subagent returns an artefact, before downstream consumer reads. |

## Related

- [[user-interviews]] — related methodology.
- [[problem-validation-2026]] — related methodology.
- [[validation-paralysis-breaker]] — related methodology.

## Decision tree

Lives at `content/06-decision-tree.xml`. The tree gates whether to apply the methodology at all (preconditions present? required inputs present?) and routes the decision into either 'run-it' (produce the artefact per output contract) or 'skip-it' (defer, naming the missing precondition).
