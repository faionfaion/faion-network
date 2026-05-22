---
slug: mcp-security
tier: geek
group: ai
domain: ml-engineering
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: MCP tools represent arbitrary code execution.
content_id: "f482e2ebcfbcdf7a"
tags: [mcp, security, prompt-injection, authorization, consent]
---
# MCP Security — Consent, Injection Defenses, and Access Controls

## Summary

**One-sentence:** MCP tools represent arbitrary code execution.

**One-paragraph:** MCP tools represent arbitrary code execution. The four security principles are: explicit user consent for all data access and tool invocations, data privacy via appropriate access controls, tool safety via input sanitization and validation, and controlled LLM sampling that requires host approval. Known attack vectors as of April 2025: prompt injection via tool responses, tool permission escalation, and lookalike tool replacement.

## Applies If (ALL must hold)

- Before deploying any MCP server that has write access (file writes, DB mutations, API POSTs).
- When building a host application that must enforce security policies across multiple MCP servers.
- When a server must be accessible over HTTP (requires auth, unlike stdio).
- Security review of an existing MCP server before production promotion.

## Skip If (ANY kills it)

- Read-only MCP servers with no external state — standard input validation still applies but full consent flows may be excessive.

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

- parent skill: `geek/ai/ml-engineer/`
