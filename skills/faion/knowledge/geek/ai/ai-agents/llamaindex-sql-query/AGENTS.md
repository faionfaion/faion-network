---
slug: llamaindex-sql-query
tier: geek
group: ai
domain: ai-agents
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: NLSQLTableQueryEngine translates natural language questions into SQL via an LLM, executes against a SQLAlchemy-connected database, and returns the answer with the generated SQL for inspection.
content_id: "074dcd7a49dcf51e"
tags: [llamaindex, nl-to-sql, structured-data, sql, rag]
---
# LlamaIndex NL-to-SQL with NLSQLTableQueryEngine

## Summary

**One-sentence:** NLSQLTableQueryEngine translates natural language questions into SQL via an LLM, executes against a SQLAlchemy-connected database, and returns the answer with the generated SQL for inspection.

**One-paragraph:** NLSQLTableQueryEngine translates natural language questions into SQL via an LLM, executes against a SQLAlchemy-connected database, and returns the answer with the generated SQL for inspection. Restrict include_tables to only relevant tables. Always use a read-only database connection. For large schemas, use ObjectIndex-based table schema retrieval to narrow the LLM's schema context before SQL generation.

## Applies If (ALL must hold)

- Business users need to query a relational database without writing SQL — NLSQLTableQueryEngine is the standard LlamaIndex pattern.
- Agent needs to combine document RAG with structured data queries in one pipeline — route SQL queries to NLSQLTableQueryEngine and document queries to VectorStoreIndex.
- Schema is known upfront and changes infrequently — the LLM needs stable table descriptions for reliable SQL generation.
- Debugging or auditing agent SQL — the engine returns the generated SQL in response.metadata["sql_query"] for logging.

## Skip If (ANY kills it)

- Database schema is large (50+ tables) or changes frequently — dedicated text-to-SQL services (Vanna, SQLAI) handle schema evolution better.
- Write operations are required — NLSQLTableQueryEngine does not prevent destructive SQL; never use with a read-write connection for agent-driven queries.
- Query patterns are known and fixed — parameterized SQL queries are cheaper and safer than LLM-generated SQL for static workloads.
- The database is large and complex/dynamic — dedicated text-to-SQL services handle schema evolution better than a general-purpose LLM.

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
