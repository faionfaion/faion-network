# REST API Design Examples

Real-world examples of REST API design patterns.

## Example 1: E-commerce Products API

### Resource Structure

```
/products                     # All products
/products/{id}                # Single product
/products/{id}/reviews        # Product reviews
/products/{id}/images         # Product images
/categories                   # All categories
/categories/{id}/products     # Products in category
```

### Endpoints

```http
# List products with filtering
GET /products?category=electronics&minPrice=100&maxPrice=500&sort=-rating&page=1&limit=20

# Response
{
  "data": [
    {
      "id": "prod_123",
      "name": "Wireless Headphones",
      "price": 149.99,
      "currency": "USD",
      "category": "electronics",
      "rating": 4.5,
      "reviewCount": 234,
      "inStock": true,
      "images": [
        {"url": "https://...", "alt": "Front view"}
      ]
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 156,
    "totalPages": 8
  }
}
```

```http
# Create product
POST /products
Content-Type: application/json

{
  "name": "New Product",
  "description": "Product description",
  "price": 99.99,
  "categoryId": "cat_456",
  "sku": "PROD-001"
}

# Response 201 Created
Location: /products/prod_789

{
  "id": "prod_789",
  "name": "New Product",
  ...
}
```

---

## Example 2: User Management API

### Authentication Flow

```http
# Login
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure123"
}

# Response
{
  "accessToken": "eyJhbG...",
  "refreshToken": "dGhpcy...",
  "expiresIn": 3600,
  "tokenType": "Bearer"
}
```

```http
# Refresh token
POST /auth/refresh
Content-Type: application/json

{
  "refreshToken": "dGhpcy..."
}
```

### User Profile

```http
# Get current user
GET /users/me
Authorization: Bearer eyJhbG...

# Response
{
  "id": "usr_123",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": "https://...",
  "role": "user",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

```http
# Update profile
PATCH /users/me
Authorization: Bearer eyJhbG...
Content-Type: application/json

{
  "name": "John Updated"
}
```

---

## Example 3: Order Management API

### Order Lifecycle

```http
# Create order
POST /orders
Content-Type: application/json

{
  "items": [
    {"productId": "prod_123", "quantity": 2},
    {"productId": "prod_456", "quantity": 1}
  ],
  "shippingAddress": {
    "street": "123 Main St",
    "city": "New York",
    "country": "US",
    "postalCode": "10001"
  }
}

# Response 201 Created
{
  "id": "ord_789",
  "status": "pending",
  "items": [...],
  "subtotal": 299.97,
  "shipping": 9.99,
  "tax": 26.00,
  "total": 335.96,
  "createdAt": "2024-01-20T14:00:00Z"
}
```

```http
# Get order status
GET /orders/ord_789

# Response
{
  "id": "ord_789",
  "status": "shipped",
  "tracking": {
    "carrier": "UPS",
    "number": "1Z999AA10123456784",
    "url": "https://..."
  },
  "estimatedDelivery": "2024-01-25"
}
```

```http
# Cancel order (action endpoint)
POST /orders/ord_789/cancel
Content-Type: application/json

{
  "reason": "Changed my mind"
}

# Response 200 OK
{
  "id": "ord_789",
  "status": "cancelled",
  "cancelledAt": "2024-01-20T15:00:00Z"
}
```

---

## Example 4: Search API

### Full-text Search

```http
# Search products
GET /search?q=wireless+headphones&type=products&page=1&limit=20

# Response
{
  "data": [
    {
      "type": "product",
      "id": "prod_123",
      "name": "Wireless Headphones Pro",
      "highlight": {
        "name": ["<em>Wireless</em> <em>Headphones</em> Pro"]
      },
      "score": 0.95
    }
  ],
  "meta": {
    "query": "wireless headphones",
    "took": 45,
    "total": 23
  }
}
```

### Autocomplete

```http
# Autocomplete suggestions
GET /search/suggest?q=wire&limit=5

# Response
{
  "suggestions": [
    {"text": "wireless headphones", "count": 156},
    {"text": "wireless mouse", "count": 89},
    {"text": "wireless keyboard", "count": 67}
  ]
}
```

---

## Example 5: Bulk Operations

### Batch Create

```http
# Bulk create products
POST /products/batch
Content-Type: application/json

{
  "items": [
    {"name": "Product 1", "price": 10.00},
    {"name": "Product 2", "price": 20.00}
  ]
}

# Response 207 Multi-Status
{
  "results": [
    {"status": 201, "id": "prod_001"},
    {"status": 422, "error": {"field": "price", "message": "Required"}}
  ],
  "summary": {
    "total": 2,
    "succeeded": 1,
    "failed": 1
  }
}
```

### Batch Update

```http
# Bulk update prices
PATCH /products/batch
Content-Type: application/json

{
  "updates": [
    {"id": "prod_001", "price": 15.00},
    {"id": "prod_002", "price": 25.00}
  ]
}
```

---

## Example 6: Error Responses

### Validation Error

```http
POST /users
Content-Type: application/json

{
  "email": "invalid-email",
  "name": ""
}

# Response 422 Unprocessable Entity
{
  "code": "VALIDATION_ERROR",
  "message": "Request validation failed",
  "requestId": "req_abc123",
  "errors": [
    {"field": "email", "message": "Invalid email format"},
    {"field": "name", "message": "Name is required"}
  ]
}
```

### Not Found

```http
GET /users/usr_nonexistent

# Response 404 Not Found
{
  "code": "USER_NOT_FOUND",
  "message": "User with ID 'usr_nonexistent' does not exist",
  "requestId": "req_def456"
}
```

### Rate Limited

```http
GET /products

# Response 429 Too Many Requests
# Headers:
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 0
# X-RateLimit-Reset: 1706187600
# Retry-After: 60

{
  "code": "RATE_LIMITED",
  "message": "Too many requests. Please retry after 60 seconds.",
  "requestId": "req_ghi789"
}
```

---

*REST API Design Examples v1.0*
