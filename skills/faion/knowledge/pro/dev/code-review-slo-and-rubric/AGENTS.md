---
slug: code-review-slo-and-rubric
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Code Review Slo And Rubric: codified dev practice that turns the recurring 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' decision into a repeatable, auditable artefact.
content_id: "32c554fef309477a"
tags: [code-review-slo-and-rubric, dev, pro]
---
# Code Review Slo And Rubric

## Summary

**One-sentence:** Code Review Slo And Rubric: codified dev practice that turns the recurring 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' decision into a repeatable, auditable artefact.

**One-paragraph:** Code Review Slo And Rubric addresses the gap surfaced by 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop'. `code-review` exists at free tier but is generic. Teams need: review-time SLO (24h business), reviewer-rotation algorithm, reviewer-load cap, what blocks vs nit-picks rubric, AI-pre-review-then-human-final pattern. Without SLO, PRs sit for days and devs context-switch endlessly Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop' task (last 30 days of activity)
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
| `templates/code-review-slo-and-rubric.json` | JSON schema for the Code Review Slo And Rubric output contract |
| `templates/code-review-slo-and-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-code-review-slo-and-rubric.py` | Enforce Code Review Slo And Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `p6-product-dev-team/Cross-role handoff: PM -> Architect -> Dev -> QA -> DevOps in one loop`
- methodology family: `pro/dev/` (gap-p2 batch, F-059-063)
