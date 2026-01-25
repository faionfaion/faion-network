---
id: graphql-api-design
name: "GraphQL API Design"
domain: DEV
skill: faion-software-developer
category: "development"
---

# GraphQL API Design

## Schema Design

```graphql
# Scalar types
scalar DateTime
scalar UUID
scalar Email

# Enums
enum UserRole {
  ADMIN
  MODERATOR
  MEMBER
}

# Interfaces
interface Node {
  id: ID!
}

interface Timestamped {
  createdAt: DateTime!
  updatedAt: DateTime!
}

# Types
type User implements Node & Timestamped {
  id: ID!
  email: Email!
  name: String!
  role: UserRole!
  isActive: Boolean!
  createdAt: DateTime!
  updatedAt: DateTime!

  # Relationships
  organization: Organization!
  orders(first: Int, after: String, status: OrderStatus): OrderConnection!
  posts(first: Int, after: String): PostConnection!
}

# Input types
input CreateUserInput {
  email: Email!
  name: String!
  role: UserRole = MEMBER
  organizationId: ID!
}

# Payload types
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}

# Root types
type Query {
  user(id: ID!): User
  users(first: Int = 20, after: String, filter: UserFilterInput): UserConnection!
  me: User
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeletePayload!
}

type Subscription {
  orderStatusChanged(orderId: ID!): Order!
}
```

## DataLoader for N+1 Prevention

```python
from strawberry.dataloader import DataLoader
from typing import List
from uuid import UUID

class OrganizationLoader(DataLoader[UUID, Organization]):
    async def batch_load_fn(self, keys: List[UUID]) -> List[Organization]:
        # Fetch all organizations in single query
        organizations = await self.repository.find_by_ids(keys)

        # Return in same order as keys
        org_map = {org.id: org for org in organizations}
        return [org_map.get(key) for key in keys]
```

## Authentication and Authorization

```python
from strawberry.permission import BasePermission
from strawberry.types import Info

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        return info.context.current_user_id is not None

class IsAdmin(BasePermission):
    message = "User is not an admin"

    async def has_permission(self, source, info: Info, **kwargs) -> bool:
        if not info.context.current_user_id:
            return False

        user = await info.context.services.user.get_by_id(
            info.context.current_user_id
        )
        return user and user.role == UserRole.ADMIN

@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def create_order(self, info: Info, input: CreateOrderInput) -> Order:
        ...

    @strawberry.mutation(permission_classes=[IsAdmin])
    async def delete_user(self, info: Info, id: strawberry.ID) -> bool:
        ...
```

## Query Complexity and Depth Limiting

```python
from strawberry.extensions import QueryDepthLimiter
from strawberry.extensions.query_complexity import QueryComplexityExtension

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[
        QueryDepthLimiter(max_depth=10),
        QueryComplexityExtension(max_complexity=100),
    ],
)

# Field-level complexity
@strawberry.type
class User:
    @strawberry.field(complexity=1)
    def name(self) -> str:
        return self._name

    @strawberry.field(complexity=10)
    async def orders(self, first: int = 10) -> List[Order]:
        return await self._load_orders(first)
```

## Error Handling

```python
# Union types for errors
@strawberry.type
class UserNotFoundError:
    message: str
    user_id: str

@strawberry.type
class ValidationError:
    message: str
    field: str

UserResult = strawberry.union(
    "UserResult",
    [User, UserNotFoundError, PermissionDeniedError],
)

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, info: Info, id: strawberry.ID) -> UserResult:
        if not info.context.current_user_id:
            return PermissionDeniedError(message="Authentication required")

        user = await info.context.services.user.get_by_id(UUID(id))

        if not user:
            return UserNotFoundError(
                message=f"User not found",
                user_id=id,
            )

        return user
```

## Best Practices

- Use input types for all mutations
- Implement cursor-based pagination (Relay spec)
- Use DataLoader to prevent N+1 queries
- Add depth and complexity limits
- Implement field-level authorization
- Use union types for error handling
- Always paginate list fields

## Sources

- [GraphQL Specification](https://spec.graphql.org/)
- [Strawberry GraphQL](https://strawberry.rocks/)
- [Relay Connection Spec](https://relay.dev/graphql/connections.htm)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
