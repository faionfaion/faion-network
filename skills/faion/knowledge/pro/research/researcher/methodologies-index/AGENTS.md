---
slug: methodologies-index
tier: pro
group: research
domain: researcher
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Routing table mapping 22 research methodology slugs to one of 5 topic files (idea-generation, market-analysis, user-research, business-model-planning, naming-and-domains) and to the corresponding faion-research-agent mode.
content_id: "2240d98bb7d9e509"
tags: [research, index, routing, methodology, agent-mode]
---
# Methodologies Index

## Summary

**One-sentence:** Routing table mapping 22 research methodology slugs to one of 5 topic files (idea-generation, market-analysis, user-research, business-model-planning, naming-and-domains) and to the corresponding faion-research-agent mode.

**One-paragraph:** Routing table mapping 22 research methodology slugs to one of 5 topic files (idea-generation, market-analysis, user-research, business-model-planning, naming-and-domains) and to the corresponding faion-research-agent mode. Use this index as the O(1) entry point: resolve slug, open the topic file, then read the canonical per-folder methodology if depth is needed.

## Applies If (ALL must hold)

- Resolving a slug (e.g. jobs-to-be-done) to its topic file (user-research.md) before reading.
- Routing an orchestrator to the correct topic file before spawning a research subagent.
- Mapping a methodology slug to the matching faion-research-agent mode (ideas, market, competitors, validate, personas, pains, niche, pricing, names).
- Discovering peer methodologies inside the same topic group when planning a multi-step research task.
- Sanity-checking that a slug still exists before referencing it from a spec or plan document.

## Skip If (ANY kills it)

- As the source of truth for methodology content — fields here are abridged stubs; open the referenced topic file or canonical per-folder methodology.xml for the full body.
- For agent-integration patterns per methodology — those live in each methodology's own folder under pro/research/researcher/ and pro/research/market-researcher/.
- For mode routing in orchestrators — the canonical mode table is in ../CLAUDE.md (## Research Modes); this index mirrors it for read-only lookup, not mutation.
- For methodologies outside the 22 covered here (e.g. opportunity-solution-trees, audience-segmentation) — those are tracked in their own per-folder methodology.xml files.

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

- parent skill: `pro/research/researcher/`
