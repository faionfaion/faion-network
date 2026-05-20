---
slug: ai-transcript-to-traceable-requirement
tier: geek
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Ai Transcript to Traceable Requirement: codified business-analysis practice that turns the recurring 'role-business-analyst/Stakeholder interview: prep + run + capture' decision into a repeatable, auditable artefact.
content_id: "91e2b9105808d2ad"
tags: [ai-transcript-to-traceable-requirement, ba, geek]
---
# Ai Transcript to Traceable Requirement

## Summary

**One-sentence:** Ai Transcript to Traceable Requirement: codified business-analysis practice that turns the recurring 'role-business-analyst/Stakeholder interview: prep + run + capture' decision into a repeatable, auditable artefact.

**One-paragraph:** Ai Transcript to Traceable Requirement addresses the gap identified by the role-business-analyst/Stakeholder interview: prep + run + capture playbook: Bridge between raw transcripts and a traceable requirement row is the highest-leverage automation point for BAs; no methodology covers it. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/Stakeholder interview: prep + run + capture OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/Stakeholder interview: prep + run + capture task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `templates/ai-transcript-to-traceable-requirement.json` | JSON schema for the Ai Transcript to Traceable Requirement output contract |
| `templates/ai-transcript-to-traceable-requirement.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-transcript-to-traceable-requirement.py` | Enforce Ai Transcript to Traceable Requirement output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ba/`
- upstream playbook: `role-business-analyst/Stakeholder interview: prep + run + capture`
- external: [RAGAS](https://docs.ragas.io/) · [Anthropic agent design](https://docs.anthropic.com/en/docs/build-with-claude/agents)
