---
slug: llm-observability-stack-2026
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Integrates Langfuse (tracing), Helicone (cost analytics), Arize Phoenix (eval), and Braintrust (multi-agent tracing) behind a one-line SDK wrapper so each tool sees the same span tree.
content_id: "19b1b24515fa6ef1"
complexity: deep
produces: config
est_tokens: 5000
tags: [observability, monitoring, llm, tracing, cost-analytics]
---
# LLM Observability Stack (2026)

## Summary

**One-sentence:** Integrates Langfuse (tracing), Helicone (cost analytics), Arize Phoenix (eval), and Braintrust (multi-agent tracing) behind a one-line SDK wrapper so each tool sees the same span tree.

**One-paragraph:** Production LLM apps need four observability planes: traces (Langfuse), cost analytics (Helicone), evaluation (Arize Phoenix), multi-agent tracing (Braintrust). Running them in silos forces redundant span emission and makes correlation impossible. This methodology defines a one-line SDK wrapper that emits OTEL-format spans consumed by all four tools, plus a hostable Langfuse + Phoenix self-host config when data-residency matters.

**Ефективно для:**

- Multi-agent product where one trace spans 5+ tool calls.
- Cost re-attribution audit (Helicone shines).
- Eval dashboard for stakeholders (Phoenix shines).
- Self-hosted observability for data-residency compliance.

## Applies If (ALL must hold)

- Pipeline runs ≥10 LLM calls per request OR multi-agent.
- Cost is non-trivial ($500/mo+).
- Team has bandwidth to wire OTEL exporters.

## Skip If (ANY kills it)

- Single-call pipeline — Helicone alone suffices.
- Spend < $100/mo — observability cost outweighs value.
- Closed-API only with provider dashboard sufficient.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| OTEL exporter | library | Already in stack or being added |
| Tool accounts | API keys | Provider signup |
| Data-residency rules | policy | Legal |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules with rationale + source | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid / invalid examples | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns (symptom / root-cause / fix) | 800 |
| `content/04-procedure.xml` | reference | 5-step procedure | 700 |
| `content/05-examples.xml` | reference | Worked example end-to-end | 500 |
| `content/06-decision-tree.xml` | essential | Routing tree referencing rule ids | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `wrapper_author` | sonnet | One-line SDK wrapper emitting OTEL spans. |
| `config_self_host` | sonnet | Langfuse + Phoenix self-host compose. |
| `dashboard_setup` | haiku | Default dashboards per tool. |

## Templates

| File | Purpose |
|------|---------|
| `templates/otel-wrapper.py` | One-line SDK wrapper skeleton |
| `templates/docker-compose.yml` | Self-host Langfuse + Phoenix compose |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-observability-stack-2026.py` | Validate JSON artefact against 02-output-contract schema | After draft, before publish |

## Related

- [[llm-cost-basics]]
- [[evaluation-framework]]

## Decision tree

See `content/06-decision-tree.xml`. Root: Is data residency required (EU)? Branches route to a rule id from `content/01-core-rules.xml` (self-host-when-residency, one-span-tree, pii-redaction-edge, ...) so every leaf is traceable to a testable statement.
