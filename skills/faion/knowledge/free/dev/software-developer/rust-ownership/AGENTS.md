# Rust Ownership Model

## Summary

Rust's ownership model eliminates memory errors and data races at compile time: each value has exactly one owner, ownership transfers on assignment (move semantics), and references borrow values temporarily under strict aliasing rules enforced by the borrow checker. Before writing a function body, answer three questions: does it consume, borrow, or share its inputs? Does it return owned data or a reference into existing data? Does it cross a thread boundary (requiring `Send + Sync`)?

## Why

Memory safety without GC is only achievable because the compiler enforces ownership rules statically. Every `clone()` added to silence the borrow checker is a sign the data layout or function signature is wrong, not that the checker is wrong. Fighting the borrow checker with `.clone()` or `Rc<RefCell<T>>` costs runtime performance and signals a design flaw.

## When To Use

- Any Rust project — ownership rules are always in effect
- Designing function signatures (consume vs borrow vs share decision is upfront)
- Translating algorithms from GC languages (Python, Go, JS) to Rust
- Refactoring code that fights the borrow checker with `.clone()` or `Rc<RefCell<T>>`
- Writing async code where `'static` and `Send + Sync` bounds appear

## When NOT To Use

- Tiny scripts where `.clone()` everywhere is acceptable — borrow-checker design costs more than it saves
- Procedural macros — token stream manipulation has different ownership idioms
- Wrapping C APIs via FFI — manual lifetime management dominates; standard ownership advice barely applies
- Code generated from schemas (Prost, sqlx) — accept the generated ownership shape

## Content

| File | What's inside |
|------|---------------|
| `content/01-ownership-rules.xml` | Core three rules, move semantics, borrowing rules, lifetime annotations |
| `content/02-smart-pointers.xml` | Box, Rc, RefCell, Arc, Mutex — when each applies and runtime costs |
| `content/03-patterns-and-antipatterns.xml` | Builder pattern, Copy/Clone traits, Cow, closure ownership, common antipatterns |

## Templates

| File | Purpose |
|------|---------|
| `templates/api-surface-cheatsheet.rs` | Canonical function signature patterns for Rust APIs |

## Scripts

none
