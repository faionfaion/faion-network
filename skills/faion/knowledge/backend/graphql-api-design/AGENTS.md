# GraphQL API Design

## Summary

**One-sentence:** Designs a GraphQL service schema-first: Relay cursor pagination, per-request DataLoaders, mutation payloads with typed error unions, and depth/complexity limits.

**One-paragraph:** Designs a GraphQL service schema-first: Relay cursor pagination, per-request DataLoaders, mutation payloads with typed error unions, and depth/complexity limits. Decision tree, output contract, failure modes, and a procedure (when complexity ≥ medium) live under `content/`. Templates in `templates/` start with a 5-line `__faion_header__` block; the validator script in `scripts/` is stdlib-only with `--help` and `--self-test`.

**Ефективно для:**

- New GraphQL service designed schema-first with SDL reviewed by humans + consumed by codegen.
- Multiple distinct clients (web, mobile, partner) need different shapes of the same domain.
- Schema has nested reads with field-level auth (SaaS dashboards with org/role).
- Output produces `spec` matching the schema in `content/02-output-contract.xml`.

## Applies If (ALL must hold)

- New GraphQL service designed schema-first with SDL reviewed by humans + consumed by codegen.
- Multiple distinct clients (web, mobile, partner) need different shapes of the same domain.
- Schema has nested reads with field-level auth (SaaS dashboards with org/role).

## Skip If (ANY kills it)

- Public cacheable read API — REST + CDN wins.
- Single-client, single-team CRUD with no nested reads — overhead of DataLoader + depth/complexity not paid back.
- File upload / streaming-binary workloads — use REST or gRPC.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Domain entity model | diagram or doc | team |
| Client query mock list | *.graphql samples | frontend |
| Auth/permission model | table of roles → fields | team |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rest-design]] | Some clients may also need REST endpoints next to GraphQL |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 12 testable rules (payload+userErrors, directive auth, naming, opaque IDs, run + skip leaves) with rationale + source | 1800 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden patterns + allowed transformations | 1200 |
| `content/03-failure-modes.xml` | essential | 8 antipatterns with symptom + root-cause + fix | 1300 |
| `content/04-procedure.xml` | essential | 8-step end-to-end procedure incl. auth-directive authoring + naming audit | 1300 |
| `content/05-examples.xml` | reference | Two full worked examples end-to-end with the trace and the resulting artefact | 1200 |
| `content/06-decision-tree.xml` | essential | Root question + 13 branches incl. the shape gates → conclusion(ref=rule-id); skip leaf always reachable | 900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema-design` | opus | Domain modelling + nullability decisions need strongest judgement. |
| `resolver-implementation` | sonnet | Mechanical SDL → resolver + DataLoader wiring. |
| `permission-audit` | haiku | Grep-style scan for missing permission_classes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | SDL skeleton: Node/Timestamped interfaces, Relay Connection/Edge/PageInfo, Payload with userErrors, @auth directive |
| `templates/dataloader.py` | Strawberry DataLoaders: per-request batching, key-order preservation, 1:N grouping, context factory |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-graphql-api-design.py` | Validate the produced artefact against the schema in `content/02-output-contract.xml`. | Pre-commit; CI on each artefact change; `--self-test` in dev. |

## Related

- [[api-rest-design]]
- [[api-authentication]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. Root question: *Is the use case multi-client with nested reads or single-client CRUD?* The tree's purpose is to route an input through observable signals to a conclusion that references a rule from `content/01-core-rules.xml`; the skip-this-methodology branch is always reachable so an inappropriate caller exits cleanly.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/schema.graphql`

```graphql
scalar DateTime
scalar Email

enum AuthScope { ADMIN ORDERS_WRITE PAYMENTS_WRITE }
directive @auth(scope: AuthScope!) on FIELD_DEFINITION

interface Node { id: ID! }
interface Timestamped { createdAt: DateTime!; updatedAt: DateTime! }

enum UserRole { ADMIN MODERATOR MEMBER }
enum OrderStatus { DRAFT PLACED PAID SHIPPED DELIVERED CANCELLED }

type User implements Node & Timestamped {
  id: ID!
  email: Email! @auth(scope: ADMIN)
  name: String!
  role: UserRole!
  isActive: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
  orders(first: Int, after: String, status: OrderStatus): OrderConnection!
}

type Order implements Node & Timestamped {
  id: ID!
  status: OrderStatus!
  totalAmount: Float!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}
type OrderEdge { cursor: String!; node: Order! }
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type UserError { field: String; message: String!; code: String! }

input CreateUserInput { email: Email!; name: String!; role: UserRole }
input UpdateUserInput { email: Email; name: String; role: UserRole }

type CreateUserPayload { user: User; userErrors: [UserError!]! }
type UpdateUserPayload { user: User; userErrors: [UserError!]! }
type DeleteUserPayload { deletedId: ID; userErrors: [UserError!]! }

type Query {
  user(id: ID!): User
  me: User
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload! @auth(scope: ADMIN)
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload! @auth(scope: ADMIN)
  deleteUser(id: ID!): DeleteUserPayload! @auth(scope: ADMIN)
}
```

### `templates/dataloader.py`

```python
from typing import List
from uuid import UUID

from strawberry.dataloader import DataLoader


class OrganizationLoader(DataLoader):
    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, keys: List[UUID]):
        orgs = await self.repository.find_by_ids(keys)
        org_map = {org.id: org for org in orgs}
        # CRITICAL: return in the same order as keys; None for missing.
        return [org_map.get(key) for key in keys]


class UserLoader(DataLoader):
    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, keys: List[UUID]):
        users = await self.repository.find_by_ids(keys)
        user_map = {u.id: u for u in users}
        return [user_map.get(key) for key in keys]


class OrdersByUserLoader(DataLoader):
    """1:N grouping — one list of orders per user_id, empty list when none."""

    def __init__(self, repository):
        super().__init__(load_fn=self.batch_load_fn)
        self.repository = repository

    async def batch_load_fn(self, user_ids: List[UUID]):
        orders = await self.repository.find_by_user_ids(user_ids)
        grouped: dict[UUID, list] = {uid: [] for uid in user_ids}
        for order in orders:
            grouped[order.user_id].append(order)
        return [grouped[uid] for uid in user_ids]


def create_loaders(repository_factory) -> dict:
    """Call once per request from get_context(). Never at module scope —
    a module-level loader caches across requests and leaks user data."""
    return {
        "organization": OrganizationLoader(repository_factory.organization),
        "user": UserLoader(repository_factory.user),
        "orders_by_user": OrdersByUserLoader(repository_factory.order),
    }
```
