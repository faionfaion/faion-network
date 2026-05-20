---
slug: agent-rollback-button-design
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Evaluation method for agent rollback button design that defines test set, scoring function, pass/fail thresholds, and regression rules so quality is comparable across runs.
content_id: "f75f907a32ec5c60"
tags: [agent, ai, eval]
---
# Agent Rollback Button Design

## Summary

**One-sentence:** Evaluation method for agent rollback button design that defines test set, scoring function, pass/fail thresholds, and regression rules so quality is comparable across runs.

**One-paragraph:** Evaluation method for agent rollback button design that defines test set, scoring function, pass/fail thresholds, and regression rules so quality is comparable across runs. Rolling back an agent is harder than rolling back a microservice: prompts, schemas, eval set, tools, model version are coupled. Needs a pattern for atomic rollback that preserves customer state.

## Applies If (ALL must hold)

- You are stabilizing or comparing the AI feature behavior described by agent rollback button design across model, prompt, or retrieval versions.
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
| `geek/ai/ai-agents/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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

- parent skill: `geek/ai/ai-agents/`
- peer methodologies: see siblings under `geek/ai/ai-agents/`
- external: industry references cited inline in `content/01-core-rules.xml`
