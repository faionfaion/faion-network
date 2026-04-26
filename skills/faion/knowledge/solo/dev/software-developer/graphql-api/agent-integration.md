# Agent Integration — GraphQL API

## When to use
- Mobile + web clients with divergent data shapes against the same backend
- Aggregating 3+ microservices into one client-facing API (federation/stitching)
- Internal tooling where consumers need fast schema iteration without versioned REST
- Real-time UIs needing subscriptions over WebSocket / SSE
- Backend-for-frontend (BFF) layers where you want type-safe client codegen

## When NOT to use
- File upload heavy APIs (use multipart REST or presigned URLs)
- Public APIs where caching by URL is critical (CDN-cache-friendly REST wins)
- Simple CRUD with one consumer — REST is shorter to ship
- Strict bandwidth-constrained environments where query strings inflate payloads
- Teams without query-cost / depth limiting infrastructure (DoS risk)

## Where it fails / limitations
- N+1 by default — without a `DataLoader` per request, nested resolvers explode DB queries; agents commonly forget per-request loader scoping and end up sharing caches across users
- No HTTP-level cache; everything is `POST /graphql` — agents misconfigure CDNs that cache nothing or cache too much
- Authorization is per-field, not per-route; missing checks on a deep resolver leaks data via unrelated query paths
- Schema breaking changes are silent until clients break; need automated `graphql-inspector` diffs in CI
- Persisted queries vs ad-hoc queries: enabling one without the other breaks tooling assumptions
- Subscription back-pressure: under load, Redis-backed pub/sub drops messages without telemetry
- Federation v1 vs v2 syntax differs subtly; agents trained on older docs emit broken `@key` directives

## Agentic workflow
Adopt schema-first development: agent edits `*.graphql` SDL, runs codegen (`graphql-codegen` or server-language equivalent), implements resolvers, then a review subagent runs `graphql-inspector diff` against the production schema and fails on breaking changes without an explicit migration note. Pair with persisted-query enforcement and a query-cost analyzer; the agent must include cost annotations on new fields and the gate rejects unbounded list returns.

### Recommended subagents
- General-purpose subagent — schema authoring, resolver implementation
- `faion-feature-executor` — pipeline: edit SDL → codegen → impl resolvers → write integration tests → run schema diff
- `faion-sdd-execution` — gate that enforces DataLoader presence, depth limit, and cost limit middleware on every server boot
- Code-review subagent — diff-based check for new resolvers without auth + DataLoader

### Prompt pattern
```
Add a `userOrders(first: Int, status: OrderStatus): OrderConnection!` field on User.
1. Edit schema/user.graphql with the connection type + edges.
2. Generate types: `pnpm graphql-codegen`.
3. Implement resolver in src/resolvers/user.ts using a per-request orderByUserLoader.
4. Wire authorization: only owner or admin can list orders.
5. Add Vitest test that asserts N=1 db query for 100 users.
6. Run `graphql-inspector diff origin/main schema.graphql`; output the report.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `graphql-codegen` | Generate TS/Go/Python types from SDL | `npm i -D @graphql-codegen/cli` |
| `graphql-inspector` | Schema diff, breaking change detection | `npm i -g @graphql-inspector/cli` |
| `rover` (Apollo) | Schema registry + federation composition | https://www.apollographql.com/docs/rover |
| `graphqurl` (`gq`) | Curl-equivalent for GraphQL | `npm i -g graphqurl` |
| `Altair` / `Insomnia` | GraphQL client for manual queries | desktop apps |
| `graphql-eslint` | Lint queries + SDL | `npm i -D @graphql-eslint/eslint-plugin` |
| `apollo-cost-analysis` / `graphql-query-complexity` | Query-cost guards | server middleware |
| `genql` | Type-safe TS client from SDL | `npm i genql` |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apollo Studio / GraphOS | SaaS | Yes (Rover CLI) | Schema registry, persisted queries, perf tracing |
| Hasura | OSS + SaaS | Yes (CLI + REST admin API) | Auto-generates GraphQL from Postgres; agents drive via `hasura migrate` |
| WunderGraph / Cosmo | OSS | Yes | Federation router, agent-driven config |
| The Guild / GraphQL Mesh | OSS | Yes (config files) | Stitches REST/gRPC into GraphQL |
| AWS AppSync | SaaS | Yes (CDK) | Managed GraphQL with VTL/JS resolvers |
| `pothos` / `nexus` | OSS libs | Yes | Code-first schema for TS — friendlier to LLM codegen than SDL-first |
| `gqlgen` (Go) | OSS | Yes | SDL-first Go server with codegen |

## Templates & scripts
See `templates.md` for full DataLoader, depth-limit, and cost-analysis middleware. Minimal codegen config:

```yaml
# codegen.yml
schema: 'src/schema/**/*.graphql'
documents: 'src/**/*.{ts,tsx,graphql}'
generates:
  src/__generated__/types.ts:
    plugins: [typescript, typescript-resolvers]
    config:
      contextType: '../context#GraphQLContext'
      mappers:
        User: '../db/user#UserRecord'
        Order: '../db/order#OrderRecord'
  src/__generated__/operations.ts:
    plugins: [typescript-operations, typed-document-node]
hooks:
  afterAllFileWrite: [prettier --write]
```

## Best practices
- Per-request DataLoader scoping: instantiate inside the request context, never module-level — module-level caches leak across users
- Depth limit (5–8) + complexity limit (e.g., 1000 cost units) on the server, before resolvers run
- Persisted queries in production: clients send a hash, server resolves SDL — kills query-injection DoS and slashes bandwidth
- Connection-style pagination (Relay cursor) for any list >20 items; do not return raw arrays for tables
- Authorization in a directive (`@auth(requires: ROLE)`) or per-resolver guard, never in the gateway alone
- Versioning: never bump v1→v2; deprecate fields with `@deprecated(reason: "...")` and remove after analytics show 0 use
- Subscriptions over `graphql-ws` (modern) not `subscriptions-transport-ws` (deprecated) — server libs default to old; agents must opt in
- Mutations return the modified entity + `clientMutationId`; never return `Boolean` — clients can't refetch optimistically

## AI-agent gotchas
- Agents emit field resolvers without DataLoader because tutorials skip it — always require an `XByYLoader` for any 1:N traversal
- LLMs over-nest input types creating impossible-to-validate shapes; flatten to single-purpose `<Entity><Action>Input!`
- Schema-first vs code-first: codegen output drift between the two confuses agents reading half the codebase. Pick one; document the choice in CLAUDE.md
- Agents copy the original `subscriptions-transport-ws` from old docs; current standard is `graphql-ws` — pin the protocol explicitly
- N+1 detection is not free — wire `apollo-tracing` or OpenTelemetry GraphQL instrumentation and assert tracing is on in tests
- Human-in-loop checkpoint required when: making any breaking schema change, adding a federation `@key`, raising depth/cost limits in production
- Token waste: do not paste the entire schema into context; rely on `graphql-inspector` summary + the touched type only
- Agents forget that `Boolean!` non-null returns from mutations make rollback impossible; insist on entity returns

## References
- Spec: https://spec.graphql.org/
- Apollo best practices: https://www.apollographql.com/docs/technotes/
- DataLoader: https://github.com/graphql/dataloader
- Relay cursor connections spec: https://relay.dev/graphql/connections.htm
- `graphql-inspector` docs: https://the-guild.dev/graphql/inspector
- Pothos (code-first TS): https://pothos-graphql.dev/
- Apollo Federation v2: https://www.apollographql.com/docs/federation/
- Query cost analysis: https://github.com/slicknode/graphql-query-complexity
