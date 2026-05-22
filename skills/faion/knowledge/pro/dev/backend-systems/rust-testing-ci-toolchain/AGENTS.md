---
slug: rust-testing-ci-toolchain
tier: pro
group: dev
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: The production Rust test toolchain in CI uses cargo nextest for parallel execution with per-test timeouts, cargo llvm-cov for LCOV coverage reports, cargo +nightly miri for UB detection in unsafe code, and taiki-e/install-action to cache tool installs in GitHub Actions.
content_id: "ca1e0028544ca8b2"
tags: [rust, ci, cargo-nextest, coverage, cargo-miri]
---
# Rust Testing CI Toolchain — nextest, llvm-cov, miri

## Summary

**One-sentence:** The production Rust test toolchain in CI uses cargo nextest for parallel execution with per-test timeouts, cargo llvm-cov for LCOV coverage reports, cargo +nightly miri for UB detection in unsafe code, and taiki-e/install-action to cache tool installs in GitHub Actions.

**One-paragraph:** The production Rust test toolchain in CI uses cargo nextest for parallel execution with per-test timeouts, cargo llvm-cov for LCOV coverage reports, cargo +nightly miri for UB detection in unsafe code, and taiki-e/install-action to cache tool installs in GitHub Actions. Pin all tool versions via Renovate to avoid silent breakage.

## Applies If (ALL must hold)

- Any Rust project with more than a handful of integration tests where cargo test's sequential-within-binary model causes slow CI.
- Multi-crate workspaces where cargo nextest provides much faster, more parallel test execution than cargo test.
- Codebases with unsafe blocks or FFI where cargo +nightly miri test catches UB the compiler does not.
- Any project uploading coverage to Codecov or Coveralls where cargo llvm-cov provides the LCOV feed.
- Library crates where cargo test --doc should run on every PR.

## Skip If (ANY kills it)

- Trivial scripts with two or three test functions — cargo test is sufficient; nextest setup cost is not justified.
- cargo bench / criterion benchmarks — nextest and llvm-cov do not apply to perf-sensitive code paths; keep them in a separate job.
- Cross-compile targets where running tests on the host does not reflect the target — use cross + Docker, or skip and rely on a hardware-in-the-loop CI runner.

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
