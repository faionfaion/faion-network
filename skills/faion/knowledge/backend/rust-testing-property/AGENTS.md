# Property-Based Testing in Rust with proptest

## Summary

**One-sentence:** Produces property-based tests in Rust using proptest with persisted regression seeds, approx assertions for floats, and bounded `cases` to keep CI minutes predictable.

**One-paragraph:** proptest generates hundreds of random inputs and verifies an invariant for all of them — catching edge cases hand-written tables miss. Failing inputs shrink to a minimal reproducer; seeds persist in a regression file (checked into git). Float comparisons use approx; bare assert! is replaced with prop_assert! inside proptest! blocks so failure messages contain the shrunk counterexample.

**Ефективно для:**

- Парсери, кодеки, серіалізація — `decode(encode(x)) == x` за один блок `proptest!`.
- Замінити велику параметризовану табличку на один інваріант.
- Чисті математичні функції з властивостями (sort stability, монотонність).
- Регресія через persisted seed file у git.

## Applies If (ALL must hold)

- Pure function with an invariant: parser, codec, serializer, math utility.
- Output must satisfy a property for all valid inputs (encode/decode identity, sort stability).
- Input space is large or irregular and hand-written tables miss edge cases.
- Replacing a long parameterized test table with a single proptest! block.

## Skip If (ANY kills it)

- Test needs precise control over a single input — use a regular #[test].
- Test involves I/O — proptest does not compose well with async setup/teardown.
- Benchmarks — overhead per iteration is unsuited to perf measurement.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Pure function with declared invariant | Rust fn | service code |
| proptest dev-dep | Cargo dep | Cargo.toml |
| approx dev-dep (for floats) | Cargo dep | Cargo.toml |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[rust-testing-unit]] | Property tests live in the same #[cfg(test)] mod blocks as unit tests |

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
| `identify-invariant` | sonnet | Derive the property from the function's contract. |
| `write-proptest-block` | sonnet | proptest! with strategy and prop_assert!. |
| `validate-output` | haiku | Schema check via the validator script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/proptest_block.rs` | Rust proptest! skeleton with persisted-regression config + approx for floats. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-rust-testing-property.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |

## Related

- [[rust-testing-unit]]
- [[rust-testing-integration]]
- [[rust-testing-ci-toolchain]]

## Decision tree

See `content/06-decision-tree.xml`. Tree decides when proptest is the right tool (pure + invariant) vs unit tests with mocks vs integration with testcontainers.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/proptest_block.rs`

```rust
use proptest::prelude::*;
use proptest::test_runner::{Config, FileFailurePersistence};

proptest! {
    #![proptest_config(Config {
        failure_persistence: Some(Box::new(FileFailurePersistence::WithSource("regression"))),
        cases: 256,
        .. Config::default()
    })]

    #[test]
    fn roundtrip(s in "\\PC*") {
        let bytes = my_codec::encode(&s);
        let back = my_codec::decode(&bytes).expect("decode should succeed for any input");
        prop_assert_eq!(back, s);
    }
}

// For float invariants:
//   use approx::assert_relative_eq;
//   assert_relative_eq!(actual, expected, epsilon = 1e-9);
```
