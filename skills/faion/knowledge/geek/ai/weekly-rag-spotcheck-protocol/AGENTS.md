---
slug: weekly-rag-spotcheck-protocol
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "3cd46423d403e0f1"
summary: "Weekly Rag Spotcheck Protocol: produces a versioned, owner-signed artefact that closes the gap 'role-ml-engineer/Weekly RAG retrieval quality spot-check'."
tags: [weekly-rag-spotcheck-protocol, ai, geek]
---
# Weekly Rag Spotcheck Protocol

## Summary

**One-sentence:** Weekly Rag Spotcheck Protocol: produces a versioned, owner-signed artefact that closes the gap 'role-ml-engineer/Weekly RAG retrieval quality spot-check'.

**One-paragraph:** Addresses the gap surfaced by 'role-ml-engineer/Weekly RAG retrieval quality spot-check': rag-eval-* methodologies cover metrics but not the weekly cadence: sample size, stratification, label rubric, time-boxing. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a weekly rag spotcheck protocol artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-ml-engineer/Weekly RAG retrieval quality spot-check' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == geek or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working weekly rag spotcheck protocol artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-ml-engineer/Weekly RAG retrieval quality spot-check' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai` | parent domain group — provides operating context for Weekly Rag Spotcheck Protocol |

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
| `templates/weekly-rag-spotcheck-protocol.json` | JSON schema for the Weekly Rag Spotcheck Protocol output contract |
| `templates/weekly-rag-spotcheck-protocol.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-weekly-rag-spotcheck-protocol.py` | Enforce Weekly Rag Spotcheck Protocol output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `geek/ai/`
- upstream playbook: `role-ml-engineer/Weekly RAG retrieval quality spot-check`
- geek/ai/role-ml-engineer
