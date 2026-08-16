# QA Suite Health Metrics Canon

## Summary

**One-sentence:** Closed set of 6 suite-health metrics (flake_rate, p95_runtime_sec, failure_attribution_pct, coverage_pct, quarantine_count, mttd_minutes) with thresholds and trend direction.

**One-paragraph:** Closed set of 6 suite-health metrics (flake_rate, p95_runtime_sec, failure_attribution_pct, coverage_pct, quarantine_count, mttd_minutes) with thresholds and trend direction. Six metrics, one canonical definition, named owner, threshold + trend direction. Reported weekly; breach drives action via linked methodologies. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Test suite ≥500 tests; trends matter and per-test debugging won't scale.
- Multiple teams own subsets and need shared health signals.
- Leadership asks for test-stability KPIs and they're improvised today.
- Output produces `rubric` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Test suite ≥500 tests; trends matter and per-test debugging won't scale.
- Multiple teams own subsets and need shared health signals.
- Leadership asks for test-stability KPIs and they're improvised today.

## Skip If (ANY kills it)

- Suite < 100 tests — health is observable by eye.
- Single-team repo with informal health checks already working.
- No CI metrics platform — set up CI metrics first.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| CI history | JSON last 30 days | CI provider |
| Test ownership map | CODEOWNERS | repo |
| Existing dashboards | Grafana/Datadog access | ops |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[qa-flake-ledger-template]] | Flake rate feeds the ledger. |
| [[qa-flaky-test-root-cause-taxonomy]] | Failure attribution uses the taxonomy. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `compute-metric` | haiku | Mechanical aggregation of CI history. |
| `interpret-trend` | sonnet | Apply threshold + direction; flag breaches. |

## Templates

| File | Purpose |
|------|---------|
| `templates/canon.json` | JSON template scaffolding the artefact contract. |
| `templates/ingest.py` | Python scaffold realising the artefact in code. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-suite-health-metrics-canon.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[qa-flake-ledger-template]]
- [[qa-flaky-test-root-cause-taxonomy]]
- [[qa-rollback-trigger-canon]]
- [[qa-test-strategy-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the suite large enough that trends matter more than per-test debugging?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/canon.json`

```json
{
  "canon_id": "suite-health-1.0",
  "metrics": [
    {
      "id": "flake_rate",
      "threshold": 0.01,
      "direction": "lower_is_better",
      "owner": "alice",
      "route_to_methodology": "qa-flake-ledger-template"
    },
    {
      "id": "p95_runtime_sec",
      "threshold": 600,
      "direction": "lower_is_better",
      "owner": "bob",
      "route_to_methodology": "perf-test-tools"
    },
    {
      "id": "failure_attribution_pct",
      "threshold": 0.9,
      "direction": "higher_is_better",
      "owner": "carol",
      "route_to_methodology": "qa-flaky-test-root-cause-taxonomy"
    },
    {
      "id": "coverage_pct",
      "threshold": 0.8,
      "direction": "higher_is_better",
      "owner": "dave",
      "route_to_methodology": "qa-test-strategy-template"
    },
    {
      "id": "quarantine_count",
      "threshold": 10,
      "direction": "lower_is_better",
      "owner": "alice",
      "route_to_methodology": "qa-flake-ledger-template"
    },
    {
      "id": "mttd_minutes",
      "threshold": 30,
      "direction": "lower_is_better",
      "owner": "eve",
      "route_to_methodology": "qa-rollback-trigger-canon"
    }
  ],
  "cadence_days": 7,
  "report_window_days": 14,
  "latest_report_path": "qa/reports/2026-W21.json"
}
```

### `templates/ingest.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Python scaffold realising the artefact in code.","consumes":"see content/02-output-contract.xml","produces":"rubric","depends_on":"content/01-core-rules.xml#closed-6-metric","token_budget_impact":"~150 tokens when loaded"}}
"""QA Suite Health Metrics Canon scaffold. See AGENTS.md for context and content/02-output-contract.xml for the contract."""
from __future__ import annotations

# Minimal scaffold for the qa-suite-health-metrics-canon methodology.
# Replace this stub with real implementation; keep the header intact.

def main() -> int:
    """Entrypoint; returns exit code."""
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
```

### `templates/_smoke-test.json`

```json
{
  "canon_id": "suite-health-1.0",
  "metrics": [
    {
      "id": "flake_rate",
      "threshold": 0.01,
      "direction": "lower_is_better",
      "owner": "alice",
      "route_to_methodology": "qa-flake-ledger-template"
    },
    {
      "id": "p95_runtime_sec",
      "threshold": 600,
      "direction": "lower_is_better",
      "owner": "bob",
      "route_to_methodology": "perf-test-tools"
    },
    {
      "id": "failure_attribution_pct",
      "threshold": 0.9,
      "direction": "higher_is_better",
      "owner": "carol",
      "route_to_methodology": "qa-flaky-test-root-cause-taxonomy"
    },
    {
      "id": "coverage_pct",
      "threshold": 0.8,
      "direction": "higher_is_better",
      "owner": "dave",
      "route_to_methodology": "qa-test-strategy-template"
    },
    {
      "id": "quarantine_count",
      "threshold": 10,
      "direction": "lower_is_better",
      "owner": "alice",
      "route_to_methodology": "qa-flake-ledger-template"
    },
    {
      "id": "mttd_minutes",
      "threshold": 30,
      "direction": "lower_is_better",
      "owner": "eve",
      "route_to_methodology": "qa-rollback-trigger-canon"
    }
  ],
  "cadence_days": 7,
  "report_window_days": 14,
  "latest_report_path": "qa/reports/2026-W21.json"
}
```
