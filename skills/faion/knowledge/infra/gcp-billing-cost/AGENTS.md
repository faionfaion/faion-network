# Gcp Billing Cost

## Summary

**One-sentence:** Configure GCP billing accounts, budget alerts at multiple thresholds, BigQuery billing exports, and cost allocation labels for per-team chargeback and spend optimization.

**One-paragraph:** GCP billing is structured around billing accounts linked to projects, with costs attributed via resource labels. Budget alerts at 50%, 90%, and 100% thresholds prevent surprise overspend. BigQuery billing exports enable custom dashboards and per-team chargeback via label-based queries. Labels are the only mechanism for cost allocation — enforce them from day one via org policy.

**Ефективно для:**

- BigQuery billing export з добовим analysis за project/label.
- Budget alerts на 50/90/100% поточного місячного forecast.
- FinOps tagging convention (env, team, cost-center) на всіх ресурсах.
- Committed-use discount планування за 1- або 3-річними коміттами.

## Applies If (ALL must hold)

- Setting up billing for a new GCP organization, project, or environment.
- Implementing cost chargeback by team, cost center, or application.
- Configuring budget alerts before launching production workloads.
- Analyzing and optimizing existing GCP spend (rightsizing, CUDs, storage class).

## Skip If (ANY kills it)

- Pre-launch cost forecast for unknown workload — use sizing guides first.
- Per-resource debugging of a single anomaly without aggregate data.
- Non-GCP cost analysis (AWS/Azure).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| BigQuery billing export dataset | dataset id | billing admin |
| Period of interest | from / to dates | FinOps |
| Cost-center labels | label keys | FinOps |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[gcp-resource-hierarchy]] | Sibling methodology that supplies context required here. |
| [[gcp-org-policies]] | Sibling methodology that supplies context required here. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules with statement + rationale + source | ~1000 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input/action/output | ~900 |
| `content/05-examples.xml` | essential | Worked end-to-end example | ~800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule id from 01-core-rules | ~600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `decide-applicability` | sonnet | Decision tree application — needs nuance + context awareness. |
| `draft-report` | sonnet | Light judgement on field selection + naming conventions. |
| `validate-output` | haiku | Mechanical schema validation via `scripts/validate-gcp-billing-cost.py`. |

## Templates

| File | Purpose |
|------|---------|
| `templates/gcp-billing-cost.md` | Skeleton for the report artefact this methodology produces. |
| `templates/_smoke-test.md` | Minimum viable filled-in example. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-gcp-billing-cost.py` | Validate the report artefact against the JSON Schema in `02-output-contract.xml`. | CI on each artefact change; pre-commit; manual on draft. |

## Related

- [[gcp-resource-hierarchy]]
- [[gcp-org-policies]]
- [[gcp-overview-cli]]

## Decision tree

See `content/06-decision-tree.xml`. The tree branches on observable workload / configuration signals and routes to a specific rule id from `01-core-rules.xml`. Use it whenever the input shape is ambiguous between two adjacent methodologies in this sub-skill (e.g. gcp-billing-cost vs an adjacent sibling).
