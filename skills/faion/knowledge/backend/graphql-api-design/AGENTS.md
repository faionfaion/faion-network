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
| `content/01-core-rules.xml` | essential | 7 testable rules (incl. skip-this-methodology) with rationale + source | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid example + invalid example + forbidden traits | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 800 |
| `content/04-procedure.xml` | essential | 5-step end-to-end procedure with input/action/output per step | 900 |
| `content/05-examples.xml` | reference | One full worked example end-to-end with the trace and the resulting artefact | 700 |
| `content/06-decision-tree.xml` | essential | Root question + observable branches → conclusion(ref=rule-id); skip leaf always reachable | 600 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `schema-design` | opus | Domain modelling + nullability decisions need strongest judgement. |
| `resolver-implementation` | sonnet | Mechanical SDL → resolver + DataLoader wiring. |
| `permission-audit` | haiku | Grep-style scan for missing permission_classes. |

## Templates

| File | Purpose |
|------|---------|
| `templates/schema.graphql` | SDL skeleton: Node/Timestamped interfaces, Relay Connection/Edge/PageInfo, payload with error union |
| `templates/dataloader.py` | Strawberry DataLoader: per-request batch loading with key-order preservation |

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
<!-- faion_header_json: {"__faion_header__":{"purpose":"SDL skeleton: Node/Timestamped interfaces, Relay Connection/Edge/PageInfo, payload with error union","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#schema-first","token_budget_impact":"~150 tokens when loaded"}} -->
scalar DateTime
scalar UUID
scalar Email

interface Node { id: ID! }
interface Timestamped { createdAt: DateTime!; updatedAt: DateTime! }

enum UserRole { ADMIN MODERATOR MEMBER }

type User implements Node & Timestamped {
  id: ID!
  email: Email!
  name: String!
  role: UserRole!
  isActive: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!
  orders(first: Int, after: String): OrderConnection!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
}
type OrderEdge { cursor: String!; node: Order! }
type PageInfo { endCursor: String; hasNextPage: Boolean! }

type Order implements Node { id: ID!; total: Float! }

type UserError { field: String; message: String!; code: String! }

input CreateUserInput { email: Email!; name: String!; role: UserRole }
type CreateUserPayload { user: User; errors: [UserError!] }

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type Query {
  user(id: ID!): User
}
```

### `templates/dataloader.py`

```python
# faion_header_json: {"__faion_header__":{"purpose":"Strawberry DataLoader: per-request batch loading with key-order preservation","consumes":"see content/02-output-contract.xml","produces":"spec","depends_on":"content/01-core-rules.xml#schema-first","token_budget_impact":"~150 tokens when loaded"}}
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
        return [org_map.get(key) for key in keys]
```
