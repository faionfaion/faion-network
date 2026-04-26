# GraphQL Patterns

## Summary

GraphQL lets clients fetch nested, multi-resource data in a single request against a typed schema. The schema (SDL) is the contract; code is derived from it. Every relation field must use DataLoader to prevent N+1 queries. Public endpoints must enforce depth and complexity limits.

## Why

Without DataLoader, every nested field triggers a separate DB query — one list of 100 orders fires 100 user lookups in production. Depth/complexity limits prevent DoS via deeply nested or astronomically large queries. Schema-first development (SDL reviewed before code) gives backend and frontend teams a stable contract to work against concurrently.

## When To Use

- Clients need to fetch nested data (user → orders → items) in one round-trip
- Multiple consumers (web, mobile, partner) want different shapes off the same backend
- Typed SDL contract needed for codegen (Apollo, urql, Relay, graphql-codegen)
- Real-time fan-out via subscriptions alongside the same query/mutation graph
- Federating multiple services into one supergraph

## When NOT To Use

- Simple CRUD on a single resource — REST is shorter, cacheable, and well-tooled
- File upload heavy / streaming binary — multipart REST or gRPC stream is better
- Public, CDN-cached read APIs — GET + URL semantics outperform POST `/graphql`
- Hard p99 latency budgets where resolver fan-out is unpredictable
- Small team without bandwidth to operate persisted queries, depth limits, complexity scoring

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-patterns.xml` | SDL structure, Query/Mutation/Subscription, cursor pagination (Relay), federation `@key` |
| `content/02-operations.xml` | DataLoader N+1 prevention, error envelope format, persisted queries |

## Templates

| File | Purpose |
|------|---------|
| `templates/dataloader.ts` | TypeScript DataLoader pattern: batch load + key ordering |

## Scripts

none
