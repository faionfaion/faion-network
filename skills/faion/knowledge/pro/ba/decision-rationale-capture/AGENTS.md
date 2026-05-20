---
slug: decision-rationale-capture
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Decision Rationale Capture: codified ba practice that turns the recurring 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture' decision into a repeatable, auditable artefact.
content_id: "fe140079552ed1bb"
tags: [decision-rationale-capture, ba, pro]
---
# Decision Rationale Capture

## Summary

**One-sentence:** Decision Rationale Capture: codified ba practice that turns the recurring 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture' decision into a repeatable, auditable artefact.

**One-paragraph:** Decision Rationale Capture addresses the gap surfaced by 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture'. Closest existing artefact is pro/ba-modeling/decision-analysis (decision tables, business rules) — that is logic modeling, not decision-record capture. Missing: a lightweight ADR-equivalent for BA-level decisions (scope-cuts, prioritisation choices, conflict resolutions) with options-considered + chosen + rationale + reversibility. Outsource BAs need this for audit and for the inevitable post-mortem. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture' task (last 30 days of activity)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream
- baseline conventions documented (CLAUDE.md / AGENTS.md / CONVENTIONS.md)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

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
| `templates/decision-rationale-capture.json` | JSON schema for the Decision Rationale Capture output contract |
| `templates/decision-rationale-capture.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-decision-rationale-capture.py` | Enforce Decision Rationale Capture output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/business-analyst/`
- upstream playbook: `role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture`
- methodology family: `pro/ba/` (gap-p2 batch, F-059-063)
