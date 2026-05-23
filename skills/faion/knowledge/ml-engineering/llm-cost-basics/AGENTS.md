# LLM Cost Basics — Pricing, Usage Tracking, Baseline Optimisation

## Summary

**One-sentence:** Tracks per-call input/output tokens + cost, attributes spend by feature / tenant, and applies the cheap baseline optimisations (cache, truncate, route) before considering anything exotic.

**One-paragraph:** Before reaching for advanced cost reduction (cost-reduction-strategies), get the basics right: every call carries input_tokens, output_tokens, model_id, feature_id, tenant_id; spend is attributable; baselines (response cache, prompt truncation to last-N turns, model router default-to-cheap) are applied; per-feature cost is published in a dashboard the team can see weekly.

**Ефективно для:**

- First production launch where cost was not measured before.
- Cost-related stakeholder pressure ('why is our bill $X?').
- Multi-tenant SaaS where per-tenant cost must be billable.
- Pre-pivot to cost-reduction-strategies (need the baseline first).

## Applies If (ALL must hold)

- Pipeline emits LLM calls in production.
- Cost > $50/mo and rising.
- Observability stack exists (or will exist) to log per-call metadata.

## Skip If (ANY kills it)

- Spend < $10/mo — overhead exceeds value.
- Already past basics — use cost-reduction-strategies for advanced levers.
- Self-hosted only — different cost model (GPU hours, not tokens).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Provider invoice | PDF/CSV | Finance |
| Per-call log | JSONL | Observability |
| Feature taxonomy | list | Product |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `log_emitter` | haiku | Add input_tokens/output_tokens/model_id to each call. |
| `attribution` | sonnet | Map calls → feature + tenant. |
| `dashboard_author` | haiku | Per-feature spend chart. |

## Templates

| File | Purpose |
|------|---------|
| `templates/usage-log.json` | Per-call usage log schema |
| `templates/cost-dashboard.md` | Weekly cost dashboard skeleton |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-cost-basics.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[cost-reduction-strategies]]
- [[llm-observability-stack-2026]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is per-call metadata logged? Branches route to a rule id from `content/01-core-rules.xml` (per-call-metadata, cache-as-baseline, truncate-history-default, ...) so every leaf is traceable to a testable statement.
