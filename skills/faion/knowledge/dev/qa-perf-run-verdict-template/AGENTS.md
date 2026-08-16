# QA Performance Run Verdict Template

## Summary

**One-sentence:** Records a perf run verdict: baseline + current p50/p95/p99, error rate, sample size, environment, and a binary pass/fail against pre-declared SLOs.

**One-paragraph:** Records a perf run verdict: baseline + current p50/p95/p99, error rate, sample size, environment, and a binary pass/fail against pre-declared SLOs. Verdict is binary, anchored on pre-declared SLOs. Includes baseline ref, sample size sanity, environment fingerprint, and a release-decision recommendation. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium), and a worked example live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- Release candidate has a perf gate before promotion.
- Team has historical baselines and an SLO definition per critical path.
- Need a reviewable artefact to attach to the release ticket.
- Output produces `report` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- Release candidate has a perf gate before promotion.
- Team has historical baselines and an SLO definition per critical path.
- Need a reviewable artefact to attach to the release ticket.

## Skip If (ANY kills it)

- No SLOs defined yet — write SLOs first (see perf-test-basics).
- Pre-MVP product with no users — perf gating is premature.
- Internal tool used by one team where slowness is tolerable.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Perf run results | k6/locust JSON | perf CI |
| Baseline metrics | JSON | previous green run |
| SLO definition | YAML | ops/slo.yaml |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[perf-test-basics]] | Underlying perf-test methodology. |
| [[qa-rollback-trigger-canon]] | Rollback triggers consume this verdict. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 6-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `diff-baselines` | haiku | Mechanical: percentile diffs vs baseline. |
| `apply-slo` | sonnet | Binary pass/fail per SLO. |
| `draft-recommendation` | sonnet | Release/hold/rollback recommendation. |

## Templates

| File | Purpose |
|------|---------|
| `templates/verdict.json` | JSON template scaffolding the artefact contract. |
| `templates/slo.yaml` | YAML configuration scaffolding the artefact. |
| `templates/_smoke-test.json` | Minimum viable filled-in artefact for sanity-checking the schema. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-qa-perf-run-verdict-template.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[perf-test-basics]]
- [[perf-test-tools]]
- [[qa-rollback-trigger-canon]]
- [[qa-rc-smoke-pack-template]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is there a perf gate with declared SLOs blocking release promotion?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/verdict.json`

```json
{
  "run_id": "perf-2026-05-23-rc1",
  "verdict": "FAIL",
  "baseline_ref": "perf-2026-05-16-green",
  "environment_fingerprint": "c5.2xlarge|dataset-v3|shape-A",
  "samples_per_endpoint": 4200,
  "metrics": [
    {
      "endpoint": "POST /orders",
      "p50": 145,
      "p95": 690,
      "p99": 1200,
      "error_rate": 0.002,
      "slo_target": "p95<500ms",
      "pass": false
    }
  ],
  "recommendation": "hold"
}
```

### `templates/slo.yaml`

```yaml
# faion_header_json: {"__faion_header__":{"purpose":"YAML configuration scaffolding the artefact.","consumes":"see content/02-output-contract.xml","produces":"report","depends_on":"content/01-core-rules.xml#binary-verdict","token_budget_impact":"~150 tokens when loaded"}}
# QA Performance Run Verdict Template configuration scaffold.
version: 1
slug: qa-perf-run-verdict-template
items: []
```

### `templates/_smoke-test.json`

```json
{
  "run_id": "perf-2026-05-23-rc1",
  "verdict": "FAIL",
  "baseline_ref": "perf-2026-05-16-green",
  "environment_fingerprint": "c5.2xlarge|dataset-v3|shape-A",
  "samples_per_endpoint": 4200,
  "metrics": [
    {
      "endpoint": "POST /orders",
      "p50": 145,
      "p95": 690,
      "p99": 1200,
      "error_rate": 0.002,
      "slo_target": "p95<500ms",
      "pass": false
    }
  ],
  "recommendation": "hold"
}
```
