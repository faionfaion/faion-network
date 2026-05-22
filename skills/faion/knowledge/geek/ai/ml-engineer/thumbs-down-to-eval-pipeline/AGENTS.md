---
slug: thumbs-down-to-eval-pipeline
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
content_id: "6cc30a59c35ed0b7"
summary: Closes the loop from a user thumbs-down (or hallucination report) to a row in the regression eval set within 24h, with PII scrubbing, judgment voting, and deterministic eval-set growth caps.
complexity: deep
produces: config
est_tokens: 4200
tags: [eval, feedback-loop, llm-ops, regression-test, ml-engineer]
---

# Thumbs Down to Eval Pipeline

## Summary

**One-sentence:** Closes the loop from a user thumbs-down (or hallucination report) to a row in the regression eval set within 24h, with PII scrubbing, judgment voting, and deterministic eval-set growth caps.

**One-paragraph:** Most LLM products collect thumbs-up/down feedback but never funnel it into evals; the data dies in a Kafka topic. This methodology codifies a 4-stage pipeline (ingest → scrub → judge → admit) plus a stop-the-bleed escalation rule (3+ thumbs-down on same response pattern → human-on-call within 4h). Eval set growth is capped at 50 rows/week to keep CI runtime bounded. Output: `EvalCandidate` records routed to admit/reject + `EvalSet` with versioned rows. Built on OpenAI Evals, Anthropic AISI patterns, and the Lilian Weng "LLM ops" playbook.

**Ефективно для:**

- Продуктів із thumbs widget + регресійним eval suite — закриває loop між сигналом і регресією за 24h, не вручну.
- Hallucination-sensitive feature (legal, medical, support) — stop-the-bleed gate ловить кластер однотипних відмов за 4h.
- CI-budget-aware команд — cap 50 rows/week тримає eval runtime bounded; eval suite не вибухає.
- Privacy-strict пайплайнів — обовʼязковий PII-scrub gate перед admit оберігає eval-suite від витоків.

## Applies If (ALL must hold)

- production LLM feature with ≥ 1000 daily interactions
- user-facing feedback widget (thumbs / report) writes to a queryable store
- existing regression eval suite with at least 50 baseline rows
- model deployment uses a runner (Modal, Replicate, vLLM, OpenAI) that supports versioned evals

## Skip If (ANY kills it)

- product has &lt; 50 daily interactions — feedback volume too thin
- no eval suite exists yet — bootstrap that first (`eval-set-bootstrap` methodology)
- PII can leak in feedback content and no scrubbing infrastructure — fix scrubbing first
- team has no triage rotation — pipeline produces alerts no one reads

## Prerequisites

- feedback store with `(interaction_id, prompt, response, signal: enum {up, down, report}, comment, timestamp, user_hash)` rows
- PII scrubber (Presidio, AWS Comprehend, regex) integrated
- eval suite stored as code (Anthropic Evals format, OpenAI Evals format, or YAML)
- on-call rotation defined for hallucination incidents

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/regression-eval-set` | Defines the eval set structure this pipeline writes to |
| `geek/ai/ml-engineer/hallucination-incident-triage` | Downstream when stop-the-bleed fires |
| `geek/ai/ml-engineer/customer-ai-feedback-triage` | Sister methodology for weekly triage; this is automated daily |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-stage pipeline, PII scrub gate, judge voting, weekly cap, stop-the-bleed | 1000 |
| `content/02-output-contract.xml` | essential | `EvalCandidate` + admitted-row schema | 700 |
| `content/03-failure-modes.xml` | essential | 6 modes: noisy thumbs, PII leak, judge bias, etc. | 900 |
| `content/04-procedure.xml` | essential | 6 steps: ingest → scrub → cluster → judge vote → admit → ship | 800 |
| `content/05-examples.xml` | essential | Worked example: 3-thumbs-down cluster fires stop-the-bleed | 500 |
| `content/06-decision-tree.xml` | essential | Routes by cluster-size, judge-vote, PII-status, weekly-cap | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `feedback_ingest_normalise` | haiku | Field extraction from queue events |
| `pii_scrub` | sonnet | Presidio-like entity detection bounded by allow-list |
| `triple_judge_vote` | sonnet | 3-judge LLM voting on whether to admit |
| `cluster_for_stop_bleed` | sonnet | Embedding clustering of same-pattern failures |
| `eval_set_admit_pr` | sonnet | Compose PR adding rows to eval suite |

## Templates

| File | Purpose |
|------|---------|
| `templates/eval-candidate.json` | EvalCandidate schema |
| `templates/admitted-row.json` | Eval suite row schema |
| `templates/stop-bleed-alert.json` | Pagerduty-compatible alert |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/ingest-pipeline.py` | Hourly: ingest, scrub, judge, queue admits | Cron hourly |
| `scripts/admit-weekly.py` | Apply weekly cap, raise eval-suite PR | Cron Fri 09:00 |
| `scripts/stop-bleed-detector.py` | Cluster-detect 3+ same failures, page on-call | Cron 15min |

## Related

- parent skill: `geek/ai/ml-engineer/`
- peer methodologies: `regression-eval-set`, `hallucination-incident-triage`, `customer-ai-feedback-triage`
- external: [Anthropic — Building Evals](https://docs.anthropic.com/claude/docs/evaluating-prompts) · [OpenAI Evals](https://github.com/openai/evals) · [Lilian Weng — LLM-powered Autonomous Agents](https://lilianweng.github.io/) · [Hamel Husain — Your AI product needs evals](https://hamel.dev/blog/posts/evals/)
