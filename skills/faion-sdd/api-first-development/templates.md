# OpenAPI Templates

Reusable templates for common API patterns. Copy and adapt for your projects.

## Minimal Starter Template

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  version: 1.0.0
  description: |
    [Brief API description]

    ## Authentication
    [Auth method description]

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:3000/v1
    description: Local

security:
  - bearerAuth: []

paths:
  /health:
    get:
      operationId: healthCheck
      summary: Health check endpoint
      security: []
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    const: "ok"

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

## Full Specification Template

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  version: 1.0.0
  description: |
    [Detailed API description]

    ## Authentication
    All endpoints require Bearer token authentication unless marked otherwise.
    Obtain tokens via the `/auth/login` endpoint.

    ## Rate Limiting
    - Standard: 100 requests/minute
    - Premium: 1000 requests/minute

    ## Pagination
    List endpoints support pagination via `page` and `limit` query parameters.

    ## Error Handling
    Errors follow RFC 7807 Problem Details format.
  contact:
    name: API Support
    email: api-support@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
  x-logo:
    url: https://example.com/logo.png

externalDocs:
  description: Full API Documentation
  url: https://docs.example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging
  - url: http://localhost:3000/v1
    description: Local development

tags:
  - name: Resources
    description: Resource management operations
  - name: Authentication
    description: Authentication and authorization

security:
  - bearerAuth: []

paths:
  /resources:
    get:
      operationId: listResources
      summary: List all resources
      description: Retrieve a paginated list of resources with optional filtering.
      tags:
        - Resources
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
        - $ref: '#/components/parameters/SortParam'
        - $ref: '#/components/parameters/FilterParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

    post:
      operationId: createResource
      summary: Create a new resource
      description: Create a new resource with the provided data.
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateResourceRequest'
      responses:
        '201':
          description: Resource created successfully
          headers:
            Location:
              description: URL of the created resource
              schema:
                type: string
                format: uri
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'
        '500':
          $ref: '#/components/responses/InternalError'

  /resources/{resourceId}:
    parameters:
      - $ref: '#/components/parameters/ResourceIdParam'

    get:
      operationId: getResource
      summary: Get a resource by ID
      tags:
        - Resources
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'

    put:
      operationId: updateResource
      summary: Update a resource
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateResourceRequest'
      responses:
        '200':
          description: Resource updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '409':
          $ref: '#/components/responses/Conflict'
        '500':
          $ref: '#/components/responses/InternalError'

    patch:
      operationId: patchResource
      summary: Partially update a resource
      tags:
        - Resources
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PatchResourceRequest'
      responses:
        '200':
          description: Resource updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Resource'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'

    delete:
      operationId: deleteResource
      summary: Delete a resource
      tags:
        - Resources
      responses:
        '204':
          description: Resource deleted successfully
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT token obtained from `/auth/login` endpoint.
        Include in Authorization header: `Bearer <token>`

    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
      description: API key for service-to-service authentication

  schemas:
    # --- Base Resource ---
    Resource:
      type: object
      required:
        - id
        - name
        - createdAt
      properties:
        id:
          type: string
          format: uuid
          description: Unique resource identifier
          readOnly: true
        name:
          type: string
          minLength: 1
          maxLength: 200
          description: Resource name
        description:
          type: ['string', 'null']
          maxLength: 5000
          description: Detailed description
        status:
          $ref: '#/components/schemas/ResourceStatus'
        metadata:
          type: object
          additionalProperties: true
          description: Custom metadata key-value pairs
        createdAt:
          type: string
          format: date-time
          description: Creation timestamp
          readOnly: true
        updatedAt:
          type: ['string', 'null']
          format: date-time
          description: Last update timestamp
          readOnly: true

    ResourceStatus:
      type: string
      enum:
        - active
        - inactive
        - archived
      default: active
      description: Resource status

    # --- Request Schemas ---
    CreateResourceRequest:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 5000
        status:
          $ref: '#/components/schemas/ResourceStatus'
        metadata:
          type: object
          additionalProperties: true

    UpdateResourceRequest:
      type: object
      required:
        - name
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: ['string', 'null']
          maxLength: 5000
        status:
          $ref: '#/components/schemas/ResourceStatus'
        metadata:
          type: object
          additionalProperties: true

    PatchResourceRequest:
      type: object
      minProperties: 1
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: ['string', 'null']
          maxLength: 5000
        status:
          $ref: '#/components/schemas/ResourceStatus'
        metadata:
          type: object
          additionalProperties: true

    # --- List Response ---
    ResourceList:
      type: object
      required:
        - data
        - pagination
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Resource'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      required:
        - page
        - limit
        - total
        - totalPages
      properties:
        page:
          type: integer
          minimum: 1
          description: Current page number
        limit:
          type: integer
          minimum: 1
          maximum: 100
          description: Items per page
        total:
          type: integer
          minimum: 0
          description: Total number of items
        totalPages:
          type: integer
          minimum: 0
          description: Total number of pages
        hasNext:
          type: boolean
          description: Whether there are more pages
        hasPrevious:
          type: boolean
          description: Whether there are previous pages

    # --- Error Schemas ---
    Error:
      type: object
      required:
        - type
        - title
        - status
      properties:
        type:
          type: string
          format: uri
          description: URI reference identifying the error type
        title:
          type: string
          description: Short, human-readable summary
        status:
          type: integer
          description: HTTP status code
        detail:
          type: string
          description: Human-readable explanation
        instance:
          type: string
          format: uri
          description: URI reference identifying the specific occurrence
        errors:
          type: array
          items:
            $ref: '#/components/schemas/ValidationError'
          description: Validation errors (for 400 responses)

    ValidationError:
      type: object
      required:
        - field
        - message
      properties:
        field:
          type: string
          description: Field path (e.g., "body.name" or "query.page")
        message:
          type: string
          description: Error message
        code:
          type: string
          description: Error code for programmatic handling

  parameters:
    ResourceIdParam:
      name: resourceId
      in: path
      required: true
      description: Unique resource identifier
      schema:
        type: string
        format: uuid

    PageParam:
      name: page
      in: query
      description: Page number (1-indexed)
      schema:
        type: integer
        minimum: 1
        default: 1

    LimitParam:
      name: limit
      in: query
      description: Number of items per page
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20

    SortParam:
      name: sort
      in: query
      description: |
        Sort field and direction. Format: `field:direction`
        Direction: `asc` or `desc`
        Example: `createdAt:desc`
      schema:
        type: string
        pattern: '^[a-zA-Z]+:(asc|desc)$'
        default: 'createdAt:desc'

    FilterParam:
      name: filter
      in: query
      description: |
        Filter expression. Format: `field:operator:value`
        Operators: `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `contains`
        Example: `status:eq:active`
      schema:
        type: string

  responses:
    BadRequest:
      description: Invalid request parameters
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            type: "https://api.example.com/errors/validation"
            title: "Validation Error"
            status: 400
            detail: "Request validation failed"
            errors:
              - field: "body.name"
                message: "Name is required"
                code: "required"

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            type: "https://api.example.com/errors/unauthorized"
            title: "Unauthorized"
            status: 401
            detail: "Authentication token is missing or invalid"

    Forbidden:
      description: Insufficient permissions
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            type: "https://api.example.com/errors/forbidden"
            title: "Forbidden"
            status: 403
            detail: "You do not have permission to access this resource"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            type: "https://api.example.com/errors/not-found"
            title: "Not Found"
            status: 404
            detail: "The requested resource was not found"

    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            type: "https://api.example.com/errors/conflict"
            title: "Conflict"
            status: 409
            detail: "A resource with this identifier already exists"

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            type: "https://api.example.com/errors/internal"
            title: "Internal Server Error"
            status: 500
            detail: "An unexpected error occurred"
```

## Authentication Components Template

```yaml
components:
  securitySchemes:
    # JWT Bearer Token
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

    # API Key in header
    apiKeyHeader:
      type: apiKey
      in: header
      name: X-API-Key

    # API Key in query
    apiKeyQuery:
      type: apiKey
      in: query
      name: api_key

    # OAuth 2.0
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          refreshUrl: https://auth.example.com/refresh
          scopes:
            read: Read access
            write: Write access
            admin: Admin access

    # OpenID Connect
    openIdConnect:
      type: openIdConnect
      openIdConnectUrl: https://auth.example.com/.well-known/openid-configuration
```

## Spectral Configuration Template

```yaml
# .spectral.yaml - Linting rules for OpenAPI
extends:
  - spectral:oas

rules:
  # Required rules (error)
  operation-operationId: error
  operation-tags: error
  oas3-schema: error
  path-params: error

  # Recommended rules (warning)
  info-contact: warn
  info-description: warn
  operation-description: warn
  operation-summary: warn
  tag-description: warn

  # Custom rules
  operation-operationId-valid-in-url:
    description: operationId must be URL-safe
    given: "$.paths[*][*].operationId"
    severity: error
    then:
      function: pattern
      functionOptions:
        match: "^[a-zA-Z][a-zA-Z0-9]*$"

  path-no-trailing-slash:
    description: Paths must not have trailing slash
    given: "$.paths[*]~"
    severity: error
    then:
      function: pattern
      functionOptions:
        notMatch: "/$"

  response-error-schema:
    description: Error responses must use Error schema
    given: "$.paths[*][*].responses[?(@property >= '400')].content.application/json.schema"
    severity: warn
    then:
      field: "$ref"
      function: pattern
      functionOptions:
        match: "Error"
```

## Common Schemas Template

```yaml
components:
  schemas:
    # Timestamps
    Timestamps:
      type: object
      properties:
        createdAt:
          type: string
          format: date-time
          readOnly: true
        updatedAt:
          type: ['string', 'null']
          format: date-time
          readOnly: true

    # Soft delete
    SoftDelete:
      type: object
      properties:
        deletedAt:
          type: ['string', 'null']
          format: date-time
          readOnly: true
        isDeleted:
          type: boolean
          default: false
          readOnly: true

    # Audit fields
    Audit:
      type: object
      properties:
        createdBy:
          type: string
          format: uuid
          readOnly: true
        updatedBy:
          type: ['string', 'null']
          format: uuid
          readOnly: true

    # Money/Currency
    Money:
      type: object
      required:
        - amount
        - currency
      properties:
        amount:
          type: integer
          description: Amount in smallest currency unit (cents)
        currency:
          type: string
          pattern: '^[A-Z]{3}$'
          description: ISO 4217 currency code

    # Address
    Address:
      type: object
      properties:
        line1:
          type: string
          maxLength: 200
        line2:
          type: ['string', 'null']
          maxLength: 200
        city:
          type: string
          maxLength: 100
        state:
          type: ['string', 'null']
          maxLength: 100
        postalCode:
          type: string
          maxLength: 20
        country:
          type: string
          pattern: '^[A-Z]{2}$'
          description: ISO 3166-1 alpha-2 country code

    # Phone
    Phone:
      type: object
      required:
        - number
      properties:
        countryCode:
          type: string
          pattern: '^\+[1-9]\d{0,2}$'
          description: Country code with + prefix
        number:
          type: string
          pattern: '^\d{4,14}$'
          description: Phone number without country code

    # Date range
    DateRange:
      type: object
      properties:
        from:
          type: string
          format: date
        to:
          type: string
          format: date

    # Geolocation
    GeoLocation:
      type: object
      required:
        - latitude
        - longitude
      properties:
        latitude:
          type: number
          minimum: -90
          maximum: 90
        longitude:
          type: number
          minimum: -180
          maximum: 180
```
