---
slug: agent-invocation
tier: pro
group: research
domain: research
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Reference for invoking faion-researcher agents from orchestrators.
content_id: "d19bf5332a582c57"
tags: [research, agents, orchestration, workflow, subagents]
---
# Agent Invocation Reference

## Summary

**One-sentence:** Reference for invoking faion-researcher agents from orchestrators.

**One-paragraph:** Reference for invoking faion-researcher agents from orchestrators. Covers two agents (faion-research-agent with 9 modes, faion-domain-checker-agent) and a sequential workflow pattern where each mode's output feeds the next. All outputs land in .aidocs/product_docs/.

## Applies If (ALL must hold)

- Orchestrating a multi-stage research run (ideas → market → competitors → pains → personas → validate → niche → pricing → names → domain-check).
- Picking the right mode for a user "research X" request without polluting parent context.
- Naming + domain-check workflows where names mode must chain to faion-domain-checker-agent.
- Ensuring outputs land deterministically in .aidocs/product_docs/<file>.md for downstream consumption by faion-sdd or faion-product-manager.

## Skip If (ANY kills it)

- One-off factual lookup (single TAM number, single competitor URL) — call WebSearch directly; a research subagent costs 10x more tokens.
- Internal codebase research — use Grep/Glob/Agent instead; this agent is tuned for external web sources.
- Purely creative ideation (brand voice, copy variants) — use brainstorm instead of mode: ideas.
- Project already has fresh market-research.md / competitive-analysis.md — re-running burns budget; read existing files first.

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

- parent skill: `pro/research/researcher/`
