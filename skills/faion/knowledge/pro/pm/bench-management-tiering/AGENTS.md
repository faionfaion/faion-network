---
slug: bench-management-tiering
tier: pro
group: pm
domain: pm
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Bench Management Tiering: codified delivery-management practice that turns the recurring 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' decision into a repeatable, auditable artefact.
content_id: "dcfd28b2960f2898"
tags: [bench-management-tiering, pm, pro]
---
# Bench Management Tiering

## Summary

**One-sentence:** Bench Management Tiering: codified delivery-management practice that turns the recurring 'p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies' decision into a repeatable, auditable artefact.

**One-paragraph:** Bench Management Tiering addresses the gap identified by the p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies playbook: ops-contractor-management treats all contractors as one pool with one cadence. Real micro-agencies operate a tiered bench (rapid-call / regular / occasional / blacklist) with different rates and SLAs. There is no methodology for designing or running the tier system. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/pm/project-manager` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-headroom-floor | ~900 |
| `content/02-output-contract.xml` | essential | Required fields, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 failure modes with detector + repair | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft_inputs_summary` | haiku | Template fill, bounded transformation |
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/bench-management-tiering.json` | JSON schema for the Bench Management Tiering output contract |
| `templates/bench-management-tiering.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bench-management-tiering.py` | Enforce Bench Management Tiering output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/pm/`
- upstream playbook: `p5-micro-agency-founder/Build a bench of vetted subcontractors without becoming an agency-of-agencies`
