# M-API-008: API Documentation

## Metadata
- **ID:** M-API-008
- **Category:** API
- **Difficulty:** Beginner
- **Tags:** [api, documentation, swagger, redoc]
- **Agent:** faion-api-agent

---

## Problem

Without good documentation:
- Developers can't figure out how to use your API
- Support requests increase dramatically
- Integration time grows from hours to days
- Errors multiply due to misunderstanding
- API adoption suffers

---

## Framework

### Step 1: Choose Documentation Tools

| Tool | Type | Best For |
|------|------|----------|
| Swagger UI | Interactive | Testing endpoints directly |
| ReDoc | Reference | Clean, readable docs |
| Stoplight | Full suite | Enterprise teams |
| Postman | Collections | Testing + docs |
| ReadMe | Hosted | Developer portals |

### Step 2: Write OpenAPI Spec First

```yaml
# openapi.yaml
openapi: 3.1.0
info:
  title: My API
  version: 1.0.0
  description: |
    Welcome to the API documentation.

    ## Getting Started
    1. Create an account at dashboard.example.com
    2. Generate an API key
    3. Include the key in your requests

    ## Authentication
    All endpoints require Bearer token authentication:
    \`\`\`
    Authorization: Bearer YOUR_TOKEN
    \`\`\`

    ## Rate Limits
    - Free tier: 100 requests/minute
    - Pro tier: 1000 requests/minute

  contact:
    name: API Support
    email: api-support@example.com
    url: https://support.example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://sandbox.api.example.com/v1
    description: Sandbox (test data)

tags:
  - name: Users
    description: User management endpoints
  - name: Orders
    description: Order processing
```

### Step 3: Document Each Endpoint Thoroughly

```yaml
paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      description: |
        Returns a paginated list of users.

        **Permissions required:** `users:read`

        **Use cases:**
        - Admin dashboard user list
        - User search functionality

      tags:
        - Users

      parameters:
        - name: page
          in: query
          description: Page number (starts at 1)
          schema:
            type: integer
            default: 1
            minimum: 1
          example: 1

        - name: per_page
          in: query
          description: Items per page (max 100)
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
          example: 20

        - name: status
          in: query
          description: Filter by user status
          schema:
            type: string
            enum: [active, inactive, pending]
          example: active

        - name: search
          in: query
          description: Search by name or email (min 3 characters)
          schema:
            type: string
            minLength: 3
          example: john

      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              examples:
                withUsers:
                  summary: Users found
                  value:
                    data:
                      - id: "usr_123"
                        email: "john@example.com"
                        name: "John Doe"
                        status: "active"
                    meta:
                      total: 150
                      page: 1
                      per_page: 20
                emptyResult:
                  summary: No users found
                  value:
                    data: []
                    meta:
                      total: 0
                      page: 1
                      per_page: 20

        '401':
          $ref: '#/components/responses/Unauthorized'

        '403':
          description: Insufficient permissions
          content:
            application/json:
              example:
                error:
                  code: FORBIDDEN
                  message: "Requires 'users:read' permission"
```

### Step 4: Add Request/Response Examples

```yaml
paths:
  /users:
    post:
      operationId: createUser
      summary: Create a new user
      description: |
        Creates a new user account.

        **Permissions required:** `users:write`

        **Notes:**
        - Email must be unique
        - Password must meet strength requirements
        - A confirmation email will be sent

      tags:
        - Users

      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
            examples:
              basicUser:
                summary: Basic user creation
                description: Minimal required fields
                value:
                  email: "john@example.com"
                  password: "SecurePass123!"

              fullUser:
                summary: User with all fields
                description: All optional fields included
                value:
                  email: "john@example.com"
                  password: "SecurePass123!"
                  name: "John Doe"
                  phone: "+1234567890"
                  preferences:
                    newsletter: true
                    language: "en"

      responses:
        '201':
          description: User created successfully
          headers:
            Location:
              description: URL of the created user
              schema:
                type: string
                example: /users/usr_abc123
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
              example:
                data:
                  id: "usr_abc123"
                  email: "john@example.com"
                  name: "John Doe"
                  status: "pending"
                  createdAt: "2024-01-15T10:30:00Z"

        '409':
          description: Email already exists
          content:
            application/json:
              example:
                error:
                  code: CONFLICT
                  message: "User with email 'john@example.com' already exists"

        '422':
          description: Validation failed
          content:
            application/json:
              example:
                error:
                  code: VALIDATION_ERROR
                  message: "The request contains invalid data"
                  details:
                    - field: email
                      message: "Must be a valid email address"
                    - field: password
                      message: "Must be at least 8 characters"
```

### Step 5: Set Up Swagger UI

**Express.js:**

```javascript
// swagger.js
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');

const options = {
  definition: {
    openapi: '3.1.0',
    info: {
      title: 'My API',
      version: '1.0.0',
      description: 'API documentation'
    },
    servers: [
      { url: 'http://localhost:3000/api', description: 'Development' },
      { url: 'https://api.example.com', description: 'Production' }
    ]
  },
  apis: ['./routes/*.js', './docs/*.yaml']
};

const spec = swaggerJsdoc(options);

module.exports = { spec, swaggerUi };

// app.js
const { spec, swaggerUi } = require('./swagger');

app.use('/docs', swaggerUi.serve, swaggerUi.setup(spec, {
  customCss: '.swagger-ui .topbar { display: none }',
  customSiteTitle: 'My API Docs'
}));

// Serve raw spec
app.get('/docs/openapi.json', (req, res) => {
  res.json(spec);
});
```

**Django:**

```python
# settings.py
INSTALLED_APPS = [
    ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My API',
    'DESCRIPTION': 'API documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
    },
}

# urls.py
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

### Step 6: Set Up ReDoc

**Standalone HTML:**

```html
<!DOCTYPE html>
<html>
<head>
  <title>API Documentation</title>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700" rel="stylesheet">
  <style>
    body { margin: 0; padding: 0; }
  </style>
</head>
<body>
  <redoc spec-url='/api/openapi.json'></redoc>
  <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
```

**Express.js:**

```javascript
const redoc = require('redoc-express');

app.get('/docs/redoc', redoc({
  title: 'API Docs',
  specUrl: '/docs/openapi.json',
  nonce: '',
  redocOptions: {
    theme: {
      colors: { primary: { main: '#dd5522' } }
    }
  }
}));
```

### Step 7: Write Getting Started Guide

```markdown
# Getting Started

## 1. Create an Account

Sign up at [dashboard.example.com](https://dashboard.example.com).

## 2. Get Your API Key

1. Go to Settings > API Keys
2. Click "Create New Key"
3. Copy your key (you won't see it again!)

## 3. Make Your First Request

\`\`\`bash
curl -X GET "https://api.example.com/v1/users/me" \
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

**Response:**
\`\`\`json
{
  "data": {
    "id": "usr_123",
    "email": "you@example.com",
    "name": "Your Name"
  }
}
\`\`\`

## 4. Try Creating a Resource

\`\`\`bash
curl -X POST "https://api.example.com/v1/products" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Product",
    "price": 29.99
  }'
\`\`\`

## Next Steps

- [Authentication Guide](/docs/authentication)
- [Error Handling](/docs/errors)
- [Rate Limits](/docs/rate-limits)
- [API Reference](/docs/reference)
```

### Step 8: Document Authentication

```markdown
# Authentication

## Overview

All API requests require authentication using a Bearer token.

## Getting a Token

### Option 1: API Key (Server-to-Server)

Use for backend integrations:

\`\`\`bash
curl -X GET "https://api.example.com/v1/users" \
  -H "Authorization: Bearer sk_live_xxxxx"
\`\`\`

### Option 2: JWT (User Authentication)

1. **Login to get tokens:**

\`\`\`bash
curl -X POST "https://api.example.com/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'
\`\`\`

Response:
\`\`\`json
{
  "accessToken": "eyJhbG...",
  "refreshToken": "eyJhbG...",
  "expiresIn": 900
}
\`\`\`

2. **Use the access token:**

\`\`\`bash
curl -X GET "https://api.example.com/v1/users/me" \
  -H "Authorization: Bearer eyJhbG..."
\`\`\`

3. **Refresh when expired:**

\`\`\`bash
curl -X POST "https://api.example.com/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refreshToken": "eyJhbG..."}'
\`\`\`

## Token Scopes

| Scope | Description |
|-------|-------------|
| \`users:read\` | Read user data |
| \`users:write\` | Create/update users |
| \`orders:read\` | Read orders |
| \`orders:write\` | Create/update orders |
| \`admin\` | Full access |

## Security Best Practices

- Never expose API keys in client-side code
- Rotate keys regularly
- Use environment variables
- Implement token refresh for user sessions
```

---

## Templates

### Documentation Structure

```
docs/
├── index.md                    # Overview, getting started
├── authentication.md           # Auth guide
├── errors.md                   # Error codes reference
├── rate-limits.md              # Rate limiting info
├── changelog.md                # API version history
├── sdks.md                     # SDK downloads
│
├── guides/
│   ├── quickstart.md          # 5-minute tutorial
│   ├── pagination.md          # Pagination patterns
│   ├── webhooks.md            # Webhook integration
│   └── best-practices.md      # Usage recommendations
│
├── api-reference/
│   ├── users.md               # Users endpoints
│   ├── orders.md              # Orders endpoints
│   └── products.md            # Products endpoints
│
└── openapi.yaml               # OpenAPI spec
```

### Endpoint Documentation Template

```markdown
## {HTTP Method} {Endpoint}

{Short description}

### Overview

{Longer description with use cases}

### Authentication

{Required scopes or permissions}

### Request

#### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource ID |

#### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |

#### Request Body

\`\`\`json
{
  "field": "value"
}
\`\`\`

### Response

#### Success (200)

\`\`\`json
{
  "data": { ... }
}
\`\`\`

#### Errors

| Code | Description |
|------|-------------|
| 404 | Resource not found |
| 422 | Validation error |

### Examples

#### cURL

\`\`\`bash
curl -X GET "https://api.example.com/v1/resource"
\`\`\`

#### Python

\`\`\`python
import requests
response = requests.get("https://api.example.com/v1/resource")
\`\`\`

#### JavaScript

\`\`\`javascript
const response = await fetch("https://api.example.com/v1/resource");
\`\`\`
```

---

## Examples

### Complete API Documentation Page

```markdown
# Users API

Manage user accounts and profiles.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | List all users |
| POST | /users | Create a user |
| GET | /users/{id} | Get a user |
| PATCH | /users/{id} | Update a user |
| DELETE | /users/{id} | Delete a user |

---

## List Users

\`GET /users\`

Returns a paginated list of users.

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| page | query | integer | No | Page number (default: 1) |
| per_page | query | integer | No | Items per page (default: 20, max: 100) |
| status | query | string | No | Filter by status: active, inactive, pending |

### Response

\`\`\`json
{
  "data": [
    {
      "id": "usr_123",
      "email": "john@example.com",
      "name": "John Doe",
      "status": "active",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "perPage": 20,
    "totalPages": 8
  }
}
\`\`\`

### Example

\`\`\`bash
curl "https://api.example.com/v1/users?status=active&page=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
\`\`\`

---

## Create User

\`POST /users\`

Creates a new user account.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address |
| password | string | Yes | Password (min 8 chars) |
| name | string | No | User's display name |

\`\`\`json
{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}
\`\`\`

### Response

**201 Created**

\`\`\`json
{
  "data": {
    "id": "usr_abc123",
    "email": "john@example.com",
    "name": "John Doe",
    "status": "pending",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
\`\`\`

**409 Conflict** (Email exists)

\`\`\`json
{
  "error": {
    "code": "CONFLICT",
    "message": "User with email 'john@example.com' already exists"
  }
}
\`\`\`
```

---

## Common Mistakes

1. **No examples**
   - Developers need to see real requests/responses
   - Include multiple examples per endpoint

2. **Outdated documentation**
   - Spec doesn't match implementation
   - Generate from code or validate in CI

3. **Missing error documentation**
   - Only happy path documented
   - Document all possible errors

4. **No getting started guide**
   - Reference docs only
   - Include quickstart tutorial

5. **Technical jargon without explanation**
   - Assumes knowledge
   - Define terms, link to guides

---

## Next Steps

1. **Write OpenAPI spec** - Source of truth
2. **Set up Swagger UI** - Interactive testing
3. **Add ReDoc** - Clean reference docs
4. **Write guides** - Getting started, tutorials
5. **Automate** - Generate from code, validate in CI

---

## Related Methodologies

- [M-API-004: OpenAPI Specification](./M-API-004_openapi_specification.md)
- [M-API-007: Error Handling](./M-API-007_error_handling.md)
- [M-API-012: Contract-First Development](./M-API-012_contract_first_development.md)

---

*Methodology: API Documentation*
*Version: 1.0*
*Agent: faion-api-agent*
