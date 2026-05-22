---
slug: patterns-overview
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Design patterns are language-agnostic solutions to recurring software design problems, grouped into three GoF categories (Creational, Structural, Behavioral) plus Architectural and Distributed/Cloud-Native patterns.
content_id: "b5deacf85d0bbd6f"
tags: [design-patterns, gof, architectural-patterns, distributed-patterns, pattern-selection]
---
# Design Patterns Overview

## Summary

**One-sentence:** Design patterns are language-agnostic solutions to recurring software design problems, grouped into three GoF categories (Creational, Structural, Behavioral) plus Architectural and Distributed/Cloud-Native patterns.

**One-paragraph:** Design patterns are language-agnostic solutions to recurring software design problems, grouped into three GoF categories (Creational, Structural, Behavioral) plus Architectural and Distributed/Cloud-Native patterns. This overview is the routing layer: it maps problems to pattern categories and points to the deep-dive methodologies for each category. Use it to select a pattern; use the category-specific methodology to implement it.

## Applies If (ALL must hold)

- Identifying which pattern applies to a new design problem
- Reviewing code for pattern misuse or missed pattern opportunities
- Communicating design intent to teammates using shared vocabulary
- Choosing between similar patterns (Adapter vs Facade, Proxy vs Decorator)
- Understanding architectural patterns (Clean, Hexagonal, Layered) before selecting one
- Learning which distributed patterns (CQRS, Saga, Outbox, Circuit Breaker) address a given distributed-system concern

## Skip If (ANY kills it)

- Applying a pattern because it sounds sophisticated — only apply when the problem it solves actually exists
- When a simple function or module achieves the same goal as a class-based pattern
- Forcing GoF patterns onto functional or reactive codebases where first-class functions already solve the problem
- Using this overview as a substitute for the category-specific methodology when implementing (load creational-patterns, structural-patterns, or behavioral-patterns instead)

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
