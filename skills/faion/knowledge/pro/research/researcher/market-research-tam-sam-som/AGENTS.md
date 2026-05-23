---
slug: market-research-tam-sam-som
tier: pro
group: research
domain: research
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Triangulates TAM/SAM/SOM with both top-down (industry report scaled) and bottom-up (price x reachable units) numbers; demands both to agree within 30% and refuses single-source figures.
content_id: "bb8d6b2d66706f2a"
complexity: medium
produces: report
est_tokens: 5000
tags: [market-sizing, tam, sam, som, triangulation]
---
# Market Research: TAM/SAM/SOM

## Summary

**One-sentence:** Triangulates TAM/SAM/SOM with both top-down (industry report scaled) and bottom-up (price x reachable units) numbers; demands both to agree within 30% and refuses single-source figures.

**One-paragraph:** Computes TAM (Total Addressable Market), SAM (Serviceable Available Market), and SOM (Serviceable Obtainable Market) using a triangulation pattern: one top-down number (industry report scaled), one bottom-up number (price x reachable units), reconciliation when they disagree by more than 30%. Output ships SOM as the revenue ceiling that business-model-research consumes.

**Ефективно для:**

- Ideation: треба підтвердити, чи ринок взагалі достатньо великий.
- Pitch deck або investor memo з 'market size' slide.
- Pre-spec: вибір ніші серед 2-3 кандидатів.
- Geographic expansion: чи варто йти на новий ринок (DE / BR / IN).
- Quarterly market refresh: чи виросла SOM з минулого разу.

## Applies If (ALL must hold)

- Ideation stage: confirm the market is large enough to justify product investment.
- Pitch deck or investor memo with a 'market size' slide.
- Pre-spec niche selection among 2-3 candidates.
- Geographic expansion decision (DE / BR / IN).
- Quarterly market refresh: did SOM grow since last cycle?

## Skip If (ANY kills it)

- Product already at scale with real ARR - track penetration, not market size.
- Internal tool with a captive audience (employees).
- Government / grant work where market size is irrelevant.
- Hobby project with no revenue target.
- Category-creation play where TAM cannot be sized yet.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Category definition | 1 sentence | founder / positioning doc |
| Geography list | ISO country codes | GTM doc |
| Ideal customer profile | persona doc | persona-building |
| Price band | USD/EUR | business-model-research or competitor pricing |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[persona-building]] | supplies the reachable-units denominator |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip gate | ~1200 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns (symptom/root-cause/fix) | ~900 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | ~900 |
| `content/05-examples.xml` | essential | Worked example trace | ~900 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule id | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `top-down-pull` | haiku | Mechanical pull of industry-report numbers + URL citation. |
| `bottom-up-build` | sonnet | Reasoning: price x reachable units within geo + ICP. |
| `triangulate` | sonnet | Reconcile top-down vs bottom-up if delta > 30%. |
| `som-confidence` | sonnet | Score SOM confidence high/medium/low with reason. |

## Templates

| File | Purpose |
|------|---------|
| `templates/market-sizing-report.md` | Full TAM/SAM/SOM report skeleton with triangulation |
| `templates/quick-market-check.md` | Lightweight check (TAM + SOM only) for early ideation |
| `templates/tam-triangulate.sh` | Bash helper to compute SOM and reconciliation delta |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-market-research-tam-sam-som.py` | Validate the artefact against `content/02-output-contract.xml` schema | CI on each artefact change; pre-commit |

## Related

- [[business-model-research]]
- [[persona-building]]
- [[competitor-analysis]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals onto a rule id from `content/01-core-rules.xml`, so the agent can decide in one read whether to run the methodology, halt, or route elsewhere. Use it whenever the inputs feel ambiguous.
