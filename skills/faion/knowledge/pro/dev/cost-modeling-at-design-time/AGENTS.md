---
slug: cost-modeling-at-design-time
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Cost Modeling At Design Time: codified dev practice that turns the recurring 'role-software-architect/Cost + latency budget BEFORE design freeze' decision into a repeatable, auditable artefact.
content_id: "54fcc1214f0ac780"
tags: [cost-modeling-at-design-time, dev, pro]
---
# Cost Modeling At Design Time

## Summary

**One-sentence:** Cost Modeling At Design Time: codified dev practice that turns the recurring 'role-software-architect/Cost + latency budget BEFORE design freeze' decision into a repeatable, auditable artefact.

**One-paragraph:** Cost Modeling At Design Time addresses the gap surfaced by 'role-software-architect/Cost + latency budget BEFORE design freeze'. FinOps methodologies exist under devops-engineer and infrastructure-engineer but only at run-time. Architects need a pre-implementation $/1M-requests model with vendor cost-cliff identification (LLM tokens, vector DB tier, egress) wired into the ADR before code is written. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Cost + latency budget BEFORE design freeze' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-software-architect/Cost + latency budget BEFORE design freeze' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/software-developer` | parent role skill — provides the operating context for this methodology |

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
| `templates/cost-modeling-at-design-time.json` | JSON schema for the Cost Modeling At Design Time output contract |
| `templates/cost-modeling-at-design-time.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-cost-modeling-at-design-time.py` | Enforce Cost Modeling At Design Time output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `role-software-architect/Cost + latency budget BEFORE design freeze`
- methodology family: `pro/dev/` (gap-p2 batch, F-059-063)
