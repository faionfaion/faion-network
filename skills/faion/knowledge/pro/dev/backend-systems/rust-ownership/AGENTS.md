---
slug: rust-ownership
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Rust's ownership system enforces memory safety without GC: each value has one owner, borrows are either multiple shared (&T) or one exclusive (&mut T), and lifetimes express reference validity across scope boundaries.
content_id: "2e33e2effa6c9910"
tags: [rust, ownership, borrowing, lifetimes]
---
# Rust Ownership Model

## Summary

**One-sentence:** Rust's ownership system enforces memory safety without GC: each value has one owner, borrows are either multiple shared (&T) or one exclusive (&mut T), and lifetimes express reference validity across scope boundaries.

**One-paragraph:** Rust's ownership system enforces memory safety without GC: each value has one owner, borrows are either multiple shared (&T) or one exclusive (&mut T), and lifetimes express reference validity across scope boundaries. Use Arc<T> for read-only sharing across threads, Arc<Mutex<T>> for shared mutable state, and Cow<'a, str> to avoid cloning when the input might not need mutation. Pass &str/&[T]/&Path in function signatures; only accept String/Vec<T> when storing.

## Applies If (ALL must hold)

- New contributor (human or LLM) writing code that crosses function or thread boundaries with non-Copy types.
- Reviewing PRs that introduce Clone, Rc, Arc, RefCell, or lifetime annotations.
- Designing data flow for a long-running service (connection pool ownership, shared mutable state).
- Refactoring code that compiles only because of excessive clone() calls.
- Modeling builder/typestate APIs that consume self to enforce state machines.

## Skip If (ANY kills it)

- Pure-CPU numeric code on Copy primitives — borrow checker rarely fires.
- One-off scripts or examples/ where clone() cost is irrelevant.
- FFI thin wrappers where lifetimes are dictated by the C API.
- Throwaway prototypes — fighting the borrow checker before the design is settled wastes tokens.

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

- parent skill: `pro/dev/backend-systems/`
