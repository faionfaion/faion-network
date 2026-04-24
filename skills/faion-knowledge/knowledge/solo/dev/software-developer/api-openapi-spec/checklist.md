# Checklist

## Planning Phase

- [ ] Define API title, version, and description
- [ ] Document base URL(s) (production, staging, dev)
- [ ] Identify all resources and operations
- [ ] Design consistent naming conventions
- [ ] Plan request/response structure
- [ ] Define error response format
- [ ] Plan authentication/security schemes

## Schema Definition Phase

- [ ] Create schema for each resource/entity
- [ ] Define all properties with types and constraints
- [ ] Add examples to all schemas
- [ ] Create reusable component schemas
- [ ] Add validation rules (minLength, maxLength, pattern, enum)
- [ ] Define required vs optional fields
- [ ] Create pagination metadata schema

## Endpoint Documentation Phase

- [ ] Document all GET endpoints (list, detail)
- [ ] Document all POST endpoints (create)
- [ ] Document all PATCH endpoints (update)
- [ ] Document all DELETE endpoints
- [ ] Add clear summaries and descriptions
- [ ] Document request/response for each
- [ ] Add example requests/responses
- [ ] Document status codes returned
- [ ] Document parameters (path, query, header)

## Error Response Phase

- [ ] Define error response schema
- [ ] Document all error codes returned
- [ ] Add error examples for each code
- [ ] Document error message format
- [ ] Include troubleshooting guidance

## Security Phase

- [ ] Define authentication scheme (Bearer, OAuth, API Key)
- [ ] Document required headers/parameters
- [ ] Define authorization scopes if applicable
- [ ] Mark endpoints with required auth
- [ ] Document rate limiting headers

## Parameters Phase

- [ ] Document all query parameters (filtering, sorting, pagination)
- [ ] Add parameter constraints (min, max, pattern)
- [ ] Add parameter examples
- [ ] Document deprecated parameters
- [ ] Document parameter validation rules

## Validation Phase

- [ ] Validate spec with Spectral or Redocly
- [ ] Check all endpoints have descriptions
- [ ] Check all schemas have examples
- [ ] Verify all required fields marked
- [ ] Check consistency in naming/structure

## Testing Phase

- [ ] Generate client SDKs from spec
- [ ] Test generated clients work correctly
- [ ] Test spec matches actual API behavior
- [ ] Validate responses against spec
- [ ] Test spec with API mock tools

## Documentation Phase

- [ ] Generate Swagger UI docs
- [ ] Generate Redoc docs
- [ ] Publish spec for clients
- [ ] Document how to use docs
- [ ] Create API reference guide

## Deployment

- [ ] Version control the OpenAPI spec
- [ ] Publish spec changes with API versions
- [ ] Monitor spec usage/validation in CI