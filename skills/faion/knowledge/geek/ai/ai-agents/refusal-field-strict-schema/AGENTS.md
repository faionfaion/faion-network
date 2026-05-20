---
slug: refusal-field-strict-schema
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Add an explicit nullable refusal: str | None field at the TOP of every strict-mode SO schema in safety-sensitive domains.
content_id: "3eff4f127bf9643d"
tags: [structured-output, safety, strict-mode, extraction, openai]
---
# Refusal Field for Safety-Aware Strict Extraction

## Summary

**One-sentence:** Add an explicit nullable refusal: str | None field at the TOP of every strict-mode SO schema in safety-sensitive domains.

**One-paragraph:** Add an explicit nullable refusal: str | None field at the TOP of every strict-mode SO schema in safety-sensitive domains. When the model declines to answer, it writes the explanation into refusal and leaves payload fields null — instead of corrupting the JSON with a free-form refusal that breaks parsing. OpenAI's strict-mode response already exposes a top-level refusal; mirroring that field inside your own schema unifies the contract across providers and lets a single downstream branch handle "I cannot answer" without try/except.

## Applies If (ALL must hold)

- PII / medical / legal / financial extraction with strict mode.
- Content moderation outputs where "this content is abusive, refusing to score" must not throw.
- Any pipeline that bills only on success and needs to log refusals separately from errors.
- Multi-provider deployments where refusal handling must be uniform across OpenAI/Anthropic/local.
- Long batch jobs where one item refusing must not abort the batch.

## Skip If (ANY kills it)

- Trivial transformations (uppercase, regex extract) where refusal is not in the model's repertoire.
- Pipelines where any refusal is upstream policy violation and should hard-fail anyway.
- When the only consumer is a human reviewer who already reads free-form responses.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `geek/ai/ai-agents/`
