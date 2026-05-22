---
slug: decision-tree-process
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Six-phase process for making architecture decisions systematically: (1) problem definition, (2) options generation, (3) trade-off analysis, (4) technical and stakeholder validation, (5) ADR documentation, (6) implementation planning.
content_id: "6733eaa84b9a7baa"
tags: [decision-process, architecture-decisions, trade-off-analysis, adr, decision-matrix]
---
# Architecture Decision Process

## Summary

**One-sentence:** Six-phase process for making architecture decisions systematically: (1) problem definition, (2) options generation, (3) trade-off analysis, (4) technical and stakeholder validation, (5) ADR documentation, (6) implementation planning.

**One-paragraph:** Six-phase process for making architecture decisions systematically: (1) problem definition, (2) options generation, (3) trade-off analysis, (4) technical and stakeholder validation, (5) ADR documentation, (6) implementation planning. This is the meta-process; the domain-specific trees (architecture-style, tech-stack, cloud-provider, build-vs-buy) are inputs to phase 2.

## Applies If (ALL must hold)

- Any significant architecture choice — style, technology, database, cloud provider, build vs buy.
- Decisions that are hard or expensive to reverse (one-way doors): cloud provider, architecture style, core frameworks.
- Cross-team decisions where stakeholder alignment and documentation are essential.
- Any decision where "why did we choose this?" will be asked in 12+ months.

## Skip If (ANY kills it)

- Trivial reversible decisions (library choice, CLI tool) — lightweight ADR or comment in PR is sufficient.
- Decisions already made and working well — run the process only at planned review intervals.
- Time-critical emergencies where speed matters more than process — decide, act, document retroactively.

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
