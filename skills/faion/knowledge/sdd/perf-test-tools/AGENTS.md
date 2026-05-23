# Performance Testing Tools: k6 and Locust

## Summary

**One-sentence:** Implements k6 (JS, single binary) and Locust (Python, web UI) load tests with CI/CD perf gates that fail PRs on >10% p95 regression.

**One-paragraph:** Implements k6 (JS, single binary) and Locust (Python, web UI) load tests with CI/CD perf gates that fail PRs on >10% p95 regression. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- perf-test-basics output (baselines + tool choice) in hand.
- Team chose k6 (JS scripts, single binary) or Locust (Python, web UI for distributed runs).
- Want CI to fail PRs that regress latency above the configured threshold.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- perf-test-basics output (baselines + tool choice) in hand.
- Team chose k6 (JS scripts, single binary) or Locust (Python, web UI for distributed runs).
- Want CI to fail PRs that regress latency above the configured threshold.

## Skip If (ANY kills it)

- perf-test-basics output missing — define baselines first.
- Workload requires browser automation (use Playwright + Lighthouse instead).
- Need realistic browser timings (use WebPageTest, not k6/Locust).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| baselines.json | from perf-test-basics | perf-test-basics output |
| CI runner | GitHub Actions | infra |
| Test environment | staging URL + warm fixtures | infra |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[perf-test-basics]] | baselines + SLO upstream of tooling |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-k6-script` | sonnet | VU + duration + threshold setup. |
| `scaffold-locust-script` | sonnet | User class + tasks. |
| `ci-gate` | haiku | Action step calling k6 / locust + exit on threshold breach. |

## Templates

| File | Purpose |
|------|---------|
| `templates/k6-load.js` | k6 load test with thresholds + stages |
| `templates/locustfile.py` | Locust user class with weighted tasks + threshold check |
| `templates/ci-perf-gate.yml` | GitHub Actions step: run k6 with thresholds and fail PR on regression |
| `templates/_smoke-test.js` | Minimum viable filled-in artefact for sanity-checking the schema. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-perf-test-tools.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[perf-test-basics]]
- [[dev-methodologies-architecture]]
- [[cd-pipelines]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Are baselines defined AND is staging available AND is BASE_URL not prod?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.
