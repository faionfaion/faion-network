# API-First Development Checklist

Use this checklist to ensure your API-first workflow follows best practices.

## Pre-Design Phase

- [ ] **Define API purpose** - Clear problem statement and use cases
- [ ] **Identify consumers** - Who will use this API? (Frontend, mobile, third-party)
- [ ] **Choose versioning strategy** - URL path, header, or query parameter
- [ ] **Select OpenAPI version** - Prefer 3.1 for JSON Schema alignment
- [ ] **Set up tooling** - Editor, linter, mock server

## Design Phase

### Specification Structure

- [ ] **info object complete**
  - [ ] title, version, description
  - [ ] contact information
  - [ ] license (if applicable)
- [ ] **servers defined**
  - [ ] Production URL
  - [ ] Staging URL
  - [ ] Local development URL
- [ ] **security schemes defined**
  - [ ] Authentication method(s)
  - [ ] Scopes (for OAuth)

### Paths & Operations

- [ ] **RESTful naming**
  - [ ] Plural nouns for collections (`/users`, not `/user`)
  - [ ] Kebab-case for multi-word (`/user-profiles`)
  - [ ] No verbs in paths (use HTTP methods)
- [ ] **operationId for each endpoint** - Unique, camelCase
- [ ] **Tags for grouping** - Logical organization
- [ ] **Summary and description** - Clear, concise explanations

### Schemas

- [ ] **All schemas in components/schemas** - Reusable definitions
- [ ] **Required fields marked** - Explicit `required` array
- [ ] **Validation constraints**
  - [ ] minLength/maxLength for strings
  - [ ] minimum/maximum for numbers
  - [ ] pattern for formats (regex)
  - [ ] enum for fixed values
- [ ] **Format hints** - uuid, date-time, email, uri
- [ ] **Examples provided** - Request and response examples

### Responses

- [ ] **All status codes documented**
  - [ ] 200/201/204 - Success responses
  - [ ] 400 - Bad Request (validation errors)
  - [ ] 401 - Unauthorized
  - [ ] 403 - Forbidden
  - [ ] 404 - Not Found
  - [ ] 500 - Internal Server Error
- [ ] **Error schema defined** - Consistent error format
- [ ] **Pagination for lists** - page, limit, total parameters

### Parameters

- [ ] **Reusable parameters in components** - PageParam, LimitParam, etc.
- [ ] **Default values** - Sensible defaults for optional params
- [ ] **Parameter descriptions** - What each parameter does

## Validation Phase

- [ ] **Spectral linting passes** - No errors or warnings
- [ ] **Custom rules applied** - Organization-specific standards
- [ ] **Breaking change detection** - Compare with previous version
- [ ] **Security scan** - OWASP ZAP or similar

### Spectral Rules to Enable

```yaml
# .spectral.yaml
extends: spectral:oas
rules:
  operation-operationId: error
  operation-tags: error
  oas3-schema: error
  info-contact: warn
  operation-description: warn
```

## Mock Phase

- [ ] **Mock server deployed** - Prism or WireMock
- [ ] **Examples generate realistic data** - Use faker patterns
- [ ] **Frontend team testing** - Integration verified
- [ ] **Edge cases mocked** - Error responses, empty states

## Implementation Phase

- [ ] **Code generated from spec** - Server stubs, types
- [ ] **Business logic implemented** - In generated handlers
- [ ] **Spec is source of truth** - Don't modify generated types manually
- [ ] **Implementation matches spec** - Contract tests pass

### Code Generation Checklist

- [ ] **Choose generator** - openapi-generator, openapi-stack
- [ ] **Configure output** - Language, framework, options
- [ ] **Generate types/interfaces** - DTOs from schemas
- [ ] **Generate route stubs** - Endpoints with validation
- [ ] **Implement handlers** - Add business logic

## Testing Phase

- [ ] **Contract tests written** - Pact or Dredd
- [ ] **All endpoints tested** - Coverage for each operation
- [ ] **Validation tested** - Invalid input rejected correctly
- [ ] **Error responses verified** - Match defined schemas
- [ ] **Authentication tested** - Protected endpoints secure

### Contract Testing Checklist

```bash
# Run contract tests
dredd openapi.yaml http://localhost:3000

# Or with Prism
prism mock openapi.yaml
prism proxy openapi.yaml http://localhost:3000
```

## Documentation Phase

- [ ] **Swagger UI deployed** - Interactive documentation
- [ ] **Descriptions are clear** - Non-technical language where appropriate
- [ ] **Examples are realistic** - Real-world use cases
- [ ] **Getting started guide** - Quick start for consumers
- [ ] **Authentication documented** - How to get credentials

## Deployment Phase

- [ ] **Version in URL** - `/v1/`, `/v2/` for breaking changes
- [ ] **SDKs generated** - Client libraries for major languages
- [ ] **Changelog maintained** - Version history documented
- [ ] **Deprecation notices** - Old endpoints marked deprecated
- [ ] **Migration guide** - For breaking changes

## LLM Integration Checklist

When using LLMs to generate code from OpenAPI:

- [ ] **Natural language descriptions** - Rich descriptions in spec
- [ ] **Examples included** - Request/response examples
- [ ] **Small, focused specs** - Break large APIs into modules
- [ ] **Type information complete** - All types explicitly defined
- [ ] **Validation rules explicit** - Constraints in schema

### LLM-Friendly Spec Tips

1. **Use descriptive operationIds** - `createUser`, not `post1`
2. **Add x-examples** - Multiple examples per operation
3. **Document edge cases** - In description fields
4. **Include error examples** - Show validation error format
5. **Use $ref** - Reusable components reduce context size

## Common Mistakes to Avoid

| Mistake | Fix |
|---------|-----|
| Spec written after code | Design spec first, generate code from it |
| No versioning strategy | Plan for v1, v2 from the start |
| Missing error schemas | Define all error response formats |
| No examples | Include request/response examples in spec |
| Generic descriptions | Write detailed, context-rich descriptions |
| Manual type definitions | Generate types from spec |
| Spec drift | Use contract testing to catch mismatches |
| Monolithic spec | Split into modules with $ref |

## Review Checklist

Before marking API design complete:

- [ ] Spec passes all linting rules
- [ ] All consumers reviewed and approved
- [ ] Security review completed
- [ ] Performance considerations documented
- [ ] Rate limiting defined
- [ ] Pagination strategy consistent
- [ ] Versioning strategy documented
- [ ] Breaking change policy defined
