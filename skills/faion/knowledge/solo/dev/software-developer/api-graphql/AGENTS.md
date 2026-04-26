# GraphQL API Patterns

## Summary

GraphQL allows clients to specify exactly what data they need, reducing over-fetching and under-fetching versus REST. Core rule: every resolver returning a list of related entities must use a DataLoader instantiated per-request — without it, a list of 100 parents generates 101 database queries (N+1).

## Why

Multiple consumer types (web, mobile, partner) have divergent field needs from the same domain. REST forces either over-fetching (large responses) or API proliferation (one endpoint per client type). GraphQL solves this with a single typed schema where clients compose their own queries. DataLoader solves the resulting N+1 problem by batching and deduplicating DB calls within a request.

## When To Use

- Frontends composing data from many backend resources per screen (one round-trip)
- Multiple consumer types (web, iOS, Android, partner API) with different field requirements
- Federated services where independent teams own subgraphs stitched at a gateway
- Real-time features (subscriptions over WebSocket/SSE) for live dashboards, chat, presence
- BFF layer composing REST microservices into one typed graph

## When NOT To Use

- File uploads or streaming binary — multipart REST or signed URLs are simpler
- Public cache-heavy read APIs — REST + HTTP cache headers + CDN is faster and simpler
- Single-app, single-consumer CRUD — schema overhead and N+1 traps are not worth it
- Hard real-time latency budgets — every query parses and plans, adding overhead vs REST

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-patterns.xml` | Schema design: types, enums, interfaces, Relay cursor pagination, input types, mutation payloads |
| `content/02-dataloader.xml` | N+1 prevention with DataLoader: batch load functions, per-request instantiation, grouping patterns |
| `content/03-security.xml` | Depth limiting, query complexity, field-level auth, persisted queries, introspection control |
| `content/04-antipatterns.xml` | Over-fetching resolvers, missing pagination, N+1 without DataLoader, forgotten auth on new fields |

## Templates

| File | Purpose |
|------|---------|
| `templates/dataloader-factory.ts` | TypeScript DataLoader factory with grouping pattern for 1:N relationships |
| `templates/schema.graphql` | Reference schema with Node interface, Connection types, input types, mutation payloads |
