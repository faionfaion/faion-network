---
slug: model-onboarding-checklist
tier: geek
group: ai
domain: ml-engineering
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Step-by-step checklist from new SOTA model announced to gated in production — pulls the right slices of gateway, router, eval methodologies into one sheet.
content_id: "da591b695172f1af"
complexity: deep
produces: checklist
est_tokens: 4200
tags: [llm, model-onboarding, gateway, router, eval, production-gating]
---
# Model Onboarding Checklist

## Summary

**One-sentence:** Step-by-step checklist from new SOTA model announced to gated in production — pulls the right slices of gateway, router, eval methodologies into one sheet.

**One-paragraph:** When a new model lands (Claude 4.7, GPT-5, Gemini 3, open-source) LLM-agent teams scramble through 6+ scattered methodologies. This artefact unifies them into one 12-step onboarding checklist with phase gates, named approvers and rollback criteria. Output is a per-model onboarding record (Notion/repo/Jira epic) with completion status, evaluation diffs vs incumbent, and named approver for production exposure.

**Ефективно для:** ML engineer that just got an alert «нова SOTA — спробуй» і потребує дисциплінованого 12-кроку замість «vibes-промоції» в продакшн.

## Applies If (ALL must hold)

- team operates an LLM-agent system with ≥1 model in production
- team owns a model gateway / router OR direct provider integration
- team has an eval suite (golden set, hallucination tests)
- ≥1 production model is on a SaaS provider with a release cadence
- engineering team can pause or roll back model routing

## Skip If (ANY kills it)

- single-model deployment with no router — onboarding is a simple swap
- experimental sandbox with no production exposure
- regulated environment where model changes require external certification
- team uses a fully-managed provider that auto-onboards models

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=checklist + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 4-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=checklist`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-model-onboarding-checklist.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/onboarding-checklist.md` | 12-step master checklist filled per model |
| `templates/phase-gate-memo.md` | Per-phase go/no-go decision memo template |
| `templates/cost-comparison.md` | Per-task cost + accuracy delta vs incumbent |
| `templates/rollback-plan.md` | Per-model rollback procedure with named approver |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-model-onboarding-checklist.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-named-trigger`, `r2-four-phases`, `r3-eval-before-route`, `r4-cost-compare`, `r5-named-approver` from `content/01-core-rules.xml`.
