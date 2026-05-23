# MCP Development Prompts — Server, Debug, Architecture, Testing

## Summary

**One-sentence:** Produces a curated library of versioned LLM prompts for the full MCP development lifecycle — creating servers, debugging, architecture review, security audit, performance, test generation, documentation.

**One-paragraph:** Produces a curated library of versioned LLM prompts covering the full MCP development lifecycle: creating servers, adding tools, designing resources, debugging connection and execution failures, validating JSON-RPC messages, designing multi-server architectures, security review, performance optimization, test generation, and documentation. Each prompt carries: id, version, purpose, expected input shape, expected output shape, model recommendation, and known failure modes.

**Ефективно для:** Розробник MCP servers — fixed library з ID-prompted шаблонами, не імпровізує stand-up promo щоразу.

## Applies If (ALL must hold)

- Building or maintaining one or more MCP servers.
- Want a shared, versioned prompt library across the team.
- Need reproducible LLM-assisted prompts for review / debug / test-gen.
- Have an LLM stack to run prompts (Anthropic / OpenAI / Gemini).
- Doc / playbook discipline already in place (markdown commits).

## Skip If (ANY kills it)

- One-off prototype — copy-paste prompts is faster than maintaining a library.
- No MCP server work — out of scope.
- Team rejects shared prompt discipline — defer until accepted.
- Prompts already maintained elsewhere — adopt theirs, don't duplicate.

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Prompt catalogue (titles + intents) | markdown | ML lead |
| Versioning policy | yaml | doc-ops |
| LLM provider | string | decision record |
| Storage path | directory | repo convention |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/ml-engineer/mcp-architecture` | Source of architectural prompts. |
| `geek/ai/ml-engineer/mcp-security` | Source of security-audit prompts. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules each with rationale + source. | ~900 |
| `content/02-output-contract.xml` | essential | JSON Schema + valid/invalid examples + self-check. | ~800 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix. | ~800 |
| `content/06-decision-tree.xml` | essential | Branch by prompt purpose + model recommendation. | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-prompt` | haiku | Fill prompt template from intent + I/O shape. |
| `review-prompt-quality` | sonnet | Spot ambiguity / leaking context / over-prompt. |
| `audit-prompt-library` | opus | Periodic library audit; surface drift + duplication. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prompt-server-create.txt` | Prompt: generate an MCP server skeleton from a spec. |
| `templates/prompt-debug-connection.txt` | Prompt: diagnose MCP connection failure from logs. |
| `templates/prompt-security-audit.txt` | Prompt: security review of an MCP server. |
| `templates/prompt-test-gen.txt` | Prompt: generate pytest cases for an MCP server. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-mcp-dev-prompts.py` | Validate the prompt library (id, version, I/O shape, model recommendation). | Pre-merge of every prompt-library PR. |

## Related

- [[mcp-architecture]] — source of architectural prompts.
- [[mcp-security]] — source of security prompts.
- [[mcp-client-integration]] — bridge debug prompts.

## Decision tree

Decision tree at `content/06-decision-tree.xml` picks model (haiku / sonnet / opus) per prompt purpose and surfaces the canonical prompt slug.
