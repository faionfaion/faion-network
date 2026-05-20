---
slug: mixed-methods-triangulation
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Mixed Methods Triangulation: codified research practice that turns the recurring 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog' decision into a repeatable, auditable artefact.
content_id: "8c96257d50f83240"
tags: [mixed-methods-triangulation, research, pro]
---
# Mixed Methods Triangulation

## Summary

**One-sentence:** Mixed Methods Triangulation: codified research practice that turns the recurring 'role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog' decision into a repeatable, auditable artefact.

**One-paragraph:** Mixed Methods Triangulation addresses the gap identified by the role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog playbook: Designers need a methodology that fuses qualitative interview signal with quantitative analytics + support-ticket data + behavioural session-replay. Faion treats each source in isolation. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/research/researcher` | parent role skill — provides the operating context for this methodology |

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
| `templates/mixed-methods-triangulation.json` | JSON schema for the Mixed Methods Triangulation output contract |
| `templates/mixed-methods-triangulation.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mixed-methods-triangulation.py` | Enforce Mixed Methods Triangulation output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/research/researcher/`
- upstream playbook: `role-ux-ui-designer/AI-assisted research synthesis: interview transcripts → tagged insights → design-backlog`
