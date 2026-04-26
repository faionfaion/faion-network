# GraphQL API Design

## Summary

Schema-first GraphQL design where the SDL is the source of truth, codegen drives client and server types, and every mutation returns a typed `<MutationName>Payload` with a `userErrors` array. Core rule: every list-returning resolver must use a DataLoader instantiated per-request; every field with sensitive data must have explicit field-level authorization.

## Why

Schema-first with codegen eliminates type drift between client and server. DataLoader prevents N+1 query explosions — the canonical GraphQL performance failure. Typed mutation payloads surface business errors structurally rather than as exceptions, enabling partial-success handling that REST cannot express. Query depth and cost limits prevent DoS from malicious nested queries.

## When To Use

- Multiple clients (web + iOS + Android + partner) with divergent field needs over the same domain
- Highly relational data where REST would force N+1 round-trips or sprawling `?expand=` params
- Schema-first development where the contract is the source of truth and codegen drives types
- Subscriptions for live dashboards, chat, or collaborative editing
- Federated services (Apollo Federation, GraphQL Hive) with one supergraph over many teams

## When NOT To Use

- Public cache-heavy CDN-fronted APIs — REST + HTTP cache headers wins
- File upload or streaming binary payloads — multipart REST or signed URLs are simpler
- Tiny CRUD app with a single client — schema overhead and N+1 traps are not worth it
- Latency-sensitive RPC inside a cluster — gRPC is faster and stricter

## Content

| File | What's inside |
|------|---------------|
| `content/01-schema-design.xml` | Scalars, enums, interfaces, Node/Timestamped, Relay Connection, input types, mutation payloads |
| `content/02-resolvers.xml` | Python/Strawberry resolver implementation, DataLoader per-request, context pattern |
| `content/03-auth-limits.xml` | Permission classes, field-level auth, query depth limiter, complexity extension, pagination caps |
| `content/04-antipatterns.xml` | Over-fetching resolvers, missing pagination, N+1 without DataLoader, forgotten auth on new fields |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | Full reference schema: scalars, interfaces, Connection types, Query/Mutation/Subscription roots |
| `templates/dataloader.py` | Strawberry DataLoader batch_load_fn with key-to-result mapping |
