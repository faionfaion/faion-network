# Design Patterns Overview

## Summary

Design patterns are language-agnostic solutions to recurring software design problems, grouped into three GoF categories (Creational, Structural, Behavioral) plus Architectural and Distributed/Cloud-Native patterns. This overview is the routing layer: it maps problems to pattern categories and points to the deep-dive methodologies for each category. Use it to select a pattern; use the category-specific methodology to implement it.

## Why

Without a shared pattern vocabulary, teams rediscover the same solutions inconsistently, accumulate coupling, and resist change. Patterns encode decades of proven trade-off decisions — knowing that "add behavior without subclassing" maps to Decorator, not inheritance, prevents entire classes of design mistakes. Modern language features (first-class functions, module systems, DI frameworks) have replaced some classic patterns but the structural vocabulary remains the fastest shared communication tool.

## When To Use

- Identifying which pattern applies to a new design problem
- Reviewing code for pattern misuse or missed pattern opportunities
- Communicating design intent to teammates using shared vocabulary
- Choosing between similar patterns (Adapter vs Facade, Proxy vs Decorator)
- Understanding architectural patterns (Clean, Hexagonal, Layered) before selecting one
- Learning which distributed patterns (CQRS, Saga, Outbox, Circuit Breaker) address a given distributed-system concern

## When NOT To Use

- Applying a pattern because it sounds sophisticated — only apply when the problem it solves actually exists
- When a simple function or module achieves the same goal as a class-based pattern
- Forcing GoF patterns onto functional or reactive codebases where first-class functions already solve the problem
- Using this overview as a substitute for the category-specific methodology when implementing (load creational-patterns, structural-patterns, or behavioral-patterns instead)

## Content

| File | What's inside |
|------|---------------|
| `content/01-gof-catalog.xml` | All 23 GoF patterns: Creational (5), Structural (7), Behavioral (11) — name, problem solved, canonical use case |
| `content/02-architectural-patterns.xml` | Layered, Clean, Hexagonal architectures — key principles and when to choose each |
| `content/03-distributed-patterns.xml` | Resilience (Circuit Breaker, Bulkhead, Retry, Timeout, Fallback) and data patterns (CQRS, Event Sourcing, Saga, Outbox, Repository) |
| `content/04-selection-guide.xml` | Decision rules: scenario → pattern mapping; modern language alternatives to classic patterns; AI-influenced patterns (RAG, Agent, Guardrail) |

## Templates

none
