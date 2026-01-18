# M-API-001: REST API Design

## Metadata
- **ID:** M-API-001
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, rest, http, backend]
- **Agent:** faion-api-agent

---

## Problem

You need to design an API that is intuitive, predictable, and follows industry standards. Poor API design leads to:
- Confusing endpoints that developers struggle to use
- Inconsistent behavior across different resources
- Documentation that never matches reality
- Breaking changes that frustrate API consumers

---

## Framework

### Step 1: Define Resources

Resources are nouns, not verbs. Think of them as entities in your system.

**Good resources:**
```
/users
/orders
/products
/invoices
```

**Bad resources (verb-based):**
```
/getUsers        # Don't use verbs
/createOrder     # HTTP method defines action
/fetchProducts   # REST uses nouns
```

### Step 2: Use HTTP Methods Correctly

| Method | Purpose | Idempotent | Safe |
|--------|---------|------------|------|
| GET | Read resource(s) | Yes | Yes |
| POST | Create resource | No | No |
| PUT | Replace resource | Yes | No |
| PATCH | Update resource partially | No | No |
| DELETE | Remove resource | Yes | No |

**Example operations:**

```http
# List all users
GET /users

# Get specific user
GET /users/123

# Create new user
POST /users
Content-Type: application/json
{"name": "John", "email": "john@example.com"}

# Replace user completely
PUT /users/123
Content-Type: application/json
{"name": "John Doe", "email": "john.doe@example.com"}

# Update user partially
PATCH /users/123
Content-Type: application/json
{"email": "new.email@example.com"}

# Delete user
DELETE /users/123
```

### Step 3: Design URL Structure

**Hierarchy pattern:**
```
/users/{userId}/orders/{orderId}/items/{itemId}
```

**Rules:**
1. Use lowercase letters
2. Use hyphens for multi-word resources: `/user-profiles`
3. Use plural nouns: `/users` not `/user`
4. Limit nesting to 2-3 levels
5. Avoid query params for required data

**Examples:**

```http
# User's orders
GET /users/123/orders

# Specific order
GET /users/123/orders/456

# Order items
GET /users/123/orders/456/items

# Alternative: flatten deep nesting
GET /orders/456/items
```

### Step 4: Handle Filtering, Sorting, Pagination

**Filtering:**
```http
GET /products?category=electronics&price_min=100&price_max=500
GET /users?status=active&created_after=2024-01-01
```

**Sorting:**
```http
GET /products?sort=price          # Ascending
GET /products?sort=-price         # Descending
GET /products?sort=category,price # Multiple fields
```

**Pagination:**
```http
# Offset-based
GET /users?page=2&per_page=20

# Cursor-based (better for large datasets)
GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
```

**Response with pagination metadata:**
```json
{
  "data": [...],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total_items": 156,
    "total_pages": 8
  },
  "links": {
    "first": "/users?page=1&per_page=20",
    "prev": "/users?page=1&per_page=20",
    "next": "/users?page=3&per_page=20",
    "last": "/users?page=8&per_page=20"
  }
}
```

### Step 5: Use Proper Status Codes

**Success codes:**

| Code | Meaning | When to use |
|------|---------|-------------|
| 200 | OK | GET, PUT, PATCH success |
| 201 | Created | POST success |
| 204 | No Content | DELETE success, no body needed |

**Client error codes:**

| Code | Meaning | When to use |
|------|---------|-------------|
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing/invalid auth |
| 403 | Forbidden | Valid auth, no permission |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, state conflict |
| 422 | Unprocessable Entity | Validation failed |
| 429 | Too Many Requests | Rate limit exceeded |

**Server error codes:**

| Code | Meaning | When to use |
|------|---------|-------------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Upstream service failed |
| 503 | Service Unavailable | Maintenance, overload |

### Step 6: Design Response Format

**Consistent structure:**

```json
{
  "data": {
    "id": "123",
    "type": "user",
    "attributes": {
      "name": "John Doe",
      "email": "john@example.com",
      "created_at": "2024-01-15T10:30:00Z"
    },
    "relationships": {
      "orders": {
        "links": {
          "related": "/users/123/orders"
        }
      }
    }
  },
  "links": {
    "self": "/users/123"
  }
}
```

**Collection response:**

```json
{
  "data": [
    {"id": "1", "type": "user", "attributes": {...}},
    {"id": "2", "type": "user", "attributes": {...}}
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 20
  }
}
```

### Step 7: Implement HATEOAS (Optional)

HATEOAS (Hypermedia as the Engine of Application State) provides navigation links.

```json
{
  "data": {
    "id": "123",
    "status": "pending",
    "total": 99.99
  },
  "links": {
    "self": "/orders/123",
    "cancel": "/orders/123/cancel",
    "pay": "/orders/123/pay",
    "items": "/orders/123/items"
  }
}
```

Benefits:
- API is self-documenting
- Clients discover available actions
- Server controls workflow

---

## Templates

### Resource Design Checklist

```markdown
## Resource: {name}

### Endpoints
- [ ] GET /{resources} - List all
- [ ] GET /{resources}/{id} - Get one
- [ ] POST /{resources} - Create
- [ ] PUT /{resources}/{id} - Replace
- [ ] PATCH /{resources}/{id} - Update
- [ ] DELETE /{resources}/{id} - Delete

### Nested Resources
- [ ] GET /{resources}/{id}/{sub-resources}

### Filters
- [ ] Field 1: ?field1=value
- [ ] Field 2: ?field2=value

### Sorting
- [ ] ?sort=field,-field2

### Pagination
- [ ] ?page=N&per_page=M
```

### API Endpoint Documentation Template

```markdown
## {Method} {Endpoint}

**Description:** {What it does}

**Authentication:** Required/Optional

**Request:**
- Path params: {id}
- Query params: {filters}
- Body: {JSON schema}

**Response:**
- 200: Success
- 400: Bad request
- 404: Not found

**Example:**
\`\`\`http
{HTTP request example}
\`\`\`
```

---

## Examples

### E-commerce API Design

```http
# Products
GET    /products                    # List products
GET    /products/{id}               # Get product
POST   /products                    # Create product (admin)
PATCH  /products/{id}               # Update product
DELETE /products/{id}               # Delete product

# Categories
GET    /categories                  # List categories
GET    /categories/{id}/products    # Products in category

# Cart
GET    /cart                        # Get current cart
POST   /cart/items                  # Add to cart
PATCH  /cart/items/{id}             # Update quantity
DELETE /cart/items/{id}             # Remove from cart

# Orders
GET    /orders                      # User's orders
POST   /orders                      # Create order
GET    /orders/{id}                 # Order details
POST   /orders/{id}/cancel          # Cancel order

# Users
GET    /users/me                    # Current user profile
PATCH  /users/me                    # Update profile
GET    /users/me/addresses          # User addresses
POST   /users/me/addresses          # Add address
```

### Django REST Framework Implementation

```python
# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'status']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Custom filtering
        min_price = self.request.query_params.get('price_min')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        return queryset

    @action(detail=True, methods=['post'])
    def archive(self, request, pk=None):
        product = self.get_object()
        product.status = 'archived'
        product.save()
        return Response({'status': 'archived'})

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = router.urls
```

### Express.js Implementation

```javascript
// routes/products.js
const express = require('express');
const router = express.Router();

// GET /products
router.get('/', async (req, res) => {
  const { page = 1, per_page = 20, sort, category } = req.query;

  const filters = {};
  if (category) filters.category = category;

  const products = await Product.find(filters)
    .sort(parseSort(sort))
    .skip((page - 1) * per_page)
    .limit(per_page);

  const total = await Product.countDocuments(filters);

  res.json({
    data: products,
    meta: {
      page: parseInt(page),
      per_page: parseInt(per_page),
      total,
      total_pages: Math.ceil(total / per_page)
    }
  });
});

// GET /products/:id
router.get('/:id', async (req, res) => {
  const product = await Product.findById(req.params.id);

  if (!product) {
    return res.status(404).json({
      error: {
        code: 'NOT_FOUND',
        message: 'Product not found'
      }
    });
  }

  res.json({ data: product });
});

// POST /products
router.post('/', async (req, res) => {
  const product = new Product(req.body);
  await product.save();

  res.status(201)
    .location(\`/products/\${product.id}\`)
    .json({ data: product });
});

module.exports = router;
```

---

## Common Mistakes

1. **Using verbs in URLs**
   - Wrong: \`POST /createUser\`
   - Right: \`POST /users\`

2. **Inconsistent plurality**
   - Wrong: \`/user/123/order\`
   - Right: \`/users/123/orders\`

3. **Ignoring HTTP semantics**
   - Wrong: \`POST /users/123\` for updates
   - Right: \`PATCH /users/123\` for updates

4. **Overloading query params**
   - Wrong: \`GET /data?action=delete&id=123\`
   - Right: \`DELETE /items/123\`

5. **Deep nesting**
   - Wrong: \`/users/1/orders/2/items/3/reviews/4\`
   - Right: \`/reviews/4\` or \`/items/3/reviews/4\`

---

## Next Steps

1. **Define your resources** - List all entities in your system
2. **Map CRUD operations** - Determine which operations each resource needs
3. **Design URL hierarchy** - Plan nested resources carefully
4. **Document early** - Write OpenAPI spec before coding (see M-API-004)
5. **Implement authentication** - See M-API-005 for auth patterns

---

## Related Methodologies

- [M-API-003: API Versioning](./M-API-003_api_versioning.md)
- [M-API-004: OpenAPI Specification](./M-API-004_openapi_specification.md)
- [M-API-007: Error Handling](./M-API-007_error_handling.md)
- [M-API-012: Contract-First Development](./M-API-012_contract_first_development.md)

---

*Methodology: REST API Design*
*Version: 1.0*
*Agent: faion-api-agent*
