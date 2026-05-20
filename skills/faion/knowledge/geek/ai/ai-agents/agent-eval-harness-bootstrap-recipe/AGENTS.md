---
slug: agent-eval-harness-bootstrap-recipe
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Numeric scoring rubric for agent eval harness bootstrap recipe that converts qualitative judgment into a comparable 0-100 (or 1-5 weighted) signal usable across cohorts.
content_id: "6291b267c09f0f30"
tags: [agent, ai, scorecard]
---
# Agent Eval Harness Bootstrap Recipe

## Summary

**One-sentence:** Numeric scoring rubric for agent eval harness bootstrap recipe that converts qualitative judgment into a comparable 0-100 (or 1-5 weighted) signal usable across cohorts.

**One-paragraph:** Numeric scoring rubric for agent eval harness bootstrap recipe that converts qualitative judgment into a comparable 0-100 (or 1-5 weighted) signal usable across cohorts. Atomized methodologies exist (`trajectory-eval-otel`, `llm-judge-rubric-evidence-first`, `record-replay-debugging`, `chaos-eval-fault-injection`, `behavioral-evals-adversarial`, `llm-as-judge-harness`). Missing: the wiring playbook that turns those 6 into a working CI gate in one engineer-week. Right now P7 reinvents the integration for every agent.

## Applies If (ALL must hold)

- You evaluate >1 instance against the same criteria addressed by agent eval harness bootstrap recipe (calls, vendors, candidates).
- Scores will be used for a binary decision (advance, reject, prioritize).
- Each criterion has a defined 1-5 anchor; raters trained on the rubric before scoring.
- ≥2 raters per instance for any score that gates a >$10k or strategic decision.

## Skip If (ANY kills it)

- n < 3 instances — gut feel is faster and accuracy is similar.
- Decisions are single-criterion (price-only, deadline-only) — full rubric is overhead.
- Strategic, single-shot decisions where qualitative narrative beats numeric blend.

## Prerequisites

- Rubric file or sheet with anchors written for each criterion 1-5.
- Rater(s) trained on at least 3 calibration examples before scoring real instances.
- Storage for scores reachable from downstream decision step (CRM, spreadsheet).

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
| `per_criterion_score` | sonnet | Anchored 1-5 judgment per dimension |
| `multi_rater_reconciliation` | opus | Resolve divergent scores with rationale |

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
