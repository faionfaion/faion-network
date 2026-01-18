# M-API-004: OpenAPI Specification

## Metadata
- **ID:** M-API-004
- **Category:** API
- **Difficulty:** Intermediate
- **Tags:** [api, openapi, swagger, documentation]
- **Agent:** faion-api-agent

---

## Problem

Without a formal API specification:
- Documentation goes out of sync with implementation
- No single source of truth for API contracts
- Manual testing and validation
- Difficult to generate client SDKs
- Inconsistent error handling

OpenAPI (formerly Swagger) provides a standard way to describe REST APIs.

---

## Framework

### Step 1: Understand OpenAPI Structure

```yaml
# openapi.yaml
openapi: 3.1.0

info:
  title: My API
  version: 1.0.0
  description: API description

servers:
  - url: https://api.example.com/v1
    description: Production

paths:
  /users:
    get:
      # Endpoint definition
    post:
      # Endpoint definition

components:
  schemas:
    # Reusable data models
  securitySchemes:
    # Authentication definitions
  responses:
    # Reusable responses

security:
  - bearerAuth: []
```

### Step 2: Define Info and Servers

```yaml
openapi: 3.1.0

info:
  title: E-commerce API
  version: 2.0.0
  description: |
    API for managing products, orders, and users.

    ## Authentication
    All endpoints require Bearer token authentication.

    ## Rate Limiting
    - 100 requests per minute for authenticated users
    - 20 requests per minute for anonymous users
  contact:
    name: API Support
    email: api@example.com
    url: https://docs.example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v2
    description: Production
  - url: https://staging-api.example.com/v2
    description: Staging
  - url: http://localhost:3000/v2
    description: Development

externalDocs:
  description: Full documentation
  url: https://docs.example.com
```

### Step 3: Define Paths (Endpoints)

```yaml
paths:
  /users:
    get:
      operationId: listUsers
      summary: List all users
      description: Returns a paginated list of users
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: status
          in: query
          schema:
            type: string
            enum: [active, inactive, pending]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      operationId: createUser
      summary: Create a new user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
            example:
              email: john@example.com
              name: John Doe
              password: securePassword123
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: Email already exists

  /users/{userId}:
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid
        description: User ID

    get:
      operationId: getUser
      summary: Get user by ID
      tags:
        - Users
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

    patch:
      operationId: updateUser
      summary: Update user
      tags:
        - Users
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserInput'
      responses:
        '200':
          description: User updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

    delete:
      operationId: deleteUser
      summary: Delete user
      tags:
        - Users
      responses:
        '204':
          description: User deleted
        '404':
          $ref: '#/components/responses/NotFound'
```

### Step 4: Define Components (Schemas)

```yaml
components:
  schemas:
    # Base User schema
    User:
      type: object
      required:
        - id
        - email
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
          maxLength: 100
        status:
          type: string
          enum: [active, inactive, pending]
          default: pending
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: string
          format: date-time
          readOnly: true

    # Input schemas
    CreateUserInput:
      type: object
      required:
        - email
        - password
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100
        password:
          type: string
          minLength: 8
          format: password

    UpdateUserInput:
      type: object
      properties:
        name:
          type: string
          maxLength: 100
        status:
          type: string
          enum: [active, inactive]

    # List response
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        meta:
          $ref: '#/components/schemas/PaginationMeta'
        links:
          $ref: '#/components/schemas/PaginationLinks'

    # Pagination
    PaginationMeta:
      type: object
      properties:
        currentPage:
          type: integer
        perPage:
          type: integer
        totalItems:
          type: integer
        totalPages:
          type: integer

    PaginationLinks:
      type: object
      properties:
        first:
          type: string
          format: uri
        prev:
          type: string
          format: uri
          nullable: true
        next:
          type: string
          format: uri
          nullable: true
        last:
          type: string
          format: uri

    # Error schema
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          example: VALIDATION_ERROR
        message:
          type: string
          example: Invalid input data
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
```

### Step 5: Define Security Schemes

```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token from /auth/login

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for server-to-server

    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          scopes:
            read:users: Read user data
            write:users: Modify user data
            admin: Full access

# Apply globally
security:
  - bearerAuth: []

# Or per-endpoint
paths:
  /public/products:
    get:
      security: []  # No auth required
      # ...

  /admin/users:
    get:
      security:
        - bearerAuth: []
        - oauth2: [admin]
```

### Step 6: Define Reusable Responses

```yaml
components:
  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VALIDATION_ERROR
            message: Invalid input data
            details:
              - field: email
                message: Must be a valid email

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Authentication required

    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: FORBIDDEN
            message: Insufficient permissions

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: Resource not found

    TooManyRequests:
      description: Rate limit exceeded
      headers:
        X-RateLimit-Limit:
          schema:
            type: integer
        X-RateLimit-Remaining:
          schema:
            type: integer
        X-RateLimit-Reset:
          schema:
            type: integer
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: RATE_LIMIT_EXCEEDED
            message: Too many requests
```

### Step 7: Add Examples

```yaml
paths:
  /orders:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderInput'
            examples:
              simpleOrder:
                summary: Simple order
                value:
                  items:
                    - productId: "prod_123"
                      quantity: 2
                  shippingAddressId: "addr_456"

              complexOrder:
                summary: Order with discount
                value:
                  items:
                    - productId: "prod_123"
                      quantity: 2
                    - productId: "prod_456"
                      quantity: 1
                  shippingAddressId: "addr_456"
                  discountCode: "SAVE10"
                  giftWrap: true
                  giftMessage: "Happy Birthday!"
```

---

## Templates

### Complete OpenAPI Template

```yaml
openapi: 3.1.0

info:
  title: {API Name}
  version: 1.0.0
  description: |
    {API description}

    ## Authentication
    {Auth description}

servers:
  - url: https://api.example.com/v1
    description: Production

tags:
  - name: {Resource}
    description: {Resource description}

paths:
  /{resources}:
    get:
      operationId: list{Resources}
      summary: List {resources}
      tags: [{Resource}]
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/PerPageParam'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{Resource}List'
    post:
      operationId: create{Resource}
      summary: Create {resource}
      tags: [{Resource}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create{Resource}Input'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{Resource}'

  /{resources}/{id}:
    parameters:
      - $ref: '#/components/parameters/{Resource}IdParam'
    get:
      operationId: get{Resource}
      summary: Get {resource}
      tags: [{Resource}]
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{Resource}'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        default: 1
    PerPageParam:
      name: per_page
      in: query
      schema:
        type: integer
        default: 20
    {Resource}IdParam:
      name: id
      in: path
      required: true
      schema:
        type: string

  schemas:
    {Resource}:
      type: object
      properties:
        id:
          type: string
        # Add fields

  responses:
    NotFound:
      description: Not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer

security:
  - bearerAuth: []
```

---

## Examples

### Django REST Framework with drf-spectacular

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
    'TITLE': 'E-commerce API',
    'DESCRIPTION': 'API for products and orders',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}

# urls.py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]

# views.py
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ProductViewSet(viewsets.ModelViewSet):
    @extend_schema(
        summary="List products",
        parameters=[
            OpenApiParameter("category", str, description="Filter by category"),
            OpenApiParameter("min_price", float, description="Minimum price"),
        ],
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request):
        ...

    @extend_schema(
        summary="Create product",
        request=CreateProductSerializer,
        responses={201: ProductSerializer}
    )
    def create(self, request):
        ...
```

### Express.js with swagger-jsdoc

```javascript
// swagger.js
const swaggerJSDoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.1.0',
    info: {
      title: 'E-commerce API',
      version: '1.0.0',
    },
    servers: [
      { url: 'http://localhost:3000/api' }
    ],
  },
  apis: ['./routes/*.js'],
};

const spec = swaggerJSDoc(options);
module.exports = spec;

// routes/products.js
/**
 * @openapi
 * /products:
 *   get:
 *     summary: List products
 *     tags: [Products]
 *     parameters:
 *       - name: category
 *         in: query
 *         schema:
 *           type: string
 *     responses:
 *       200:
 *         description: Product list
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Product'
 */
router.get('/', async (req, res) => {
  // ...
});

/**
 * @openapi
 * components:
 *   schemas:
 *     Product:
 *       type: object
 *       properties:
 *         id:
 *           type: string
 *         name:
 *           type: string
 *         price:
 *           type: number
 */

// app.js
const swaggerUi = require('swagger-ui-express');
const spec = require('./swagger');

app.use('/docs', swaggerUi.serve, swaggerUi.setup(spec));
```

---

## Common Mistakes

1. **Not using $ref**
   - Duplicated schemas
   - Use references for reusability

2. **Missing examples**
   - Hard to understand without examples
   - Add examples for all endpoints

3. **Incomplete error responses**
   - Only documenting 200
   - Document all possible errors

4. **No operationId**
   - Needed for code generation
   - Use unique, descriptive IDs

5. **Spec not in sync**
   - Generated vs written
   - Use validation in CI

---

## Next Steps

1. **Write spec first** - Contract-first development
2. **Set up Swagger UI** - For interactive docs
3. **Add to CI** - Validate spec on each commit
4. **Generate SDKs** - Use openapi-generator
5. **Monitor changes** - Detect breaking changes

---

## Related Methodologies

- [M-API-001: REST API Design](./M-API-001_rest_api_design.md)
- [M-API-008: API Documentation](./M-API-008_api_documentation.md)
- [M-API-012: Contract-First Development](./M-API-012_contract_first_development.md)

---

*Methodology: OpenAPI Specification*
*Version: 1.0*
*Agent: faion-api-agent*
