---
slug: mcp-resource-vs-tool-vs-prompt
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Model Context Protocol (MCP) servers expose three types of capabilities: Tools (actions the model invokes), Resources (content the model reads), and Prompts (templates the user invokes as slash commands).
content_id: "a45933c854249515"
tags: [mcp, model-context-protocol, server-design, architecture]
---
# MCP — Resource vs Tool vs Prompt: The Three-Question Test

## Summary

**One-sentence:** Model Context Protocol (MCP) servers expose three types of capabilities: Tools (actions the model invokes), Resources (content the model reads), and Prompts (templates the user invokes as slash commands).

**One-paragraph:** Model Context Protocol (MCP) servers expose three types of capabilities: Tools (actions the model invokes), Resources (content the model reads), and Prompts (templates the user invokes as slash commands). The most common MCP design mistake is misclassification — exposing a Resource as a Tool, or a Tool as a Prompt. Use the three-question test to classify every capability correctly, ensuring the model can reason about side effects and the user gets the right interface.

## Applies If (ALL must hold)

- Designing any MCP server, no matter the domain (docs, code, infra, issues).
- Auditing an existing MCP server and finding tools that always return the same content or resources with side effects.
- Deciding whether to expose a capability as a Tool, Resource, or Prompt.
- Building servers that must work across multiple runtimes (Claude Code, OpenAI, Vercel, LangChain).

## Skip If (ANY kills it)

- Using an existing third-party MCP server — this is design guidance for server authors.
- Writing a single-shot script that doesn't expose an MCP interface.

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
