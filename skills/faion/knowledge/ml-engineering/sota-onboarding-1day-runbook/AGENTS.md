# SOTA Onboarding 1-Day Runbook

## Summary

**One-sentence:** Wires a freshly released SOTA LLM into staging in one day: announce-scan → gateway adapter → smoke eval → bench vs incumbent → cost-quality readout → GO/NO-GO.

**One-paragraph:** When Anthropic / OpenAI / Google ship a new flagship model, teams typically waste 2-3 weeks discussing whether to integrate, then either rush it or never get around to it. This runbook fixes a six-stage one-day flow with a hard 8-hour wall-clock budget. The output is either a merged adapter behind a feature flag with a documented decision, or a written 'skip this release' record with reasons.

**Ефективно для:** тімам, які отримують повідомлення про новий SOTA LLM і потребують структурованого 1-денного циклу: інтегрувати чи відкласти.

## Applies If (ALL must hold)

- A major lab released a new SOTA model in the last 7 days.
- The team has an existing model-gateway adapter pattern.
- The team has a non-trivial eval set (>=50 cases tied to product flows).
- There is an incumbent model in production to benchmark against.

## Skip If (ANY kills it)

- Release is a minor point version — schedule a normal model-upgrade check instead.
- Team has no eval set — fix that first; SOTA onboarding without evals is theatre.
- Model is private-preview or has no production-grade API SLA.
- Team is in the middle of an active incident or migration — defer.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Working gateway-adapter pattern | code | llm-integration |
| Stratified eval set | JSONL | eval-set-stratified-sampling-recipe |
| Benchmark harness | code | rag-bench-harness-template |
| Feature flag for percent rollout | infra | ops |
| Cost-quality budget per task | doc | cost-quality-pareto-template |

## Assumes Loaded

| Methodology | Why |
|---|---|
| `geek/ai/llm-integration/gateway-adapter-template` | Adapter wired in stage 2. |
| `geek/ai/llm-integration/model-migration-checklist` | Safety frame around the swap. |
| `geek/ai/llm-integration/eval-set-stratified-sampling-recipe` | Source of the eval set. |
| `geek/ai/llm-integration/cost-quality-pareto-template` | Cost-quality decision frame. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules | ~900 |
| `content/02-output-contract.xml` | essential | JSON schema + valid/invalid examples | ~700 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns with symptom/root-cause/fix | ~700 |
| `content/06-decision-tree.xml` | essential | Decision tree with rule-id refs | ~500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| Read model spec + breaking changes | sonnet | Quality matters. |
| Wire gateway adapter | haiku | Standard pattern. |
| Run benchmark + cost-quality readout | haiku | Mechanical eval. |
| Write decision record | sonnet | Trade-off framing. |

## Templates

| File | Purpose |
|------|---------|
| `templates/onboarding-schedule.md` | 8-hour wall-clock schedule template. |
| `templates/decision-record.md` | 1-page decision record skeleton. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-sota-onboarding-1day-runbook.py` | Validates output against the 02-output-contract schema. | Pre-commit; CI. |

## Related

- [[model-migration-checklist]]
- [[model-upgrade-checklist]]
- [[cost-quality-pareto-template]]
- [[eval-set-stratified-sampling-recipe]]

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` decides whether to run the 1-day onboarding now, defer, or skip. Each leaf references a rule id from `01-core-rules.xml`.
