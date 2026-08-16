# GraphQL API

## Summary

**One-sentence:** Build a GraphQL API with schema-first SDL, codegen, per-request DataLoader, depth + complexity limits, cursor pagination, and breaking-change CI gates.

**One-paragraph:** Schema-first SDL development with codegen; every 1:N relation served by a per-request DataLoader to prevent N+1; depth limit (5-8) and query complexity cap enforced before resolvers run; cursor-based (Relay) pagination for any list; graphql-inspector or graphql-cli check diff in CI to block breaking schema changes. Mutations return typed `MutationNamePayload` types with explicit userErrors arrays. Output is schema.graphql + resolvers + dataloader wiring + CI gates.

**Ефективно для:**

- BFF-style GraphQL APIs serving multiple clients.
- Federated graphs where schema discipline is essential.
- Replacing REST endpoints whose payload composition is client-specific.
- AI-agent-generated services where the schema is the deterministic contract.

## Applies If (ALL must hold)

- GraphQL is the deliberate protocol (not retrofitted onto REST).
- Multiple consumers benefit from per-client payload shaping.
- Relations are graph-like (1:N, N:M) where DataLoader earns its place.
- Engineering owns schema discipline (codegen, depth/complexity, diff gates).

## Skip If (ANY kills it)

- Single consumer + simple resource shape — REST is simpler.
- Internal RPC where types matter more than payload shaping — use gRPC.
- Embedded systems or constrained environments where GraphQL overhead is prohibitive.
- Project relies on stack that doesn't support per-request DataLoader semantics.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Schema decisions: types, relations, paginated lists | SDL draft | tech-lead |
| Codegen target language + library (gqlgen, Apollo Server, Pothos) | config | platform |
| Depth + complexity caps decided + measured against worst-case queries | config | tech-lead |
| Schema diff tool wired (graphql-inspector or graphql-cli check) | config | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-versioning]] | Breaking-change policy aligns with schema diff gate. |
| [[logging-patterns]] | Resolver instrumentation logs operation_name + duration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 6 testable rules (schema-first, codegen, dataloader for 1:N, depth+complexity caps, cursor pagination, diff gate in CI) | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema for GraphQL API spec + valid/invalid examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom/root-cause/fix | 800 |
| `content/04-procedure.xml` | essential | 6-step procedure: SDL → codegen → resolvers → dataloaders → depth/complexity → diff gate | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree → rule from 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema_design` | opus | Type design + relations + pagination shape need deep synthesis. |
| `dataloader_wiring` | sonnet | Per-relation: declare, batch, register. |
| `depth_complexity_caps` | sonnet | Configure plugin; measure worst-case queries. |
| `diff_gate_setup` | sonnet | graphql-inspector CI job + baseline schema commit. |

## Templates

| File | Purpose |
|------|---------|
| `templates/codegen.yml` | graphql-codegen config for TS/server + client types |
| `templates/dataloader-pattern.ts` | DataLoader factory pattern per request |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graphql-api.py` | Validate GraphQL API spec against 02-output-contract schema | Pre-publish gate / pre-commit |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[graphql-api-design]]
- [[api-versioning]]
- [[logging-patterns]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps protocol choice, consumer shape, and DataLoader readiness to a rule from `01-core-rules.xml`, telling the agent whether to apply GraphQL conventions or skip for REST/gRPC. Walk it on every fresh invocation; do not memo-ise outcomes across distinct engagements.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/codegen.yml`

```yaml
# codegen.yml — graphql-codegen config for TypeScript + typed document nodes
# Run: pnpm graphql-codegen
# Generates: TypeScript resolver types + typed operation documents

schema: 'src/schema/**/*.graphql'
documents: 'src/**/*.{ts,tsx,graphql}'

generates:
  src/__generated__/types.ts:
    plugins:
      - typescript
      - typescript-resolvers
    config:
      contextType: '../context#GraphQLContext'
      mappers:
        User: '../db/user#UserRecord'
        Order: '../db/order#OrderRecord'
      # Prefer undefined over null for optional fields
      maybeValue: T | undefined

  src/__generated__/operations.ts:
    plugins:
      - typescript-operations
      - typed-document-node

hooks:
  afterAllFileWrite:
    - prettier --write
```

### `templates/dataloader-pattern.ts`

```typescript
// dataloader-pattern.ts — Per-request DataLoader context factory
// Wire into your GraphQL server context function.
// Each request gets fresh DataLoader instances — never share across requests.

import DataLoader from 'dataloader';
import { db } from './db';

// Batch function: receives array of IDs, returns array of items in same order
async function batchUsers(ids: readonly string[]) {
  const users = await db.user.findMany({ where: { id: { in: [...ids] } } });
  const userMap = new Map(users.map((u) => [u.id, u]));
  // Must return items in the same order as input IDs, null for missing
  return ids.map((id) => userMap.get(id) ?? null);
}

async function batchProductsByOrderId(orderIds: readonly string[]) {
  const items = await db.orderItem.findMany({
    where: { orderId: { in: [...orderIds] } },
    include: { product: true },
  });
  const grouped = new Map<string, typeof items>();
  for (const item of items) {
    const list = grouped.get(item.orderId) ?? [];
    list.push(item);
    grouped.set(item.orderId, list);
  }
  return orderIds.map((id) => grouped.get(id) ?? []);
}

export interface GraphQLContext {
  userId: string | null;
  loaders: {
    user: DataLoader<string, Awaited<ReturnType<typeof batchUsers>>[number]>;
    productsByOrder: DataLoader<string, Awaited<ReturnType<typeof batchProductsByOrderId>>[number]>;
  };
}

// Called once per request by the GraphQL server
export function createContext(req: { user?: { id: string } }): GraphQLContext {
  return {
    userId: req.user?.id ?? null,
    loaders: {
      user: new DataLoader(batchUsers),
      productsByOrder: new DataLoader(batchProductsByOrderId),
    },
  };
}
```
