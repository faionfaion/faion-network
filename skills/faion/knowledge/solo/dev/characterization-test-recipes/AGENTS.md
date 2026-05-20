---
slug: characterization-test-recipes
tier: solo
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "9350e455b9b15254"
summary: A recipe collection for pinning legacy behavior with characterization tests before refactoring — input capture, output snapshot, edge-case sweep, and pinning the diff to a baseline.
tags: [legacy-code, characterization-tests, refactoring, snapshot-testing, working-with-legacy]
---
# Characterization Test Recipes

## Summary

**One-sentence:** Concrete recipes for writing characterization tests that pin observable behavior of legacy code before any refactor — input fuzzing, output snapshotting, side-effect capture — so the refactor diff is the only behavior change.

**One-paragraph:** Michael Feathers's premise (Working Effectively With Legacy Code): you cannot refactor what you cannot test, and legacy code by definition has no tests. The fix is characterization tests — tests that document what the code currently does, not what it should do. Faion has unit/integration/e2e methodologies but no recipe collection for the specific moves: how to capture real input, how to snapshot output safely, how to handle non-determinism, how to bound the sweep so it terminates. This methodology gives 6 recipes plus the rules that gate when each is appropriate. Output: a characterization-test suite that fails on any behavior change, ready to wrap a refactor.

## Applies If (ALL must hold)

- A legacy code path (no tests OR low-confidence tests) is targeted for refactor / migration / extraction.
- The path is callable in isolation (or behind a thin adapter that can be).
- A representative production input set is reachable (logs, sampled requests, exported fixtures).
- Refactor goal is behavior-preserving (rewrite, language migration, extract method), not behavior-changing.

## Skip If (ANY kills it)

- Code path being deleted entirely — characterization is wasted effort; just remove with grep coverage.
- Code path that is currently buggy and the refactor includes fixing the bug — pinning the bug as expected is a trap.
- Path with strong existing unit-test coverage — extend those tests, do not create a parallel characterization layer.
- Cannot get any real input sample — pure synthetic inputs miss the long-tail behavior that matters.

## Prerequisites

- Working dev environment for the legacy code (build + run).
- Ability to capture inputs (request logs, function-call traces, fixture exports).
- A scratch directory for snapshot files (git-tracked so diffs are reviewable).
- A snapshot/assertion library (pytest+syrupy, jest snapshot, approvaltests, etc).

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/testing-developer/unit-testing` | Test fundamentals (arrange-act-assert, fixtures) assumed. |
| `geek/sdlc-ai/test-golden-master-legacy-rewrite` | Geek-tier sibling for full golden-master setup; recipes here are the lighter version. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: capture before refactor, snapshot review, non-determinism handling, sweep termination, pinning the diff | ~900 |
| `content/02-output-contract.xml` | essential | Test-suite layout; fixture storage; snapshot review process | ~700 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: pinned bugs, leaked PII, flaky timestamps, etc. | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input-capture-from-logs` | sonnet | Parse logs, extract representative samples |
| `snapshot-stabilize` | sonnet | Normalize timestamps/IDs to deterministic placeholders |
| `coverage-gap-detection` | opus | Identify branches uncovered by current sweep |

## Templates

| File | Purpose |
|------|---------|
| `templates/snapshot-stabilize-rules.md` | Common normalization rules: timestamps, UUIDs, ordering |
| `templates/characterization-suite-skeleton/` | Folder layout with fixtures/, snapshots/, tests/, README |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/branch-coverage-diff.sh` | Run coverage tool, surface lines not exercised by the suite | After sweep, before refactor |

## Related

- parent skill: `solo/dev/testing-developer/`
- peer methodology: `unit-testing`, `integration-testing`, `golden-master-testing` (geek)
- external: [Working Effectively With Legacy Code, Feathers (2004)](https://www.oreilly.com/library/view/working-effectively-with/0131177052/) · [ApprovalTests.com](https://approvaltests.com/)
