# Agent Integration — Rust Testing Patterns

## When to use
- Rust services using Axum/Actix/Tonic where you need both fast feedback (unit tests with `mockall`) and confidence (integration tests against the real router + Testcontainers DB).
- Library crates where doc-tests, property-based tests (`proptest`/`quickcheck`), and `cargo test --doc` should run on every PR.
- Async-heavy code (`tokio` runtime) where the test harness must use `#[tokio::test]` with controlled time (`tokio::time::pause`) to avoid wall-clock dependence.
- Codebases with `unsafe` blocks or FFI where Miri (`cargo +nightly miri test`) catches UB the compiler doesn't.
- Multi-crate workspaces where `cargo nextest` provides much faster, more parallel test execution than `cargo test`.

## When NOT to use
- Trivial scripts where `assert!` inside `main()` is enough; the harness costs more than the test.
- Code where mocks dominate signal — if every dep is mocked, the test asserts the mock setup, not behavior. Prefer integration tests with real components.
- Hot-path benchmarks. `cargo test` is not `cargo bench`; use `criterion` for perf-sensitive code.
- Pure `serde` round-trips where `quickcheck`/`proptest` is the right tool, not hand-written `#[test]`s.
- Cross-compile targets where running tests on the host doesn't reflect the target. Use `cross` + Docker, or skip and rely on CI.

## When tests fail / limitations
- **`mockall` cycles.** Auto-mocking a trait that returns a type defined in the same crate creates `mock!` macros that fail to compile because of feature flags or async signatures. The README example handles this by `mock!`-ing concrete `Database` instead of a trait.
- **Async test runtime collision.** Mixing `#[tokio::test]` with `#[test]` on `async` blocks compiled under different runtime flavors (`current_thread` vs `multi_thread`) flakes under contention.
- **Order-sensitive tests.** Two `#[tokio::test]`s sharing a `lazy_static` mock state — passing locally, failing under `cargo test -- --test-threads=N`.
- **Time-dependent assertions.** `Utc::now()` in production paths makes tests flaky; the README's `chrono::Utc::now()` in test fixtures is benign but tests that compare timestamps need `mockall`-time or `tokio::time::pause`.
- **Database state leak.** Integration tests share a Postgres container without truncation/transaction-rollback; tests fail in CI in random order.
- **Slow link times.** `cargo test` rebuilds bin + integration tests; without `cargo nextest` and shared `target/` cache, CI minutes balloon.
- **Doctests against private items.** Doc examples on private fns are silently ignored; agents copy doctest patterns onto private fns and miss coverage.
- **`tokio::test(flavor = "multi_thread")`** masks Send/Sync bugs that `current_thread` would surface. Run both flavors at least sometimes.
- **`assert_eq!`** on `f64` — agents use it; flake follows. Force `approx::assert_relative_eq!`.

## Agentic workflow
Drive Rust testing as a four-stage pipeline: (1) a coverage agent reads the crate, lists public functions/methods, and proposes a test inventory categorised as unit, integration, doctest, or property-based; (2) a code-gen agent emits the tests using `mockall` for traits, `proptest` for invariants, `axum-test` / `tower::ServiceExt::oneshot` for HTTP integration, and `testcontainers-rs` for DB; (3) a flake agent runs tests under `cargo nextest run --partition` with seeded randomness and quarantines flakes; (4) a review agent runs the anti-pattern checklist (no `unwrap()` in tests, no `Utc::now()` for assertion, no `sleep`, no shared global state, mocks vs reals balance). Persist the test stack (nextest, mockall, proptest, testcontainers, axum-test) in `.aidocs/product_docs/rust-test-stack.md`.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — one task = one module's test suite (unit + at least one integration). Sonnet for routine; opus only when designing test fixtures for state machines.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — Rust integration tests embed test JWTs / API keys / DB URLs in setup; scrub fixtures before commit.
- A **rust-test-review-agent** (worth adding under `agents/`): linter that flags `.unwrap()` outside `#[cfg(test)]`-only test code, `std::thread::sleep`/`tokio::time::sleep` in tests, `Utc::now()` in assertion paths, mocks for types that have a cheap real (e.g., `serde_json::Value`).

### Prompt pattern
Test inventory:
```
You are a Rust test architect. For the crate at <path>, list every
public fn/method and propose tests:
  type ∈ {unit, integration, doctest, property},
  fixture (mock|real|testcontainer),
  async (yes|no, runtime flavor),
  invariants (for property tests).
Reject `Utc::now()` or `std::time::*` in assertion paths — propose
`tokio::time::pause` or injected clock instead.
```

Anti-pattern review:
```
Review a Rust test PR. Flag:
(1) .unwrap() / .expect() in non-test code paths,
(2) std::thread::sleep or tokio::time::sleep used to wait for async,
(3) Utc::now() compared in an assertion,
(4) #[tokio::test] missing flavor when it relies on multi-threading,
(5) shared `lazy_static` state across tests without reset,
(6) mock for a type with a trivial real (e.g., chrono, serde_json),
(7) integration test that spawns a real network listener on a fixed
   port (collision risk),
(8) doctest on a private item.
Cite file:line. No fixes — only flags.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo test` | Built-in test runner | bundled |
| `cargo nextest` | Faster, more parallel test runner | https://nexte.st |
| `cargo llvm-cov` / `cargo tarpaulin` | Coverage reports | https://github.com/taiki-e/cargo-llvm-cov |
| `cargo bench` + `criterion` | Statistical benches separated from tests | https://bheisler.github.io/criterion.rs |
| `cargo +nightly miri` | UB detector for `unsafe` and FFI | https://github.com/rust-lang/miri |
| `cargo expand` | View macro expansions when `mockall` errors are cryptic | https://github.com/dtolnay/cargo-expand |
| `cargo udeps` | Detect unused dependencies in `[dev-dependencies]` | https://github.com/est31/cargo-udeps |
| `cargo deny` | Vet licenses / yanked / advisories | https://github.com/EmbarkStudios/cargo-deny |
| `cargo audit` | RustSec advisories | https://rustsec.org |
| `cross` | Run tests for cross-compile targets in Docker | https://github.com/cross-rs/cross |
| `bacon` | Test-watch loop in TUI | https://dystroy.org/bacon/ |
| `wiremock` (Rust crate) | Mock HTTP server for integration tests | https://docs.rs/wiremock |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions w/ `dtolnay/rust-toolchain` | SaaS | yes | `cargo nextest run` + `cargo clippy --all-targets`. |
| `taiki-e/install-action` | SaaS | yes | Cached install of nextest/llvm-cov/etc. in CI. |
| Codecov / Coveralls | SaaS | yes | Upload `cargo-llvm-cov` reports. |
| Testcontainers Cloud | SaaS | yes | Offload Docker for integration tests; agents drive same API. |
| Datadog / Honeycomb (test-trace) | SaaS | yes | Optional — emit `tracing` spans during tests for flake diagnosis. |
| Sentry (release tracking) | SaaS | yes | Tie test failures to release for triage. |
| `nextest`'s self-update | OSS | yes | Pin in CI; auto-update via Renovate. |

## Templates & scripts
README ships unit + integration patterns. Add a `.config/nextest.toml`:

```toml
[profile.default]
fail-fast = false
retries = 0
slow-timeout = { period = "30s", terminate-after = 1 }

[profile.ci]
fail-fast = false
retries = 1
slow-timeout = { period = "60s", terminate-after = 1 }
final-status-level = "fail"

[[profile.ci.overrides]]
filter = 'test(integration)'
threads-required = 2
```

Inline test-quality lint:

```bash
#!/usr/bin/env bash
# rust-test-lint.sh — flag common test anti-patterns
set -euo pipefail
root="${1:-.}"
fail=0
echo "## std::thread::sleep / tokio::time::sleep in tests"
grep -rEn '#\[(tokio::)?test' "$root/src" "$root/tests" -A 60 \
  | grep -E '(thread::sleep|tokio::time::sleep)\(' && fail=1 || true
echo "## Utc::now() in assertion path of a test"
grep -rEn '#\[(tokio::)?test' "$root/src" "$root/tests" -A 60 \
  | grep -E 'assert.*Utc::now' && fail=1 || true
echo "## .unwrap() outside test code"
grep -rEn '\.unwrap\(\)' "$root/src" \
  | grep -v -E '#\[cfg\(test\)\]|tests/|//' && fail=1 || true
echo "## Hardcoded port in integration test"
grep -rEn 'bind\(' "$root/tests" \
  | grep -E '127\.0\.0\.1:[0-9]+' && fail=1 || true
exit "$fail"
```

## Best practices
- **`#[cfg(test)] mod tests` colocated with code.** Black-box tests go to `tests/` directory at crate root. Don't mix.
- **`mockall::mock!` for traits with side effects.** Don't mock pure types; use the real one.
- **`#[tokio::test(flavor = "multi_thread", worker_threads = 2)]`** when the unit under test spawns tasks. Keep `current_thread` for cheaper tests.
- **`tokio::time::pause` for time-sensitive code.** Never `sleep` to wait; advance virtual time.
- **`testcontainers-rs` for DB integration tests.** Per-test Postgres container or shared with per-test schema; never depend on a shared dev DB.
- **`tower::ServiceExt::oneshot`** for axum handler tests — drives the router without binding a port.
- **`proptest` for invariants** of pure functions (parsers, codecs, math). Cheap signal vs hand-written tables.
- **`cargo nextest` in CI** for parallelism + per-test timeout + flake detection (`--retries 1`).
- **Coverage on PRs, not as a gate by itself.** `cargo llvm-cov --lcov` uploaded to Codecov; reviewers eyeball the diff.
- **Doctest production examples.** Top-of-crate `//!` rustdoc with a `# Examples` section that compiles and runs is the cheapest end-to-end test.
- **Snapshot tests with `insta`.** For complex output (rendered emails, AST), `insta` keeps tests readable and review-friendly.
- **Seeded randomness.** `proptest` and any `rand` use must accept a seed; record failing seeds in CI and replay locally.

## AI-agent gotchas
- **`Utc::now()` everywhere.** Agents inject the current time inside the unit under test and inside the assertion. Tests pass at noon, fail at midnight crossing day boundary. Force injected clock or `mockall::time`.
- **`sleep`-driven async waits.** Agents `tokio::time::sleep(Duration::from_millis(50))` to "give the task time"; flaky in CI. Use `tokio::join!`, `tokio::time::pause`, or wait on a channel.
- **`#[tokio::test]` flavor mismatch.** Default flavor is `current_thread`; agents call `spawn_blocking` and the test panics under load. Pin flavor explicitly.
- **Mocking through trait gymnastics.** Agents define one-method traits just to mock a free function; a function-pointer or generic param is cleaner.
- **Hardcoded ports.** Integration tests bind `127.0.0.1:8080`; CI runs them in parallel and one fails. Bind to `:0` and discover.
- **Hidden global state.** Tests touching `lazy_static`/`once_cell` without reset fail when reordered. Force per-test setup or a fixture struct.
- **Hallucinated `mockall::predicate` APIs.** Agents invent `predicate::eq_ignoring_case` etc. Pin to docs.rs version in `Cargo.toml`.
- **`unwrap()` in test makes failures unreadable.** `expect("user repository should return user")` gives the next agent a starting point.
- **Skipping `cargo deny`/`cargo audit` in CI.** Agents add a dependency, security advisory ships next week. Wire into CI.
- **Human-in-loop on flake quarantine.** Don't auto-mark tests as `#[ignore]`; flagging a flake without root cause hides bugs. Human triages.
- **Doctest on private items.** Agents add ` ``` ... ``` ` blocks to private fn rustdoc; they don't run. Promote to integration test or move to a public example.

## References
- The Rust Programming Language — Testing chapter. https://doc.rust-lang.org/book/ch11-00-testing.html
- Rust By Example — Testing. https://doc.rust-lang.org/rust-by-example/testing.html
- `cargo nextest` book. https://nexte.st
- `mockall` docs. https://docs.rs/mockall
- `proptest` book. https://altsysrq.github.io/proptest-book/
- `tokio` test guide (`tokio::test`, `tokio::time::pause`). https://docs.rs/tokio/latest/tokio/time/fn.pause.html
- `testcontainers-rs`. https://docs.rs/testcontainers
- `axum-test` / `tower::ServiceExt`. https://docs.rs/axum-test
- `insta` snapshot testing. https://insta.rs
- "Programming Rust," 2nd ed. — Blandy/Orendorff/Tindall (testing chapter).
- Sibling methodologies in this repo: `pro/dev/backend-systems/rust-backend/`, `pro/dev/backend-systems/rust-tokio-async/`, `pro/dev/backend-systems/rust-error-handling/`, `pro/dev/backend-systems/rust-ownership/`.
