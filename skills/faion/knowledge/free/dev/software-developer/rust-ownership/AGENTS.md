---
slug: rust-ownership
tier: free
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Ownership eliminates memory errors at compile time.
content_id: "2e33e2effa6c9910"
tags: [rust, ownership, borrowing, memory-safety]
---
# Rust Ownership Model

## Summary

**One-sentence:** Ownership eliminates memory errors at compile time.

**One-paragraph:** Ownership eliminates memory errors at compile time. One owner per value; transfers on assignment. References borrow temporarily. Answer three questions before writing function bodies.

## Applies If (ALL must hold)

- Any Rust project — ownership rules are always in effect.
- Designing function signatures (consume vs borrow vs share decision is upfront).
- Translating algorithms from GC languages (Python, Go, JS) to Rust.
- Refactoring code that fights the borrow checker with .clone() or Rc<RefCell<T>>.
- Writing async code where 'static and Send + Sync bounds appear.

## Skip If (ANY kills it)

- Tiny scripts where .clone() everywhere is acceptable — borrow-checker design costs more than it saves.
- Procedural macros — token stream manipulation has different ownership idioms.
- Wrapping C APIs via FFI — manual lifetime management dominates; standard ownership advice barely applies.
- Code generated from schemas (Prost, sqlx) — accept the generated ownership shape.

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

- parent skill: `free/dev/software-developer/`
