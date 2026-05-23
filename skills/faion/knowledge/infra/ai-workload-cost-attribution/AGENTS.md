# AI Workload Cost Attribution

## Summary

**One-sentence:** Per-tenant / per-feature LLM + GPU cost attribution: token-meter ingestion, GPU-second mapping, cost-per-request rollup, monthly invoice-ready report.

**One-paragraph:** Per-tenant / per-feature LLM + GPU cost attribution: token-meter ingestion, GPU-second mapping, cost-per-request rollup, monthly invoice-ready report. This methodology converts the inputs in Prerequisites into the artefact described in Output Contract, gated by the rules in 01-core-rules.xml and the decision tree in 06-decision-tree.xml.

**Ефективно для:** the kinds of tasks listed in 'Applies If' — primary use cases are teams shipping the artefact (`report`) at a medium complexity level, where the failure modes in 03-failure-modes.xml are realistic risks worth the methodology's overhead.

## Applies If (ALL must hold)

- Production LLM / GPU workload with ≥2 tenants or features sharing one provider account.
- Monthly cost ≥$2k OR per-tenant unit economics are required.
- Token meter (provider API or self-hosted gateway) is available.

## Skip If (ANY kills it)

- Single-tenant single-feature workload — flat monthly invoice suffices.
- Pre-revenue workload <$100/month — overhead exceeds value.
- Provider does not expose per-call usage metadata (rare in 2026).

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| LLM usage events | OTel GenAI spans / provider usage API | llm-observability |
| GPU node metrics | DCGM / NVML exporter | platform team |
| Tenant tag | header / JWT claim | API gateway |
| Pricing catalogue | JSON / YAML | FinOps team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-observability` | Token & latency telemetry source. |
| `pro/infra/devops-engineer/cost-monitoring-baseline` | Underlying FinOps stack. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3-5 antipatterns with symptom/root-cause/fix | ~800 |
| `content/04-procedure.xml` | medium | 4-6 step procedure with input/action/output per step | ~900 |
| `content/05-examples.xml` | medium | One end-to-end worked example | ~800 |
| `content/06-decision-tree.xml` | essential | Decision tree gating whether this methodology applies | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `usage_event_normalize` | haiku | Deterministic schema mapping. |
| `cost_rollup_per_tenant` | sonnet | Aggregate + reconcile against provider invoice. |
| `variance_explain` | opus | Diagnose >10% variance between rollup and invoice. |

## Templates

| File | Purpose |
|------|---------|
| `templates/attribution-report.md` | Monthly per-tenant cost report skeleton. |
| `templates/pricing-catalogue.yaml` | Provider pricing as machine-readable YAML. |
| `templates/usage-event-schema.json` | Canonical usage event JSON Schema. |
| `templates/_smoke-test.md` | Minimum-viable filled-in example (smoke test). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-workload-cost-attribution.py` | Validate methodology output against `02-output-contract.xml` schema. | Pre-commit and CI before merge. |

## Related

- parent skill: `geek/infra/`
- `[[llm-observability]]`
- `[[cost-monitoring-baseline]]`

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether ai-workload-cost-attribution applies: root question — "Are there ≥2 tenants/features sharing one LLM/GPU provider account AND monthly cost ≥$2k?". Branches lead to a specific core rule (e.g., `rule:r1`) when the methodology fits, or to a `skip-this-methodology` conclusion when it does not.
