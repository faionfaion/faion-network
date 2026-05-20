---
slug: rag-canary-rollout-plan
tier: geek
group: ai
domain: ml-ops
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
content_id: "e1dc6570331dfbe4"
summary: A staged-rollout plan for a RAG-backed feature with answer-quality-based auto-rollback — canary percentage curve, golden-eval guardrails, online-quality scoring, kill-switch criteria, and a 60-second rollback path.
tags: [rag, canary, rollout, auto-rollback, answer-quality, llm-feature]
---

# RAG Canary Rollout with Auto-Rollback

## Summary

**One-sentence:** Ship a RAG-backed feature on a staged canary (1% → 5% → 25% → 100%) with golden-eval guardrails before each step, live answer-quality scoring at the gateway, and an auto-rollback trigger when quality drops below the floor for ≥ 5 minutes.

**One-paragraph:** ml-ops covers drift monitoring; canary rollout for RAG features specifically needs answer-quality scoring and an auto-rollback decision tree. Traditional canaries gate on latency and error rate; RAG features additionally need to gate on answer quality (groundedness, relevance, completeness) because a "successful" call with low latency can still be a wrong answer. The methodology pins six choices: (1) the canary curve (1% / 5% / 25% / 100% with hold periods), (2) the golden-eval gate at each step (offline regression on a frozen set), (3) the online-quality scoring stack (LLM-as-judge or rubric-based, sampled), (4) the rollback floor (paired with the eval suite), (5) the kill-switch trigger logic, (6) the rollback path that must complete in &lt; 60 seconds. Primary output: a rollout-plan.yaml + an answer-quality dashboard + a rehearsed rollback runbook.

## Applies If (ALL must hold)

- production system has a RAG-backed feature ready to ship (new or major change)
- LLM gateway or proxy exists with traffic-routing primitives (percentage split, kill switch)
- frozen golden-eval set exists for the feature (≥ 50 representative questions)
- answer-quality scoring runs (or can run) on a sample of live traffic

## Skip If (ANY kills it)

- pre-launch feature with no live traffic — golden eval is sufficient; canary applies after launch
- no eval set — build the eval first, canary is downstream
- gateway cannot do percentage splits — implement the split first; client-side feature flags are too leaky for RAG quality canary
- single user / private beta with manual quality review — direct rollout with manual oversight, canary overhead is excess

## Prerequisites

- working RAG pipeline that the rollout will target
- frozen golden eval set with per-question expected answer or expected facts
- answer-quality scoring infrastructure (LLM judge, rubric scorer, or human review queue)
- gateway with kill-switch primitive that fires in &lt; 60 seconds

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/prompt-version-pinning-runbook` | Pinned prompt version is the unit being canaried |
| `geek/ai/rag-engineer/rag-eval-strategy` | The eval framework feeding both offline and online quality scoring |
| `pro/infra/devops-engineer/dora-metrics` | MTTR target for the rollback |

## Content

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules: canary curve, golden eval at each step, online quality scoring, kill-switch criteria, 60s rollback | ~900 |
| `content/02-output-contract.xml` | essential | rollout-plan.yaml + online-quality-event + rollback-receipt schemas | ~600 |
| `content/03-failure-modes.xml` | essential | 6 failure modes: kill-switch slow, eval-set stale, sampling-too-thin, etc. | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `golden_eval_run_at_step` | sonnet | Per-step eval execution and delta interpretation |
| `online_quality_judge` | sonnet | Per-sample bounded judgment using rubric |
| `canary_health_summary` | sonnet | Cross-metric synthesis per step |
| `rollback_orchestration` | opus | Cross-system reasoning during an incident (gateway, observability, comms) |

## Templates

| File | Purpose |
|------|---------|
| `templates/rollout-plan.yaml` | Per-feature rollout plan with curve, gates, floors |
| `templates/answer-quality-rubric.md` | Rubric for the online judge: groundedness, relevance, completeness, hallucination |
| `templates/rollback-runbook.md` | The 60-second runbook for kill-switch + comms |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/canary-step-gate.py` | At each step transition, runs golden eval, computes pass/fail, posts to channel | Step boundary |
| `scripts/online-quality-monitor.py` | Samples live traffic, scores via judge, alerts on floor breach | Continuous during canary |
| `scripts/auto-rollback-trigger.py` | When online quality &lt; floor for N consecutive minutes, fires the kill switch and records the receipt | On floor breach |

## Related

- parent skill: `geek/ai/ml-ops/SKILL.md`
- peer methodologies: `geek/ai/rag-engineer/rag-eval-strategy`, `geek/ai/ml-engineer/prompt-version-pinning-runbook`, `geek/ai/ml-ops/llm-observability-stack-2026`
- external: [DeepEval / RAGAS / Ragatouille evaluation tooling] · [LangSmith canary deployment docs] · [Microsoft RAG production case studies] · [Google PaLM/Gemini deployment whitepapers on quality canaries]
