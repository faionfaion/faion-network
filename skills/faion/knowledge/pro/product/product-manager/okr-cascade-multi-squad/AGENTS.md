---
slug: okr-cascade-multi-squad
tier: pro
group: product
domain: pm
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Cascade a single company OKR set into 3-6 squad OKR sets with explicit cross-squad dependency edges, weekly check-in cadence, and a post-quarter retro that closes the loop.
content_id: "bb834b589eaafb77"
complexity: deep
produces: spec
est_tokens: 6700
tags: [okr, product-management, multi-team, cascading, dependencies, quarter-planning]
---
# OKR Cascade for Multi-Squad Product

## Summary

**One-sentence:** Cascade a single company OKR set into 3-6 squad OKR sets with explicit cross-squad dependency edges, weekly check-in cadence, and a post-quarter retro that closes the loop.

**One-paragraph:** Per-squad 1 Objective + 3-5 KRs; explicit dependency-edge graph across squads; weekly confidence check-ins (0-10) with blocker name; cause-tagged retros that feed next-quarter Objectives. Output: cascade graph (YAML) + per-squad OKR docs + weekly check-in log + post-quarter retro.

**Ефективно для:**

- Product у multi-squad org (3-6 squads, shared product surface).
- Quarterly planning, де команди формулюють незалежні OKRs без dependency awareness.
- OKR drift: squad-level KRs не складаються в company-level Objective.
- Promotion-time для Group PM: декілька squads потребують узгоджених планів.

## Applies If (ALL must hold)

- Product spans 3-6 squads sharing a customer surface.
- Quarterly planning is starting and squad OKRs need cross-team alignment.
- Previous quarter had cross-squad dependency surprises (Q3 'we needed their API').
- Squad-level KRs need traceability to company-level Objectives.
- Promotion to Group PM / Portfolio PM in progress.

## Skip If (ANY kills it)

- Single-squad product — overhead exceeds benefit.
- Team uses non-OKR framework (V2MOM, MBO) consistently.
- Quarter < 60 days where cascade overhead exceeds value.
- Pre-PMF squad where outcome metrics are too unstable for OKRs.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Company OKRs | YAML | exec / Head of Product |
| Squad roster | list with PM + tech lead per squad | org chart |
| Last quarter outcomes | scorecard | previous retro |
| Dependency map seed | best-guess edges | PMs |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[portfolio-strategy]] | Horizons constrain which Objectives the cascade flows from. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology: 1O-3-5KR, explicit dependency edges, KR-to-company trace, weekly cadence, cause-tagged retro | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema draft-07 for cascade graph + squad OKRs | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: implicit dependencies, KR drift, weekly skipped, retro without cause | 800 |
| `content/04-procedure.xml` | essential | 5-step procedure: company-OKR -> per-squad-draft -> dependency-edge -> sign -> cadence | 900 |
| `content/05-examples.xml` | medium | Worked Q2 cascade with explicit dependency on Identity squad | 800 |
| `content/06-decision-tree.xml` | essential | Apply/skip routing on squad count + cadence + framework | 650 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `cascade-graph-author` | sonnet | Build dependency graph from squad drafts. |
| `kr-traceability-audit` | haiku | Mechanical trace of squad KR -> company KR. |
| `retro-synthesis` | opus | Cross-squad pattern across cause-tagged outcomes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/squad-okr.md` | Per-squad OKR doc with O + 3-5 KRs + dependencies + check-in cadence. |
| `templates/dependency-graph.yaml` | Cascade graph YAML with {producer, consumer, deliverable, by_date} edges. |
| `templates/checkin.md` | Weekly check-in template with confidence + blocker. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-okr-cascade-multi-squad.py` | Validate the methodology output artefact against the schema in content/02-output-contract.xml | Pre-commit + CI on artefact changes |

## Related

- [[portfolio-strategy]]
- [[stakeholder-management]]
- [[release-planning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals to apply / skip / route-elsewhere, with each leaf referencing a rule id from `01-core-rules.xml`. Consult the tree before applying the methodology when signals are ambiguous.
