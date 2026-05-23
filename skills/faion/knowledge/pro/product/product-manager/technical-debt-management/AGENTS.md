---
slug: technical-debt-management
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Six-step technical-debt discipline (register -> score impact via interest × contagion / effort -> allocate capacity -> pay down -> prevent -> track) shared between PM and engineering with a quarterly capacity contract.
content_id: "759372ba0be34756"
complexity: medium
produces: spec
est_tokens: 5500
tags: [technical-debt, product-management, engineering, prioritization, roadmap]
---
# Technical Debt Management

## Summary

**One-sentence:** Six-step technical-debt discipline (register -> score impact via interest × contagion / effort -> allocate capacity -> pay down -> prevent -> track) shared between PM and engineering with a quarterly capacity contract.

**One-paragraph:** Typed debt register (design/code/test/infra/docs/dependency); impact score = (interest_per_month × contagion_factor) / paydown_effort; written quarterly capacity contract (% sprint for debt); prevention policy paired with every paydown; public visibility to non-engineering stakeholders. Output: debt-register YAML + capacity contract memo.

**Ефективно для:**

- Roadmap velocity видимо падає при стабільному headcount.
- Quarterly planning, де 15-20% capacity резервується на paydown.
- Post-P0 outage, що ідентифікував debt як root cause.
- Перед major architectural change (auth rewrite, billing migration).

## Applies If (ALL must hold)

- Roadmap velocity visibly declining despite stable headcount.
- Quarterly planning where 15-20% capacity is reserved for paydown.
- Post-P0 outage or regression cluster where the post-mortem identifies debt as root cause.
- Before a major architectural change (auth rewrite, billing migration).
- Multi-repo solopreneur portfolio where debt silently compounds in lower-traffic repos.

## Skip If (ANY kills it)

- Greenfield product <3 months of code (premature optimization).
- Throwaway prototype.
- Team explicitly running tracer-bullet methodology with debt-acceptable-by-design.
- Capacity contract already in force <=90 days with no trigger event.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Codebase ownership map | table | engineering |
| Recent incident log | table | SRE / on-call |
| Sprint capacity baseline | doc | team lead |
| Roadmap of next quarter | doc | PM |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[release-planning]] | Provides the release cadence the paydown capacity contract slots into. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: typed register, interest × contagion / effort score, capacity contract, prevention policy paired, public visibility | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for debt-register + capacity-contract | 850 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: untyped register, effort-only score, soft capacity, fix-without-prevention | 750 |
| `content/04-procedure.xml` | essential | 5-step procedure: inventory -> classify -> score -> contract -> prevent | 800 |
| `content/05-examples.xml` | medium | Worked debt register with capacity contract + prevention policy | 700 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on code age + velocity trend | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `debt-classify` | haiku | Tag debt items by type. |
| `impact-score` | sonnet | Compute interest × contagion / effort with cited evidence. |
| `capacity-contract-author` | sonnet | Draft the quarterly capacity contract memo. |

## Templates

| File | Purpose |
|------|---------|
| `templates/debt-register.md` | Debt register skeleton with type + interest + contagion + effort. |
| `templates/debt-prioritization-matrix.md` | Prioritization matrix template. |
| `templates/debt-hotspots.sh` | Compute hotspots from churn + bug density. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-technical-debt-management.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[release-planning]]
- [[product-lifecycle]]
- [[product-operations]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
