---
slug: quality-attributes-analysis
tier: pro
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Quality Attributes Analysis (QAA) is the systematic process of identifying, prioritizing, and binding non-functional requirements (NFRs) to architectural decisions using ISO/IEC 25010:2023 characteristics, 6-part quality attribute scenarios, utility trees with (Importance, Difficulty) scoring, and ATAM-style trade-off analysis.
content_id: "c5723af11b05be4a"
tags: [quality-attributes, non-functional-requirements, architecture, atam, utility-trees]
---
# Quality Attributes Analysis

## Summary

**One-sentence:** Quality Attributes Analysis (QAA) is the systematic process of identifying, prioritizing, and binding non-functional requirements (NFRs) to architectural decisions using ISO/IEC 25010:2023 characteristics, 6-part quality attribute scenarios, utility trees with (Importance, Difficulty) scoring, and ATAM-style trade-off analysis.

**One-paragraph:** Quality Attributes Analysis (QAA) is the systematic process of identifying, prioritizing, and binding non-functional requirements (NFRs) to architectural decisions using ISO/IEC 25010:2023 characteristics, 6-part quality attribute scenarios, utility trees with (Importance, Difficulty) scoring, and ATAM-style trade-off analysis. The concrete rule: every (H,H) scenario must have an executable fitness function (load test, chaos drill, security scan) wired into CI/CD — a scenario without a test is decoration.

## Applies If (ALL must hold)

- Pre-architecture phase of a non-trivial system — surface NFRs that will drive structural decisions.
- Major architectural pivot (monolith → microservices, on-prem → cloud, sync → async).
- Investor / customer due diligence requiring evidence the architecture meets SLA / compliance promises.
- Postmortem after a performance, security, or availability incident that the original architecture did not anticipate.
- Multi-tenant or regulated domain (healthcare, finance, public sector) requiring ISO/IEC 25010 traceability.
- New team onboarding — utility tree + scenarios align priorities faster than any wiki page.

## Skip If (ANY kills it)

- Idea / prototype stage with fewer than 5 paying customers — quality attributes are imagined; bottleneck is product-market fit.
- Tactical sprint planning — utility trees are not a substitute for backlogs.
- Single-developer side project with no SLA — overhead exceeds value.
- Team will not revisit the artifact after the workshop — a one-shot ATAM is theater.
- Trade-offs are already political, not technical — no analysis method survives a pre-decided executive choice.

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

- parent skill: `pro/dev/software-architect/`
