---
slug: shadow-traffic-rollout-pattern
tier: pro
group: ml-engineer
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "0beaa317c80d6a68"
summary: AI-specific shadow rollout pattern for new model + prompt combos — mirror live traffic, compute per-request quality delta with a judge, gate promotion on the paired quality + latency + cost metric rather than feature-flag percentage.
tags: [shadow-deploy, model-rollout, llm-quality, ml-engineer, feature-flags]
---

# Shadow Traffic Rollout Pattern

## Summary

**One-sentence:** AI-specific shadow rollout — mirror production traffic to a candidate model+prompt, compute per-request quality delta via judge, gate promotion on quality + latency + cost metric, NOT on time-in-flag or simple percentage rollout.

**One-paragraph:** Generic feature-flag rollout (10%, 25%, 50%, 100% based on no-error-spike) is insufficient for AI features because errors are not the dominant risk — quality regression is. A model + prompt change can pass health checks while producing subtly worse outputs that surface as CSAT drift two weeks later. This methodology pins an AI-specific shadow protocol: mirror 100% of live traffic to the candidate, NEVER return its output to users, compute per-request quality delta using a judge (LLM-judge or rubric-based), latency delta, cost delta, and gate promotion on all three being within the contract for ≥48 hours of representative traffic AND ≥500 scored requests. Then proceed with the standard percentage rollout but with the shadow remaining active as a continuous quality monitor. Mechanism: shadow window → joint metric review → gradual real-traffic split → continuous shadow monitor. Primary output: a `shadow-rollout.yaml` config + per-window quality report.

## Applies If (ALL must hold)

- AI feature is being upgraded (new model, new prompt, new chunk strategy, new tool set)
- existing production version handles ≥500 requests / week (enough volume to gather scores)
- a judge or rubric exists to score quality (LLM-judge, expert label, or proxy signal)
- the feature is user-facing (errors and quality matter to end-users), not internal-only
- rollback path defined

## Skip If (ANY kills it)

- internal-only AI tool with no end-users — A/B at engineering speed instead
- traffic too low (&lt;100 req/week) — gather more first; shadow without volume is anecdote
- no judge available — build offline labelled dataset first
- non-AI feature — use the generic feature-flag rollout methodology

## Prerequisites

- traffic-mirror primitive (gateway, sidecar, app-level)
- judge configured (LLM-judge with pinned model version, OR expert label, OR business proxy)
- baseline cost and latency captured for current version
- rollout flag system (LaunchDarkly, Unleash, Statsig, or in-house feature flags)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/rag-feature-acceptance-contract` | Defines the metrics the shadow gates against (if a contract is in place) |
| `geek/ai/ml-engineer/router-shadow-deploy-protocol` | Specialised geek-tier sibling for routers; this is the broader pro-tier pattern |
| `pro/infra/devops-engineer/canary-and-feature-flags` | Underlying flag machinery |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: shadow-first not flag-first, joint quality+latency+cost gate, judge calibration, sustained window, continuous shadow post-promotion | ~1000 |
| `content/02-output-contract.xml` | essential | shadow-rollout.yaml schema, per-window quality report, promotion gate decision | ~800 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: judge-pinning omitted, premature promotion, shadow leak, etc. | ~1000 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `per_request_judge_call` | sonnet | High volume bounded scoring |
| `quality_delta_summary` | sonnet | Compact per-window summary |
| `promotion_recommendation` | opus | Cross-metric synthesis with risk framing |
| `shadow_health_monitor` | n/a | Deterministic |

## Templates

| File | Purpose |
|------|---------|
| `templates/shadow-rollout.schema.yaml` | Config schema |
| `templates/quality-report.md` | Per-window quality report layout |
| `templates/promotion-decision.md` | Go/no-go template with sign-off |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/score-shadow-window.py` | Run judge over the shadow window's scored requests; produce report | Nightly during shadow |
| `scripts/promote-or-hold.py` | Apply joint-gate logic; return decision and rationale | Before each rollout step |

## Related

- parent skill: `pro/ai/ml-engineer/`
- peer methodologies: `router-shadow-deploy-protocol` (geek), `rag-feature-acceptance-contract`, `retrieval-drift-alerting-recipe`, `canary-and-feature-flags`
- external: [Anthropic — Building effective AI agents](https://www.anthropic.com/research) · [LaunchDarkly — Feature flag best practices](https://launchdarkly.com/) · [Statsig — Experimentation platform](https://statsig.com/)
