# Agent Integration — GraphQL API Patterns

## When to use
- Frontends that compose data from many backend resources per screen and want one round-trip.
- Multiple consumer types (web, mobile, partner API) with very different field needs from the same domain.
- Federated organizations: independent teams each owning a subgraph, stitched at gateway.
- Real-time UI: subscriptions over WebSocket/SSE for live updates (orders, notifications, presence).
- BFF (Backend-for-Frontend) layer where REST microservices stay simple and GraphQL composes.

## When NOT to use
- File uploads / streaming responses — GraphQL upload is awkward; use multipart REST or signed URLs.
- Public APIs valuing extreme simplicity, REST + OpenAPI is more discoverable for third parties.
- Single-app, single-consumer CRUD — REST/JSON or tRPC is lighter.
- Caching-heavy read paths benefiting from HTTP cache + CDN — GraphQL POSTs miss CDN by default (persisted queries help, but add complexity).
- Hard real-time latency budgets — every query parses + plans, adding µs to ms over REST.

## Where it fails / limitations
- N+1 query explosion — the canonical pitfall; without DataLoader, a list of 100 users × `orders` resolver = 101 DB calls.
- Complexity / depth attacks — a malicious nested query crashes the server; needs depth + cost limits.
- Caching is hard — no built-in HTTP cache semantics; clients (Apollo, Relay, urql) implement their own normalized caches.
- Authorization is granular and easy to mess up — agents add new fields without auth checks at the field-resolver level.
- Schema evolution: removing a field breaks unknown clients; needs `@deprecated` workflow + usage analytics.
- Federation footguns: two subgraphs claiming the same `@key` field, or entity resolution loops.
- Subscription scaling: stateful WebSocket connections need sticky sessions or Redis pub/sub fan-out.
- Error model confusion: partial-success responses (`data` + `errors`) trip up clients expecting REST-style status codes.

## Agentic workflow
Drive GraphQL work in a schema-first loop: (1) author the SDL (`.graphql` files) as the source of truth, (2) generate types/clients with codegen (`graphql-codegen`, `gqlgen`, `async-graphql` derive macros), (3) implement resolvers wrapping DataLoader for any 1:N relationship, (4) verify with the introspection schema diff against last published version, (5) run query-cost + depth tests. Never let an agent write resolvers before SDL is reviewed — the schema is the API contract.

### Recommended subagents
- `graphql-schema-architect` (Sonnet) — designs SDL, naming, pagination shape, error union types from a domain spec.
- `graphql-resolver-implementer` (Sonnet) — writes resolvers + DataLoaders; required to pair every list field with a loader.
- `graphql-security-reviewer` (Sonnet) — checks field-level auth, depth limit, query cost limit, persisted-query allowlist.
- `graphql-codegen-runner` (Haiku) — runs codegen on PR, fails CI if generated files drift.
- `graphql-schema-diff-reviewer` (Haiku) — runs `graphql-inspector diff` to flag breaking changes.

### Prompt pattern
```
Schema task: add a `posts(first: Int, after: String, filter: PostFilter)` field on User.
Constraints:
- Relay-style cursor pagination (UserPostsConnection, UserPostsEdge, PageInfo).
- Filter input: status (PostStatus enum), tag (String).
- Implement with DataLoader keyed by (userId, filterHash).
- Add field-level @auth(requires: USER) directive.
- Update graphql-codegen typescript-resolvers config.
Done = schema validates, codegen runs, no field added without resolver, query cost ≤ 100 for default page size.
```

```
Audit: scan resolvers/ for N+1 risk.
For each resolver returning [Type] or Type within a list parent:
- Confirm a DataLoader (or batched repository) is used.
- If not, propose patch wiring the loader.
Output: list of risk sites + diff per fix.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `graphql-codegen` | TS types + clients from schema | `npm i -D @graphql-codegen/cli` · https://the-guild.dev/graphql/codegen |
| `graphql-inspector` | Schema diff + linting | `npm i -D @graphql-inspector/cli` |
| `gqlgen` (Go) | Schema-first Go server codegen | https://gqlgen.com |
| `async-graphql` (Rust) | Code-first Rust server lib | https://async-graphql.github.io |
| `strawberry` / `ariadne` (Python) | Python GraphQL servers | https://strawberry.rocks · https://ariadnegraphql.org |
| `graphql-armor` | Cost/depth/intro guards | `npm i @escape.tech/graphql-armor` |
| `relay-compiler` | Required for Relay clients | `npm i -D relay-compiler` |
| `apollo` CLI / Apollo Studio CLI (`rover`) | Schema publish/check, federation | https://www.apollographql.com/docs/rover/ |
| `mercurius` (Fastify) | High-perf JS server | https://mercurius.dev |
| `pothos` | Code-first TS schema builder | https://pothos-graphql.dev |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apollo GraphOS / Studio | SaaS | Yes via `rover` | Schema registry, usage analytics, breaking-change checks in CI |
| Hasura | OSS / SaaS | Yes via metadata API | Auto-generates GraphQL over Postgres; agents drive via metadata YAML |
| WunderGraph | OSS / SaaS | Yes | Federation + persisted queries |
| The Guild Hive | SaaS / OSS | Yes via CLI | Open alternative to GraphOS |
| GraphQL Yoga | OSS | Yes | Server library with sane defaults (CSRF, helmet, plugins) |
| Mesh (The Guild) | OSS | Yes | Stitches REST/SOAP/gRPC into GraphQL |
| Apollo Server / Apollo Router | OSS | Yes | Federation gateway |
| Postgraphile | OSS | Yes | Postgres → GraphQL auto-API |
| Stellate | SaaS | Yes | GraphQL CDN edge cache (persisted queries required) |

## Templates & scripts
See `templates.md`. Useful one-liner DataLoader factory pattern (Node/TS):

```ts
// loaders/index.ts
import DataLoader from 'dataloader';
import { db } from '../db';

export const createLoaders = () => ({
  userById: new DataLoader<string, User | null>(async (ids) => {
    const rows = await db.users.findMany({ where: { id: { in: [...ids] } } });
    const map = new Map(rows.map(u => [u.id, u]));
    return ids.map(id => map.get(id) ?? null);
  }),
  ordersByUserId: new DataLoader<string, Order[]>(async (ids) => {
    const rows = await db.orders.findMany({ where: { userId: { in: [...ids] } } });
    const grouped = new Map<string, Order[]>();
    for (const r of rows) {
      const arr = grouped.get(r.userId) ?? [];
      arr.push(r); grouped.set(r.userId, arr);
    }
    return ids.map(id => grouped.get(id) ?? []);
  }),
});
// Per-request in context: ctx.loaders = createLoaders();
```

## Best practices
- Treat the SDL as the source of truth; commit `schema.graphql` and run codegen in CI.
- Pair every resolver returning a list of related entities with a DataLoader instantiated per-request (never global).
- Use Relay cursor connections for any list field that could grow; never offset+limit on the public API.
- Use input types for all mutations (`CreateUserInput`) — never positional args.
- Field-level authorization at the resolver, not the gateway. Composition allows arbitrary client shapes; auth must be per-field.
- Add depth (≤ 10), cost (e.g., 1000 points), and rate limits in production. Use `graphql-armor` or equivalent.
- Use persisted queries (allowlist) for production clients — eliminates injection risk and enables CDN caching.
- Mark deprecated fields with `@deprecated(reason: "...")`; remove only after usage drops to 0 in analytics.
- Prefer error union types (`type CreateUserResult = User | UserAlreadyExists | ValidationError`) over `errors[]` for expected business errors.
- Use a context-per-request pattern; never share resolver state.

## AI-agent gotchas
- Agents introduce N+1 by adding a relation field with a naive resolver that calls the DB per parent — require DataLoader or column-aware batched repos.
- Forgotten field-level auth: agents add `User.email` without `@auth` directive or check; auth audits should be automated.
- Agents propose breaking schema changes (rename, remove field, change non-null → nullable) without a deprecation cycle. Run `graphql-inspector diff` in CI.
- Mixing code-first and schema-first patterns in one repo confuses tooling — pick one per service.
- Subscription leaks: agents wire `pubsub` listeners without cleanup on disconnect; review every subscription resolver for teardown.
- Resolver-level transactions: agents wrap a single resolver in a DB tx that doesn't include sibling resolver calls running in parallel. Use UoW pattern at request level if you need atomic groups.
- Generated types committed by hand: agents edit codegen output; require it to be `.gitignore`d or regenerated in CI to detect drift.
- Human-in-loop checkpoint: any schema change touching public types or removing a field needs human review + Apollo Studio (or Hive) check passing.

## References
- https://spec.graphql.org
- https://graphql.org/learn/best-practices/
- https://relay.dev/graphql/connections.htm (cursor pagination)
- https://github.com/graphql/dataloader
- https://www.apollographql.com/docs/federation/
- https://escape.tech/graphql-armor/
- https://principledgraphql.com
- https://graphql-rules.com
- https://www.apollographql.com/docs/technotes/TN0021-graph-versioning/
