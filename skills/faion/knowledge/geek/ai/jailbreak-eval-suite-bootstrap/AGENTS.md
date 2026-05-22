---
slug: jailbreak-eval-suite-bootstrap
tier: geek
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "083aacd9617d37e9"
summary: "Jailbreak Eval Suite Bootstrap — testable methodology for LLM-agent design, evals, safety, cost. `behavioral-evals-adversarial` exists as a playbook but doesn't ship a baseline attack suite. P7 needs a starter library (DAN-family, role-play-escape, encoded-prompt, tool-confusion, persona-jailbreak) with scoring rubric. Without a baseline, every agent buil..."
tags: [ai, geek, methodology]
---
# Jailbreak Eval Suite Bootstrap

## Summary

**One-sentence:** Jailbreak Eval Suite Bootstrap — testable methodology for LLM-agent design, evals, safety, cost. `behavioral-evals-adversarial` exists as a playbook but doesn't ship a baseline attack suite. P7 needs a starter library (DAN-family, role-play-escape, encoded-prompt, tool-confusion, persona-jailbreak) with scoring rubric. Without a baseline, every agent buil...

**One-paragraph:** Jailbreak Eval Suite Bootstrap closes a known gap in ai practice: `behavioral-evals-adversarial` exists as a playbook but doesn't ship a baseline attack suite. P7 needs a starter library (DAN-family, role-play-escape, encoded-prompt, tool-confusion, persona-jailbreak) with scoring rubric. Without a baseline, every agent builder writes their own from scratch. The methodology is anchored to the recurring activity 'Harden an agent against prompt injection and jailbreak across tool boundaries (role: p7-llm-agent-developer)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Harden an agent against prompt injection and jailbreak across tool boundaries (role: p7-llm-agent-developer)' shows up in the user's workload at least once per cycle.
- The operator has authority to act on the artefact this methodology produces (write access, sign-off rights).
- A named consumer exists for the output — either a human reviewer or a downstream agent.
- An auditable source-of-truth is available for the inputs this methodology requires.

## Skip If (ANY kills it)

- One-off, never-to-repeat work — methodology overhead does not pay back.
- No named consumer — the artefact will be orphaned regardless of quality.
- Cannot access the input source-of-truth (system down, access denied) — paraphrased substitutes are worse than skipping.

## Prerequisites

- Read access to the systems, dashboards, or transcripts that feed the methodology's inputs.
- A storage location for the produced artefact (git repo, doc, ticket) where the consumer can read it.
- Prior cycle's artefact (if any) accessible for carry-forward and trend comparison.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/AGENTS.md` | Parent group context (vocabulary, neighbouring methodologies) |
| `geek/sdd/AGENTS.md` if present | SDD discipline for the artefact lifecycle (status flow, owners, review) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 3-5 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 4-8 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `jailbreak_eval_suite_bootstrap_template_fill` | haiku | Template fill, no judgement |
| `jailbreak_eval_suite_bootstrap_evidence_check` | sonnet | Bounded comparison + judgement |
| `jailbreak_eval_suite_bootstrap_synthesis` | opus | Cross-input synthesis + final write-up |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `geek/ai/` (see neighbouring methodologies)
- triggering activity: `Harden an agent against prompt injection and jailbreak across tool boundaries (role: p7-llm-agent-developer)`
- external: industry references cited inline in `content/01-core-rules.xml`
