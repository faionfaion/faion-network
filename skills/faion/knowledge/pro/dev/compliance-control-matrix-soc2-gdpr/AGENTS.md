---
slug: compliance-control-matrix-soc2-gdpr
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Compliance Control Matrix Soc2 Gdpr: codified dev practice that turns the recurring 'role-software-architect/Security-by-design audit + threat-modelling cycle' decision into a repeatable, auditable artefact.
content_id: "2182e39e18ea8fbd"
tags: [compliance-control-matrix-soc2-gdpr, dev, pro]
---
# Compliance Control Matrix Soc2 Gdpr

## Summary

**One-sentence:** Compliance Control Matrix Soc2 Gdpr: codified dev practice that turns the recurring 'role-software-architect/Security-by-design audit + threat-modelling cycle' decision into a repeatable, auditable artefact.

**One-paragraph:** Compliance Control Matrix Soc2 Gdpr addresses the gap surfaced by 'role-software-architect/Security-by-design audit + threat-modelling cycle'. Architects keep being pulled into compliance mappings (SOC2 / GDPR / PCI). A reusable control matrix keyed to architecture components would compress a multi-day exercise. Mechanism: typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of 'role-software-architect/Security-by-design audit + threat-modelling cycle' OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is a greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)
- single-use throwaway task — overhead of the contract is not justified

## Prerequisites

- recent context for the 'role-software-architect/Security-by-design audit + threat-modelling cycle' task (last 30 days of activity)
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
| `templates/compliance-control-matrix-soc2-gdpr.json` | JSON schema for the Compliance Control Matrix Soc2 Gdpr output contract |
| `templates/compliance-control-matrix-soc2-gdpr.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-compliance-control-matrix-soc2-gdpr.py` | Enforce Compliance Control Matrix Soc2 Gdpr output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/dev/software-developer/`
- upstream playbook: `role-software-architect/Security-by-design audit + threat-modelling cycle`
- methodology family: `pro/dev/` (gap-p2 batch, F-059-063)
