---
slug: knowledge-areas-detail
tier: pro
group: ba
domain: ba
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Detailed reference for all six BABOK Knowledge Areas (KA-1 through KA-6): per-KA task table, key outputs, linked methodologies, and the canonical workflow sequence for greenfield engagements and change requests.
content_id: "209fe48b4a1a5c4c"
tags: [babok, knowledge-areas, workflow, requirements, ba-planning]
---
# BA Knowledge Areas Detail

## Summary

**One-sentence:** Detailed reference for all six BABOK Knowledge Areas (KA-1 through KA-6): per-KA task table, key outputs, linked methodologies, and the canonical workflow sequence for greenfield engagements and change requests.

**One-paragraph:** Detailed reference for all six BABOK Knowledge Areas (KA-1 through KA-6): per-KA task table, key outputs, linked methodologies, and the canonical workflow sequence for greenfield engagements and change requests. This is a routing and reference index — it does not replace per-methodology folders. Use it to select KAs, sequence subagents, and audit artifact coverage.

## Applies If (ALL must hold)

- Starting a new BA engagement: scope which KAs apply and in what order.
- Routing a vague stakeholder request to the correct KA and downstream methodology.
- Building a multi-step agentic pipeline crossing several KAs (elicit → model → validate → trace).
- Auditing an existing BA artifact set for KA coverage gaps before a release gate.

## Skip If (ANY kills it)

- You already know the methodology — go straight to that methodology's folder.
- Pure product discovery with no formal requirements artifacts — use product-manager continuous-discovery instead.
- Pure UX research — use pro/ux/ux-researcher/ skills instead.
- One-off ad-hoc questions that produce no tracked artifact.

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

- parent skill: `pro/ba/business-analyst/`
