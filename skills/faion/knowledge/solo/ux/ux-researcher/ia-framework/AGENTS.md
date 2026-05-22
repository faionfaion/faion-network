---
slug: ia-framework
tier: solo
group: ux
domain: ux
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Information architecture (IA) is the structural design of shared information environments.
content_id: "31838a185658da75"
tags: [information-architecture, navigation, content-organization, findability, taxonomy]
---
# Information Architecture - Framework

## Summary

**One-sentence:** Information architecture (IA) is the structural design of shared information environments.

**One-paragraph:** Information architecture (IA) is the structural design of shared information environments. It involves organizing, labeling, and creating navigation systems that help users find and understand information. A robust IA framework prevents low findability, user frustration, increased support costs, and poor scalability as content grows.

## Applies If (ALL must hold)

- At the start of a product or site build, before any navigation or page structure is committed to code.
- When users consistently report they cannot find things and analytics confirm high search usage and low direct navigation.
- During a content migration or redesign where the existing structure needs to be evaluated and reorganized.
- When adding a new content type or feature to an existing product — to validate it fits the current IA before creating a one-off page.
- When onboarding stakeholders who need to understand the product's structural logic before contributing content.

## Skip If (ANY kills it)

- For single-purpose tools with fewer than 10 distinct screens — a simple user flow diagram suffices.
- When the product's navigation is already well-validated by tree testing and usability data — redo IA only when evidence warrants it.
- As the first step in a research process; IA should follow user research (card sorting, interviews), not precede it.
- When the team has no authority over navigation or content organization (e.g., working inside a locked CMS template).

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

- parent skill: `solo/ux/ux-researcher/`
