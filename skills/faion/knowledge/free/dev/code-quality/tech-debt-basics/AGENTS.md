---
slug: tech-debt-basics
tier: free
group: dev
domain: code-quality
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: A framework for making technical debt visible, typed, and actionable.
content_id: "d3129117f85edec8"
tags: [technical-debt, code-quality, risk-management, refactoring, monitoring]
---
# Technical Debt Basics

## Summary

**One-sentence:** A framework for making technical debt visible, typed, and actionable.

**One-paragraph:** A framework for making technical debt visible, typed, and actionable. Debt items are classified in Martin Fowler's quadrant (deliberate/inadvertent × reckless/prudent) and tracked in a TECH_DEBT_REGISTER.md with type, severity, location, evidence, and interest cost. Agents scan for candidates; humans approve before items are registered. Cap the register at 20–30 items.

## Applies If (ALL must hold)

- Sprint/quarterly planning: surface debt before picking payoff items.
- Post-incident review: register the debt that caused the incident with severity and evidence.
- New-codebase onboarding: inventory existing debt before estimating work.
- Feature trade-off: deliberately taking prudent debt and logging it in the same commit.

## Skip If (ANY kills it)

- Greenfield prototypes likely to be thrown away — registering debt is overhead with no reader.
- Sub-100-line scripts where the debt framework is heavier than the code.
- Code under active full rewrite — log the rewrite, not item-level debt deleted next week.
- Teams with no payoff process — registering debt no one will pay is theatre.

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

- parent skill: `free/dev/code-quality/`
