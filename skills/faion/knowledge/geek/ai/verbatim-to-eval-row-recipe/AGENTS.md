---
slug: verbatim-to-eval-row-recipe
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "5543e441096bb07a"
summary: "Verbatim To Eval Row Recipe: produces a versioned, owner-signed artefact that closes the gap 'p7-llm-agent-developer/Customer-zero feedback loop session'."
tags: [verbatim-to-eval-row-recipe, ai, geek]
---
# Verbatim To Eval Row Recipe

## Summary

**One-sentence:** Verbatim To Eval Row Recipe: produces a versioned, owner-signed artefact that closes the gap 'p7-llm-agent-developer/Customer-zero feedback loop session'.

**One-paragraph:** Addresses the gap surfaced by 'p7-llm-agent-developer/Customer-zero feedback loop session': Translating a customer's 'I expected X, got Y' quote into a deterministic, automatable eval row is a learned skill. Codifying it shortens the loop dramatically. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a verbatim to eval row recipe artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'p7-llm-agent-developer/Customer-zero feedback loop session' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working verbatim to eval row recipe artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'p7-llm-agent-developer/Customer-zero feedback loop session' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai` | parent domain group — provides operating context for Verbatim To Eval Row Recipe |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules grounded in the cited gap | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/verbatim-to-eval-row-recipe.json` | JSON schema for the Verbatim To Eval Row Recipe output contract |
| `templates/verbatim-to-eval-row-recipe.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-verbatim-to-eval-row-recipe.py` | Enforce Verbatim To Eval Row Recipe output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `p7-llm-agent-developer/Customer-zero feedback loop session`
- geek/ai/p7-llm-agent-developer
