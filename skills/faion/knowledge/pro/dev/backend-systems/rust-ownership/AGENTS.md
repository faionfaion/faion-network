# Rust Ownership Model

## Summary

Rust's ownership system enforces memory safety without GC: each value has one owner, borrows are either multiple shared (`&T`) or one exclusive (`&mut T`), and lifetimes express reference validity across scope boundaries. Use `Arc<T>` for read-only sharing across threads, `Arc<Mutex<T>>` for shared mutable state, and `Cow<'a, str>` to avoid cloning when the input might not need mutation. Pass `&str`/`&[T]`/`&Path` in function signatures; only accept `String`/`Vec<T>` when storing.

## Why

The borrow checker is the primary correctness mechanism in Rust. Most agent-generated Rust code fails because LLMs reach for `.clone()` or `'static` bounds to silence compiler errors rather than restructuring the ownership graph. A plan-then-implement loop — draft the ownership topology first, then code one module at a time with `cargo check` as the feedback signal — catches structural mistakes before they cascade.

## When To Use

- New contributor (human or LLM) writing code that crosses function or thread boundaries with non-Copy types.
- Reviewing PRs that introduce `Clone`, `Rc`, `Arc`, `RefCell`, or lifetime annotations.
- Designing data flow for a long-running service (connection pool ownership, shared mutable state).
- Refactoring code that compiles only because of excessive `clone()` calls.
- Modeling builder/typestate APIs that consume `self` to enforce state machines.

## When NOT To Use

- Pure-CPU numeric code on `Copy` primitives — borrow checker rarely fires.
- One-off scripts or `examples/` where `clone()` cost is irrelevant.
- FFI thin wrappers where lifetimes are dictated by the C API.
- Throwaway prototypes — fighting the borrow checker before the design is settled wastes tokens.

## Content

| File | What's inside |
|------|---------------|
| `content/01-ownership-rules.xml` | Move semantics, Copy vs Clone, borrowing rules, lifetime basics. |
| `content/02-smart-pointers.xml` | `Box`, `Rc`, `RefCell`, `Arc`, `Mutex`, `Cow`; when to use each. |
| `content/03-patterns.xml` | Builder pattern consuming `self`, struct ownership, closures capturing by move. |
| `content/04-gotchas.xml` | Self-referential structs, async + borrows with `tokio::spawn`, `'static` misuse, clone abuse. |

## Templates

| File | Purpose |
|------|---------|
| `templates/audit-clones.sh` | Clippy script surfacing needless `clone()`, `to_string()`, `to_owned()` calls in a crate. |
