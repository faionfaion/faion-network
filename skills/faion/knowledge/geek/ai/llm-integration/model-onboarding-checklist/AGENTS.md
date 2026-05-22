---
slug: model-onboarding-checklist
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Step-by-step checklist from "new SOTA model announced" to "gated in production" — pulls the right slices of gateway, router, eval methodologies into a single sheet.
content_id: "927620cb249ee876"
tags: [llm,model-onboarding,gateway,router,eval,production-gating]
---
# Model Onboarding Checklist

## Summary

**One-sentence:** Step-by-step checklist from "new SOTA model announced" to "gated in production" — pulls the right slices of gateway, router, eval methodologies into a single sheet.

**One-paragraph:** When a new model lands (Claude 4.7, GPT-5, Gemini 3, open-source), LLM-agent teams scramble through 6+ scattered methodologies (gateway config, router weights, eval suite refresh, cost calibration, safety guardrails, rollback plan). This methodology unifies them into one 12-step onboarding checklist with explicit per-step owners, gate criteria, and exit conditions. Mechanism: 4 phases (intake → safety/eval → integration → production-gate), with per-step references to the underlying methodology, plus a "go/no-go" gate decision at each phase boundary. Primary output: a per-model onboarding record (Notion / repo / Jira epic) with completion status, evaluation diffs vs incumbent, and named approver for production exposure.

## Applies If (ALL must hold)

- team operates an LLM-agent system with ≥ 1 model in production
- team owns a model gateway / router (LiteLLM, custom proxy, in-house) OR direct provider integration
- team has an eval suite (golden set, hallucination tests, etc.) per F-feature
- ≥ 1 production model is on a SaaS provider with a release cadence (Anthropic, OpenAI, Google)
- engineering team can pause or roll back model routing

## Skip If (ANY kills it)

- single-model deployment with no router — onboarding is a simple swap
- experimental sandbox with no production exposure
- regulated environment where model changes require external certification — separate flow
- internal-only tooling where cost / safety budget is fully discretionary
- team uses a fully-managed provider (e.g., Vertex AI Agent Builder) that auto-onboards models

## Prerequisites (must be true before starting)

- new model is publicly available OR private-beta access confirmed
- API endpoint + auth credentials provisioned in dev / staging
- baseline golden set + hallucination test suite ready
- incumbent model's per-task accuracy + cost recorded
- on-call team informed of onboarding timeline + rollback plan

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ai-agents/model-gateway` | Gateway config patterns this checklist references |
| `geek/ai/ml-engineer/router-weights` | Per-task routing rules and weight updates |
| `pro/ai/ml-engineer/golden-set-curation-and-maintenance` | Eval runs against the new model |
| `pro/ai/qa-engineer/llm-hallucination-test-patterns` | Hallucination regression check |
| `geek/ai/ai-agents/cheap-guardrail-tripwire` | Safety guardrail re-verification |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: 4-phase sequence, per-phase gate, eval-before-route, cost-vs-incumbent compare, named approver | ~1000 |
| `content/02-output-contract.xml` | essential | Onboarding-record schema, per-step status, gate decisions, rollback plan | ~700 |
| `content/03-failure-modes.xml` | essential | 7 failure modes (skip eval, instant route, vibes-promotion, etc.) | ~1100 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `intake_step_executor` | haiku | Standard step executor (gateway-register, auth, smoke) |
| `eval_run_orchestrator` | sonnet | Run golden + hallucination suites against new model |
| `cost_comparator` | haiku | Compute $/task delta vs incumbent |
| `gate_decision_drafter` | sonnet | Compose go/no-go memo with evidence |

## Templates

| File | Purpose |
|------|---------|
| `templates/onboarding-checklist.md` | 12-step master checklist |
| `templates/phase-gate-memo.md` | Per-phase go/no-go decision memo |
| `templates/cost-comparison.md` | Per-task cost / accuracy diff vs incumbent |
| `templates/rollback-plan.md` | Per-model rollback procedure |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/smoke-test-new-model.sh` | Run smoke test via gateway | Phase 1 |
| `scripts/eval-diff-report.py` | Diff eval results vs incumbent | Phase 2 |
| `scripts/cost-calc.py` | Project monthly cost based on route share | Phase 3 |
| `scripts/canary-route-switcher.sh` | Switch a percentage of traffic to new model | Phase 4 |

## Related

- parent skill: `geek/ai/llm-integration/`
- peer methodologies: `golden-set-curation-and-maintenance`, `llm-hallucination-test-patterns`, `geek/ai/ai-agents/model-gateway`
- external: [LiteLLM model registry](https://docs.litellm.ai/) · [Anthropic model card archive](https://docs.anthropic.com/claude/docs/models-overview) · [OpenAI model release notes](https://platform.openai.com/docs/models)
