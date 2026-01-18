# M-API-002: GraphQL Patterns

## Metadata
- **ID:** M-API-002
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, graphql, backend, schema]
- **Agent:** faion-api-agent

---

## Problem

REST APIs often lead to:
- Over-fetching: Getting more data than needed
- Under-fetching: Multiple requests to get related data
- Rigid endpoints: Backend changes required for new client needs
- Version proliferation: Multiple API versions to maintain

GraphQL solves these by letting clients request exactly what they need.

---

## Framework

### Step 1: Design Your Schema

The schema is the contract between client and server.

**Type definitions:**

```graphql
# Basic types
type User {
  id: ID!
  email: String!
  name: String
  createdAt: DateTime!
  orders: [Order!]!
  profile: Profile
}

type Profile {
  bio: String
  avatar: String
  website: String
}

type Order {
  id: ID!
  status: OrderStatus!
  total: Float!
  items: [OrderItem!]!
  user: User!
  createdAt: DateTime!
}

type OrderItem {
  id: ID!
  product: Product!
  quantity: Int!
  price: Float!
}

type Product {
  id: ID!
  name: String!
  description: String
  price: Float!
  category: Category!
  inStock: Boolean!
}

# Enums
enum OrderStatus {
  PENDING
  PROCESSING
  SHIPPED
  DELIVERED
  CANCELLED
}

# Custom scalars
scalar DateTime
scalar JSON
```

### Step 2: Define Queries

Queries are for reading data.

```graphql
type Query {
  # Single resource
  user(id: ID!): User
  product(id: ID!): Product
  order(id: ID!): Order

  # Collections with filtering/pagination
  users(
    filter: UserFilter
    sort: UserSort
    pagination: PaginationInput
  ): UserConnection!

  products(
    filter: ProductFilter
    sort: ProductSort
    first: Int
    after: String
  ): ProductConnection!

  # Current user (auth required)
  me: User
  myOrders(status: OrderStatus): [Order!]!
}

# Filter inputs
input UserFilter {
  email: String
  name: String
  createdAfter: DateTime
  createdBefore: DateTime
}

input ProductFilter {
  category: ID
  priceMin: Float
  priceMax: Float
  inStock: Boolean
  search: String
}

# Sort inputs
input UserSort {
  field: UserSortField!
  direction: SortDirection!
}

enum UserSortField {
  NAME
  EMAIL
  CREATED_AT
}

enum SortDirection {
  ASC
  DESC
}

# Pagination
input PaginationInput {
  page: Int
  perPage: Int
}
```

### Step 3: Define Mutations

Mutations are for creating, updating, deleting data.

```graphql
type Mutation {
  # User mutations
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
  deleteUser(id: ID!): DeleteUserPayload!

  # Order mutations
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
  cancelOrder(id: ID!): CancelOrderPayload!

  # Auth mutations
  login(email: String!, password: String!): AuthPayload!
  register(input: RegisterInput!): AuthPayload!
  refreshToken(token: String!): AuthPayload!
}

# Input types
input CreateUserInput {
  email: String!
  name: String!
  password: String!
}

input UpdateUserInput {
  email: String
  name: String
  bio: String
}

input CreateOrderInput {
  items: [OrderItemInput!]!
  shippingAddressId: ID!
}

input OrderItemInput {
  productId: ID!
  quantity: Int!
}

# Payload types (include possible errors)
type CreateUserPayload {
  user: User
  errors: [Error!]
}

type AuthPayload {
  token: String
  user: User
  errors: [Error!]
}

type Error {
  field: String
  message: String!
  code: String!
}
```

### Step 4: Define Subscriptions

Subscriptions are for real-time updates.

```graphql
type Subscription {
  # Order status changes
  orderStatusChanged(orderId: ID!): Order!

  # New orders (for admin)
  newOrder: Order!

  # Product inventory updates
  productInventoryChanged(productId: ID!): Product!

  # Chat messages
  messageReceived(channelId: ID!): Message!
}
```

### Step 5: Implement Resolvers

**Query resolvers:**

```javascript
// Node.js with Apollo Server
const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return dataSources.userAPI.getUser(id);
    },

    products: async (_, { filter, sort, first, after }, { dataSources }) => {
      return dataSources.productAPI.getProducts({
        filter,
        sort,
        first: first || 20,
        after
      });
    },

    me: async (_, __, { user }) => {
      if (!user) throw new AuthenticationError('Not authenticated');
      return user;
    }
  },

  // Field resolvers
  User: {
    orders: async (user, _, { dataSources }) => {
      return dataSources.orderAPI.getOrdersByUser(user.id);
    },

    profile: async (user, _, { dataSources }) => {
      return dataSources.profileAPI.getProfile(user.id);
    }
  },

  Order: {
    items: async (order, _, { dataSources }) => {
      return dataSources.orderAPI.getOrderItems(order.id);
    },

    user: async (order, _, { dataSources }) => {
      return dataSources.userAPI.getUser(order.userId);
    }
  }
};
```

**Mutation resolvers:**

```javascript
const resolvers = {
  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      try {
        const user = await dataSources.userAPI.createUser(input);
        return { user, errors: [] };
      } catch (error) {
        return {
          user: null,
          errors: [{ message: error.message, code: 'CREATE_FAILED' }]
        };
      }
    },

    createOrder: async (_, { input }, { user, dataSources }) => {
      if (!user) {
        return {
          order: null,
          errors: [{ message: 'Not authenticated', code: 'UNAUTHENTICATED' }]
        };
      }

      const order = await dataSources.orderAPI.createOrder({
        ...input,
        userId: user.id
      });

      return { order, errors: [] };
    }
  }
};
```

### Step 6: Prevent N+1 Problem with DataLoader

The N+1 problem: When fetching a list of users with their orders, you make 1 query for users + N queries for orders.

**Solution: DataLoader**

```javascript
const DataLoader = require('dataloader');

// Create loaders
const createLoaders = () => ({
  userLoader: new DataLoader(async (userIds) => {
    const users = await User.find({ _id: { $in: userIds } });
    const userMap = new Map(users.map(u => [u.id.toString(), u]));
    return userIds.map(id => userMap.get(id.toString()));
  }),

  ordersByUserLoader: new DataLoader(async (userIds) => {
    const orders = await Order.find({ userId: { $in: userIds } });
    const orderMap = new Map();
    orders.forEach(order => {
      if (!orderMap.has(order.userId.toString())) {
        orderMap.set(order.userId.toString(), []);
      }
      orderMap.get(order.userId.toString()).push(order);
    });
    return userIds.map(id => orderMap.get(id.toString()) || []);
  })
});

// Use in resolvers
const resolvers = {
  Order: {
    user: (order, _, { loaders }) => {
      return loaders.userLoader.load(order.userId);
    }
  },

  User: {
    orders: (user, _, { loaders }) => {
      return loaders.ordersByUserLoader.load(user.id);
    }
  }
};

// Add loaders to context
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    user: getUser(req),
    loaders: createLoaders()
  })
});
```

### Step 7: Implement Pagination

**Cursor-based pagination (recommended):**

```graphql
type ProductConnection {
  edges: [ProductEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type ProductEdge {
  node: Product!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

**Implementation:**

```javascript
const resolvers = {
  Query: {
    products: async (_, { first = 20, after, filter }) => {
      let query = Product.find(buildFilter(filter));

      if (after) {
        const cursor = decodeCursor(after);
        query = query.where('_id').gt(cursor);
      }

      const products = await query.limit(first + 1).exec();
      const hasNextPage = products.length > first;

      if (hasNextPage) products.pop();

      return {
        edges: products.map(product => ({
          node: product,
          cursor: encodeCursor(product.id)
        })),
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: products[0] ? encodeCursor(products[0].id) : null,
          endCursor: products.length
            ? encodeCursor(products[products.length - 1].id)
            : null
        },
        totalCount: await Product.countDocuments(buildFilter(filter))
      };
    }
  }
};

function encodeCursor(id) {
  return Buffer.from(id.toString()).toString('base64');
}

function decodeCursor(cursor) {
  return Buffer.from(cursor, 'base64').toString('utf8');
}
```

---

## Templates

### Schema Design Checklist

```markdown
## GraphQL Schema Review

### Types
- [ ] All types have ID field
- [ ] Required fields marked with !
- [ ] Relationships defined correctly
- [ ] Enums for fixed value sets

### Queries
- [ ] Single resource queries (user, product)
- [ ] Collection queries with filters
- [ ] Pagination implemented
- [ ] Auth-required queries protected

### Mutations
- [ ] Input types for complex inputs
- [ ] Payload types with errors
- [ ] Validation in resolvers

### Performance
- [ ] DataLoaders for N+1 prevention
- [ ] Query complexity limits
- [ ] Depth limiting
```

### Apollo Server Setup Template

```javascript
// server.js
const { ApolloServer } = require('@apollo/server');
const { expressMiddleware } = require('@apollo/server/express4');
const express = require('express');
const cors = require('cors');
const { typeDefs } = require('./schema');
const { resolvers } = require('./resolvers');
const { createLoaders } = require('./loaders');
const { getUser } = require('./auth');

async function startServer() {
  const app = express();

  const server = new ApolloServer({
    typeDefs,
    resolvers,
    plugins: [
      // Logging plugin
      {
        requestDidStart: async () => ({
          didEncounterErrors: async ({ errors }) => {
            console.error('GraphQL Errors:', errors);
          }
        })
      }
    ]
  });

  await server.start();

  app.use(
    '/graphql',
    cors(),
    express.json(),
    expressMiddleware(server, {
      context: async ({ req }) => ({
        user: await getUser(req),
        loaders: createLoaders()
      })
    })
  );

  app.listen(4000, () => {
    console.log('GraphQL server ready at http://localhost:4000/graphql');
  });
}

startServer();
```

---

## Examples

### E-commerce GraphQL API

```graphql
# Query: Get product with reviews
query GetProduct($id: ID!) {
  product(id: $id) {
    id
    name
    price
    description
    inStock
    category {
      id
      name
    }
    reviews(first: 5) {
      edges {
        node {
          id
          rating
          comment
          author {
            name
          }
        }
      }
      pageInfo {
        hasNextPage
      }
    }
  }
}

# Query: Search products
query SearchProducts($search: String!, $category: ID, $first: Int) {
  products(
    filter: { search: $search, category: $category, inStock: true }
    sort: { field: RELEVANCE, direction: DESC }
    first: $first
  ) {
    edges {
      node {
        id
        name
        price
        thumbnail
      }
    }
    totalCount
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}

# Mutation: Add to cart
mutation AddToCart($input: AddToCartInput!) {
  addToCart(input: $input) {
    cart {
      id
      items {
        product {
          name
          price
        }
        quantity
      }
      subtotal
    }
    errors {
      field
      message
    }
  }
}

# Subscription: Order updates
subscription OrderUpdates($orderId: ID!) {
  orderStatusChanged(orderId: $orderId) {
    id
    status
    updatedAt
    trackingNumber
  }
}
```

### Python Implementation (Strawberry)

```python
# schema.py
import strawberry
from typing import List, Optional
from strawberry.types import Info

@strawberry.type
class User:
    id: strawberry.ID
    email: str
    name: Optional[str]

    @strawberry.field
    async def orders(self, info: Info) -> List["Order"]:
        return await info.context.loaders.orders_by_user.load(self.id)

@strawberry.type
class Order:
    id: strawberry.ID
    status: str
    total: float

@strawberry.input
class CreateUserInput:
    email: str
    name: str
    password: str

@strawberry.type
class CreateUserPayload:
    user: Optional[User]
    errors: List[str]

@strawberry.type
class Query:
    @strawberry.field
    async def user(self, id: strawberry.ID, info: Info) -> Optional[User]:
        return await info.context.user_service.get_user(id)

    @strawberry.field
    async def me(self, info: Info) -> Optional[User]:
        return info.context.current_user

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self,
        input: CreateUserInput,
        info: Info
    ) -> CreateUserPayload:
        try:
            user = await info.context.user_service.create_user(input)
            return CreateUserPayload(user=user, errors=[])
        except Exception as e:
            return CreateUserPayload(user=None, errors=[str(e)])

schema = strawberry.Schema(query=Query, mutation=Mutation)
```

---

## Common Mistakes

1. **Not using DataLoader**
   - Causes N+1 queries
   - Performance degrades with nested queries

2. **Exposing database structure**
   - Schema should reflect business domain
   - Not database tables

3. **No error handling in mutations**
   - Always return errors in payload
   - Don't rely on exceptions only

4. **Unlimited query depth**
   - Allows malicious deep queries
   - Use depth limiting middleware

5. **Missing pagination**
   - Collections without limits
   - Can overwhelm server

---

## Next Steps

1. **Design schema first** - Define types before implementing
2. **Set up DataLoaders** - Critical for performance
3. **Add query complexity limits** - Prevent abuse
4. **Implement subscriptions** - For real-time features
5. **Document with GraphQL Playground** - Built-in exploration

---

## Related Methodologies

- [M-API-001: REST API Design](./M-API-001_rest_api_design.md)
- [M-API-005: API Authentication](./M-API-005_api_authentication.md)
- [M-API-009: API Testing](./M-API-009_api_testing.md)

---

*Methodology: GraphQL Patterns*
*Version: 1.0*
*Agent: faion-api-agent*
