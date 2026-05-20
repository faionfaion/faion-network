---
slug: platform-native-format-matrix
tier: solo
group: marketing
domain: marketing
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Platform Native Format Matrix: codified marketing practice that turns the recurring 'role-growth-marketing/Social cadence post: X / LinkedIn / threads (per-post, 20 min)' decision into a repeatable, auditable artefact.
content_id: "148b9cec7ae88993"
tags: [platform-native-format-matrix, marketing, solo]
---
# Platform Native Format Matrix

## Summary

**One-sentence:** Platform Native Format Matrix: codified marketing practice that turns the recurring 'role-growth-marketing/Social cadence post: X / LinkedIn / threads (per-post, 20 min)' decision into a repeatable, auditable artefact.

**One-paragraph:** Platform Native Format Matrix addresses the gap identified by the role-growth-marketing/Social cadence post: X / LinkedIn / threads (per-post, 20 min) playbook: Cross-poster slop is the default failure. Matrix of platform x format x stage prevents lazy reuse. Mechanism: a typed input → bounded transformation → contract-checked output. Primary output: a versioned artefact (decision record, checklist, score, or report) that downstream tasks can consume without re-deriving the rationale.

## Applies If (ALL must hold)

- task is an instance of role-growth-marketing/Social cadence post: X / LinkedIn / threads (per-post, 20 min) OR a closely-adjacent variant
- the operator has the artefacts named in Prerequisites available before starting
- output will be consumed by a downstream agent or human reviewer (not discarded)
- tier == solo or higher (gating enforced by tier-manifest)

## Skip If (ANY kills it)

- the team already maintains a working artefact for this gap — replace, do not duplicate
- the change being decided is greenfield prototype with no production users
- regulatory / compliance context overrides any in-methodology guidance (defer to legal)

## Prerequisites

- recent context for the role-growth-marketing/Social cadence post: X / LinkedIn / threads (per-post, 20 min) task (last 30 days)
- write-access to the artefact store (repo / wiki / decision log)
- named owner who is accountable for the output downstream

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/marketing/content-marketer` | parent role skill — provides the operating context for this methodology |

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
| `templates/platform-native-format-matrix.json` | JSON schema for the Platform Native Format Matrix output contract |
| `templates/platform-native-format-matrix.md` | Markdown skeleton with the required fields |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-platform-native-format-matrix.py` | Enforce Platform Native Format Matrix output contract | After subagent returns, before downstream consumer reads |

## Related

- parent skill: `solo/marketing/content-marketer/`
- upstream playbook: `role-growth-marketing/Social cadence post: X / LinkedIn / threads (per-post, 20 min)`
