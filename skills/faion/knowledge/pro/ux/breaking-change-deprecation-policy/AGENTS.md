---
slug: breaking-change-deprecation-policy
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Breaking Change Deprecation Policy: codified design / UX practice that turns the recurring 'role-ux-ui-designer/Design-system component update (single component)' decision into a repeatable, auditable artefact.
content_id: "c49cb5381b3230bb"
tags: [breaking-change-deprecation-policy, ux, pro]
---
# Breaking Change Deprecation Policy

## Summary

**One-sentence:** Breaking Change Deprecation Policy: codified design / UX practice that turns the recurring 'role-ux-ui-designer/Design-system component update (single component)' decision into a repeatable, auditable artefact.

**One-paragraph:** Breaking Change Deprecation Policy addresses the gap identified by the role-ux-ui-designer/Design-system component update (single component) playbook: Designers improvise deprecation timelines per component; a single rule (e.g. 2-sprint deprecation, breaking-change opt-in) eliminates negotiation overhead. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ux-ui-designer/Design-system component update (single component) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ux-ui-designer/Design-system component update (single component) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/ux-designer` | parent role skill — provides the operating context for this methodology |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 4 testable rules: r1-bound-scope, r2-typed-input, r3-named-owner, r4-versioned | ~900 |
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
| `templates/breaking-change-deprecation-policy.json` | JSON schema for the Breaking Change Deprecation Policy output contract |
| `templates/breaking-change-deprecation-policy.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-breaking-change-deprecation-policy.py` | Enforce Breaking Change Deprecation Policy output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ux/`
- upstream playbook: `role-ux-ui-designer/Design-system component update (single component)`
