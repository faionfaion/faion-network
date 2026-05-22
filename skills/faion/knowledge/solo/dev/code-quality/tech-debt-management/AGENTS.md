---
slug: tech-debt-management
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Prioritization and payoff strategy for technical debt using a scoring formula (Impact x Risk x Interest / Cost), four execution strategies (Boy Scout, feature-attached, dedicated sprint, Strangler Fig), and CI/pre-commit gates to prevent accumulation.
content_id: "a3813b675c136f7f"
tags: [tech-debt, refactoring, prioritization, strangler-fig, quality-gates]
---
# Technical Debt Management

## Summary

**One-sentence:** Prioritization and payoff strategy for technical debt using a scoring formula (Impact x Risk x Interest / Cost), four execution strategies (Boy Scout, feature-attached, dedicated sprint, Strangler Fig), and CI/pre-commit gates to prevent accumulation.

**One-paragraph:** Prioritization and payoff strategy for technical debt using a scoring formula (Impact x Risk x Interest / Cost), four execution strategies (Boy Scout, feature-attached, dedicated sprint, Strangler Fig), and CI/pre-commit gates to prevent accumulation. The concrete rule: track debt as labels on existing feature tickets, never in a separate backlog — separate backlogs are where debt goes to die.

## Applies If (ALL must hold)

- Sprint planning where engineering velocity has visibly decayed and the team disagrees on which debt to address.
- Onboarding a new codebase where debt is undocumented and you need a quick triage of high-impact items.
- Setting up CI quality gates and pre-commit hooks to prevent debt accumulation on a fresh project.
- Planning a Strangler Fig migration of a legacy module that cannot be replaced atomically.
- Deciding between Boy Scout Rule, dedicated debt sprints, feature-attached payoff, or strangler-fig per debt item.

## Skip If (ANY kills it)

- Greenfield codebase younger than 6 months — there is no real debt yet, just inexperience; focus on prevention (linters, tests, ADRs).
- Codebase you intend to throw away in less than 3 months — paying down debt on a doomed system is sunk cost.
- During an outage / launch crunch — debt management requires calm and capacity.
- As a substitute for refactoring patterns — debt management is prioritization; the actual code work is in refactoring-patterns.
- Solo project with no other contributors — most debt frameworks optimize for team coordination overhead you do not have.

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

- parent skill: `solo/dev/code-quality/`
