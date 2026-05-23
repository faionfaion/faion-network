# Rust Unit Testing with mockall and tokio::test

## Summary

**One-sentence:** Produces Rust unit tests in #[cfg(test)] mod tests blocks with mockall trait mocks, explicit tokio runtime flavor, virtual-time control, and descriptive expect() messages.

**One-paragraph:** Unit tests live in #[cfg(test)] mod tests colocated with production code. Trait dependencies are mocked with mockall::mock!; async tests declare flavor explicitly. Virtual time (tokio::time::pause) replaces sleeps. Assertions use expect("descriptive message") for traceability. Black-box tests against the public API go to tests/ at the crate root; never mix placements.

**Ефективно для:**

- Швидкий feedback на pure logic + trait mock через `mockall`.
- Async код під `tokio::test` із керованим часом (`tokio::time::pause`).
- Тест трейту, не плоского struct (mock-ing concrete `chrono` — антипатерн).
- Doctest публічних API + `cargo test --doc`.

## Applies If (ALL must hold)

- Rust service module needing fast feedback with mockall mocks.
- Async code where tests must control time deterministically.
- Service method depends on a trait that can be mocked cheaply.
- Library crate where doc-tests should run on every PR.

## Skip If (ANY kills it)

- Trivial scripts where assert! in main() is enough.
- Code where mocks dominate signal — prefer integration tests with real components.
- Pure serde round-trips — use proptest.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Production module file | Rust source | service repo |
| mockall dev-dep | Cargo dep | Cargo.toml |
| tokio with macros + time | Cargo dep | Cargo.toml |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-testing-ci-toolchain]] | CI must run cargo nextest to actually execute the tests authored here |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-test-module` | sonnet | #[cfg(test)] mod tests skeleton with super::*. |
| `write-mock` | sonnet | mockall::mock! invocation + expectations. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unit_test_module.rs` | Rust #[cfg(test)] mod tests skeleton with mockall + explicit tokio flavor. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing-unit.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[rust-testing-integration]]
- [[rust-testing-property]]
- [[rust-testing-ci-toolchain]]

## Decision tree

See `content/06-decision-tree.xml`. Tree decides colocated vs tests/-dir placement, trait-mock vs real-impl, runtime flavor, and time strategy based on what the SUT touches.
