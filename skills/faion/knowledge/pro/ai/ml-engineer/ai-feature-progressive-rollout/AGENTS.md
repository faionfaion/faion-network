---
slug: ai-feature-progressive-rollout
tier: pro
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Evaluation method for ai feature progressive rollout that defines test set, scoring function, pass/fail thresholds, and regression rules so quality is comparable across runs.
content_id: "f280df396319c135"
tags: [ai, eval]
---
# AI Feature Progressive Rollout

## Summary

**One-sentence:** Evaluation method for ai feature progressive rollout that defines test set, scoring function, pass/fail thresholds, and regression rules so quality is comparable across runs.

**One-paragraph:** Evaluation method for ai feature progressive rollout that defines test set, scoring function, pass/fail thresholds, and regression rules so quality is comparable across runs. 1%→10%→50%→100% rollout with quality-regression auto-rollback — AI-specific because the rollback signal is not a 5xx rate but an eval-score delta. No coverage today.

## Applies If (ALL must hold)

- You are stabilizing or comparing the AI feature behavior described by ai feature progressive rollout across model, prompt, or retrieval versions.
- A ground-truth set ≥30 examples exists OR can be assembled in one work-cycle.
- Eval results gate at least one production decision (deploy, rollback, freeze).
- Cost ceiling per eval run is defined before the first run.

## Skip If (ANY kills it)

- Pre-MVP exploration where output quality is judged by founders eyeballing.
- Features so niche that authoring a ground-truth set takes longer than 3 sprints.
- Cost-prohibitive evals when cheaper proxies (regression of intermediate metric) cover risk.

## Prerequisites

- Ground-truth set with ≥30 examples and a versioned identifier.
- Run-isolation: same eval can be replayed on different model / prompt versions.
- Cost dashboard or per-run budget enforced.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/ai/ml-engineer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `eval_runner_orchestration` | haiku | Test harness driver |
| `judge_scoring` | sonnet | LLM-as-judge per rubric |
| `regression_diagnosis` | opus | Cross-version drift analysis |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `pro/ai/ml-engineer/`
- peer methodologies: see siblings under `pro/ai/ml-engineer/`
- external: industry references cited inline in `content/01-core-rules.xml`
