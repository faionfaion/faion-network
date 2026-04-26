# Agent Integration — Rust Testing

## When to use
- Rust services where correctness is non-negotiable (auth, billing, infra control planes) — `cargo test` + `mockall` + `proptest` give compile-time + property-level guarantees beyond what dynamic-language tests reach.
- Async services on `tokio` — `#[tokio::test]` is the de-facto runner; agents writing axum/tonic services need consistent test shape.
- Library crates publishing to crates.io — doctest discipline (`/// # Examples`) prevents silent doc rot.
- Refactor work where the borrow checker shifts function signatures — typed tests fail closed; LLM regressions surface immediately.
- Codebases enforcing `cargo deny` + coverage threshold via `cargo llvm-cov` in CI.

## When NOT to use
- Hot iteration prototypes — Rust's slow incremental compile + test startup punishes small loops; write the impl first.
- Pure FFI shims to C libs — testing requires the linked C side; integration tests pay double cost. Prefer a thin Rust wrapper + tests on the wrapper.
- Code where mocks dominate the test (`mockall` everywhere) — that's a sign the design is over-coupled. Refactor toward trait-based seams or use real implementations behind `#[cfg(test)]`.
- Macro-heavy crates where the test of value is `trybuild` (compile-fail tests), not runtime assertions.
- Embedded `no_std` targets — `cargo test` needs std; use `defmt-test` / on-target runners instead.

## Where it fails / limitations
- **Compile-time tests are slow.** Adding 50 test cases compiles 50 binaries by default. Use `cargo nextest` (10–60% faster, parallel by default) or share a test harness crate.
- **`mockall` macro-generated mocks** confuse rust-analyzer + LLMs. Agents read the mock impl, not the trait, and "fix" the wrong code. Pin to one mocking approach per crate.
- **Async test deadlocks.** `#[tokio::test(flavor = "current_thread")]` deadlocks if the SUT spawns a blocking task. Use `flavor = "multi_thread", worker_threads = 2` for code that does `spawn_blocking`.
- **Test isolation across `mod tests`.** `static` state inside the SUT (lazy_static, OnceLock) leaks across tests. `cargo test -- --test-threads=1` works around but disables parallelism.
- **`tokio::test` swallows panics in spawned tasks.** Tests pass while a background task panicked. Always `await` joined handles or use `tokio::task::JoinSet` and assert.
- **Property tests with bad shrinkers.** `proptest!` finds a 200-byte counterexample but minimization runs forever. Constrain inputs early (`Strategy::filter`).
- **Snapshot tests via `insta`.** Flaky on platforms with different float formatting; agents commit unreviewed snapshots → bug locked in.
- **Coverage tools.** `tarpaulin` underreports for async; `cargo llvm-cov` is more accurate but needs nightly toolchain features for branch coverage.
- **Doctest brittleness.** Code in doc comments compiles + runs; refactor a public API and 50 doctests break silently if not run in CI.

## Agentic workflow
Drive Rust tests in 4 stages: (1) a **trait-mapper** subagent reads the SUT and identifies trait boundaries → emits `mockall` mock declarations or test doubles via `#[cfg(test)] impl Trait for FakeX`; (2) a **unit-test-author** subagent writes `#[test]` / `#[tokio::test]` cases following Arrange/Act/Assert; (3) an **integration-test-author** writes `tests/*.rs` against real `axum::Router` via `tower::ServiceExt`; (4) a **coverage-triage** subagent runs `cargo llvm-cov --lcov` and reports per-module misses. Always run `cargo test --all-features --workspace` + `cargo clippy --all-targets --all-features -- -D warnings` before commit; LLMs commonly add tests that compile but trigger clippy lints.

### Recommended subagents
- `faion-sdd-executor-agent` (`agents/faion-sdd-executor-agent.md`) — quality gate: `cargo nextest run` + `cargo clippy -D warnings` + coverage threshold.
- A purpose-built **rust-mock-author-agent** (worth creating): given a trait, emit a `mockall::mock!` block + canonical test setup for happy/error paths.
- A **proptest-strategy-agent** (worth creating): given a struct, propose `Arbitrary` impls + property invariants (round-trip, idempotency, monotonicity).
- A **trybuild-agent** for proc-macro crates: scaffold compile-fail tests with expected `stderr` snippets.
- `password-scrubber-agent` (`agents/password-scrubber-agent.md`) — scrub `tests/fixtures/`, `.env.test`, `config/test.toml` before commit.

### Prompt pattern
Unit-test scaffold:
```
You are a Rust 1.7x engineer using tokio + mockall + assert_matches.
For src/services/users.rs::UserService::create, generate
#[cfg(test)] mod tests covering:
1. happy path: returns User
2. duplicate email: AppError::Conflict
3. db failure: AppError::Internal
Use mockall for Database trait. async via #[tokio::test].
Run: cargo nextest run -p users.
Do NOT use unwrap() in production code paths under test.
```

Property-test prompt:
```
For crate `parser`, write proptest! cases covering:
- round-trip: parse(serialize(x)) == x for all valid AST
- no-panic: parse never panics on arbitrary &[u8] input
Constrain Vec<u8> length to 0..=1024. Use 1024 cases.
Run: cargo test --release prop_.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `cargo test` | Bundled test runner | `cargo --help test` |
| `cargo nextest` | Faster, parallel runner with retries | `cargo install cargo-nextest` |
| `cargo llvm-cov` | Coverage via LLVM source-based instrumentation | `cargo install cargo-llvm-cov` |
| `cargo tarpaulin` | Coverage (Linux x86_64) | `cargo install cargo-tarpaulin` |
| `cargo mutants` | Mutation testing — find tests that pass when code is broken | `cargo install cargo-mutants` |
| `cargo deny` | Dep audit (licenses, advisories) — gate alongside tests | `cargo install cargo-deny` |
| `cargo audit` | RustSec advisory check | `cargo install cargo-audit` |
| `cargo bench` / `criterion` | Benchmarks; treat as separate gate | https://bheisler.github.io/criterion.rs |
| `cargo expand` | Show macro expansions when mocks misbehave | `cargo install cargo-expand` |
| `insta` | Snapshot testing | `cargo add insta --dev` |
| `proptest` | Property-based testing | `cargo add proptest --dev` |
| `mockall` | Trait mocking | `cargo add mockall --dev` |
| `wiremock` | HTTP stubbing | `cargo add wiremock --dev` |
| `testcontainers` | Real Postgres/Redis in tests | `cargo add testcontainers --dev` |
| `trybuild` | Compile-fail tests for proc-macros | `cargo add trybuild --dev` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| GitHub Actions | OSS / SaaS | yes | `dtolnay/rust-toolchain` + `Swatinem/rust-cache` + `cargo nextest`. |
| Codecov / Coveralls | SaaS | yes | Parses `lcov.info` from `cargo llvm-cov`. |
| crates.io | SaaS | yes | Publish gating via `cargo publish --dry-run` in CI. |
| docs.rs | SaaS | n/a | Builds doctests on publish — CI must run `cargo test --doc`. |
| Snyk / RustSec | SaaS / OSS | yes | Advisory feed for `cargo audit`. |
| Testcontainers Cloud | SaaS | yes | Reduces local Docker pressure when crate uses Postgres/Kafka. |
| GitLab CI / Buildkite | SaaS | yes | Same matrix patterns as GH Actions. |

## Templates & scripts
See `templates.md` and `examples.md` for axum integration tests, mockall stubs. Add a coverage-gate script (≤50 lines):

```bash
#!/usr/bin/env bash
# rust-coverage-gate.sh — enforce line + branch coverage thresholds.
# Usage: rust-coverage-gate.sh LINE BRANCH
set -euo pipefail
LINE="${1:-70}"
BRANCH="${2:-60}"
cargo llvm-cov --workspace --lcov --output-path lcov.info >/dev/null
python3 - "$LINE" "$BRANCH" <<'PY'
import re, sys
line_t, branch_t = float(sys.argv[1]), float(sys.argv[2])
with open("lcov.info") as f: data = f.read()
lf = sum(int(x) for x in re.findall(r"^LF:(\d+)", data, re.M))
lh = sum(int(x) for x in re.findall(r"^LH:(\d+)", data, re.M))
bf = sum(int(x) for x in re.findall(r"^BRF:(\d+)", data, re.M))
bh = sum(int(x) for x in re.findall(r"^BRH:(\d+)", data, re.M))
line = (lh / lf * 100) if lf else 100.0
branch = (bh / bf * 100) if bf else 100.0
print(f"line={line:.1f}% branch={branch:.1f}%")
fails = []
if line < line_t:   fails.append(f"line {line:.1f} < {line_t}")
if branch < branch_t: fails.append(f"branch {branch:.1f} < {branch_t}")
if fails: print("FAIL:", "; ".join(fails)); sys.exit(1)
print("OK")
PY
```

Run after `cargo nextest run` in CI.

## Best practices
- **`#[cfg(test)] mod tests` co-located with SUT** — fastest dev loop. Use `tests/` only for integration tests against the public API.
- **`cargo nextest` over `cargo test`** in CI — orders of magnitude faster on multi-core, retries flaky tests, JUnit XML for dashboards.
- **`assert_matches!(result, Err(AppError::Conflict(_)))`** — pattern-matching assertions over `assert_eq` on Debug strings.
- **Prefer fakes over mocks for trait-heavy code.** A 30-line in-memory `impl Database for FakeDb` is more maintainable than 30 mockall expectations.
- **Always `await` joined async tasks.** `tokio::spawn` panics are silent unless joined.
- **Pin tokio runtime flavor** explicitly (`#[tokio::test(flavor = "multi_thread", worker_threads = 2)]`) so tests don't depend on default.
- **`insta` for complex assertions** (JSON shape, error messages) — review snapshots in PRs as code.
- **Run doctests in CI** (`cargo test --doc`) — public API doc rot is a real bug source.
- **`testcontainers` over `sqlx-mock`** for repository tests — real Postgres catches dialect bugs.
- **`cargo mutants`** weekly on the critical-path crate; tune kill rate >70%.
- **Workspace test isolation:** `[workspace.metadata.cargo-machete]` to detect unused dev-deps; agents tend to leak prod deps into dev-deps.

## AI-agent gotchas
- **`unwrap()` inside test bodies** is fine. `unwrap()` inside the SUT under test is a bug. LLMs blur the line.
- **Mocking the wrong direction.** Agent mocks the consumer instead of the dependency; SUT becomes a no-op. Force prompt to name the SUT and what's mocked.
- **`mockall` `expect_*` ordering.** Setting `.times(1)` after `.returning(...)` works; placing `.times(1)` before changes meaning. Agents copy from old crates and produce silent under/over-call.
- **Async drops.** `#[tokio::test]` exits before `tokio::spawn` completes; assertion never runs. Use `JoinSet` or `await` the handle.
- **Borrow-checker workaround tests.** Agent uses `unsafe { std::mem::transmute }` in tests to satisfy the compiler. Reject — refactor SUT instead.
- **Hidden global state.** `OnceLock` initialized in test #1 leaks to test #2. Detect with `cargo test -- --test-threads=1` then fix the SUT (DI the dep instead of `static`).
- **`assert!(left == right)`** with no message — failure shows nothing. Always `assert_eq!` or `assert!(cond, "context: {x:?}")`.
- **`tokio::time::sleep` in tests.** Real wall clock; flaky in CI. Use `tokio::time::pause()` + `advance(...)` or `tokio_test::block_on`.
- **`std::env::set_var` in tests.** Process-wide; collides with parallel tests. Wrap in serial mutex (`serial_test::serial`) or refactor SUT to take config.
- **`cargo test --release`** when code has `#[cfg(debug_assertions)]` paths — agent doesn't realize behaviors diverge. Document which profile each test targets.
- **Insta snapshots committed without review.** `cargo insta accept` runs in CI → tests "pass" by accepting the bug. Force `cargo insta review` locally only.
- **Proptest run count too low** (`PROPTEST_CASES=16`) — finds nothing. Default 256 in CI; bump to 1024 for critical invariants.
- **Mockall + generic methods.** `mock!` doesn't auto-generate generic method mocks; LLMs hallucinate the syntax. Use `expect_call` with concrete monomorphization.
- **`.expect_*().returning(|_| Ok(...))`** with non-`Send` capture in `#[tokio::test(flavor="multi_thread")]` — compile error agents misdiagnose. Wrap state in `Arc<Mutex<...>>`.

## References
- The Rust Programming Language — Testing chapter: https://doc.rust-lang.org/book/ch11-00-testing.html
- Tokio testing guide: https://docs.rs/tokio/latest/tokio/attr.test.html
- mockall docs: https://docs.rs/mockall
- proptest book: https://proptest-rs.github.io/proptest/
- cargo-nextest book: https://nexte.st
- cargo-llvm-cov: https://github.com/taiki-e/cargo-llvm-cov
- cargo-mutants: https://github.com/sourcefrog/cargo-mutants
- Testcontainers Rust: https://docs.rs/testcontainers
- Insta snapshot testing: https://insta.rs
- Sibling methodologies: `free/dev/software-developer/rust-error-handling/`, `free/dev/software-developer/rust-ownership/`, `free/dev/software-developer/test-fixtures/`.
