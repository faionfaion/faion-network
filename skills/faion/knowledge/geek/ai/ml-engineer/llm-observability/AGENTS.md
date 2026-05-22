---
slug: llm-observability
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Produces an LLM observability spec covering trace coverage, cost analytics, quality evaluation, alert rules, and vendor selection (Langfuse / LangSmith / Phoenix / native OTel).
content_id: "243f8ecd439b15e3"
complexity: medium
produces: spec
est_tokens: 4200
tags: [llm, observability, tracing, monitoring, evaluation]
---
# LLM Observability and Monitoring

## Summary

**One-sentence:** Produces an LLM observability spec covering trace coverage, cost analytics, quality evaluation, alert rules, and vendor selection (Langfuse / LangSmith / Phoenix / native OTel).

**One-paragraph:** Produces an LLM observability spec. Covers tracing every LLM call (input + output + tokens + latency + cost), continuous evaluation against held-out probes, quality / cost / latency dashboards, and alert rules for cost spikes + p95 latency + quality drops. Unlike traditional APM, LLM observability focuses on non-determinism: output quality + cost / token + prompt effectiveness. Vendor choice (Langfuse, LangSmith, Arize Phoenix, native OTel) follows the data-residency + integration matrix.

**Ефективно для:** SRE / ML-ops для production LLM stack — fixed spec з trace coverage + cost + quality + alerts.

## Applies If (ALL must hold)

- LLM-powered feature in production (or pre-prod with traffic).
- Need cost / quality / latency dashboards and alerts.
- Compliance or finance requires per-call audit trail.
- Continuous-eval probes against held-out questions are planned.
- Team can absorb the observability vendor lock or stand up OTel native.

## Skip If (ANY kills it)

- One-off script / prototype — observability adds friction.
- Single LLM call per request with no chain — provider dashboard suffices.
- Air-gapped no-vendor environment — only native OTel works; vendor choice moot.
- No budget for observability infrastructure yet — defer; document the gap.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Production LLM stack | markdown | ML lead |
| Compliance / data-residency | yaml | trust+safety |
| Cost budget | yaml | finance |
| Held-out eval probes | jsonl | eval team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/llm-observability-stack` | Concrete stack implementation. |
| `geek/ai/ml-engineer/cost-optimization` | Cost-watch inputs. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/04-procedure.xml` | essential | 5-step procedure: pick-vendor → instrument-traces → wire-cost → wire-eval → wire-alerts. | ~700 |
| `content/05-examples.xml` | medium | Worked example: Langfuse stack for a multi-step agent. | ~600 |
| `content/06-decision-tree.xml` | essential | Vendor branch (Langfuse / LangSmith / Phoenix / OTel). | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-traces` | haiku | Wire @observe / langfuse_handler into existing code. |
| `design-eval-probes` | sonnet | Pick probe set + scoring rubric. |
| `audit-cost-spike` | opus | Cross-system cost-spike triage. |

## Templates

| File | Purpose |
|------|---------|
| `templates/observability-spec.md` | Spec skeleton with vendor / traces / eval / alerts. |
| `templates/langfuse-init.py` | Langfuse client init. |
| `templates/eval-probe-runner.py` | Periodic eval-probe runner. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-llm-observability.py` | Validate the spec (vendor, trace coverage, cost alert, eval cadence). | Pre-merge of every observability spec PR. |

## Related

- [[llm-observability-stack]] — concrete impl.
- [[cost-optimization]] — cost-watch.
- [[fine-tuning-openai-eval]] — eval pattern.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks vendor (Langfuse self-host / LangSmith SaaS / Phoenix OSS / native OTel) from data-residency + integration + budget.
