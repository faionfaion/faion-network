---
slug: ai-assisted-specification-writing
tier: geek
group: sdd
domain: sdd
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: AI-assisted specification workflow at the planning layer: translate a product concept or backlog item into spec.
content_id: "8daa6240b93f156a"
tags: [specification, sdd-planning, requirements, implementation-plan, ai-assisted]
---
# AI-Assisted Specification Writing (SDD Planning)

## Summary

**One-sentence:** AI-assisted specification workflow at the planning layer: translate a product concept or backlog item into spec.

**One-paragraph:** AI-assisted specification workflow at the planning layer: translate a product concept or backlog item into spec.md + implementation-plan.md before the design phase. The agent reads feature intent, asks clarifying questions, generates FR list with Given-When-Then acceptance criteria, then generates task breakdown with token estimates. Human approval is required before implementation tasks are created.

## Applies If (ALL must hold)

- At the sdd-planning phase: translating a product concept or backlog item into a structured spec.md before the design phase starts
- When a feature ticket (e.g., Linear issue, Jira story) exists but the acceptance criteria are vague or missing
- For sprint planning: AI drafts specifications for upcoming sprint items so the team can review and approve them in advance
- When iterative refinement of a rough draft spec is needed — using an AI dialogue to progressively sharpen requirements
- For generating task breakdowns (implementation-plan.md) from an approved spec

## Skip If (ANY kills it)

- As a replacement for stakeholder discovery — AI cannot substitute for interviews, user research, or business requirements sessions
- When the spec is a regulatory artifact (e.g., FDA submission, GDPR DPA) — legal precision is beyond AI spec generation reliability
- For real-time collaborative specification during a meeting — the async AI drafting + human review loop is not suited for synchronous sessions
- When no product context is available — agent cannot invent a business model or market requirements

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

- parent skill: `geek/sdd/sdd-planning/`
