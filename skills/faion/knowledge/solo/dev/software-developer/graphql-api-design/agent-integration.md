# Agent Integration — GraphQL API Design

## When to use
- Multiple clients (web + iOS + Android + partner) with divergent field needs over the same domain.
- Highly relational data where REST would force N+1 round-trips or sprawling `?expand=` query params.
- Schema-first development where the contract is the source of truth and codegen drives client + server types.
- Subscriptions over WebSocket / SSE for live dashboards, chat, collaborative editing.
- Federated services (Apollo Federation, GraphQL Hive) when you want one supergraph over many domain teams.

## When NOT to use
- Public, cache-heavy, CDN-fronted read APIs — REST + HTTP cache headers wins.
- File upload / streaming binary payloads — multipart REST or signed URLs are simpler.
- Tiny CRUD app with a single client — schema overhead, resolver wiring, and N+1 traps are not worth it.
- Latency-sensitive RPC inside the cluster — gRPC is faster and stricter.
- When your team has zero GraphQL experience and the deadline is tight; learning curve hits hard at the resolver-and-dataloader stage.

## Where it fails / limitations
- N+1 queries by default — every nested resolver fetches separately unless DataLoader / batching is in place.
- HTTP-level caching is essentially gone (single POST endpoint); you need persisted queries + APQ + custom cache plugin.
- Authorization spreads across every resolver; easy to leave a field unprotected. Field-level auth must be policy-driven, not ad-hoc.
- Query cost / depth attacks: a malicious client can request `friends.friends.friends...` and DoS the server.
- File uploads via the multipart spec are clunky; most teams sidestep with S3 presigned URLs.
- Tooling fatigue: codegen + Apollo client + cache normalization + typed resolvers is a lot of moving parts.

## Agentic workflow
Schema-first: write or evolve `schema.graphql` first; agents then run codegen for typed resolvers (`graphql-codegen`, `strawberry`, `ariadne-codegen`) and stub each missing resolver. A second agent audits the schema for N+1 risk (any list field that returns objects with their own resolvers) and inserts DataLoader scaffolding. A third agent generates persisted-query manifests for production. Always gate schema breaking changes behind `graphql-inspector` diff in CI; never auto-merge a breaking change.

### Recommended subagents
- `faion-sdd-executor-agent` — drives the schema → resolver → test loop one type at a time.
- A custom `graphql-schema-reviewer` (you create it under `agents/`) — reads only `schema.graphql` + diff and produces breaking-change reports.

### Prompt pattern
```
You are extending schema.graphql. Add type <X> with fields <...>.
Constraints:
- Use Relay-style Connection for any list field returning >10 items.
- Every nullable field must have a justification comment.
- Output a breaking-change diff against current schema using graphql-inspector format.
```

```
For resolver <Type.field>, write a DataLoader-batched implementation.
Inputs: <parent type>, batch by <key>, fetch via <repo method>.
Output: resolver fn + dataloader registration + 1 unit test asserting N+1 collapses to 1 DB call.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| graphql-codegen | TS/Go/Python type + resolver codegen | `npm i -D @graphql-codegen/cli` · the-guild.dev |
| graphql-inspector | Schema diff, breaking-change CI gate | `npm i -D @graphql-inspector/cli` |
| Apollo Rover | Federated supergraph composition + checks | `curl -sSL https://rover.apollo.dev/nix/latest \| sh` |
| spectaql / magidoc | Static schema docs site | npm |
| graphqurl / gq | curl-equivalent for GraphQL endpoints | npm |
| strawberry-graphql | Python schema-first lib (codegen via decorators) | `pip install strawberry-graphql` |
| ariadne-codegen | Python typed client codegen | `pip install ariadne-codegen` |
| genql | TS typed client codegen from schema | npm |
| GraphQL Armor | Security middleware (depth, cost, alias limits) | escape.tech/graphql-armor |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Apollo GraphOS / Studio | SaaS | Yes — Rover CLI + REST API | Schema registry, checks, federation; agents drive via `rover subgraph publish`. |
| GraphQL Hive | OSS + SaaS | Yes — CLI + API | OSS alternative to Apollo Studio. |
| Hasura | OSS + SaaS | Yes — `hasura` CLI + metadata files | Auto-generated GraphQL over Postgres; metadata is YAML, agent-friendly. |
| PostGraphile | OSS | Partial — config + plugin code | Postgres → GraphQL with row-level security. |
| Stepzen / IBM API Connect | SaaS | Partial | Schema stitching as a service. |
| AWS AppSync | SaaS | Yes — CDK / Terraform | Managed GraphQL with VTL/JS resolvers; works well in IaC pipelines. |
| Apollo Server | OSS | Yes | De-facto Node server; integrates with most tracing stacks. |
| Yoga (The Guild) | OSS | Yes | Lightweight alt to Apollo Server, modern envelop plugins. |

## Templates & scripts
See `templates.md` for the full schema, Relay Connection pattern, and resolver scaffolding. Minimal cost-limit middleware:

```ts
// src/graphql/cost-limit.ts
import { costLimitPlugin } from "@escape.tech/graphql-armor-cost-limit";
import { maxDepthPlugin }  from "@escape.tech/graphql-armor-max-depth";
import { maxAliasesPlugin } from "@escape.tech/graphql-armor-max-aliases";

export const armorPlugins = [
  costLimitPlugin({ maxCost: 1000, objectCost: 2, scalarCost: 1, depthCostFactor: 1.5 }),
  maxDepthPlugin({ n: 8 }),
  maxAliasesPlugin({ n: 15 }),
];
```

## Best practices
- Use Relay-style `Connection` (`edges`, `pageInfo`, opaque `cursor`) for every list >10 items; never `offset`/`limit` in public schema.
- DataLoader per request, not per process; keys identity-equal to the actual fetch key (don’t pre-stringify).
- Make every mutation return a typed `<MutationName>Payload` with a `userErrors: [Error!]!` array — never throw for business errors.
- Persisted queries / Automatic Persisted Queries in production; reject unknown query hashes — kills introspection-based DoS.
- Disable introspection in prod or gate it behind admin auth; tools like Apollo Studio can ingest the schema via uploads instead.
- Field-level auth via a single policy layer (e.g., `graphql-shield`, custom directive `@auth(role: "ADMIN")`); never sprinkle `if (user.role !== ...)` in resolvers.
- Track the supergraph in a registry; CI runs `inspector diff` and fails on breaking changes unless tagged `BREAKING_CHANGE_APPROVED`.

## AI-agent gotchas
- LLMs forget DataLoader. They will write `users.map(u => fetchUserOrders(u.id))` and ship N+1s. Force "every list-returning resolver MUST use a dataloader" in the prompt.
- Agents tend to expose `password`, `email`, `apiKey` on the `User` type. Provide an explicit "fields to never expose" list.
- Generated mutations often `throw new Error("not found")` instead of returning `userErrors`. Provide the `MutationPayload` template.
- Schema diffs from agents may rename fields rather than deprecate; require `@deprecated(reason: "...")` for any removal.
- Subscriptions written by agents commonly leak DB connections / forget to unsubscribe on disconnect. Add a checklist item: unsubscribe + cleanup is asserted in test.
- Cost limits: an agent will set `maxCost: 1_000_000` to "make tests pass". Lock the value and require a justification comment if changed.
- Human-in-loop checkpoint: any change to `schema.graphql` that triggers an `inspector` BREAKING result must have a human reviewer.

## References
- GraphQL Spec — https://spec.graphql.org/
- Relay Cursor Connections — https://relay.dev/graphql/connections.htm
- DataLoader — https://github.com/graphql/dataloader
- GraphQL Armor — https://escape.tech/graphql-armor/
- Apollo Federation — https://www.apollographql.com/docs/federation/
- Production Considerations (Apollo) — https://www.apollographql.com/docs/apollo-server/security/
