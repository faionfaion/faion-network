---
slug: recognition-over-recall
tier: solo
group: ux
domain: frontend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nielsen Heuristic #6: minimize memory load by making options, actions, and context visible rather than requiring users to remember them.
content_id: "c767d6692d17824a"
tags: [recognition, recall, usability-heuristics, cognitive-load, accessibility]
---
# Recognition Rather Than Recall

## Summary

**One-sentence:** Nielsen Heuristic #6: minimize memory load by making options, actions, and context visible rather than requiring users to remember them.

**One-paragraph:** Nielsen Heuristic #6: minimize memory load by making options, actions, and context visible rather than requiring users to remember them. Users should recognize what to do from visible cues rather than recall it from memory. Apply when auditing UIs, reviewing component specs, or designing multi-step flows.

## Applies If (ALL must hold)

- Auditing an existing UI for hidden options, icon-only toolbars, or multi-step flows with no context carry-over.
- Reviewing wireframes or component specs for places where users must remember prior screen content.
- Designing search, navigation, or command interfaces — autocomplete and recents are high-ROI here.
- Reviewing AI chat or developer-tool UIs for missing help text, suggestions, or history.

## Skip If (ANY kills it)

- Power-user tools where recall is intentional (vim, SQL terminals, CAD shortcuts) — violating recall norms breaks expert efficiency.
- Micro-optimization on a product not past alpha — this heuristic is for refining, not architecting.
- When the interface is already fully recognition-based and validated — audit adds no value.

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

- parent skill: `solo/ux/ux-ui-designer/`
