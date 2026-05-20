---
slug: change-request-impact-rubric
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Change Request Impact Rubric: codified business-analysis practice that turns the recurring 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture' decision into a repeatable, auditable artefact.
content_id: "d599f5e3588cffea"
tags: [change-request-impact-rubric, ba, pro]
---
# Change Request Impact Rubric

## Summary

**One-sentence:** Change Request Impact Rubric: codified business-analysis practice that turns the recurring 'role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture' decision into a repeatable, auditable artefact.

**One-paragraph:** Change Request Impact Rubric addresses the gap identified by the role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture playbook: pro/ba-core/ba-requirements-mgmt covers requirement maintenance and change impact at the definitional level. Missing: concrete rubric to score a CR by blast radius (requirement count touched, AC count touched, test count touched, regulatory-clause count touched, dependent stories), with a recommended approval route (BA approves / PO approves / steering committee). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ba/business-analyst` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned, r5-detector-first | ~900 |
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
| `templates/change-request-impact-rubric.json` | JSON schema for the Change Request Impact Rubric output contract |
| `templates/change-request-impact-rubric.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-change-request-impact-rubric.py` | Enforce Change Request Impact Rubric output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ba/`
- upstream playbook: `role-business-analyst/Stakeholder-conflict facilitation and decision rationale capture`
