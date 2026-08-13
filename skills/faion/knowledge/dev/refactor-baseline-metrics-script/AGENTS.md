# Refactor Baseline Metrics Script

## Summary

**One-sentence:** Captures pre/post refactor metrics (LOC, cyclomatic, hotspot churn, test runtime, coverage) deterministically so refactor PRs can prove the change improved measured signal.

**One-paragraph:** Captures pre/post refactor metrics (LOC, cyclomatic, hotspot churn, test runtime, coverage) deterministically so refactor PRs can prove the change improved measured signal. One script, one JSON output. Runs on the refactor branch and the base branch; produces a diff that PR reviewers consume. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Refactor PRs land without proof of improvement and reviewers cannot disprove regressions.
- Want a canonical baseline tooling that doesn't depend on flaky one-off scripts.
- Need to track refactor ROI across multiple PRs.
- Output produces `code` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Refactor PRs land without proof of improvement and reviewers cannot disprove regressions.
- Want a canonical baseline tooling that doesn't depend on flaky one-off scripts.
- Need to track refactor ROI across multiple PRs.

## Skip If (ANY kills it)

- Single-file rename or trivial reformat — metric overhead exceeds value.
- Greenfield code with no base branch to compare against.
- Org tooling (SonarQube etc.) already produces equivalent baselines.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Base branch | git ref | repo |
| Refactor branch | git ref | repo |
| Test suite | pytest/jest command | team conventions |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[django-services]] | Refactors of Django code often target this layer. |
| [[qa-suite-health-metrics-canon]] | Suite-health metrics feed the test-runtime baseline. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `capture-baseline` | haiku | Mechanical: run script on each branch. |
| `interpret-delta` | sonnet | Pass/fail vs declared targets. |

## Templates

| File | Purpose |
|------|---------|
| `templates/baseline.py` | Python scaffold realising the artefact in code. |
| `templates/targets.json` | JSON template scaffolding the artefact contract. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-refactor-baseline-metrics-script.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[qa-suite-health-metrics-canon]]
- [[decomposition-django]]
- [[code-review-process]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the refactor non-trivial and worth capturing pre/post metrics?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/baseline.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Python scaffold realising the artefact in code.","consumes":"see content/02-output-contract.xml","produces":"code","depends_on":"content/01-core-rules.xml#stdlib-only","token_budget_impact":"~150 tokens when loaded"}}
"""Refactor Baseline Metrics Script scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the refactor-baseline-metrics-script methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/targets.json`

```json
{
  "baseline_id": "refactor-f-bulk-role-edit-base",
  "branch": "main@abc123",
  "loc": 1820,
  "cyclomatic_avg": 6.4,
  "hotspot_commits_90d": 47,
  "test_runtime_sec": 312.5,
  "coverage_pct": 0.78,
  "hotspot_window_days": 90
}
```

### `templates/_smoke-test.json`

```json
{
  "baseline_id": "refactor-f-bulk-role-edit-base",
  "branch": "main@abc123",
  "loc": 1820,
  "cyclomatic_avg": 6.4,
  "hotspot_commits_90d": 47,
  "test_runtime_sec": 312.5,
  "coverage_pct": 0.78,
  "hotspot_window_days": 90
}
```
