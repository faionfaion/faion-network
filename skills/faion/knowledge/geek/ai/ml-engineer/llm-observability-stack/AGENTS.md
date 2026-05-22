---
slug: llm-observability-stack
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces a production LLM observability stack config: OpenTelemetry collectors, Langfuse / Prometheus / Grafana wiring, alert rules, and PII-redaction pipeline.
content_id: "1d558b8a4c5004cc"
complexity: deep
produces: config
est_tokens: 3700
tags: [llm, observability, tracing, monitoring, otel, langfuse, prometheus]
---
# LLM Observability Stack

## Summary

**One-sentence:** Produces a production LLM observability stack config: OpenTelemetry collectors, Langfuse / Prometheus / Grafana wiring, alert rules, and PII-redaction pipeline.

**One-paragraph:** Produces a production LLM observability stack config. Vendor-neutral OpenTelemetry-first approach for 2026: OTel collectors, Langfuse for LLM-specific tracing + cost analytics, Prometheus + Grafana for metrics, Alertmanager for paging, and a PII-redaction pipeline at the collector. The methodology pins the stack components, their versions, and the integration recipes for OpenAI / Anthropic / Gemini / LangGraph / LlamaIndex.

**Ефективно для:** SRE / Platform engineer для production LLM observability — fixed stack YAML з components + versions + alert rules.

## Applies If (ALL must hold)

- Deploying LLM in production with multi-step chains / agents.
- Need vendor-neutral OTel-first stack (avoid lock-in).
- Have Kubernetes / Docker compose infra to host OTel + Langfuse + Prom + Grafana.
- Compliance requires EU-resident self-hosted observability.
- Multiple LLM providers (OpenAI + Anthropic + Gemini) in one product.

## Skip If (ANY kills it)

- Single-provider deployment with provider-native dashboard adequate.
- Sub-scale workload — vendor SaaS (LangSmith) is cheaper than running the stack.
- Air-gapped environment with no GitHub/upstream access — vendor offline support needed.
- Cannot dedicate one engineer to operate the stack.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| k8s/docker infra | yaml | platform |
| Data-residency policy | yaml | trust+safety |
| LLM-provider catalogue | yaml | ML lead |
| Cost budget for stack | yaml | finance |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-observability` | Parent spec — this is its concrete impl. |
| `geek/ai/ml-engineer/cost-optimization` | Cost-rule sources. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 6-step procedure: deploy-otel → deploy-langfuse → deploy-prom → wire-instrumentation → wire-pricing → wire-alerts. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch by deployment topology + integration matrix. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-yaml` | haiku | Fill langfuse-stack.yaml + alert-rules.yaml + pricing.yaml. |
| `design-integration` | sonnet | Wire SDKs (langfuse / openllmetry / native OTel) per provider. |
| `debug-collector` | opus | OTel collector pipeline triage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/langfuse-stack.yaml` | Docker / k8s spec for Langfuse self-host. |
| `templates/alert-rules.yaml` | Alertmanager rules: cost / latency / quality. |
| `templates/pricing.yaml` | Per-provider per-model token-price book. |
| `templates/otel-collector-config.yaml` | OTel collector pipeline (receive → process → export). |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-observability-stack.py` | Validate the stack config (versions, components, alert rules, pricing). | Pre-merge of every stack-config PR. |

## Related

- [[llm-observability]] — parent spec.
- [[cost-optimization]] — cost-rule inputs.
- [[claude-api]] / [[gemini-api]] — provider SDKs to instrument.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks deployment topology (docker compose dev / k8s prod / managed) and integration choice per provider.
