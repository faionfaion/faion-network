---
slug: topic-cluster-architecture-with-eeat
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "95f096965a9aac1a"
summary: "Topic Cluster Architecture With Eeat: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence'."
tags: [topic-cluster-architecture-with-eeat, marketing, pro]
---
# Topic Cluster Architecture With Eeat

## Summary

**One-sentence:** Topic Cluster Architecture With Eeat: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence'.

**One-paragraph:** Addresses the gap surfaced by 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence': `topical-authority` exists but treats topical authority as a goal, not a construction process. No methodology covers pillar/spoke architecture decisions, author/expert assignment for E-E-A-T signals, first-hand-experience capture, or the link-graph topology that makes a cluster legible to ranking algorithms. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a topic cluster architecture with eeat artefact (decision record, checklist, score sheet, or report).

## Applies If (ALL must hold)

- task is an instance of 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence' or a closely-adjacent variant
- operator has the artefacts named in Prerequisites before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working topic cluster architecture with eeat artefact — replace, do not duplicate
- the change is greenfield prototype with no production users
- regulatory / compliance context overrides in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence' task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/marketing` | parent domain group — provides operating context for Topic Cluster Architecture With Eeat |

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
| `templates/topic-cluster-architecture-with-eeat.json` | JSON schema for the Topic Cluster Architecture With Eeat output contract |
| `templates/topic-cluster-architecture-with-eeat.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-topic-cluster-architecture-with-eeat.py` | Enforce Topic Cluster Architecture With Eeat output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: `role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence`
- pro/marketing/role-growth-marketing
