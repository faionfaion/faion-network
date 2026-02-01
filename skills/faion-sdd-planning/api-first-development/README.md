# API-First Development

### Problem

APIs designed after implementation lead to:
- Inconsistent API designs across services
- Breaking changes for consumers
- Documentation that doesn't match reality
- Delayed frontend/mobile development waiting for backend

### Framework

#### API-First Principles

1. **Design before code** - API contract is first artifact
2. **Contract as source of truth** - Generate code, tests, docs from spec
3. **Consumer-driven** - Design for API consumers, not implementation convenience
4. **Shift-left testing** - Mock servers enable parallel development

#### API-First Workflow

```
DESIGN -> VALIDATE -> MOCK -> IMPLEMENT -> TEST -> DEPLOY
   |         |        |         |         |
OpenAPI   Spectral  Prism    codegen   contract
  spec     linting  server   from spec   tests
```

#### OpenAPI 3.1 Key Features (2021+)

| Feature | Description |
|---------|-------------|
| **JSON Schema alignment** | Full JSON Schema vocabularies support |
| **Webhooks** | New top-level element for event-driven APIs |
| **$ref improvements** | Better reference handling |
| **Nullable simplification** | Use `type: ['string', 'null']` |

### Templates

#### OpenAPI 3.1 Specification Template

```yaml
openapi: 3.1.0
info:
  title: [API Name]
  version: 1.0.0
  description: |
    [Brief API description]

    ## Authentication
    [Auth method description]

    ## Rate Limiting
    [Rate limit details]
  contact:
    name: [Team Name]
    email: [team@example.com]

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

security:
  - bearerAuth: []

paths:
  /resources:
    get:
      summary: List resources
      operationId: listResources
      tags:
        - Resources
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResourceList'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Resource:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
          minLength: 1
          maxLength: 100
        createdAt:
          type: string
          format: date-time

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### Best Practices

| Practice | Description |
|----------|-------------|
| **Spectral linting** | Validate specs with industry-standard rules |
| **Mock server deployment** | Generate temporary servers for frontend testing |
| **Contract testing** | Ensure backend matches API contract |
| **Security scanning** | Integrate OWASP ZAP in pipeline |
| **SDK generation** | Auto-generate client libraries from spec |
| **Version in URL** | Use `/v1/`, `/v2/` for breaking changes |

### Tools (2025-2026)

| Category | Tools |
|----------|-------|
| **Specification** | OpenAPI 3.1, AsyncAPI (events) |
| **Linting** | Spectral, Redocly |
| **Mocking** | Prism, WireMock |
| **Documentation** | Swagger UI, Redoc, Stoplight |
| **Code generation** | openapi-generator, openapi-stack |
| **Contract testing** | Pact, Dredd |

### Common Mistakes

| Mistake | Fix |
|---------|-----|
| Spec written after code | Design spec first, generate code from it |
| No versioning strategy | Plan for v1, v2 from the start |
| Missing error schemas | Define all error response formats |
| No examples | Include request/response examples in spec |

## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |

## Sources

- [OpenAPI 3.1 Specification](https://spec.openapis.org/oas/v3.1.0) - Official OpenAPI standard
- [API Design Patterns](https://www.manning.com/books/api-design-patterns) - API design best practices
- [Stoplight Studio](https://stoplight.io/studio) - API-first design tools
- [Spectral Linting](https://stoplight.io/open-source/spectral) - OpenAPI validation rules
- [Swagger Editor](https://editor.swagger.io/) - Interactive OpenAPI editor
