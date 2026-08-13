# CI Prod-Readiness Gates

## Summary

**One-sentence:** Produces a single copy-paste CI config that bundles perf-budget, a11y, SLO-instrumentation, dep-vuln, lint, and license gates with a defensible blocking policy.

**One-paragraph:** Bundles perf-budget, a11y, SLO-instrumentation, dep-vuln, lint, license gates into a single CI job definition the dev can copy-paste. Gates start as non-blocking (advisory) for 2 weeks, then ratchet to blocking. Each gate has a documented owner and an exception path (label-based bypass with audit log). Output: `.github/workflows/prod-readiness.yml` (or GitLab CI snippet) plus a `prod-readiness.yaml` budget file consumed by the job.

**Ефективно для:**

- Single CI gate замість 6 розкиданих jobs.
- Perf-budget + a11y + dep-vuln + lint + license — одне місце.
- Non-blocking → blocking ratchet (2 тижні shadow mode).
- Label-based exception path з audit log.

## Applies If (ALL must hold)

- Task is an instance of role-software-developer/Make Production Readiness a PR-Level Concern OR adjacent.
- Operator has Prerequisites available before starting.
- Output consumed by downstream PR pipeline.
- Tier == pro or higher.

## Skip If (ANY kills it)

- Team already maintains an equivalent prod-readiness gate.
- Greenfield prototype with no production users.
- Single-language script repo where the 6 gates do not apply.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Existing CI provider (GHA/GitLab) | YAML | repo |
| Perf budget for the surface | JSON | ops decision |
| Dep-vuln tool (Snyk/Dependabot/Trivy) | config | platform |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 7 testable rules with rationale + source | ~1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | ~900 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-budget-file` | sonnet | Author prod-readiness.yaml thresholds per surface. |
| `draft-gates-yml` | sonnet | Bundle 6 gates into one CI job. |
| `review-for-compliance` | opus | Cross-gate synthesis when license + dep-vuln conflict. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prod-readiness.yml` | GitHub Actions workflow bundling all 6 gates. |
| `templates/prod-readiness.yaml` | Budget config consumed by the gates. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ci-prod-readiness-gates.py` | Validate the output artefact against the schema in 02-output-contract.xml. | CI on each artefact change; pre-commit. |
| `scripts/validate-ci-prod-readiness-gates.py` | Validator script. | after subagent returns, before downstream consumer reads |

## Related

- [[capacity-bottleneck-checklist]]
- [[code-review-slo-and-rubric]]

## Decision tree

See `content/06-decision-tree.xml`. Tree routes between shipping a new gate, flipping a gate to blocking, or rolling back based on shadow-mode noise rate.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/prod-readiness.yml`

```yaml
name: prod-readiness
on:
  pull_request:

jobs:
  gates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: make lint
      - name: Perf budget
        run: scripts/check-perf-budget.sh prod-readiness.yaml
      - name: A11y
        run: pa11y-ci --config .pa11yci.json
      - name: SLO instrumentation
        run: scripts/check-slo-instrumented.sh
      - name: Dep vuln
        uses: aquasecurity/trivy-action@0.19.0
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
      - name: License
        run: scripts/check-licenses.sh
```

### `templates/prod-readiness.yaml`

```yaml
version: 1
perf_budget:
  bundle_kb_max: 220
  lcp_p95_ms: 2500
  inp_p95_ms: 200
a11y:
  wcag_level: AA
dep_vuln:
  block_severity: [HIGH, CRITICAL]
licenses:
  allowed: [MIT, Apache-2.0, BSD-3-Clause]
  denied: [AGPL-3.0]
slo:
  required_metrics: [http_requests_total, http_request_duration_seconds]
shadow_mode_days: 14
```
