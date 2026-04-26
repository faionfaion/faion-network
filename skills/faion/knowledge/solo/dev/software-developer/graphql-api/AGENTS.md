# GraphQL API

## Summary

A methodology for building GraphQL APIs: schema-first SDL development with codegen, per-request DataLoader for every 1:N relation, depth limit (5-8) and query complexity cap before resolvers run, cursor-based (Relay) pagination for any list, and `graphql-inspector diff` in CI to block breaking schema changes. Mutations return the modified entity, never `Boolean`. Authorization checks live per-resolver, not just at the gateway.

## Why

Without DataLoader, nested resolvers fire one DB query per parent object (N+1). Without depth and complexity limits, a single deeply nested query can DoS the server. Schema-first codegen ensures resolvers and clients share a single type definition. `graphql-inspector` catches breaking changes before they reach external consumers who cannot roll back. Returning entities from mutations enables optimistic UI updates; returning `Boolean` makes rollback impossible.

## When To Use

- Mobile + web clients with divergent data shapes against the same backend
- Aggregating 3+ microservices into one client-facing API (federation/stitching)
- Internal tooling where consumers need fast schema iteration without REST versioning
- Real-time UIs needing subscriptions over WebSocket / SSE
- Backend-for-frontend (BFF) layers where type-safe client codegen is needed

## When NOT To Use

- File-upload-heavy APIs — use multipart REST or presigned URLs instead
- Public APIs where CDN URL-level caching is critical — REST wins
- Simple CRUD with one consumer — REST ships faster
- Teams without query-cost / depth limiting infrastructure — DoS risk is real

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-and-resolvers.xml` | SDL rules, DataLoader scoping rule, pagination rule, mutation return rule |
| `content/02-security-and-antipatterns.xml` | Depth/complexity limits, persisted queries, auth-per-resolver, N+1 detection |

## Templates

| File | Purpose |
|------|---------|
| `templates/codegen.yml` | graphql-codegen config generating TS types + typed document nodes |
| `templates/dataloader-pattern.ts` | Per-request DataLoader instantiation inside GraphQL context |
