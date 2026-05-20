---
slug: trade-off-decision-methods
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Structured evaluation methods for architecture trade-offs, from the full ATAM workshop (3-4 days, Type 1 irreversible decisions) to lightweight alternatives (Mini-ATAM, TARA, LAAAM) for sprint-level choices.
content_id: "a7d04a84c65565df"
tags: [atam, architecture, trade-off, quality-attributes, decision-making]
---
# Architecture Trade-off Decision Methods

## Summary

**One-sentence:** Structured evaluation methods for architecture trade-offs, from the full ATAM workshop (3-4 days, Type 1 irreversible decisions) to lightweight alternatives (Mini-ATAM, TARA, LAAAM) for sprint-level choices.

**One-paragraph:** Structured evaluation methods for architecture trade-offs, from the full ATAM workshop (3-4 days, Type 1 irreversible decisions) to lightweight alternatives (Mini-ATAM, TARA, LAAAM) for sprint-level choices. Select method depth based on decision reversibility.

## Applies If (ALL must hold)

- Major architecture decisions, system redesigns, technology migrations — use full ATAM.
- Sprint-level decisions with moderate quality attribute impact — use Mini-ATAM (half day).
- Focused quality attribute analysis within a bounded scope — use TARA (2-4 hours).
- Iterative architecture evaluation across incremental design sessions — use LAAAM (1 day).
- Evaluating reference architectures or architectural frameworks — use ATRAF.

## Skip If (ANY kills it)

- Type-2 reversible decisions (library choice, CSS framework) — analysis paralysis costs more than the wrong choice.
- When there is no real choice — only one option meets a hard constraint. Skip the method; document the constraint.
- When stakeholders have not been identified yet — agents will invent generic personas and the output looks plausible but binds nobody.
- Pure cost questions answered by a spreadsheet (TCO over 3 years with known unit prices).

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

- parent skill: `solo/dev/software-architect/`
