---
slug: structured-output-patterns
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Advanced structured-output: Pydantic + retry-with-error + streaming JSON + StructuredOutputService abstraction with metrics, fallback, and provider-router.
content_id: "d5780b1f38c3e988"
complexity: deep
produces: code
est_tokens: 3700
tags: [structured-output, pydantic, json, validation, agent-pipeline]
---
# Structured Output Patterns

## Summary

**One-sentence:** Advanced structured-output: Pydantic + retry-with-error + streaming JSON + StructuredOutputService abstraction with metrics, fallback, and provider-router.

**One-paragraph:** Production patterns beyond basics: a StructuredOutputService class that wraps provider-native structured output with metrics (parse_success_rate, retry_count, latency_p95), automatic provider failover, streaming JSON handling (parse partial as it arrives), and schema-evolution helpers (additive-only changes, deprecation paths). Pulls from real agent pipelines where parse failures are SLO-tracked.

**Ефективно для:** Команд, що мають кілька десятків структурованих ендпойнтів у проді і хочуть один сервіс зі SLO замість десятка ad-hoc парсерів.

## Applies If (ALL must hold)

- you have ≥3 structured-output endpoints in production
- you need parse_success_rate as an SLO
- schema evolution is happening — fields added/deprecated
- you have a provider-failover requirement (OpenAI ↔ Anthropic)
- streaming is in scope for at least some endpoints

## Skip If (ANY kills it)

- you only have 1-2 structured-output calls — use structured-output-basics
- single-provider deployment with no failover need
- streaming not needed — single-shot is enough
- no metrics infrastructure yet — build metrics first

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=code + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=code`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-structured-output-patterns.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/structured-output-service.py` | StructuredOutputService class with metrics + retry + failover |
| `templates/agent-task-schema.py` | Example Pydantic schema with versioning convention |
| `templates/partial-stream-parse.py` | Incremental JSON parsing for streaming endpoints |
| `templates/metrics-dashboard.md` | Suggested per-schema metric panels |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-structured-output-patterns.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-service-abstraction`, `r2-metrics-required`, `r3-bounded-retry`, `r4-additive-only`, `r5-stream-incremental-parse` from `content/01-core-rules.xml`.
