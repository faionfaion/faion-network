---
slug: rust-testing-property
tier: pro
group: dev
domain: backend-systems
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Property-based tests with proptest (or quickcheck) generate hundreds of random inputs and verify that a function satisfies an invariant for all of them — finding edge cases that hand-written example tables miss.
content_id: "0406fdca0d9e6e71"
tags: [rust, property-testing, proptest, quickcheck, invariants]
---
# Property-Based Testing in Rust with proptest

## Summary

**One-sentence:** Property-based tests with proptest (or quickcheck) generate hundreds of random inputs and verify that a function satisfies an invariant for all of them — finding edge cases that hand-written example tables miss.

**One-paragraph:** Property-based tests with proptest (or quickcheck) generate hundreds of random inputs and verify that a function satisfies an invariant for all of them — finding edge cases that hand-written example tables miss. Failing inputs are automatically shrunk to a minimal reproducer; the seed is recorded so failures can be replayed locally.

## Applies If (ALL must hold)

- Pure functions with invariants: parsers, codecs, math utilities, serialization round-trips.
- Any function where the output must satisfy a property for all valid inputs (encode/decode identity, sort stability, non-negative result).
- Code where the input space is large or irregular and hand-written tables are brittle.
- Replacing large hand-written parameterized test tables with a single proptest! block.

## Skip If (ANY kills it)

- Tests that require precise control over a single specific input — use a regular #[test] example.
- Integration tests involving I/O or databases — proptest's generation model does not compose well with async I/O setup/teardown.
- Benchmarks — use criterion; proptest's overhead per iteration is not suitable for perf measurement.
- Hot-path benchmarks where assert_eq! on f64 is the pattern — use approx::assert_relative_eq! regardless of test type.

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
