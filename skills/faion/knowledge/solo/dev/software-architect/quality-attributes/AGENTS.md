---
slug: quality-attributes
tier: solo
group: dev
domain: software-architect
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Identify, prioritize, and document non-functional requirements (NFRs) using ISO 25010 quality characteristics, scenario-driven specification, SLI/SLO definitions, and ATAM-style trade-off analysis.
content_id: "8ef1d6b911be325d"
tags: [quality-attributes, non-functional-requirements, slo, atam, iso-25010]
---
# Quality Attributes Framework

## Summary

**One-sentence:** Identify, prioritize, and document non-functional requirements (NFRs) using ISO 25010 quality characteristics, scenario-driven specification, SLI/SLO definitions, and ATAM-style trade-off analysis.

**One-paragraph:** Identify, prioritize, and document non-functional requirements (NFRs) using ISO 25010 quality characteristics, scenario-driven specification, SLI/SLO definitions, and ATAM-style trade-off analysis. Quality attributes must be testable: every attribute has a scenario with a measurable response measure before design decisions are made.

## Applies If (ALL must hold)

- Architecture design phase: before selecting architecture style, database, or communication pattern.
- During ATAM (Architecture Tradeoff Analysis Method) workshops to elicit and prioritize quality requirements from stakeholders.
- When writing NFR specifications for a new service, product, or major feature increment.
- Pre-launch: defining SLOs and alerting thresholds grounded in user-journey impact analysis.
- Technical debt triage: deciding which quality deficits to address first based on user and business impact.

## Skip If (ANY kills it)

- Throwaway prototypes where shipping speed is the only constraint.
- Single-user internal tools where availability, scalability, and security requirements are trivially low.
- As a substitute for actual measurement — quality attribute scenarios define what to measure, not the measurement itself.

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
