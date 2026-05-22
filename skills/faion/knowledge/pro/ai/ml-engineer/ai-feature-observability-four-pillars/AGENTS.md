---
slug: ai-feature-observability-four-pillars
tier: pro
group: ai
domain: ai-core
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "d7de3091b0710f66"
summary: Day-1 observability for any LLM-backed feature — four pillars (latency p50/p95/p99, cost-per-request, quality score, drift signal) with concrete SLO bands the ML engineer wires before launch.
tags: [llm-observability, slo, ml-engineer, day-1, pro]
---
# AI-Feature Observability — The Four Pillars

## Summary

**One-sentence:** The canonical four observability pillars an ML engineer wires on day 1 of an LLM-backed feature — latency p50/p95/p99, cost-per-request, quality score, drift signal — each with concrete SLO bands and an alert rule.

**One-paragraph:** `llm-observability` and `llm-observability-stack` describe platform-y options (Langfuse, OTEL, Helicone) but leave the engineer guessing which signals matter. This methodology pins four non-negotiable pillars every LLM feature MUST emit before it can ship: (1) per-request latency at p50/p95/p99; (2) cost-per-request in real currency with model+token breakdown; (3) a periodic quality score from an eval set or human grade; (4) a drift signal that captures whether request distribution has shifted (input-token mean, refusal rate, semantic-cluster drift). Each pillar has a default SLO band, a default alert rule, and a default storage cadence. Output: an observability checklist signed off before launch, plus a Grafana / Datadog / Helicone / Langfuse dashboard with the four pillars side-by-side.

## Applies If (ALL must hold)

- Service exposes an LLM call in production or pre-production with real or simulated user traffic.
- A metrics + tracing backend is available (Prometheus / OTEL / Datadog / Honeycomb / Langfuse / Helicone).
- A scheduled job runner exists for eval-set runs (cron, Airflow, GitHub Actions, scheduled SDK agent).
- A finance / cost dashboard is reachable (provider console or a wrapper like LiteLLM).

## Skip If (ANY kills it)

- LLM call is one-off batch with no live user impact — only pillar 2 (cost) matters; skip 1, 3, 4.
- Feature is local-only with no production traffic — observability is dev-time; lighter setup.
- LLM call is &lt; 10 req/day — drift signal has insufficient data; revert to ad-hoc review.
- Quality is already evaluated post-hoc by a separate analytics team — only pillars 1, 2, 4 are owned by this team.

## Prerequisites

- Provider SDK or wrapper that exposes token-count + cost in every response.
- An eval set checked in as `evals/` with at minimum 50 graded examples.
- A storage backend with at least 30-day retention for traces.
- A baseline pre-launch period (1-2 weeks) during which the four pillars are sampled to set initial SLO bands.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/llm-observability` | Background on observability tooling; this methodology is the floor on top. |
| `pro/ai/ml-engineer/ai-feature-incident-runbook` | Sibling — consumes pillar signals for incident classification. |
| `geek/sdlc-ai/inc-tool-tier-approval-gate` | Tool-tier policy referenced by the alert routing. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: all four pillars present, SLO bands set from baseline, cost in currency, eval-set ownership, drift signal default | ~1100 |
| `content/02-output-contract.xml` | essential | Dashboard shape, metrics schema, alert-rule defaults | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: missing pillar, vanity SLO, eval-set rot, drift signal noise, cost in tokens not currency | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `metrics-emission-stub-generate` | haiku | Mechanical: emit the four metric definitions for the chosen backend |
| `slo-band-from-baseline-compute` | sonnet | Bounded calculation: percentile from 1-2 week sample |
| `drift-signal-design` | sonnet | Bounded judgment: pick input-token mean / refusal rate / semantic-cluster drift per feature |
| `dashboard-and-alert-rules-draft` | opus | Cross-pillar synthesis; required for incident-class mapping |

## Templates

| File | Purpose |
|------|---------|
| `templates/metric-definitions.yaml` | Authoritative metric names + units for the four pillars |
| `templates/slo-baseline.json` | SLO band record with baseline statistics |
| `templates/alert-rules.yaml` | Default alert rules per pillar, parameterised by SLO band |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/baseline-sample.py` | Sample 1-2 weeks of traffic; compute p50/p95/p99 + cost + quality + drift | Pre-launch |
| `scripts/dashboard-gen.py` | Emit Grafana / Datadog / Langfuse dashboard JSON for the four pillars | Pre-launch |
| `scripts/eval-set-runner.sh` | Run the eval set on a cadence; emit quality_score metric | Daily |

## Related

- parent skill: `pro/ai/ml-engineer/`
- peer methodologies: `ai-feature-incident-runbook`, `llm-observability`, `llm-observability-stack`
- external: [Anthropic Observability Cookbook](https://github.com/anthropics/anthropic-cookbook) · [Langfuse Docs](https://langfuse.com/docs) · [Helicone](https://helicone.ai/)
