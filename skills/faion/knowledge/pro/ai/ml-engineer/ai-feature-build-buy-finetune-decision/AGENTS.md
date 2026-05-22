---
slug: ai-feature-build-buy-finetune-decision
tier: pro
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: End-to-end playbook for ai feature build buy finetune decision that walks an operator from trigger to closed outcome with named artefacts at each step.
content_id: "a64c924008f5e105"
tags: [ai, playbook]
---
# AI Feature Build Buy Finetune Decision

## Summary

**One-sentence:** End-to-end playbook for ai feature build buy finetune decision that walks an operator from trigger to closed outcome with named artefacts at each step.

**One-paragraph:** End-to-end playbook for ai feature build buy finetune decision that walks an operator from trigger to closed outcome with named artefacts at each step. There is llm-decision-framework but no opinionated playbook scoring build vs buy vs prompt vs RAG vs finetune for a single feature with cost/quality/latency/lock-in axes. Engineers fall into the 'finetune everything' or 'prompt everything' traps.

## Applies If (ALL must hold)

- You are executing the cross-cutting workflow addressed by ai feature build buy finetune decision end to end.
- All inputs the playbook calls for are reachable (people, data, artefacts).
- The output is consumed by a named downstream owner with a deadline.
- Deviations from the steps are logged with a one-line rationale.

## Skip If (ANY kills it)

- Highly contextual one-shot work where playbook constrains the wrong axes.
- Pre-discovery — playbook assumes the problem is named.
- Teams already running a well-tuned variant — re-tooling friction outweighs upside.

## Prerequisites

- Stakeholders, owners, and deadlines named in advance.
- Inputs (data, briefs, accounts) reachable at start.
- Storage location for each step's output decided.

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
| `input_collection` | haiku | Structured gather from inputs |
| `decision_steps` | sonnet | Apply playbook branches against state |
| `synthesis_writeup` | opus | Final artefact authoring |

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
