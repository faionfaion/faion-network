<!--
purpose: Skeleton ci-design.md authors fill before opening the PR.
consumes: nothing — this IS the artefact (Markdown view; JSON view is parallel).
produces: human-readable view of the design committed next to CI config.
depends-on: CI workflow YAML; 30-day runtime data.
token-budget-impact: ~200 tokens when copied.
-->

# CI Quality Gate Design

## Tier table

| Check | Tier | runtime_p50 (min) | Owner | Last reviewed |
|-------|------|--------------------|-------|----------------|
| lint        | BLOCK | 1.2 | ruslan@faion.net | 2026-05-23 |
| typecheck   | BLOCK | 1.8 | ruslan@faion.net | 2026-05-23 |
| unit-tests  | BLOCK | 3.4 | ruslan@faion.net | 2026-05-23 |
| coverage    | WARN  | 0.5 | ruslan@faion.net | 2026-05-23 |
| mutation    | NIGHTLY | 25 | ruslan@faion.net | 2026-05-23 |

## Per-BLOCK rationale

### lint
What it catches: code style + obvious bugs (T201 print, F401 unused imports). Why BLOCK and not WARN: cheap (1.2 min) and unambiguous. Workaround: `ruff check --fix` locally before pushing.

### unit-tests
What it catches: regression in core business logic. Why BLOCK: failures correlate 1:1 with real defects. Workaround: pull failing test name from CI log, run locally with `pytest -k name`.

## Budget

| Field | Value |
|-------|-------|
| target_min | 10 |
| block_critical_path_min | 6.8 |
| headroom_min | 3.2 |

## Escalation directory

- lint / typecheck / unit-tests flapping &gt; 3 days → ping `#ci` Slack, assign to owner.
- mutation regression &gt; 2 nightly runs → file a P2 issue.

## Review log

- 2026-05-23 — initial design, ruslan@faion.net
