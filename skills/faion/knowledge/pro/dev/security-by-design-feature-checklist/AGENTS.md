---
slug: security-by-design-feature-checklist
tier: pro
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: "STRIDE-lite per-feature threat-model checklist that runs before a feature design is merged, producing a small artefact the architecture review consumes."
content_id: "922bfbf1a3421b99"
tags: [security-by-design-feature-checklist, dev, pro]
---
# Security by Design Feature Checklist

## Summary

**One-sentence:** A STRIDE-lite per-feature checklist that runs before a feature design merges and emits a small artefact the architecture review consumes.

**One-paragraph:** `security-architecture` covers the system-level view; `stride-threat-model-template` covers the heavyweight workshop. Missing is the lightweight per-feature pass that fits a normal design-review meeting: 6 STRIDE categories, 2-3 prompts each, decision per prompt (mitigated / accepted / deferred). The output is a `feature-stm.md` (max ~1 page) attached to the feature's design doc. Reviewers refuse to approve a design without one. This is the architect deliverable that nobody covered cleanly before.

## Applies If (ALL must hold)

- a feature design is going into architecture review
- the feature touches identity, data flow, persistence, external integration, or trust boundary
- output (feature STM doc) will be attached to the design doc
- tier == pro or higher

## Skip If (ANY kills it)

- feature is a pure UI tweak with no data-flow change
- a parent system STRIDE already covers this feature unchanged (cite, don't re-do)
- regulatory regime mandates a different per-feature template

## Prerequisites

- the feature has a written design doc (even draft)
- a STRIDE-aware reviewer is on the architecture review
- the team has read `stride-threat-model-template` once

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/dev/stride-threat-model-template` | parent / heavyweight version |
| `pro/dev/stride-lite-checklist-for-architects` | sibling — broader-edge variant |
| `pro/dev/architecture-review-meeting-facilitation` | downstream consumer of this artefact |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (one per STRIDE letter) + 1 worked example | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `prompt_per_stride_letter` | sonnet | bounded per-category prompts |
| `summarise_decisions` | sonnet | merge decisions into 1-page artefact |
| `flag_unmitigated_high` | opus | escalation judgement when High-risk items remain |

## Related

- parent skill: `pro/dev/`
- `pro/dev/stride-threat-model-template`
- `pro/dev/stride-lite-checklist-for-architects`
- upstream playbook: `role-software-architect/Architecture review meeting facilitation`
