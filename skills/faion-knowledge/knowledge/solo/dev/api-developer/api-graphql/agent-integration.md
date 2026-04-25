# Agent Integration — GraphQL Patterns

## When to use
- Client needs to fetch nested data (user → orders → items) in a single round-trip with field selection.
- Multiple consumers (web, mobile, partner) want different shapes off the same backend without bespoke REST endpoints.
- You want a typed schema as the contract between BE and FE generators (codegen, Apollo, urql, Relay).
- Real-time fan-out via subscriptions belongs alongside the same query/mutation graph.
- Federating multiple services into one supergraph (Apollo Federation, Hot Chocolate, Mercurius).

## When NOT to use
- Simple CRUD on a single resource — REST is shorter, cacheable, and well-tooled.
- File upload heavy / streaming binary — multipart REST or gRPC stream is better.
- Public, cache-on-CDN read APIs — GET + URL semantics outperform POST /graphql.
- Hard p99 latency budgets where resolver fan-out is unpredictable.
- Tiny team without bandwidth to operate persisted queries, depth limits, complexity scoring.

## Where it fails / limitations
- N+1 queries are the default unless DataLoader is wired into every relation field.
- HTTP caching does not work out of the box (everything is POST /graphql with the same URL).
- Public schemas without depth/complexity limits are a free DoS amplifier.
- Auth at field level is hand-rolled — easy to forget on a new resolver.
- Errors arrive in a `data + errors` envelope; partial success makes status-code monitoring useless.
- Subscriptions over websockets re-introduce stateful sessions you thought GraphQL would remove.

## Agentic workflow
Drive GraphQL changes schema-first: an agent edits the SDL, regenerates types and resolvers, then writes/updates DataLoaders and tests. Treat the SDL diff as the artifact a human reviews — never let an agent autopatch a resolver without showing the schema change first. For federation, partition by subgraph and run schema composition checks (`rover supergraph compose`, `apollo schema:check`) as the gate before merge.

### Recommended subagents
- `faion-feature-executor` — sequence schema edit → codegen → resolver → DataLoader → test as ordered tasks.
- `faion-sdd-execution` — quality gate that blocks if depth/complexity limits or DataLoader are missing on new fields.
- A `graphql-resolver` task agent (Sonnet) — resolver + DataLoader implementation with paste-in SDL.
- A `schema-reviewer` task agent (Opus) — checks for breaking changes, missing pagination, cycles, naming.

### Prompt pattern
```
You are editing the orders subgraph SDL. Add a `refundedAt: DateTime` field
to type Order. Update the Strawberry resolver, add a DataLoader for
batch_load_refund_status, regenerate the TS client types, and add one
integration test that hits /graphql with the new field. Do NOT add depth or
complexity changes. Output: unified diff only.
```

```
Run `rover subgraph check orders --schema ./orders.graphql` against the
prod supergraph. If breaking, propose a deprecation plan with @deprecated
reason and migration timeline. Do not push.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `rover` | Apollo Federation schema check / publish / compose | `curl -sSL https://rover.apollo.dev/nix/latest \| sh` · apollographql.com/docs/rover |
| `graphql-codegen` | Generate TS types, hooks, resolver scaffolds | `npm i -D @graphql-codegen/cli` · the-guild.dev/graphql/codegen |
| `gql.tada` / `graphql-tag` | Inline typed queries | npm |
| `graphql-inspector` | Diff + breaking change detection | `npm i -g @graphql-inspector/cli` |
| `graphqurl` (`gq`) | curl-equivalent for GraphQL | `npm i -g graphqurl` |
| `clairvoyance` | Introspection-blind schema recovery (red team) | `pip install clairvoyance` |
| `graphw00f` | Fingerprint server engine + lookup CVEs | `pip install graphw00f` |
| `graphql-cop` | Security audit (depth, batching, suggestions) | `pip install graphql-cop` |

## Services & apps
| Service | Type | Agent-friendly? | Notes |
|---------|------|-----------------|-------|
| Apollo GraphOS / Studio | SaaS | Yes — Rover CLI | Federation registry, schema checks, ops metrics |
| Hasura | OSS + Cloud | Partial — REST-ish admin API | Auto-generates schema from Postgres; agents can add permissions via metadata YAML |
| PostGraphile | OSS | Yes — config files | Postgres → GraphQL, plugin-driven |
| WunderGraph Cosmo | OSS | Yes — `wgc` CLI | Federation router + registry, self-hostable Apollo alternative |
| Stellate | SaaS | Yes — config-as-code | GraphQL CDN + caching (the missing CDN story) |
| The Guild Hive | SaaS + OSS | Yes | Schema registry + usage analytics |
| Apollo Sandbox / GraphiQL | OSS | Manual | Used for dev; agents can hit `/graphql` directly with curl |

## Templates & scripts
See `templates.md` and `examples.md` in this directory for SDL + resolver scaffolds.

Quick smoke check that DataLoader is wired (drop in CI):

```bash
#!/usr/bin/env bash
# fail if any *Resolver.ts/py touches db inside a loop without a loader
set -euo pipefail
grep -rEn 'for .* in .*:\s*$' resolvers/ | while read -r hit; do
  file=${hit%%:*}
  if grep -q 'await.*\.find\|\.query\|session\.execute' "$file" \
     && ! grep -q 'DataLoader\|dataloader' "$file"; then
    echo "N+1 risk: $file"
    exit 1
  fi
done
```

## Best practices
- Schema-first, not code-first, when more than one client consumes the API — the SDL is the contract.
- One DataLoader per relation, instantiated per-request in context. Never module-global (cross-request leak).
- Cap query depth (8–10) and complexity (100–500) on every public endpoint. Tune from real traffic.
- Persist queries in production: client sends a hash, server resolves to canned operation. Closes injection + DoS surface in one move.
- Return `errors[].extensions.code` as a stable enum — clients should never parse `message`.
- Use Relay-style cursor pagination (`first/after`, `edges`, `pageInfo`); offset pagination breaks under writes.
- Field-level auth via directive (`@auth(role: ADMIN)`) or permission classes — not in business logic.
- Never expose `__schema` to anonymous users in production. Disable introspection or gate on auth.

## AI-agent gotchas
- Agents love to add a new field and forget the DataLoader → silently quadratic in prod. Add a lint step that fails CI when a resolver hits the DB inside a loop.
- LLM-generated SDL frequently mixes `ID` and `String`, drops `!` non-null markers, or invents `Float` for money. Pin a schema linter (`graphql-schema-linter`, `eslint-plugin-graphql`) and run before commit.
- Subscription handlers are stateful — agents trained on REST will leak listeners. Require explicit `on_disconnect` cleanup in the diff.
- Federation: an agent editing one subgraph can break the supergraph. Always run `rover subgraph check` against the production graph before merging — that's the human-in-loop checkpoint.
- Persisted queries break iterative LLM debugging. Allow a dev-only escape hatch with header `x-persisted-bypass=1`, never in prod.
- When migrating a REST endpoint to GraphQL, agents will recreate REST shapes 1:1 (one query per old endpoint). Force them to model the entity graph instead — review the type relationships, not the operation list.
- Error envelopes mean a 200 OK can carry a failure. Wire your error-budget alerts on `errors[]` count, not HTTP status.

## References
- https://spec.graphql.org/
- https://graphql.org/learn/best-practices/
- https://github.com/graphql/dataloader
- https://www.apollographql.com/docs/federation/
- https://relay.dev/graphql/connections.htm
- https://escape.tech/blog/graphql-security-checklist/
- https://github.com/dolevf/graphql-cop
