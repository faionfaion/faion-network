---
slug: motion-and-microinteraction-spec
tier: pro
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Motion And Microinteraction Spec: codified ux practice that turns the recurring 'role-ux-ui-designer/Zero-to-one product design: brief to dev handoff (8 weeks)' decision into a repeatable, auditable artefact.
content_id: "b568cb0e1e9ac463"
tags: [motion-and-microinteraction-spec, ux, pro]
---
# Motion And Microinteraction Spec

## Summary

**One-sentence:** Motion And Microinteraction Spec: codified ux practice that turns the recurring 'role-ux-ui-designer/Zero-to-one product design: brief to dev handoff (8 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Motion And Microinteraction Spec addresses the gap identified by the role-ux-ui-designer/Zero-to-one product design: brief to dev handoff (8 weeks) playbook: Hi-fi handoff is incomplete without motion. AI-generated layouts almost never include timing curves or microinteractions. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ux-ui-designer/Zero-to-one product design: brief to dev handoff (8 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ux-ui-designer/Zero-to-one product design: brief to dev handoff (8 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ux/ux-ui-designer` | parent role skill — provides the operating context for this methodology |

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
| `synthesize_decision` | sonnet | Per-instance judgment; bounded inputs |
| `review_for_compliance` | opus | Cross-input synthesis when stakes are high |

## Templates

| File | Purpose |
|------|---------|
| `templates/motion-and-microinteraction-spec.json` | JSON schema for the Motion And Microinteraction Spec output contract |
| `templates/motion-and-microinteraction-spec.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-motion-and-microinteraction-spec.py` | Enforce Motion And Microinteraction Spec output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/ux/ux-ui-designer/`
- upstream playbook: `role-ux-ui-designer/Zero-to-one product design: brief to dev handoff (8 weeks)`
