---
slug: ai-call-site-inventory
tier: pro
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: Prompt-engineering pattern for ai call site inventory — reusable prompt skeleton, parameter slots, and validation pass keyed to a concrete deliverable.
content_id: "b362f1afb143537c"
tags: [ai, prompt]
---
# AI Call Site Inventory

## Summary

**One-sentence:** Prompt-engineering pattern for ai call site inventory — reusable prompt skeleton, parameter slots, and validation pass keyed to a concrete deliverable.

**One-paragraph:** Prompt-engineering pattern for ai call site inventory — reusable prompt skeleton, parameter slots, and validation pass keyed to a concrete deliverable. Concrete technique for cataloguing every place in a codebase that calls an LLM (model name, prompt version, schema version, fallback chain). Prerequisite for any migration or audit.

## Applies If (ALL must hold)

- You build, refine, or hand off an LLM workflow that uses the prompt pattern described by ai call site inventory.
- The pattern's output is structurally validated (schema, regex, or downstream system).
- Cost and latency budget per call are known before authoring.
- Versioning rule for the prompt is in place (Git, registry, or prompt-eval harness).

## Skip If (ANY kills it)

- One-off prompts used once and discarded — versioning overhead exceeds value.
- Prompts whose output is consumed by humans only, with no downstream parser.
- Provider-specific quirks change weekly — fold pattern into a registry, not in this methodology.

## Prerequisites

- Target model and provider chosen; pricing visible.
- Eval harness or smoke test script that can run the prompt in CI.
- Versioning convention (Git, registry, or sidecar metadata).

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
| `prompt_compile` | haiku | Slot-fill from inputs |
| `eval_run` | sonnet | Run the prompt against ground-truth set |
| `pattern_refactor` | opus | Identify drift and rewrite skeleton |

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
