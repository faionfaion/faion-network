# Agent Integration — Rust Ownership Model

## When to use
- Any time an agent writes new Rust code: ownership decisions are upfront design, not afterthought.
- Translating algorithms from GC languages (Python, Go, JS) — agents must explicitly think about who owns each value.
- Designing API surfaces (`fn foo(s: String)` vs `fn foo(s: &str)` vs `fn foo(s: impl AsRef<str>)`).
- Refactoring code that fights the borrow checker with unnecessary `.clone()` / `Rc<RefCell<T>>` workarounds.
- Async code: ownership and lifetimes get harder once `'static` and `Send + Sync` bounds enter.

## When NOT to use
- Tiny scripts where `.clone()` everywhere is fine — borrow-checker fights cost more time than they save.
- Procedural macros — they manipulate token streams, ownership idioms differ.
- Wrapping C APIs via FFI — manual lifetime management dominates; the methodology's "use `&str`" advice barely applies.
- Code generated from schemas (Prost, sqlx) — accept the generated ownership shape, don't fight it.

## Where it fails / limitations
- The methodology covers basic ownership but not the deeper `Pin`, `unsafe`, or async-Send issues that bite in real apps.
- Lifetime elision rules are presented as "compiler infers" — agents that paste examples then add a second reference parameter break the elision and don't know why.
- `Rc<RefCell<T>>` and `Arc<Mutex<T>>` are introduced as escape hatches but the runtime cost (pointer chasing, lock contention, refcount atomics) is rarely quantified.
- `String` vs `&str` advice is sound, but generic `impl AsRef<str>` is the more flexible choice for libs and is under-discussed.
- Self-referential structs are flat-out unsupported by safe Rust; agents need `ouroboros` / pinning, neither is in basic ownership docs.
- Borrow-checker errors are notoriously cryptic for agents — "lifetime ‘a does not outlive 'b" doesn't explain which `&` to remove.

## Agentic workflow
A code-writing agent first answers three ownership questions: (1) does this function consume, borrow, or share its inputs? (2) does it return owned data or a reference into existing data? (3) does it cross a thread boundary (`Send + Sync` needed)? Answer is captured in the function signature before the body is written. A code-review agent runs `cargo clippy` (with `clippy::needless_pass_by_value`, `clippy::redundant_clone`, `clippy::ptr_arg`) and `cargo machete` to flag mis-ownership and dead clones. Borrow-check failures are treated as design feedback, not noise — never papered over with `.clone()`.

### Recommended subagents
- `faion-sdd-executor-agent` — runs the task; constitution.md should pin "no `.clone()` to silence borrow checker".
- A purpose-built `borrow-checker-explainer` subagent — given a `cargo build` failure, expands the cryptic error into "what `&` to remove or what to consume".
- A `clippy-enforcer` subagent — runs Clippy gates with a strict ownership-related allowlist.

### Prompt pattern
```
Before writing the body, answer:
1. Each parameter: borrowed (&T), mutably borrowed (&mut T), or owned (T)?
2. Return type: owned (T) or reference (&'a T) into a parameter?
3. Threads: is this called from spawn? If so, all captures must be 'static.
Print the signature first, then the body.
```
```
This compile error: "<paste>". Walk me through the ownership graph
of the function. Suggest the minimal fix that does not call .clone()
or wrap in Rc<RefCell<T>>. If neither is possible, say so.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo` | Build / test / borrow check | rustup default · https://doc.rust-lang.org/cargo/ |
| `cargo clippy` | Lints around ownership patterns | `rustup component add clippy` |
| `cargo expand` | Inspect generated code; useful for macros that move values | `cargo install cargo-expand` |
| `cargo machete` | Find unused deps after refactor | `cargo install cargo-machete` |
| `rust-analyzer` | LSP — inlay hints show inferred lifetimes & types | https://rust-analyzer.github.io/ |
| `bacon` | Background `cargo check` watcher | `cargo install bacon` |
| `mold` / `lld` | Faster linker | https://github.com/rui314/mold |
| `miri` | Detect undefined behavior in unsafe code | `rustup +nightly component add miri` |
| `loom` | Concurrency permutation tester | `cargo add --dev loom` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Rust Playground | SaaS | Yes | Quick borrow-checker experiments via API. |
| godbolt.org (Compiler Explorer) | SaaS | Yes | Inspect MIR / asm to verify zero-cost abstractions. |
| crates.io | SaaS | Yes | Look up `Send`/`Sync` annotations of imported types. |
| Lib.rs | SaaS | Yes | Same niche, often more accurate type info. |
| GitHub Copilot Workspace / Cursor | SaaS | Partial | Borrow-checker errors propagate poorly; needs human escalation often. |

## Templates & scripts
See `templates.md` for ownership patterns. Inline minimal "API surface" cheat sheet:

```rust
// Accept the most-permissive type:
fn read_lines(path: impl AsRef<Path>) -> io::Result<Vec<String>> { /* ... */ }

// Return owned when the buffer is freshly allocated:
fn slugify(input: &str) -> String { /* ... */ }

// Return a borrow when slicing existing data:
fn first_word<'a>(s: &'a str) -> &'a str { /* ... */ }

// Share across threads: Arc, not Rc:
use std::sync::Arc;
let shared = Arc::new(state);
std::thread::spawn({
    let shared = Arc::clone(&shared);
    move || { /* use shared */ }
});

// Single-thread shared mutable: Rc<RefCell<T>> last resort:
use std::{rc::Rc, cell::RefCell};
let counter = Rc::new(RefCell::new(0));
*counter.borrow_mut() += 1;
```

## Best practices
- API rule of thumb: take the most flexible type you can (`&str` over `&String`, `&[T]` over `&Vec<T>`, `impl IntoIterator` over `Vec<T>`).
- Return owned data when the function allocates; return a borrow when slicing into a parameter.
- Prefer iterator chains (`.iter().filter().map().collect()`) over indexing — borrow checker is happier and code is faster.
- Use `Cow<'a, str>` when sometimes-borrowed sometimes-owned (parser output, normalization).
- For shared state across threads, prefer message passing (`mpsc`, `tokio::sync::mpsc`) over `Arc<Mutex<T>>`.
- Don't reach for `Rc<RefCell<T>>` to silence the borrow checker — usually means data layout is wrong (graph in a tree, etc.).
- Lifetime elision: avoid explicit `'a` parameters until the compiler asks; once it asks, name them after their meaning (`'src`, `'config`).
- For async, all spawned tasks need `'static` — capture by value with `move`, or `Arc::clone` shared state.
- Use `rust-analyzer` inlay hints to make ownership transfers visible while typing.

## AI-agent gotchas
- LLMs default to `.clone()` to escape the borrow checker. Override with: "If you call `.clone()`, justify in a comment why the borrow can't work. Otherwise rewrite the signature."
- LLMs writing `fn foo(s: &String)` instead of `&str` — clippy lint catches; agent must accept the lint, not silence it.
- LLMs love `Rc<RefCell<T>>` from web-search results; in async contexts they then write `Arc<Mutex<T>>` and forget tokio's `Mutex` is async-aware (`std::sync::Mutex` is fine in compute-heavy code, `tokio::sync::Mutex` for `await` while holding).
- Agents accept "lifetime 'a may not outlive 'static" by adding `'static` everywhere — this poisons APIs and cascades. Walk back to the original mismatch; usually the data is borrowed when it should be owned.
- Self-referential structs: LLMs invent `&self`-referencing fields; safe Rust forbids. Agent must recognize and use `Pin`, `ouroboros`, or restructure.
- Async iterators / streams: LLMs use `.iter()` inside `async` and hold borrows across `.await`, which breaks `Send`. Refactor to consume the iterator before the await point.
- Closures capturing `&` while also `&mut` of the same value — the lint message is unhelpful; agents need to recognize the pattern (e.g., `vec.iter().for_each(|x| vec.push(x.clone()))` is illegal).
- Borrow-checker fights waste tokens fast. Budget rule: if the agent has changed the same function signature 3+ times, escalate or simplify (collect into Vec, return owned, redesign).

## References
- https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html — official chapter
- https://rust-unofficial.github.io/too-many-lists/ — Aria's "Learn Rust With Entirely Too Many Linked Lists" (deep ownership intuition)
- https://rust-lang.github.io/api-guidelines/ — function signature conventions
- https://doc.rust-lang.org/nomicon/ — for unsafe + ownership corner cases
- https://blog.logrocket.com/understanding-ownership-in-rust/ — practical walk-through
- https://docs.rs/tokio/latest/tokio/task/ — Send/'static rules for spawn
- https://github.com/dtolnay/anyhow — example of a well-designed owned-error type
- https://rust-lang.github.io/rust-clippy/master/ — clippy lints (search "redundant_clone", "needless_pass_by_value")
