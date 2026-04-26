# REST API Design

## Summary

Design REST APIs around resources (nouns, plural, lowercase, hyphenated), map CRUD to HTTP methods (GET/POST/PUT/PATCH/DELETE), and return the correct status code for each outcome. Use query parameters for filtering and sorting; nest sub-resources for ownership relationships.

## Why

Consistent resource URLs and method semantics let clients predict behavior without reading docs. Correct status codes enable transparent caching (GET 304), safe retries (idempotent PUT/DELETE), and automated monitoring. Violating REST conventions (verbs in URLs, wrong status codes) forces per-API client workarounds.

## When To Use

- Designing any new HTTP API
- Reviewing an existing API for consistency before publishing
- Generating an OpenAPI spec from scratch
- Deciding how to model a new resource or relationship

## When NOT To Use

- Real-time bidirectional communication — use WebSockets or SSE instead
- Bulk or batch operations with complex transactions — consider GraphQL or RPC
- Internal service-to-service calls where gRPC is already the standard
- File upload/download heavy APIs where multipart or streaming is dominant

## Content

| File | What's inside |
|------|---------------|
| `content/01-resource-design.xml` | URL structure rules, HTTP method semantics table, naming conventions |
| `content/02-status-codes.xml` | Status code reference with correct use cases; HATEOAS links pattern |

## Templates

none
