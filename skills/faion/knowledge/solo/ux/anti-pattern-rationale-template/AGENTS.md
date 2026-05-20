---
slug: anti-pattern-rationale-template
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Anti Pattern Rationale Template: codified design / UX practice that turns the recurring 'role-ux-ui-designer/Inspiration + patterns capture (30min/week)' decision into a repeatable, auditable artefact.
content_id: "5376be92c89c5f2a"
tags: [anti-pattern-rationale-template, ux, solo]
---
# Anti Pattern Rationale Template

## Summary

**One-sentence:** Anti Pattern Rationale Template: codified design / UX practice that turns the recurring 'role-ux-ui-designer/Inspiration + patterns capture (30min/week)' decision into a repeatable, auditable artefact.

**One-paragraph:** Anti Pattern Rationale Template addresses the gap identified by the role-ux-ui-designer/Inspiration + patterns capture (30min/week) playbook: Documenting WHY a pattern is an anti-pattern is what stops future repetition; current competitive-analysis methodology doesn't reach this granularity. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ux-ui-designer/Inspiration + patterns capture (30min/week) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ux-ui-designer/Inspiration + patterns capture (30min/week) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/ux/ux-designer` | parent role skill — provides the operating context for this methodology |

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
| `templates/anti-pattern-rationale-template.json` | JSON schema for the Anti Pattern Rationale Template output contract |
| `templates/anti-pattern-rationale-template.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-anti-pattern-rationale-template.py` | Enforce Anti Pattern Rationale Template output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/ux/`
- upstream playbook: `role-ux-ui-designer/Inspiration + patterns capture (30min/week)`
