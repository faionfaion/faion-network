---
slug: deterministic-test-data-pattern
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: Cross-stack pattern for deterministic test data — factories, frozen clocks, seeded RNG, per-test DB isolation, golden datasets, time/randomness pinning — that eliminates the bulk of suite flakiness.
content_id: 07a972a558403f04
---

# Deterministic Test Data Pattern

## Summary

Flake-elimination methodologies fix individual tests; this one fixes the test-data layer underneath them. Factories, frozen clocks, seeded RNG, per-test DB isolation, golden datasets, anonymised production snapshots, seed/teardown order, dataset versioning, and cross-environment parity are typically scattered across stacks (one team has factory-boy, another has fixtures, a third has snapshot copies). This methodology defines a single cross-stack pattern so that any test, in any stack, gets the same five guarantees about its data: deterministic identity, frozen time, seeded randomness, isolated state, and parity with prod schema.

## Applies If

- The test suite shows flakiness traceable to data, time, ordering, or random values (not network or UI timing alone).
- The team owns ≥2 services or stacks (e.g. Python backend + Node frontend + a worker) where test-data patterns currently differ.
- An E2E or integration tier exists that touches a real DB, queue, or external service stub.
- The team can change test setup code without breaking shipped behaviour.

## Skip If

- Pure unit tests with no external state — function-level testing inherits determinism from the runtime.
- The suite's flakiness is dominated by environment timing (CI runner load, network) — fix the timing tier first, then revisit data determinism.

## Content
See `content/01-core-rules.xml`.

## Related
- [[qa-flake-ledger-template]]
- [[qa-test-data-catalog]]
- [[characterization-test-recipes]]
- [[test-pyramid-policy-enforcement]]
