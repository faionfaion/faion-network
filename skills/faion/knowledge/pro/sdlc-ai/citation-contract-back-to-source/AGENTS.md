---
slug: citation-contract-back-to-source
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Citation Contract Back To Source: codified sdlc-ai practice that turns the recurring 'p7-llm-agent-developer/Make faion a programmatic context source for an agent' decision into a repeatable, auditable artefact.
content_id: "4f522c00ad7f0fb3"
tags: [citation-contract-back-to-source, sdlc-ai, pro]
---
# Citation Contract Back To Source

## Summary

**One-sentence:** Citation Contract Back To Source: codified sdlc-ai practice that turns the recurring 'p7-llm-agent-developer/Make faion a programmatic context source for an agent' decision into a repeatable, auditable artefact.

**One-paragraph:** Citation Contract Back To Source addresses the gap surfaced by 'p7-llm-agent-developer/Make faion a programmatic context source for an agent'. Strategic value of P7 to faion: 'what they cite, others cite.' But no methodology defines how an agent should emit `[faion:slug@v]` citations, what fields are required, or how to verify a citation. Without this contract, P7's agents will paraphrase faion without attribution and the network effect dies. Should ship as a forced output-schema fragment plus a CLI verifier. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p7-llm-agent-developer/Make faion a programmatic context source for an agent' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p7-llm-agent-developer/Make faion a programmatic context source for an agent' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/sdd` | parent role skill — provides the operating context for this methodology |

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
| `templates/citation-contract-back-to-source.json` | JSON schema for the Citation Contract Back To Source output contract |
| `templates/citation-contract-back-to-source.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-citation-contract-back-to-source.py` | Enforce Citation Contract Back To Source output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/sdlc-ai/sdd/`
- upstream playbook: `p7-llm-agent-developer/Make faion a programmatic context source for an agent`
- methodology family: `pro/sdlc-ai/` (gap-p2 batch, F-059-063)
