# Rust Ownership Model

## Summary

**One-sentence:** Forces a 3-question audit (who owns / who reads / who shares?) on every function signature before writing the body, producing a decision record that justifies move vs `&T` vs `&mut T` vs `Arc<T>`.

**One-paragraph:** Most Rust borrow-checker fights are signature problems, not body problems. By answering three questions BEFORE writing the body — does this function (1) consume the value, (2) read it, (3) need to share it across threads/scopes — you arrive at the only ownership shape the borrow checker will accept. Skipping the audit produces `.clone()` everywhere or `Rc<RefCell<T>>` because the author "needed mutability" — both are escape hatches that propagate complexity. This methodology pins the audit per signature, records the decision in a comment, and produces a per-module decision-record artifact.

**Ефективно для:**

- Переклад алгоритмів з Python/Go/JS на Rust — спочатку дизайн сигнатур, потім тіло.
- Refactor, де борровальник сваритися: розбираємось у сигнатурах, не додаємо `.clone()`.
- Async-код, де `'static` + `Send + Sync` bounds зненацька з'являються.
- Бібліотечний публічний API: forward-compatibility вимагає чіткої власності.

## Applies If (ALL must hold)

- Rust crate (any type — lib, bin, build-script).
- Function being designed/refactored has parameters whose ownership shape matters.
- Project uses stable Rust ≥1.65 (GATs, NLL).

## Skip If (ANY kills it)

- Throwaway scripts where `.clone()` everywhere is acceptable.
- Procedural macros — token-stream manipulation has different ownership idioms.
- FFI wrappers — manual lifetime management dominates; standard advice barely applies.
- Generated code (`prost`, `sqlx`) — accept the generated shape.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Function signature draft | Rust source | `src/` |
| Call-site list | `grep` output | `cargo check --message-format=json` |
| Concurrency requirement | yes/no | task spec |
| Crate edition | `2021` / `2024` | `Cargo.toml` |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Foundational. Feeds [[rust-error-handling]] (which decides what `Result::Err` variant owns). |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 rules: answer-3-questions, prefer-borrow, mut-only-if-needed, no-rc-refcell-default, arc-only-for-thread-share, lifetime-elision-or-explicit | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for per-function ownership decision record | 800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns: clone-everywhere, rc-refcell-as-default, str-vs-string-confusion, missing-lifetime-on-trait-return | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure per function: list callers → answer 3Q → write signature → check → commit | 700 |
| `content/06-decision-tree.xml` | essential | Routing: consumed? → shared? → mutated? → owned vs &T vs &mut T vs Arc | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `list_callers` | haiku | `grep` / `cargo check` output. |
| `answer_3_questions` | sonnet | Needs to understand call-site intent. |
| `pick_signature` | sonnet | Apply decision tree. |
| `cross_module_design` | opus | When the chosen signature affects 5+ files. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ownership-audit-comment.tmpl.rs` | 3-line comment template documenting the audit answers above each pub fn |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-ownership.py` | Validate decision-record JSON against schema | After audit completes |

## Related

- [[rust-error-handling]] — `Result::Err` variants own their data; ownership shapes apply.
- [[rust-testing]] — test fixtures often use `Arc` even when prod code does not — keep them separate.

## Decision tree

See `content/06-decision-tree.xml`. Root question: does the function need to keep the value after returning? → yes → consume (move); no → reference. Then: needs to modify? → `&mut T`; otherwise → `&T`. Then: shared across threads? → `Arc<T>` (or `Arc<Mutex<T>>` for shared mutable). All leaves reference rules from `01-core-rules.xml`.
