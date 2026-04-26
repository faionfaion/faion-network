# Agent Integration — GraphQL API Design

## When to use
- New service designed schema-first, where SDL is the contract reviewed by humans + consumed by codegen.
- Multiple distinct clients (web, mobile, partner) each need a different shape of the same domain.
- You expect federation/microservices later — start with the supergraph mindset.
- Heavy use of nested reads with field-level auth (e.g. SaaS dashboard with org/role permissions).
- Real-time + query unification: subscriptions next to queries on the same schema.

## When NOT to use
- Public, cacheable read API → REST + CDN wins.
- Hard latency budgets where unbounded resolver fan-out is unacceptable.
- File upload / streaming-binary heavy workloads.
- Single-client, single-team CRUD — overhead of schema, codegen, DataLoaders, depth/complexity is not paid back.
- Org without bandwidth to operate persisted queries, schema registry, breaking-change checks.

## Where it fails / limitations
- N+1 by default. DataLoader is mandatory infrastructure, not optional.
- HTTP caching does not work — no GET semantics, every request is POST `/graphql`.
- Depth + complexity bombs are trivial to write; without limits, public endpoints are DoS-prone.
- Field-level auth is hand-rolled per resolver; easy to miss on a new field.
- Error envelope (`data + errors`) confuses status-code-based monitoring; partial success is normal.
- Schema evolution requires deprecation (`@deprecated`) and sometimes versioned types — not a free lunch over REST.
- Persisted queries are operationally heavier (registry, build-time hashing) but mandatory for prod safety.

## Agentic workflow
Schema-first, always. The agent edits the SDL → schema lints + breaking-change check run → codegen produces typed clients + resolver scaffolds → agent fills resolvers + DataLoaders → integration test exercises the new field → human reviews the SDL diff (the contract). For federation, gate on `rover subgraph check` against the production graph before merging.

### Recommended subagents
- `faion-feature-executor` — sequence: SDL edit → codegen → resolver → DataLoader → permission → test.
- `faion-sdd-execution` — quality gate enforcing DataLoader, depth/complexity limits, permission class on every new field.
- A `schema-reviewer` agent (Opus) — checks SDL diff for naming, nullability, pagination, breaking changes.
- A `resolver-implementer` agent (Sonnet) — generates Strawberry/Apollo resolvers + DataLoaders from SDL.

### Prompt pattern
```
Edit schema/users.graphql: add an `archivedAt: DateTime` nullable field to
type User and a `archiveUser(id: ID!): ArchiveUserPayload!` mutation
returning the union of (User, ValidationError, NotAuthorizedError).

Then:
1. Run `graphql-inspector diff schema/users.graphql HEAD~1` and confirm
   non-breaking.
2. Run codegen.
3. Implement Strawberry resolver in resolvers/users.py with @permission_classes=[IsAdmin].
4. Add a UserArchivedAt DataLoader if archivedAt requires a join.
5. Add a pytest covering archive + double-archive + non-admin denial.

Output: unified diff only.
```

```
Audit resolvers/*.py for missing permission_classes on Mutation fields.
List offenders and propose the minimal permission class per field.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rover` | Apollo Federation: schema check / publish / compose | `curl -sSL https://rover.apollo.dev/nix/latest \| sh` |
| `graphql-codegen` | TS types, hooks, resolver scaffolds | `npm i -D @graphql-codegen/cli` |
| `graphql-inspector` | Diff + breaking-change detection | `npm i -g @graphql-inspector/cli` |
| `gql.tada` | Inline typed queries (zero-codegen TS) | `npm i gql.tada` |
| `graphql-schema-linter` | SDL style + naming rules | `npm i -g graphql-schema-linter` |
| `graphqurl` (`gq`) | GraphQL curl | `npm i -g graphqurl` |
| `graphql-cop` | Security audit (depth, batching, suggestions) | `pip install graphql-cop` |
| `clairvoyance` | Schema recovery when introspection is off (red team) | `pip install clairvoyance` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Apollo GraphOS / Studio | SaaS | Yes — Rover CLI, REST API | Federation registry + schema checks + ops metrics |
| WunderGraph Cosmo | OSS | Yes — `wgc` CLI | Self-hostable federation + registry |
| Hasura | OSS + Cloud | Partial — REST admin API | Postgres → GraphQL with metadata YAML |
| PostGraphile | OSS | Yes — config files | Postgres → GraphQL, plugin-driven |
| The Guild Hive | OSS + SaaS | Yes — CLI + API | Schema registry + usage analytics |
| Stellate | SaaS | Yes — config-as-code | GraphQL CDN + edge cache |
| Strawberry (Python) | OSS lib | Yes | Type-hint-driven server, Pythonic |
| Apollo Server / Yoga | OSS | Yes | TS/JS reference servers |

## Templates & scripts
See `templates.md` for SDL skeleton (Node, Connection, Payload, Error union) and `examples.md` for Strawberry permissions + DataLoader.

Lint + breaking-change gate (drop into CI):

```bash
#!/usr/bin/env bash
set -euo pipefail
graphql-schema-linter schema/*.graphql
graphql-inspector diff schema/schema.graphql origin/main:schema/schema.graphql \
  --rule considerUsage \
  --fail-on-breaking
# Federation
rover subgraph check users --schema schema/users.graphql \
  --name production --hint "$GITHUB_PR"
```

## Best practices
- One DataLoader per relation, scoped per request via context. Module-global = cross-request leak.
- Depth limit 8–10, complexity limit 100–500 on every public schema. Tune from real traffic histograms.
- Persist queries in production: client sends a hash, server resolves to a vetted operation. Closes injection + DoS surface in one move.
- Use `Result` / union types for expected errors (NotFound, Validation, NotAuthorized) — leave `errors[]` for unexpected failures.
- Stable error codes in `extensions.code` as an enum; clients never parse `message`.
- Relay-style cursor pagination on every list. Offset breaks under writes.
- Field-level auth via permission classes / directives, not in business logic.
- `@deprecated(reason: "...")` over silent removal; track usage in the schema registry before retiring.
- Disable introspection in production for non-public APIs, or gate behind auth.
- Naming: types `PascalCase`, fields `camelCase`, enums `SCREAMING_SNAKE`. Pin in schema linter.

## AI-agent gotchas
- Agents copy REST endpoints into GraphQL queries 1:1 (one query per old route). Force them to model the entity graph, not the operation list.
- LLM-generated SDL often drops non-null markers (`!`) or invents types like `Float` for money. Run `graphql-schema-linter` on every commit.
- Resolvers generated without DataLoader pass tests but quadratic in prod. Lint for "DB call inside iteration" and demand a loader.
- Permissions are forgotten on new resolvers — silently exposing data. SDD quality gate must require `permission_classes=` (or directive equivalent) on every Mutation/Query field touching auth-scoped data.
- An agent editing one subgraph can break the supergraph. Always run `rover subgraph check` before merging — the human-in-loop checkpoint.
- Persisted queries break iterative LLM debugging. Allow a dev-only escape hatch (`x-persisted-bypass=1`), never in prod.
- Error envelope means HTTP 200 can carry failure. Wire alerts on `errors[]` count, not status codes.
- Subscription handlers leak listeners when refactored by an agent that doesn't understand stateful sessions. Require explicit `on_disconnect` cleanup in any subscription PR.

## References
- https://spec.graphql.org/
- https://graphql.org/learn/best-practices/
- https://strawberry.rocks/
- https://relay.dev/graphql/connections.htm
- https://www.apollographql.com/docs/federation/
- https://www.apollographql.com/docs/apollo-server/performance/apq/
- https://github.com/dolevf/graphql-cop
- https://escape.tech/blog/graphql-security-checklist/
