---
slug: context-bleed-detection-recipe
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Context Bleed Detection Recipe: codified ai practice that turns the recurring 'p7-llm-agent-developer/Agent-state debug session (cursor + replay)' decision into a repeatable, auditable artefact.
content_id: "e9789447b8fc851a"
tags: [context-bleed-detection-recipe, ai, geek]
---
# Context Bleed Detection Recipe

## Summary

**One-sentence:** Context Bleed Detection Recipe: codified ai practice that turns the recurring 'p7-llm-agent-developer/Agent-state debug session (cursor + replay)' decision into a repeatable, auditable artefact.

**One-paragraph:** Context Bleed Detection Recipe addresses the gap surfaced by 'p7-llm-agent-developer/Agent-state debug session (cursor + replay)'. subagent-as-context-firewall + compaction-preserve-refs describe the cure; there is no recipe for noticing context bleed before a user does. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p7-llm-agent-developer/Agent-state debug session (cursor + replay)' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p7-llm-agent-developer/Agent-state debug session (cursor + replay)' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-traceable-decision | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment with bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/context-bleed-detection-recipe.json` | JSON schema for the Context Bleed Detection Recipe output contract |
| `templates/context-bleed-detection-recipe.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-context-bleed-detection-recipe.py` | Enforce Context Bleed Detection Recipe output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/ml-engineer/`
- upstream playbook: `p7-llm-agent-developer/Agent-state debug session (cursor + replay)`
- methodology family: `geek/ai/` (gap-p2 batch, F-059-063)
