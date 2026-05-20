---
slug: marketing-tool-stack-rationalization
tier: pro
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Marketing Tool Stack Rationalization: codified marketing practice that turns the recurring 'role-growth-marketing/Content Engine Build from Zero (12 weeks)' decision into a repeatable, auditable artefact.
content_id: "ad3046405c28cf7d"
tags: [marketing-tool-stack-rationalization, marketing, pro]
---
# Marketing Tool Stack Rationalization

## Summary

**One-sentence:** Marketing Tool Stack Rationalization: codified marketing practice that turns the recurring 'role-growth-marketing/Content Engine Build from Zero (12 weeks)' decision into a repeatable, auditable artefact.

**One-paragraph:** Marketing Tool Stack Rationalization addresses the gap identified by the role-growth-marketing/Content Engine Build from Zero (12 weeks) playbook: User-named pain: marketing tools sprawl. ai-marketing-tools-stack-2026 lists tools but does not provide a rationalization SOP (audit, consolidate, kill, justify). Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-growth-marketing/Content Engine Build from Zero (12 weeks) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == pro or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-growth-marketing/Content Engine Build from Zero (12 weeks) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/marketing/growth-marketer` | parent role skill — provides the operating context for this methodology |

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
| `templates/marketing-tool-stack-rationalization.json` | JSON schema for the Marketing Tool Stack Rationalization output contract |
| `templates/marketing-tool-stack-rationalization.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-marketing-tool-stack-rationalization.py` | Enforce Marketing Tool Stack Rationalization output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `pro/marketing/growth-marketer/`
- upstream playbook: `role-growth-marketing/Content Engine Build from Zero (12 weeks)`
