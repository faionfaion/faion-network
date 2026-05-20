---
slug: thematic-analysis
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "63540fe77743d7d5"
summary: "Thematic Analysis: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog'."
tags: [thematic-analysis, research, pro]
---
# Thematic Analysis

## Summary

**One-sentence:** Thematic Analysis: produces a versioned, owner-signed artefact that closes the gap 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog'.

**One-paragraph:** Addresses the gap surfaced by 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog': Faion captures interviews and diary studies but has no methodology for coding transcripts and extracting themes. AI assist exists (geek/ai-interview-analysis) but no underlying human-craft methodology to validate or override the LLM coding. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a thematic analysis artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working thematic analysis artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/research` | parent domain group — provides operating context for Thematic Analysis |

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
| `templates/thematic-analysis.json` | JSON schema for the Thematic Analysis output contract |
| `templates/thematic-analysis.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-thematic-analysis.py` | Enforce Thematic Analysis output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/research/`
- upstream playbook: `role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog`
- pro/research/role-ux-ui-designer
