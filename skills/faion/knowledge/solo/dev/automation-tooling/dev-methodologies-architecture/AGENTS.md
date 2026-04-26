# Dev Methodologies — Architecture

## Summary

A catalogue of backend architecture patterns for database, API, performance, and observability layers: schema migrations (expand-then-contract), N+1 ORM fixes via prefetch, caching strategies (cache-aside, write-through), background job queuing, consistent API response envelopes, auth pattern selection, and structured logging.

## Why

Ad-hoc architecture produces N+1 query explosions, inconsistent API shapes, untraceable errors, and single points of failure. Each pattern here encodes a concrete, testable fix: prefetch proves absence of extra queries in tests; envelope shapes are enforced by a single Pydantic model; structured log fields are a reviewable contract. Apply patterns incrementally — commit and test after each one.

## When To Use

- Drafting backend architecture for a new service (DB schema, ORM patterns, cache, queue, auth, logging).
- Reviewing an existing service for N+1 queries, missing indexes, ad-hoc auth, or unstructured logs.
- Generating migration scripts and verifying backward compatibility for CD pipelines.
- Standardizing API response envelopes across a polyglot codebase.

## When NOT To Use

- Frontend / UI architecture — this set is backend-only.
- Greenfield prototyping where the overhead of patterns exceeds the value (throwaway demos, scripts).
- High-stakes schema design requiring a DBA (sharding, multi-region, ACID vs BASE trade-offs).
- When the hosting platform prescribes patterns (Supabase, Firebase) — defer to platform conventions.

## Content

| File | What's inside |
|------|---------------|
| `content/01-database.xml` | Migration patterns (expand-then-contract), query optimization, ORM N+1 fix, HA setup. |
| `content/02-api-perf.xml` | API response envelope, auth pattern matrix, caching strategy table, background job pattern. |
| `content/03-observability.xml` | Structured logging contract (event, actor, object, latency_ms, correlation_id). |

## Templates

none
