# Characterization Test Recipes

## Summary

**One-sentence:** Concrete recipes for writing characterization tests that pin observable behavior of legacy code before any refactor — input fuzzing, output snapshotting, side-effect capture — so the refactor diff is the only behavior change.

**One-paragraph:** Michael Feathers's premise (Working Effectively With Legacy Code): you cannot refactor what you cannot test, and legacy code by definition has no tests. The fix is characterization tests — tests that document what the code currently does, not what it should do. Faion has unit/integration/e2e methodologies but no recipe collection for the specific moves: how to capture real input, how to snapshot output safely, how to handle non-determinism, how to bound the sweep so it terminates. This methodology gives 6 recipes plus the rules that gate when each is appropriate. Output: a characterization-test suite that fails on any behavior change, ready to wrap a refactor.

**Ефективно для:**

- Solo dev rewriting legacy code with no tests; wants a safety net before the diff.
- Outsource lead inheriting a codebase with low coverage and a refactor mandate.
- Language migration (Python → Go, JS → TS) — pin behavior before porting.
- AI-assisted refactor — LLM rewrites are safer when wrapped by characterization snapshots.

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

| Artefact | Format | Source |
|----------|--------|--------|
| Working dev environment for the legacy code | repo | repo |
| Input capture (logs, traces, fixtures) | JSON / replay | observability / staging |
| Scratch directory for snapshots | path | repo |
| Snapshot library | code | pytest+syrupy / jest snapshot / approvaltests |
| Branch-coverage tooling | code | coverage.py / istanbul |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/behavior-parity-verification` | Sibling: parity for production traffic; characterization for offline replay. |
| `geek/sdlc-ai/test-golden-master-legacy-rewrite` | Geek-tier sibling for full golden-master setup; recipes here are the lighter version. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ rules: capture-before-refactor, snapshot-review, non-determinism normalization, sweep termination, pin the diff, run + skip | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for the suite-manifest artefact + valid/invalid + forbidden | 800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: pinned bugs, leaked PII, flaky timestamps, snapshot churn, coverage illusion, oracle-mining | 800 |
| `content/04-procedure.xml` | medium | 5-step procedure: capture → normalize → snapshot → sweep → wrap-refactor | 700 |
| `content/06-decision-tree.xml` | essential | Tree: tests exist? bug-on-purpose? real input? → verdict | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input-capture-from-logs` | sonnet | Parse logs, extract representative samples. |
| `snapshot-stabilize` | sonnet | Normalize timestamps / IDs to deterministic placeholders. |
| `coverage-gap-detection` | opus | Identify branches uncovered by current sweep. |

## Templates

| File | Purpose |
|------|---------|
| `templates/characterization-test-recipes.json` | JSON Schema for the suite-manifest artefact. |
| `templates/snapshot-stabilize-rules.md` | Common normalization rules: timestamps, UUIDs, ordering. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-characterization-test-recipes.py` | Validate the suite-manifest JSON against schema + branch-coverage rule. | After sweep, before refactor begins. |

## Related

- [[behavior-parity-verification]] — parity for production traffic, sibling to this offline-replay methodology.
- [[ci-quality-gate-design]] — CI gate that blocks refactor PRs without a characterization manifest.
- external: [Working Effectively With Legacy Code, Feathers (2004)](https://www.oreilly.com/library/view/working-effectively-with/0131177052/) · [ApprovalTests.com](https://approvaltests.com/)

## Decision tree

See `content/06-decision-tree.xml`. The tree first checks whether the path has strong existing coverage (skip) or is being deleted (skip). It then verifies real input samples are available and branch coverage meets the threshold (≥70% lines covered by the sweep). Leaves emit `wrap-refactor`, `block-insufficient-coverage`, `block-bug-on-purpose`, or `skip-deleting-code`. Each leaf references a rule in `01-core-rules.xml`.
