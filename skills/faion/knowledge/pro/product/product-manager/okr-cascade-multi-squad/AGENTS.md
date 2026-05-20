---
slug: okr-cascade-multi-squad
tier: pro
group: product
domain: product-manager
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "22239c99b0227706"
summary: Cascades a single company OKR set into 3-6 squad OKR sets with explicit dependency edges, weekly check-in cadence, and post-quarter retro.
tags: [okr, product-management, multi-team, cascading, dependencies, quarter-planning]
---
# OKR Cascade for Multi-Squad Product

## Summary

**One-sentence:** Cascades a single company OKR set into 3-6 squad OKR sets with explicit dependency edges, weekly check-in cadence, and post-quarter retro.

**One-paragraph:** Existing single-team OKR methodology covers the "draft one OKR" step but not the harder coordination problem: how do you take 3 company-level Objectives, decompose them into ~12-18 squad-level KRs spread across 3-6 squads, declare the dependency edges between squads (who blocks whom), and run a weekly-review cadence that catches drift before quarter-end. Mechanism: starts from a finalized company set (max 3 Os, 3-5 KRs each), assigns one accountable squad per company KR (single-threaded ownership per Christina Wodtke), generates squad-level KRs with the "directional KR + measurable KR" pair, builds a directed dependency graph in Markdown, and registers a Monday 30-min cross-squad standup + a Friday async confidence-vote (0.0-1.0 per Wodtke). Primary output: a per-squad OKR doc, a `dependencies.md` adjacency list, and a quarterly retro template.

## Applies If (ALL must hold)

- product team has 3-6 squads with stable membership for the quarter
- a company-level OKR set already exists and is signed off by founders/leadership
- previous quarter's OKR scoring (0.0-1.0 per KR) is available for retro baselines
- product manager owns coordination across squads (not a chapter lead, not a delivery PM)

## Skip If (ANY kills it)

- single squad / single-team org — use `okr-setting` (it covers exactly this scope)
- < 3 squads — dependency graph degenerates to direct conversations; cascading overhead is waste
- > 8 squads — pyramidal cascade with a portfolio layer needed; use `portfolio-strategy` first
- Annual / no-quarter cadence — methodology assumes 12-13 week quarter rhythm
- OKRs are still being drafted at the company level — finish `okr-setting` first

## Prerequisites (must be true before starting)

- company OKR document (signed-off Markdown / Notion / Google Doc) with 1-3 Os and 3-5 KRs each
- squad roster: name, mission statement (one sentence), tech lead, designer, PM partner if any
- previous quarter retro notes (if Q2+) — used as confidence-vote baseline
- shared OKR tool decided: spreadsheet, Mooncamp, Quantive, or plain Markdown in repo

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager/release-planning` | Consumes cascaded KRs to seed release scope per squad |
| `pro/pm/project-manager/raci-matrix` | Used to disambiguate owner vs contributor squads on shared KRs |
| `solo/product/product-manager/okr-setting` | Upstream — produces the company-level OKR set this methodology cascades from |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: max-3-Os, single-threaded ownership, dependency edges declared, confidence-vote cadence, retro-before-next | ~900 |
| `content/02-output-contract.xml` | essential | Squad OKR schema, dependency graph schema, forbidden patterns | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (sandbagging, KR-as-task, hidden dependencies, no retro, founder override) | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `squad_okr_first_draft_per_squad` | sonnet | Bounded transformation: company KR + squad mission → squad KR draft |
| `dependency_graph_synthesis` | opus | Cross-squad reasoning, needs to spot transitive blockers |
| `weekly_checkin_summary` | haiku | Template fill: status + confidence + blockers, low complexity |
| `quarter_retro_synthesis` | opus | Cross-squad cross-quarter narrative |

## Templates

| File | Purpose |
|------|---------|
| `templates/squad-okr.md` | Per-squad OKR doc skeleton (objective + 3-5 KRs + dependencies + check-in log) |
| `templates/dependencies.md` | Cross-squad dependency graph as Markdown adjacency list |
| `templates/weekly-checkin.md` | Monday 30-min standup agenda + Friday confidence-vote template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/check-cascade-coverage.py` | Verify every company KR has exactly one accountable squad | After draft, before publish |
| `scripts/aggregate-confidence-votes.py` | Roll up squad votes into a portfolio dashboard | Friday end of each week |

## Related

- parent skill: `pro/product/product-manager/`
- peer methodologies: `release-planning`, `portfolio-strategy`, `experimentation-at-scale`
- external: [Christina Wodtke - Radical Focus](https://eleganthack.com/the-art-of-the-okr/) · [Re:Work OKRs](https://rework.withgoogle.com/guides/set-goals-with-okrs/) · [What Matters - Doerr](https://www.whatmatters.com/)
