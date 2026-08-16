# GraphQL API Design

## Summary

**One-sentence:** Designs a GraphQL schema with persisted queries, DataLoader N+1 protection, depth+complexity limits, and an error-extension envelope mirroring RFC 7807.

**One-paragraph:** GraphQL gives clients a flexible query surface but trades that flexibility for new failure modes — N+1, runaway query depth, expensive resolvers. This methodology emits a schema-pack: SDL with persisted-query allowlist, DataLoader factory per N+1-prone relation, depth + complexity caps in the gateway, and an error-extension envelope mirroring RFC 7807 so clients see one error shape across REST + GraphQL. Output: schema.graphql + DataLoader factories + depth/complexity config.

**Ефективно для:**

- Solo dev adding GraphQL alongside REST for a more flexible mobile client.
- Existing GraphQL API where p95 latency exploded due to N+1 on a popular query.
- Closing GraphQL by switching to persisted queries (kills introspection surface in prod).
- Adding query-depth + complexity limits before launching to public.

## Applies If (ALL must hold)

- Schema has &gt;= 5 types with at least one N+1-prone relation (1:N navigation).
- Gateway can enforce depth + complexity (Apollo Router / Hasura / GraphQL Yoga).
- Client surface is &lt;= 5 known clients (so persisted queries are feasible).
- Author can ship a single deprecate-then-remove window.

## Skip If (ANY kills it)

- Pure REST API (use api-rest-design).
- Public open-introspection API where clients are unknown (persisted queries impossible).
- Sub-100-RPS internal GraphQL where N+1 cost is negligible.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain model | type sketches | PRD / architect |
| Existing N+1 hotspots | trace samples | APM |
| Gateway choice | Apollo Router / Yoga / Hasura | platform |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| [[api-error-handling]] | Error-extension envelope mirrors RFC 7807. |
| [[api-rate-limiting]] | Persisted-query allowlist drives the rate-limit key. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `api_graphql_draft` | sonnet | Bounded synthesis. |
| `api_graphql_validate` | haiku | Mechanical schema check. |
| `api_graphql_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | GraphQL SDL skeleton with persisted-query pragma + nullable defaults |
| `templates/dataloader-factory.ts` | TypeScript DataLoader factory for 1-to-N relations |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-graphql artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-graphql artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-graphql.py` | Validate api-graphql artefact against schema | Pre-commit; CI on each artefact change |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[graphql-api-design]]
- [[api-rest-design]]
- [[api-documentation]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/schema.graphql`

```graphql
scalar DateTime

type User {
  id: ID!
  name: String!
  email: String!
  orders(first: Int, after: String): OrderConnection!
  createdAt: DateTime!
}

type Order {
  id: ID!
  total: Float!
  status: OrderStatus!
  items: [OrderItem!]!
}

enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

type OrderItem {
  id: ID!
  name: String!
  quantity: Int!
  unitPrice: Float!
}

# Relay-style pagination
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  cursor: String!
  node: Order!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input CreateUserInput {
  name: String!
  email: String!
}

type Query {
  user(id: ID!): User
  users(first: Int, after: String): OrderConnection!
  me: User
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input UpdateUserInput {
  name: String
  email: String
}

type Subscription {
  orderStatusChanged(userId: ID!): Order!
}
```

### `templates/dataloader-factory.ts`

```typescript
 */
import DataLoader from 'dataloader';
import { db } from '../db';

// Call once per request in context setup — never at module level
export const createLoaders = () => ({
  userById: new DataLoader<string, User | null>(async (ids) => {
    const rows = await db.users.findMany({ where: { id: { in: [...ids] } } });
    const map = new Map(rows.map(u => [u.id, u]));
    // Return in the exact same order as input ids
    return ids.map(id => map.get(id) ?? null);
  }),

  ordersByUserId: new DataLoader<string, Order[]>(async (userIds) => {
    const rows = await db.orders.findMany({
      where: { userId: { in: [...userIds] } },
    });
    const grouped = new Map<string, Order[]>();
    for (const r of rows) {
      const arr = grouped.get(r.userId) ?? [];
      arr.push(r);
      grouped.set(r.userId, arr);
    }
    return userIds.map(id => grouped.get(id) ?? []);
  }),
});

// Usage: in GraphQL context factory
// export async function getContext(request: Request) {
//   return { loaders: createLoaders(), currentUserId: ... };
// }
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-graphql.json",
  "type": "object",
  "required": [
    "pack_id",
    "schema_path",
    "persisted_queries_only",
    "dataloaders",
    "max_depth",
    "max_complexity",
    "error_extensions_format"
  ],
  "properties": {
    "pack_id": {
      "type": "string",
      "pattern": "^GQL-[A-Z0-9-]{2,40}$"
    },
    "schema_path": {
      "type": "string",
      "minLength": 4
    },
    "persisted_queries_only": {
      "type": "boolean"
    },
    "dataloaders": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "relation"
        ]
      }
    },
    "max_depth": {
      "type": "integer",
      "minimum": 1,
      "maximum": 20
    },
    "max_complexity": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10000
    },
    "error_extensions_format": {
      "type": "string",
      "enum": [
        "rfc-7807",
        "custom"
      ]
    },
    "n_plus_1_hotspots": {
      "type": "integer",
      "minimum": 0
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "pack_id": "GQL-MOBILE-API",
  "schema_path": "graphql/schema.graphql",
  "persisted_queries_only": true,
  "dataloaders": [
    {
      "name": "userByIdLoader",
      "relation": "Order.user"
    },
    {
      "name": "orderItemsLoader",
      "relation": "Order.items"
    }
  ],
  "max_depth": 10,
  "max_complexity": 1000,
  "error_extensions_format": "rfc-7807",
  "n_plus_1_hotspots": 0
}
```
