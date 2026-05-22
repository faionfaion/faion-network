---
slug: flexibility-efficiency
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #7: design for both novice and expert users simultaneously by providing accelerators (keyboard shortcuts, bulk operations, templates) that novices can ignore but experts use daily, plus progressive disclosure and multiple paths for the same goal.
content_id: "850eca43a1a85ff9"
tags: [ux, heuristics, keyboard-shortcuts, efficiency, accessibility]
---
# Flexibility and Efficiency of Use

## Summary

**One-sentence:** Nielsen Heuristic #7: design for both novice and expert users simultaneously by providing accelerators (keyboard shortcuts, bulk operations, templates) that novices can ignore but experts use daily, plus progressive disclosure and multiple paths for the same goal.

**One-paragraph:** Nielsen Heuristic #7: design for both novice and expert users simultaneously by providing accelerators (keyboard shortcuts, bulk operations, templates) that novices can ignore but experts use daily, plus progressive disclosure and multiple paths for the same goal. Interfaces tuned only for beginners frustrate power users who repeat the same tasks hundreds of times per day. Interfaces tuned only for experts overwhelm newcomers. Layered flexibility — visible affordances plus hidden accelerators — lets one interface serve the full user spectrum without cognitive overload at either end.

## Applies If (ALL must hold)

- Designing or auditing productivity tools, admin panels, developer tools, or any app with repeat-use workflows.
- Adding keyboard shortcut coverage to an existing web application.
- Auditing whether an interface serves both novice onboarding and power-user acceleration.
- Planning customization features (saved layouts, quick actions, pinned items) for SaaS products.
- Evaluating CLI tools or APIs for efficiency affordances.

## Skip If (ANY kills it)

- One-time-use flows (checkout, onboarding wizard, password reset) — shortcuts add no value here.
- Consumer apps with mostly casual, infrequent users — shortcut investment is wasted.
- Early prototype stages before task flows are validated — optimizing efficiency before correctness is premature.
- Accessibility-first flows where additional modalities must be layered carefully to avoid screen reader conflicts.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/ux/accessibility-specialist/`
