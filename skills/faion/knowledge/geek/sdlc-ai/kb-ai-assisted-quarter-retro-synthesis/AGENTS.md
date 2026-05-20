---
slug: ai-assisted-quarter-retro-synthesis
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "7311f7aea0cb0afb"
summary: AI-assisted recipe to ingest multi-squad channels, tickets, DORA metrics, and closed incidents into a themed quarterly retro doc for product-dev teams.
tags: [retro, quarterly, multi-squad, ai-agent, dora, incident-review, themed-synthesis]
---
# AI-Assisted Multi-Squad Quarter Retro Synthesis

## Summary

**One-sentence:** AI-assisted recipe to ingest multi-squad channels, tickets, DORA metrics, and closed incidents into a themed quarterly retro doc for product-dev teams.

**One-paragraph:** Quarter-end retros across 3-6 squads produce sprawling notes from each squad plus tickets, Slack threads, DORA dashboards, and incident postmortems — synthesizing manually takes a senior PM 12-20 hours and quality varies. Mechanism: ingest 4 source types — (1) per-squad retros, (2) Jira/Linear tickets closed in quarter, (3) DORA metrics deltas (deploy frequency, lead time, MTTR, CFR), (4) closed incident postmortems — cluster into themes weighted by squad-coverage × business-impact, generate the OKR-retrospective + DORA narrative + incident learnings sections, propose Q+1 process changes. Output: a 4-6 page retro doc + an action backlog item set for Q+1 planning.

## Applies If (ALL must hold)

- product-dev team with 3-6 squads operating on quarterly OKR cadence
- per-squad retros are written + accessible to the synthesizer
- DORA metrics dashboard exists (LinearB, Sleuth, Swarmia, manual export)
- ticket system + incident postmortem repo are queryable
- PM / Director-of-Engineering owns the synthesis with deadline pressure

## Skip If (ANY kills it)

- single-squad team — manual retro is faster than agent setup
- no DORA data — use `kb-ai-assisted-lessons-learned-synthesis` (project-level) instead
- agile transformation in flux (squads reorganizing) — themes won't be stable
- regulated-data context where ticket / incident data can't be sent to LLM — use manual synthesis

## Prerequisites (must be true before starting)

- per-squad retro docs at known paths
- ticket export filtered to closed-in-quarter
- DORA metrics: current quarter + previous quarter for delta analysis
- incident postmortems for any P1/P2 incidents in quarter
- previous quarter's retro doc for trend reference
- LLM API access with long-context support (≥ 100k tokens)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/product/product-manager/okr-cascade-multi-squad` | Source of OKR data the retro reviews |
| `geek/sdlc-ai/kb-ai-assisted-lessons-learned-synthesis` | Similar synthesis pattern for project retros (this is the quarter / multi-squad variant) |
| `geek/sdlc-ai/inc-postmortem-auto-draft-no-publish` | Incident postmortem format the synthesis consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-source coverage, theme requires multi-squad presence, DORA trend over snapshot, incident-themed learning, retro doc ≤ 6 pages | ~950 |
| `content/02-output-contract.xml` | essential | Retro doc schema, theme schema with sources, Q+1 process changes schema | ~750 |
| `content/03-failure-modes.xml` | essential | 6 failure modes (single-squad over-representation, DORA snapshot trap, ignored incidents, blameful tone, Q+1 promise inflation, prior-quarter ghost) | ~950 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_source_normalization` | sonnet | Convert each source type to a common evidence schema |
| `multi_squad_theme_clustering` | opus | Cross-squad pattern detection |
| `dora_trend_narrative` | sonnet | Templated narrative from before/after metrics |
| `incident_learning_extraction` | sonnet | Pull learnings from postmortems with citation |
| `q_plus_1_process_proposals` | opus | Cross-theme cross-quarter reasoning |

## Templates

| File | Purpose |
|------|---------|
| `templates/quarterly-retro-doc.md` | 4-6 page retro doc skeleton |
| `templates/theme-with-sources.md` | Theme block with multi-source evidence |
| `templates/dora-trend-table.md` | DORA quarter-over-quarter table |
| `templates/q-plus-1-process-changes.md` | Next-quarter commitments |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/ingest-quarter-sources.py` | Pull from squad retros + Jira/Linear + DORA + postmortems | Quarter-end |
| `scripts/cluster-themes-multi-squad.py` | Cluster across sources weighted by squad coverage | Synthesis core |
| `scripts/validate-retro-doc.py` | Verify all themes have multi-source evidence + Q+1 actions have owners | Pre-publication |

## Related

- parent skill: `geek/sdlc-ai/`
- peer methodologies: `kb-ai-assisted-lessons-learned-synthesis`, `inc-postmortem-auto-draft-no-publish`, `okr-cascade-multi-squad`
- external: [DORA - State of DevOps reports](https://dora.dev/) · [Esther Derby - Agile Retrospectives](https://pragprog.com/titles/dlret/agile-retrospectives/) · [Charity Majors - Engineering Effectiveness](https://charity.wtf/)
