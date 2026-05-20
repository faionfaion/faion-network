---
slug: human-in-the-loop-pattern-catalog
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "0cd8e3b7f323c314"
summary: "Human In The Loop Pattern Catalog — testable methodology for LLM-agent design, evals, safety, cost. Patterns for HITL: pre-action confirm, post-action review, sampled audit, escalation on uncertainty. ml-engineer/agents-safety-guardrails is too abstract."
tags: [ai, geek, methodology]
---
# Human In The Loop Pattern Catalog

## Summary

**One-sentence:** Human In The Loop Pattern Catalog — testable methodology for LLM-agent design, evals, safety, cost. Patterns for HITL: pre-action confirm, post-action review, sampled audit, escalation on uncertainty. ml-engineer/agents-safety-guardrails is too abstract.

**One-paragraph:** Human In The Loop Pattern Catalog closes a known gap in ai practice: Patterns for HITL: pre-action confirm, post-action review, sampled audit, escalation on uncertainty. ml-engineer/agents-safety-guardrails is too abstract. The methodology is anchored to the recurring activity 'Agentic AI feature MVP to GA (role: role-ml-engineer)' and produces an auditable artefact that a downstream agent or human reviewer can sign off without re-deriving the reasoning.

## Applies If (ALL must hold)

- The triggering activity 'Agentic AI feature MVP to GA (role: role-ml-engineer)' shows up in the user's workload at least once per cycle.
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
| `human_in_the_loop_pattern_catalog_template_fill` | haiku | Template fill, no judgement |
| `human_in_the_loop_pattern_catalog_evidence_check` | sonnet | Bounded comparison + judgement |
| `human_in_the_loop_pattern_catalog_synthesis` | opus | Cross-input synthesis + final write-up |

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
- triggering activity: `Agentic AI feature MVP to GA (role: role-ml-engineer)`
- external: industry references cited inline in `content/01-core-rules.xml`
