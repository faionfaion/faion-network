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
| `content/01-core-rules.xml` | essential | 11 rules: single-owner-clear, borrow-rules-shared-or-exclusive, answer-3-questions, prefer-borrow, mut-only-if-needed, no-rc-refcell-default, arc-only-for-thread-share, arc-mutex-across-threads, no-clone-as-shortcut, lifetime-elision-or-explicit, clone-audit-in-ci (+ skip leaf) | 1700 |
| `content/02-output-contract.xml` | essential | JSON Schema for per-function ownership decision record + crate_audit block + forbidden patterns | 1000 |
| `content/03-failure-modes.xml` | essential | 6 antipatterns: rc-refcell-across-spawn, elided-lifetime-on-returned-ref, clone-everywhere, rc-refcell-as-default, str-vs-string-confusion, missing-lifetime-on-trait-return | 1000 |
| `content/04-procedure.xml` | essential | 5-step per-function procedure (list callers → answer 3Q → signature → check → record) + 3 crate-level steps (clone audit → Rc-across-threads sweep → CI gate) | 1000 |
| `content/06-decision-tree.xml` | essential | Routing: skip leaf → consumed? → shared? → mutated? → owned vs &T vs &mut T vs Arc, plus 6 crate-level audit gates | 900 |

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
| `templates/audit-clones.sh` | Crate-level audit: clippy clone lints, clone-count baseline, Rc/RefCell-across-spawn scan |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-ownership.py` | Validate decision-record JSON against schema | After audit completes |

## Related

- [[rust-error-handling]] — `Result::Err` variants own their data; ownership shapes apply.
- [[rust-testing]] — test fixtures often use `Arc` even when prod code does not — keep them separate.

## Decision tree

See `content/06-decision-tree.xml`. Root question: does the function need to keep the value after returning? → yes → consume (move); no → reference. Then: needs to modify? → `&mut T`; otherwise → `&T`. Then: shared across threads? → `Arc<T>` (or `Arc<Mutex<T>>` for shared mutable). All leaves reference rules from `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/ownership-audit-comment.tmpl.rs`

```rust
// Ownership audit:
//   keeps_value:           false   // does this fn store / return the value?
//   modifies_value:        false   // does it write through the param?
//   shares_across_threads: false   // does any path spawn with the value?
// → param_kind: shared-ref (&T)
pub fn example(input: &str) -> usize {
    input.len()
}
```

### `templates/audit-clones.sh`

```bash
set -euo pipefail

cargo clippy --all-targets -- \
  -W clippy::needless_clone \
  -W clippy::redundant_clone \
  -W clippy::clone_on_copy \
  -W clippy::implicit_clone 2>&1 | tee target/clippy-clones.txt

echo "--- Clone call count in src/ ---"
grep -rn '\.clone()\|\.to_string()\|\.to_owned()' src/ | wc -l

# Rc / RefCell are !Send + !Sync — flag any file that both uses them and spawns.
echo "--- Files using Rc/RefCell that also spawn ---"
for f in $(grep -rl 'Rc<\|RefCell<' src/ || true); do
  if grep -q 'thread::spawn\|tokio::spawn\|rayon::' "$f"; then
    echo "  $f  (see rule arc-mutex-across-threads)"
  fi
done

echo "--- clippy-clones.txt written to target/ ---"
```
