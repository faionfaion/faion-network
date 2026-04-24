# API-First Development Checklist

## Phase 1: OpenAPI Specification Design

- [ ] Define API title, version, and description
- [ ] List authentication methods (Bearer, API Key, OAuth2)
- [ ] Document rate limiting strategy
- [ ] Define production and staging server URLs
- [ ] Plan API versioning strategy (`/v1/`, `/v2/`)

## Phase 2: Endpoint Design

- [ ] Design all resource endpoints (`/resources`, `/resources/{id}`)
- [ ] Define HTTP methods for each endpoint (GET, POST, PUT, DELETE, PATCH)
- [ ] Create operation IDs for code generation
- [ ] Define request parameters (path, query, body)
- [ ] Design response schemas for success (200, 201) and error cases
- [ ] Document HTTP status codes used
- [ ] Include examples for requests and responses

## Phase 3: Schema Definition

- [ ] Define all reusable schemas (Resource, Error, Pagination)
- [ ] Mark required properties
- [ ] Set type constraints (string, integer, boolean, array, object)
- [ ] Add format hints (uuid, date-time, email)
- [ ] Define validation rules (minLength, maxLength, minimum, maximum)
- [ ] Create references ($ref) for code reuse
- [ ] Use JSON Schema 2020-12 vocabulary

## Phase 4: OpenAPI Specification

- [ ] Write OpenAPI 3.1 YAML/JSON file
- [ ] Include all path definitions
- [ ] Define all components (schemas, parameters, responses, securitySchemes)
- [ ] Use $ref for schema reuse and DRY principle
- [ ] Add proper error response schemas
- [ ] Include security definitions globally and per-operation

## Phase 5: Specification Validation

- [ ] Validate with Spectral linting
- [ ] Check for missing error schemas
- [ ] Verify all operations have examples
- [ ] Ensure consistent naming conventions
- [ ] Check security schemes are defined
- [ ] Validate schema completeness

## Phase 6: Mock Server & Testing

- [ ] Generate mock server using Prism
- [ ] Deploy mock server for frontend/mobile testing
- [ ] Test all endpoints with mock data
- [ ] Verify response schemas match specification
- [ ] Enable parallel frontend development

## Phase 7: Code Generation

- [ ] Generate server stubs from spec
- [ ] Generate client SDKs
- [ ] Generate documentation
- [ ] Update generated code generators in CI/CD

## Phase 8: Contract Testing

- [ ] Write contract tests against spec
- [ ] Ensure backend implementation matches spec
- [ ] Add contract tests to CI/CD pipeline
- [ ] Prevent breaking changes to API contract
