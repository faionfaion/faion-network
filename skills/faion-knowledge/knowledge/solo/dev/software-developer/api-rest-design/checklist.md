# Checklist

## Planning Phase

- [ ] Define resources (nouns, not verbs)
- [ ] Design resource hierarchy (collections vs singletons)
- [ ] Plan HTTP methods for each operation
- [ ] Design consistent naming conventions
- [ ] Plan status codes for responses
- [ ] Plan error response format
- [ ] Design pagination strategy
- [ ] Document filtering/search approach

## Resource Design Phase

- [ ] Design resource URLs (plural, kebab-case)
- [ ] Use resource-oriented approach
- [ ] Nest sub-resources appropriately
- [ ] Avoid verb-based endpoints
- [ ] Keep resource structure consistent
- [ ] Document resource hierarchy

## HTTP Method Implementation Phase

- [ ] Use GET for read operations (safe, idempotent)
- [ ] Use POST for create operations
- [ ] Use PUT for full replacement (idempotent)
- [ ] Use PATCH for partial updates
- [ ] Use DELETE for removal (idempotent)
- [ ] Use correct status codes (200, 201, 204, etc)

## Request/Response Phase

- [ ] Design request body format (JSON structure)
- [ ] Design response body format (consistent structure)
- [ ] Use consistent field naming (snake_case or camelCase)
- [ ] Include metadata in responses (pagination, counts)
- [ ] Add Location header for 201 responses
- [ ] Document request/response examples

## Status Code Phase

- [ ] Use 200 for successful GET/PUT/PATCH
- [ ] Use 201 for successful POST (creation)
- [ ] Use 204 for successful DELETE
- [ ] Use 400 for validation errors
- [ ] Use 401 for auth failures
- [ ] Use 403 for permission failures
- [ ] Use 404 for not found
- [ ] Use 409 for conflicts
- [ ] Use 422 for semantic errors
- [ ] Use 429 for rate limits
- [ ] Use 5xx for server errors

## Pagination Phase

- [ ] Implement limit/offset or cursor-based pagination
- [ ] Include total count in response
- [ ] Include navigation links (next, prev)
- [ ] Document pagination format
- [ ] Set sensible defaults (page size)
- [ ] Implement max page size limits

## Filtering/Search Phase

- [ ] Design filter query parameter format
- [ ] Implement sorting (sort=field,-other_field)
- [ ] Implement search across resources
- [ ] Document filter operators if complex
- [ ] Test filters work correctly

## Error Handling Phase

- [ ] Design error response format (code, message, details)
- [ ] Document all error codes
- [ ] Provide helpful error messages
- [ ] Include stack trace only in dev
- [ ] Test error scenarios

## Versioning Phase

- [ ] Plan versioning strategy (URL path is standard)
- [ ] Support at least 2 API versions concurrently
- [ ] Document version differences
- [ ] Plan deprecation timeline
- [ ] Document migration path

## Documentation Phase

- [ ] Document all resources and endpoints
- [ ] Provide examples for each endpoint
- [ ] Document request/response formats
- [ ] Document error codes and meanings
- [ ] Create API reference guide
- [ ] Generate OpenAPI/Swagger spec

## Testing Phase

- [ ] Test all CRUD operations
- [ ] Test filtering and sorting
- [ ] Test pagination
- [ ] Test error scenarios
- [ ] Test authentication/authorization
- [ ] Load test API

## HATEOAS Phase (Optional)

- [ ] Include _links in responses
- [ ] Link to self, related resources
- [ ] Include link relations (self, next, prev)
- [ ] Document HATEOAS structure

## Deployment

- [ ] Deploy API with documentation
- [ ] Set up monitoring
- [ ] Create API changelog
- [ ] Monitor usage patterns