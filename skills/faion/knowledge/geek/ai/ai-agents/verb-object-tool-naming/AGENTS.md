---
slug: verb-object-tool-naming
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Name every agent tool as verb_object (create_issue, search_files) and prefix with a service namespace (github_create_issue, asana_search_tasks) when the catalog spans multiple servers or MCP gateways.
content_id: "334355994e23ec4d"
tags: [tool-design, naming, tool-selection, mcp-gateways]
---
# Verb-Object Tool Naming with Namespace Prefix

## Summary

**One-sentence:** Name every agent tool as verb_object (create_issue, search_files) and prefix with a service namespace (github_create_issue, asana_search_tasks) when the catalog spans multiple servers or MCP gateways.

**One-paragraph:** Name every agent tool as verb_object (create_issue, search_files) and prefix with a service namespace (github_create_issue, asana_search_tasks) when the catalog spans multiple servers or MCP gateways. Tool names matter MORE than descriptions for selection accuracy — the model parses the name first and uses the description only to disambiguate close matches. Single-token, opaque names (search, manage, do_thing) are the most common reason an agent picks the wrong tool.

## Applies If (ALL must hold)

- Any tool catalog with five or more tools.
- Anytime tools come from multiple MCP servers or pass through an MCP gateway/aggregator.
- When wrapping third-party SDKs that already use verb_object (GitHub, Stripe, Asana, Jira) — keep the verb, add the namespace.
- During tool-eval iteration: rename, re-run eval, keep the better name.

## Skip If (ANY kills it)

- Single-tool hobby scripts where there is only ever one search and no aggregator — naming is not the bottleneck.
- Inside an SDK that already enforces a non-snake_case convention (e.g., GraphQL camelCase) — match the host convention instead of fighting it.
- Do not pad with marketing nouns (acme_corp_internal_v2_search_documents_advanced) — long names hurt context budget and selection alike.

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
