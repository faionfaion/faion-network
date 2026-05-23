---
slug: faion-cli-agent-adapter-pattern
tier: pro
group: sdlc-ai
domain: sdlc-ai
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Reference implementation wrapping `faion search` + `faion get-content` as a tool inside Claude Agent SDK, LangChain, and OpenAI Assistants -- with error handling, caching, and version pinning."
content_id: "b1ea2e88ea822a97"
complexity: deep
produces: code
est_tokens: 4200
tags: ["adapter", "agent-sdk", "claude", "langchain", "openai", "sdlc-ai", "pro"]
---
# Faion CLI Agent Adapter Pattern

## Summary

**One-sentence:** Reference implementation wrapping `faion search` + `faion get-content` as a tool inside Claude Agent SDK, LangChain, and OpenAI Assistants -- with error handling, caching, and version pinning.

**One-paragraph:** Reference implementation: how to wrap `faion search` + `faion get-content` as a tool inside Claude Agent SDK / LangGraph / OpenAI Assistants. This methodology ships three adapters (Anthropic tool, LangChain Tool, OpenAI function) plus shared concerns: error handling, response caching, version pinning, citation-contract integration. Output is a working `faion-agent-adapter/` package that an LLM-agent developer can drop into their project and bind to their agent in <30 minutes.

**Ефективно для:**

- паст-готова основа для повторюваної задачі «faion cli agent adapter pattern» — без винаходу велосипеда.
- контракт виходу пинить за схемою — downstream-агент може спожити без re-derive.
- rule-set + decision tree відсіюють варіанти, де методологія НЕ підходить.
- validator-скрипт ловить дрейф артефакту до того, як він потрапить у downstream.
- версіонована, з named-owner — артефакт не стає folklore через 6 місяців.

## Applies If (ALL must hold)

- you are building an AI agent in Claude Agent SDK, LangGraph/LangChain, OpenAI Assistants, or an SDK with equivalent tool semantics.
- you want faion methodology content available to the agent as a tool, not pre-stuffed context.
- you have a Python or TypeScript runtime in your agent stack.

## Skip If (ANY kills it)

- your agent does not support tool-use semantics -- pre-load context instead.
- you are using an SDK with no documented tool API.
- your agent runs only against local non-faion methodology files -- skip.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Triggering context for the Faion CLI Agent Adapter Pattern task | recent notes / tickets / interviews | operator's inbox or system of record |
| Named consumer (human or agent) | name + handle | engagement charter |
| Source-of-truth for inputs | doc / dashboard / repo path | system of record |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `pro/sdlc-ai/methodology-as-json-feed` | supplies the JSON shape the adapter consumes. |
| `pro/sdlc-ai/citation-contract-back-to-source` | supplies the citation format the adapter emits. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5+ testable rules with rationale + skip-this-methodology fallback | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) for the artefact + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure with input / action / output / decision-gate | 800 |
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
| `templates/anthropic-adapter.py` | Claude Agent SDK adapter showing tool definition + handler + caching. |
| `templates/langchain-adapter.py` | LangChain Tool adapter (sync + async) with citation emission. |
| `templates/openai-adapter.py` | OpenAI Assistants function adapter with version pinning. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-faion-cli-agent-adapter-pattern.py` | Validate the code artefact against the 02-output-contract schema | After subagent returns, before downstream consumer reads |

## Related

- [[methodology-as-json-feed]]
- [[citation-contract-back-to-source]]
- [[ai-debt-detection]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input signals (precondition pass, named owner, input reachability, regulatory regime) to a conclusion that references a rule id from `content/01-core-rules.xml`. Use it when in doubt about whether this methodology applies or which variant rule to enforce.
