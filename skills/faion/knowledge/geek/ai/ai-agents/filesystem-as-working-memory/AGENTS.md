---
slug: filesystem-as-working-memory
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Give every long-running agent a write_file / read_file / ls tool surface backed by real disk, S3, or a state-dict virtual FS.
content_id: "37d1864802c8d5c0"
tags: [agent-architecture, working-memory, context-management, long-running-agents, state-persistence]
---
# Filesystem as Working Memory — Offload Before Summarize

## Summary

**One-sentence:** Give every long-running agent a write_file / read_file / ls tool surface backed by real disk, S3, or a state-dict virtual FS.

**One-paragraph:** Give every long-running agent a write_file / read_file / ls tool surface backed by real disk, S3, or a state-dict virtual FS. Whenever a tool produces a large blob (search dump, full document, raw API response), write it to the FS and pass back only a filename plus a short snippet. Reserve LLM-based context summarization for the moment context hits ~85% AND there is nothing left to offload — file offload preserves information losslessly, summarization does not.

## Applies If (ALL must hold)

- Research agents reading more than 5 documents per task.
- Codegen across many files (Claude Code, Aider, OpenHands, Cursor agents).
- Any task expected to run more than ~20 turns.
- Pipelines where step N's output is consumed by step N+1 — paths flow, not blobs.
- Agents that must survive process restart (FS persists, conversation does not).

## Skip If (ANY kills it)

- Short chat sessions under ~10 turns — the FS abstraction adds ceremony with no payoff.
- Single-document QA — the document already fits in context once.
- Hard real-time loops where every disk write adds unacceptable latency.
- Untrusted code execution where a writable FS is itself a security problem.

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
