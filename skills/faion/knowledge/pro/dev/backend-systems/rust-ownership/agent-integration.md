# Agent Integration — Rust Ownership Model

## When to use
- New Rust contributor (human or LLM) writing code that crosses function/thread boundaries with non-Copy types.
- Reviewing PRs that introduce `Clone`, `Rc`, `Arc`, `RefCell`, or lifetime annotations — the borrow checker is the source of truth, so structure determines correctness.
- Designing data flow for a long-running service: who owns the connection pool, who borrows it, where does shared mutable state need `Arc<Mutex<_>>`.
- Refactoring code that compiles only because of excessive `clone()` calls.
- Modeling builder/typestate APIs that consume `self` to enforce state machines.

## When NOT to use
- Pure-CPU numeric code that already runs on `Copy` primitives — borrow checker rarely fires there.
- One-off scripts or `examples/` where `clone()` cost is irrelevant.
- FFI thin wrappers where lifetimes are dictated by the C API and ownership is documented elsewhere.
- Throwaway prototypes — fighting the borrow checker before the design is settled wastes tokens.

## Where it fails / limitations
- Self-referential structs (a field that borrows from another field of the same struct) are not expressible safely without `Pin` + `unsafe` or crates like `ouroboros`. LLMs frequently try to write them and fail.
- Async closures + borrowed data: futures captured into `tokio::spawn` must be `'static`; agents miss this and produce `borrowed value does not live long enough`.
- `Rc<RefCell<T>>` chains can deadlock at runtime via overlapping `borrow_mut()` calls — compile-time safety is gone, runtime panics replace it.
- Lifetime variance and HRTB (`for<'a>`) bounds confuse most LLMs; expect spurious `'static` lifetimes added "to make it compile".
- Drop order in nested scopes is rarely intuitive for agents — releases of `MutexGuard` can sit longer than expected.
- Model code can mask logic bugs by switching `&str` to `String` everywhere, doubling allocations to silence the compiler.

## Agentic workflow
Use a planning-then-coding loop: an architect-tier agent drafts the ownership graph (who owns what, where Arc is needed, where lifetimes flow), then the coding subagent implements one module at a time with `cargo check` after each step. Treat compiler errors as the loop's primary signal — feed the full error (including E-code and span) back to the agent rather than paraphrasing. Reject any "fix" that adds `clone()` without justification or replaces `&str` with `String` to escape a lifetime.

### Recommended subagents
- `faion-sdd-executor-agent` — break ownership refactors into per-file tasks, run `cargo check` per task.
- General reviewer subagent — flag spurious `clone()`, `to_string()`, and `'static` lifetimes added without rationale.
- Architecture/planning subagent (Opus-tier) — design `Arc`/`Rc`/`Mutex` topology before coding starts.

### Prompt pattern
Plan: "Sketch ownership for module `<name>`: list each long-lived value, its owner, who borrows it, and whether it crosses thread/await boundaries. Mark which need `Arc`, which need `Arc<Mutex>`, which can stay `&` borrows. No code yet."

Implement: "Apply the plan. Run `cargo check` after each file. If a borrow error appears, do NOT add `.clone()` — explain the lifetime conflict and propose a structural fix (e.g., split borrow, move ownership, accept `&mut` earlier)."

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo check` | Fast borrow-checker pass without codegen | bundled with cargo |
| `cargo clippy -- -W clippy::needless_clone -W clippy::redundant_clone` | Surface lazy `clone()` calls | rustup component add clippy |
| `cargo expand` | See what async/macro code is actually borrowing | cargo install cargo-expand |
| `cargo asm` | Verify zero-cost abstractions hold (no hidden allocs) | cargo install cargo-show-asm |
| `miri` | Detect undefined behaviour, dangling refs in tests | rustup +nightly component add miri |
| `cargo geiger` | Audit `unsafe` introduced by ownership escape hatches | cargo install cargo-geiger |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| rust-analyzer (LSP) | OSS | Yes | Inlay hints for inferred lifetimes/types speed up agent reasoning over diffs |
| GitHub Actions + `actions-rs/clippy-check` | SaaS | Yes | CI gate that returns structured warnings agents can parse |
| Loom | OSS lib | Partial | Concurrent `Arc<Mutex>` checker; setup needs human design decisions |
| `cargo-mutants` | OSS | Yes | Mutation testing surfaces ownership-sensitive logic gaps |

## Templates & scripts
See `templates.md` for builder-with-`self`, `Arc<Mutex<_>>` shared-state, and `Cow<str>` patterns. Diagnostic helper:

```bash
#!/usr/bin/env bash
# scripts/audit-clones.sh — surface gratuitous clone() in a crate
set -euo pipefail
cargo clippy --all-targets -- \
  -W clippy::needless_clone \
  -W clippy::redundant_clone \
  -W clippy::clone_on_copy \
  -W clippy::implicit_clone 2>&1 | tee target/clippy-clones.txt
echo "---"
rg -nP '\.clone\(\)|\.to_string\(\)|\.to_owned\(\)' src/ | wc -l
```

## Best practices
- Pass `&str`, `&[T]`, `&Path` in function signatures; only take `String`/`Vec<T>`/`PathBuf` when the function will store the value.
- Prefer `impl Into<String>` in builder constructors so callers may pass `&str` or `String` without an explicit `to_owned`.
- Use `Cow<'a, str>` when a function sometimes mutates the input — avoids both clone and lifetime gymnastics.
- For shared state across tasks, default to `Arc<Mutex<_>>` only if mutation is needed; `Arc<T>` alone suffices for read-only sharing.
- Split borrows: `let (a, b) = (&mut s.a, &mut s.b);` is legal where `&mut s.a` then `&mut s.b` is not — refactor structs accordingly.
- Avoid `'static` bounds outside `tokio::spawn` and `dyn` trait objects — they are a code smell when added "to make it compile".

## AI-agent gotchas
- LLMs reach for `clone()` first when fighting the borrow checker. Force them to articulate the lifetime conflict before patching.
- Self-referential structs are an attractive nuisance — agents will write them confidently and silently break Drop semantics. Block at review.
- Async + borrows: `tokio::spawn(async move { ... &shared_ref ... })` will fail; agents will then make `shared_ref` `'static` via leak. Reject — use `Arc::clone` instead.
- `RefCell::borrow_mut()` panics rather than failing to compile; AI-generated code with multiple `borrow_mut` paths often deadlocks under load.
- Models confuse `Box<T>` (heap, owned) with `Rc<T>`/`Arc<T>` (shared); always require justification when one is swapped for another.
- Agents often add lifetime parameters to every type "to be safe"; this corrupts public APIs. Push back unless lifetimes flow through the type.
- `cargo check` failures must be fed back verbatim — paraphrasing E-numbers strips diagnostic info the next iteration needs.

## References
- The Rust Book, ch. 4 (Ownership) — https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html
- The Rust Book, ch. 10 (Lifetimes) — https://doc.rust-lang.org/book/ch10-03-lifetime-syntax.html
- The Rustonomicon — https://doc.rust-lang.org/nomicon/
- "Too Many Linked Lists" — https://rust-unofficial.github.io/too-many-lists/
- `Pin` and self-referential types — https://doc.rust-lang.org/std/pin/
- Tokio task lifetime guide — https://tokio.rs/tokio/tutorial/spawning
