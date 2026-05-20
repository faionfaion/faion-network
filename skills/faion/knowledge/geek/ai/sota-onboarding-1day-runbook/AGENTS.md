---
slug: sota-onboarding-1day-runbook
tier: geek
group: ai
domain: ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-network]
summary: One-day runbook for evaluating + provisionally onboarding a newly-released SOTA LLM — combines model-gateway, eval suite, and router methodologies into a time-boxed decision flow.
content_id: "40b4c0be5f480605"
tags: [sota-onboarding-1day-runbook, ai, geek]
---
# SOTA Onboarding 1-Day Runbook

## Summary

**One-sentence:** A one-day runbook that takes a freshly-announced SOTA LLM from "tweet" to "provisionally wired into staging with a go/no-go decision" — combining the model-gateway, eval, and router methodologies into a fixed schedule.

**One-paragraph:** When Anthropic / OpenAI / Google ship a new flagship model, agent teams typically waste 2–3 weeks discussing whether to integrate, then either rush it or never get around to it. This runbook fixes a six-stage one-day flow (announce-scan → gateway-adapter → smoke eval → benchmark vs incumbent on the team's own eval set → cost-quality readout → go/no-go decision) with a hard 8-hour wall-clock budget. The output is either a merged adapter behind a feature flag with a documented decision, or a written "skip this release" record with reasons.

## Applies If (ALL must hold)

- a major lab released a new SOTA model in the last 7 days
- the team has an existing model-gateway adapter pattern
- the team has a non-trivial eval set (≥50 cases tied to actual product flows)
- there is an incumbent model in production to benchmark against

## Skip If (ANY kills it)

- the new release is a minor point version (e.g., 3.5.1) — schedule a normal model-upgrade check instead
- the team has no eval set — fix that first; SOTA onboarding without evals is theatre
- the model is private-preview or has no production-grade API SLA
- the team is in the middle of an active incident or migration — defer

## Prerequisites

- working `gateway-adapter-template` adapter pattern in the codebase
- a stratified eval set per `eval-set-stratified-sampling-recipe`
- benchmark harness per `rag-bench-harness-template` or equivalent
- a feature flag to route a % of traffic to the candidate model
- an explicit cost-quality budget per task (see `cost-quality-pareto-template`)

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/gateway-adapter-template` | the adapter wired in stage 2 |
| `geek/ai/llm-integration/model-migration-checklist` | the safety frame around the swap |
| `geek/ai/llm-integration/eval-set-stratified-sampling-recipe` | source of the eval set |
| `geek/ai/llm-integration/cost-quality-pareto-template` | cost-quality decision frame |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: 8-hour-wallclock, gateway-not-direct, eval-against-own-set, written-decision-record, flag-gated-rollout | ~1000 |

## Related

- parent skill: `geek/ai/llm-integration`
- upstream playbook: `p7-llm-agent-developer/Bench against new SOTA model`
- siblings: `geek/ai/model-migration-checklist`, `geek/ai/model-upgrade-checklist`
