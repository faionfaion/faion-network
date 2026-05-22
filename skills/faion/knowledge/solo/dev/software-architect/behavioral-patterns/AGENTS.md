---
slug: behavioral-patterns
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Nine GoF behavioral patterns for controlling how objects communicate and distribute responsibilities at runtime.
content_id: "e54decf8a51ed833"
tags: [design-patterns, behavioral, gof, refactoring, architecture]
---
# Behavioral Design Patterns

## Summary

**One-sentence:** Nine GoF behavioral patterns for controlling how objects communicate and distribute responsibilities at runtime.

**One-paragraph:** Nine GoF behavioral patterns for controlling how objects communicate and distribute responsibilities at runtime. Strategy, Observer, and Command handle algorithm selection and operation history. State, Chain of Responsibility, Template Method, and Mediator manage complex flows and component interaction. Iterator and Visitor provide traversal and operation abstraction. Apply them when measured code smells — cyclomatic complexity >15, repeated switch-on-type, growing if-state chains — justify the abstraction cost. Start with the simplest representation (function, lookup table); promote to a class-based pattern only when type signatures or shared state demand it.

## Applies If (ALL must hold)

- Code review: long switch/match on type, duplicated event-listener boilerplate, or growing if/else state machines.
- New feature: multiple algorithms selectable at runtime (Strategy), domain events fan-out to N consumers (Observer), explicit state machine with guards (State).
- Refactoring a monolithic class into smaller testable pieces by externalizing variable behavior.
- Building extensible middleware/handler chains (Chain of Responsibility): request validation, auth pipelines, log enrichers.
- LLM-driven code generation that needs a vocabulary of named patterns to constrain output and keep code idiomatic.

## Skip If (ANY kills it)

- Two-line if/else with one likely future variant — pattern overhead outweighs benefit; revisit at third variant.
- Pure data-transformation pipelines mapping cleanly to functions or streams — patterns add ceremony.
- Languages with first-class FP idioms (Rust, Haskell, modern TS) — many GoF behavioral patterns reduce to higher-order functions.

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
