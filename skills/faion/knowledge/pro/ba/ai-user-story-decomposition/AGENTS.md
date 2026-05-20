---
slug: ai-user-story-decomposition
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai User Story Decomposition: codified business-analysis practice that turns the recurring 'role-business-analyst/AI-assisted requirements discovery on a new outsource engagement' decision into a repeatable, auditable artefact.
content_id: "6399c1a7cdf6fb77"
tags: [ai-user-story-decomposition, ba, pro]
---
# Ai User Story Decomposition

## Summary

**One-sentence:** Ai User Story Decomposition: codified business-analysis practice that turns the recurring 'role-business-analyst/AI-assisted requirements discovery on a new outsource engagement' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai User Story Decomposition addresses the gap identified by the role-business-analyst/AI-assisted requirements discovery on a new outsource engagement playbook: pro/ba-modeling/user-story-mapping covers traditional story mapping. Nothing covers AI-assisted epic→story decomposition with INVEST scoring, slicing patterns (workflow / data / business-rule), or BA review checklist. This is the single most repeated AI task BAs do today. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/AI-assisted requirements discovery on a new outsource engagement OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/AI-assisted requirements discovery on a new outsource engagement task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-llm-grounding, r5-acceptance-criteria | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/ai-user-story-decomposition.json` | JSON schema for the Ai User Story Decomposition output contract |
| `templates/ai-user-story-decomposition.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-user-story-decomposition.py` | Enforce Ai User Story Decomposition output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/AI-assisted requirements discovery on a new outsource engagement`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
