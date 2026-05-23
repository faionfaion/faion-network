---
slug: citation-contract-back-to-source
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Forced citation format `[faion:<slug>@<version>]` that AI agents emit when they use faion methodology content, with verifier that resolves the slug and rejects fabricated citations."
content_id: "9d8916aed7a9c95c"
complexity: medium
produces: spec
est_tokens: 4900
tags: ["citation", "attribution", "agent-output", "sdlc-ai", "pro"]
---
# Citation Contract Back to Source

## Summary

**One-sentence:** Forced citation format `[faion:<slug>@<version>]` that AI agents emit when they use faion methodology content, with verifier that resolves the slug and rejects fabricated citations.

**One-paragraph:** Strategic value of P7 (LLM-agent developers) to faion: 'what they cite, others cite.' But no methodology defines how an agent should emit `[faion:slug@v]` citations, what fields are required, or how to verify a citation. Without this contract, agents paraphrase faion without attribution and the network effect dies. This methodology ships as a forced output-schema fragment for agent prompts plus a CLI verifier that walks the citation, resolves it against the local content store, and rejects fabrications. Output is a stable citation format + verifier script + integration recipe for Claude Agent SDK, LangChain, and OpenAI Assistants.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «citation contract back to source» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you build an AI agent that consumes faion methodology content as context.
- the agent's outputs are read by humans OR other agents downstream.
- you have write access to the agent's output schema / system prompt.

## Skip If (ANY kills it)

- your agent reads faion content but never produces text outputs for further consumption.
- the agent is a one-off internal tool with no downstream consumers.
- your output schema is owned by an external system that forbids citation fields.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Citation Contract Back to Source task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/methodology-as-json-feed` | supplies the JSON feed the verifier resolves citations against. |
| `pro/sdlc-ai/faion-cli-agent-adapter-pattern` | adapter examples show how to wire the citation contract into Claude / LangChain / OpenAI. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
| `content/05-examples.xml` | essential | One full worked example end-to-end (anonymised) | 700 |
| `content/06-decision-tree.xml` | essential | Root-question → branches → conclusion(ref=rule-id) | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-inputs-summary` | haiku | Mechanical template fill, bounded transformation. |
| `synthesize-decision` | sonnet | Per-instance judgment against the rubric. |
| `review-for-compliance` | opus | Cross-input synthesis when stakes are high. |

## Templates

| File | Purpose |
|------|---------|
| `templates/citation-format.md` | Citation format specification + verifier recipe + 3 adapter snippets. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-citation-contract-back-to-source.py` | Validate the spec artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[methodology-as-json-feed]]
- [[faion-cli-agent-adapter-pattern]]
- [[ai-debt-detection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
