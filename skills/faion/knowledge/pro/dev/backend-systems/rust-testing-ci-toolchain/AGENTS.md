---
slug: rust-testing-ci-toolchain
tier: pro
group: dev
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Produces a pinned CI config (nextest.toml + GitHub Actions workflow) that runs cargo nextest + llvm-cov + nightly miri with cached tool installs.
content_id: "6917794e028a50ea"
complexity: medium
produces: config
est_tokens: 4300
tags: [rust, ci, cargo-nextest, coverage, cargo-miri]
---
# Rust Testing CI Toolchain — nextest, llvm-cov, miri

## Summary

**One-sentence:** Produces a pinned CI config (nextest.toml + GitHub Actions workflow) that runs cargo nextest + llvm-cov + nightly miri with cached tool installs.

**One-paragraph:** Pins the Rust CI test toolchain: cargo nextest for per-test timeouts + parallel execution, cargo llvm-cov for LCOV coverage uploads, cargo +nightly miri for UB detection on unsafe/FFI, and taiki-e/install-action to cache tool installs. Tool versions are pinned and updated via Renovate. A build cache for ~/.cargo and target/ keeps cold-build minutes off the critical path.

**Ефективно для:**

- Rust сервіси з інтеграційними тестами, де `cargo test` блокується одним hang.
- Workspace із багатьма крейтами — `nextest` дає реальну паралельність.
- Crate з `unsafe`/FFI: `miri` ловить UB, який компілятор не бачить.
- PR-флоу, що ллє LCOV у Codecov/Coveralls без hard gate.

## Applies If (ALL must hold)

- Rust project with integration tests where cargo test's sequential model is too slow.
- Multi-crate workspace needing parallel test execution.
- Crate contains unsafe or FFI and needs nightly miri coverage.
- PR pipeline must upload LCOV to Codecov or Coveralls.

## Skip If (ANY kills it)

- Trivial scripts with 2-3 test functions — cargo test is enough.
- Hot-path benchmarks — use criterion, not nextest or llvm-cov.
- Cross-compile-only targets where host tests are not representative.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Cargo workspace manifest | TOML | repo root `Cargo.toml` |
| Existing CI file | YAML | .github/workflows/test.yml or equivalent |
| Toolchain pin | rust-toolchain.toml | repo root |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-testing-unit]] | this CI gate executes the unit suite the rust-testing-unit methodology authored |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-nextest-config` | sonnet | Per-repo judgment on retries + slow-timeout. |
| `draft-github-actions-yml` | sonnet | Job topology + cache keying. |
| `validate-config` | haiku | Mechanical schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/nextest.toml` | Pinned `.config/nextest.toml` with ci profile, retries, slow-timeout. |
| `templates/ci-workflow.yml` | GitHub Actions workflow: nextest + llvm-cov + miri jobs. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing-ci-toolchain.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[rust-testing-unit]]
- [[rust-testing-integration]]
- [[rust-testing-property]]

## Decision tree

See `content/06-decision-tree.xml`. Tree maps observable signals (workspace size, unsafe presence, CI runtime budget, coverage policy) to a concrete tool-set choice; each leaf cites one rule from 01-core-rules.xml.
