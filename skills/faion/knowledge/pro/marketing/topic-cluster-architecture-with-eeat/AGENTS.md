---
slug: topic-cluster-architecture-with-eeat
tier: pro
group: marketing
domain: marketing
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Topic Cluster Architecture With Eeat: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence'."
content_id: "95f096965a9aac1a"
complexity: deep
produces: spec
est_tokens: 4400
tags: [topic-cluster-architecture-with-eeat, marketing, pro]
---
# Topic Cluster Architecture With Eeat

## Summary

**One-sentence:** Topic Cluster Architecture With Eeat: produces a versioned, owner-signed artefact that closes the gap 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence'.

**One-paragraph:** Addresses the gap surfaced by 'role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence': `topical-authority` exists but treats topical authority as a goal, not a construction process. No methodology covers pillar/spoke architecture decisions, author/expert assignment for E-E-A-T signals, first-hand-experience capture, or the link-graph topology that makes a cluster legible to ranking algorithms. Mechanism: bounded inputs → contract-checked transformation → versioned output that downstream agents or humans can consume without re-deriving the rationale. Primary output: a topic cluster architecture with eeat artefact (decision record, checklist, score sheet, or report).

**Ефективно для:**

- Pillar+spoke architecture з типографованими E-E-A-T сигналами.
- Named author/expert assignment для першоособового досвіду.
- Link-graph topology зрозуміла ranking algorithms.
- Cluster ownership + version + outcome review.

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
| `content/01-core-rules.xml` | essential | Testable rules + self-routing anchors (run-the-checklist + skip-this-methodology) | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example | ~900 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns with description + reason + repair | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on preconditions → rule from `01-core-rules.xml` | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | template fill, bounded transformation |
| `synthesize_decision` | sonnet | per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/topic-cluster-architecture-with-eeat.md` | Markdown skeleton (5-line header) for the artefact body. |
| `templates/topic-cluster-architecture-with-eeat.json` | JSON Schema (draft-07) for the output contract — see `content/02-output-contract.xml`. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-topic-cluster-architecture-with-eeat.py` | Validate a filled artefact against the schema declared in `content/02-output-contract.xml`. Supports `--help` and `--self-test`. | Pre-commit; before publishing the artefact. |

## Related

- parent skill: `pro/marketing/`
- upstream playbook: `role-growth-marketing/Synthesis: Build a topical-authority cluster end-to-end with E-E-A-T evidence`
- pro/marketing/role-growth-marketing

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable preconditions (Applies-If / Skip-If) to either `run-the-checklist` or `skip-this-methodology` from `01-core-rules.xml`. Use it whenever the operating trigger fires and you need to decide between applying this methodology now, deferring, or routing elsewhere.

