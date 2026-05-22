---
slug: ai-cost-attribution-schema
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a JSON Schema + middleware spec that tags every LLM call with tenant, feature, route, model, prompt-cache-hit so cost reports are sliceable per dimension.
content_id: "9e83778f2c9a8314"
complexity: medium
produces: spec
est_tokens: 3300
tags: [cost, attribution, finops, observability, llm-integration]
---
# AI Cost Attribution Schema

## Summary

**One-sentence:** Produces a JSON Schema + middleware spec that tags every LLM call with tenant, feature, route, model, prompt-cache-hit so cost reports are sliceable per dimension.

**One-paragraph:** A raw vendor invoice is a single number ("$8,431 this month"). Without an attribution schema the team cannot answer "which feature caused the increase?", "which tenant cost us money?", "did the prompt-cache rollout pay off?". This methodology defines the mandatory call-side metadata (tenant_id, feature, route, model, prompt_cache_hit, input_tokens, output_tokens, latency_ms, request_id), the middleware that stamps it on every request, and a daily aggregator producing a sliceable table. The schema is shared between the app, the FinOps team, and the cost dashboard.

**Ефективно для:** multi-tenant SaaS, internal AI tools shared across teams, agents with parallel tool calls, model-routing pipelines that need ROI evidence.

## Applies If (ALL must hold)

- Monthly LLM bill exceeds the threshold where slicing matters (≥ $1k/mo typical).
- Application has ≥2 features or tenants that should be attributable.
- A telemetry pipeline (logs, OTel, ClickHouse, etc.) can ingest structured records.
- A FinOps or engineering owner consumes the resulting report.

## Skip If (ANY kills it)

- Single-feature single-tenant prototype — attribution overhead exceeds insight.
- LLM bill below $100/mo — slicing doesn't unlock budget decisions.
- No telemetry pipeline yet — fix that first; this methodology assumes ingestion exists.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| List of features calling LLMs | YAML | engineering wiki |
| Tenant model (multi/single) | doc | architecture |
| Telemetry ingest endpoint | URL + creds | observability stack |
| Vendor pricing per model | table | finance |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `[[latency-vs-quality-decision-grid]]` | Routing config consumes the cost column. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|---|---|---|---|
| `content/01-core-rules.xml` | essential | 6 testable rules: 8 required tags, middleware-stamped, no-blank-tenant, cost computed at write, daily aggregator, dashboard | ~700 |
| `content/02-output-contract.xml` | essential | JSON Schema for per-call record + aggregated daily table | ~700 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns: optional tags, tenant-as-string, cost-at-read-time, sampled-not-full, no-aggregator | ~600 |
| `content/04-procedure.xml` | medium | 6-step procedure: list features → define schema → wire middleware → ingest → aggregate → dashboard | ~800 |
| `content/06-decision-tree.xml` | essential | Root: "monthly bill > $1k AND ≥2 attribution dimensions matter?" | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|---|---|---|
| Inventory feature list | sonnet | Mechanical extraction from code. |
| Author middleware sketch | opus | Cross-language reasoning. |
| Aggregate SQL drafted | haiku | Pure SQL template. |
| Dashboard layout | sonnet | UX-light. |

## Templates

| File | Purpose |
|---|---|
| `templates/attribution.schema.json` | JSON Schema for per-call attribution record. |
| `templates/middleware.py` | Python middleware reference (FastAPI/Django shape). |
| `templates/middleware.ts` | TypeScript middleware reference (Express/Next shape). |
| `templates/daily-aggregator.sql` | SQL aggregator producing the daily attribution table. |
| `templates/_smoke-test.json` | Single valid attribution record. |

## Scripts

| File | Purpose | When to call |
|---|---|---|
| `scripts/validate-ai-cost-attribution-schema.py` | Validates a JSONL of attribution records against the schema and asserts no records have blank/generic tenant or feature. | Pre-commit on test fixtures; CI on dashboard data sources. |

## Related

- parent skill: `geek/ai/llm-integration/`
- `[[latency-vs-quality-decision-grid]]` — consumes the per-call cost
- `[[llm-drift-daily-triage]]` — references cost deltas

## Decision tree

The decision tree at `content/06-decision-tree.xml` filters whether attribution is worth the wiring: skip when bill or feature count is tiny; route to baseline-instrumentation-first when telemetry pipe is missing.
