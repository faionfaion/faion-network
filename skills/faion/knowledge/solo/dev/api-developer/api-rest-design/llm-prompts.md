# LLM Prompts for REST API Design

Practical prompts for AI-assisted REST API development.

## Resource Design Prompts

### Identify Resources

```
I'm designing a REST API for [DOMAIN]. Help me identify resources.

Context:
- Business: [Brief description]
- Main entities: [List known entities]
- Key operations: [What users need to do]

Analyze this domain and suggest:
1. Core resources (nouns, plural form)
2. URL structure for each resource
3. Sub-resources and relationships
4. Query parameters for filtering/sorting

Format as a table with: Resource | URL | Sub-resources | Query Params
```

### Design Resource Relationships

```
I have these resources in my API:
[LIST YOUR RESOURCES]

Help me design the relationships:
1. Which resources should be nested? (e.g., /users/{id}/orders)
2. Which should be flat with references? (e.g., /orders?userId=123)
3. What's the maximum nesting depth?
4. How to handle many-to-many relationships?

Consider: query performance, URL readability, REST principles
```

## HTTP Methods Prompts

### Choose HTTP Methods

```
I need to implement these operations for [RESOURCE]:
[LIST OPERATIONS]

For each operation, recommend:
1. HTTP method (GET/POST/PUT/PATCH/DELETE)
2. URL pattern
3. Request body (if any)
4. Response status code
5. Response body

Follow REST best practices and explain trade-offs.
```

### Design Action Endpoints

```
I have a [RESOURCE] that needs these actions that don't fit standard CRUD:
[LIST ACTIONS, e.g., "approve order", "send notification", "archive item"]

Design REST-compliant endpoints for each action:
1. Should it be POST to sub-resource? (e.g., POST /orders/{id}/approvals)
2. Should it be PATCH with status change? (e.g., PATCH /orders/{id} {status: "approved"})
3. Something else?

Explain the trade-offs of each approach.
```

## Response Design Prompts

### Design Response Schemas

```
Design JSON response schemas for [RESOURCE] API:

Context:
- Fields: [List fields]
- Consumers: [Who uses the API]
- Needs: [Specific requirements]

Provide:
1. Single resource response schema
2. Collection response schema (with pagination)
3. Nested vs. flat decision for relationships
4. Field naming convention (camelCase/snake_case)
```

### Error Response Design

```
Design error responses for my REST API:

Error scenarios to handle:
- Validation errors (multiple fields)
- Not found errors
- Authentication errors
- Authorization errors
- Rate limiting
- Server errors

Provide:
1. Consistent error envelope structure
2. HTTP status code mapping
3. Error code naming convention
4. Example responses for each scenario
```

## OpenAPI Prompts

### Generate OpenAPI Spec

```
Generate an OpenAPI 3.1 specification for [RESOURCE]:

Operations needed:
- [LIST CRUD + custom operations]

Include:
1. All endpoints with parameters
2. Request/response schemas
3. Error responses
4. Authentication (Bearer JWT)
5. Pagination for lists
6. Example values

Output valid YAML that passes validation.
```

### Review OpenAPI Spec

```
Review this OpenAPI specification for issues:

[PASTE YOUR SPEC]

Check for:
1. Missing error responses
2. Inconsistent naming
3. Missing required fields
4. Security issues
5. Schema reuse opportunities
6. Documentation completeness

Provide specific fixes for each issue found.
```

## Implementation Prompts

### FastAPI Implementation

```
Implement a FastAPI router for [RESOURCE] based on this OpenAPI spec:

[PASTE RELEVANT SPEC SECTION]

Requirements:
- Use Pydantic models for validation
- Include proper status codes
- Add OpenAPI documentation
- Handle errors consistently
- Include pagination for lists

Provide complete, production-ready code.
```

### Django REST Framework Implementation

```
Implement a DRF ViewSet for [RESOURCE]:

Model:
[PASTE MODEL]

Requirements:
- Standard CRUD operations
- Filtering by [FIELDS]
- Ordering by [FIELDS]
- Pagination (20 items default)
- Custom action: [DESCRIBE]

Include serializers, views, and URL configuration.
```

## Testing Prompts

### Generate API Tests

```
Generate tests for this REST API endpoint:

Endpoint: [METHOD] [URL]
Request: [SCHEMA]
Response: [SCHEMA]

Generate:
1. Happy path tests
2. Validation error tests
3. Not found tests
4. Auth tests
5. Edge cases

Use pytest with httpx/requests. Include fixtures.
```

### Contract Testing

```
Create Pact contract tests for this API:

Consumer: [CONSUMER NAME]
Provider: [PROVIDER NAME]
Endpoint: [DESCRIBE ENDPOINT]

Generate:
1. Consumer expectations
2. Provider verification
3. State handlers
4. CI/CD integration instructions
```

## Documentation Prompts

### Generate API Documentation

```
Generate user-friendly documentation for this endpoint:

[PASTE OPENAPI ENDPOINT]

Include:
1. Plain English description
2. When to use this endpoint
3. Request example with curl
4. Response example
5. Error scenarios
6. Rate limits/quotas
7. SDK examples (Python, JavaScript)
```

### API Changelog

```
I made these changes to my API:
[LIST CHANGES]

Generate a changelog entry that:
1. Categorizes as: Added/Changed/Deprecated/Removed/Fixed
2. Explains impact on consumers
3. Provides migration guidance if breaking
4. Includes version number recommendation
```

---

## Quick Reference Prompts

### API Design Review

```
Review this REST API design for best practices:

[PASTE API DESIGN/OPENAPI]

Check:
- Resource naming (plural nouns)
- HTTP method usage
- Status codes
- Error handling
- Pagination
- Versioning
- Security

Rate 1-10 and provide actionable improvements.
```

### Compare Approaches

```
I'm deciding between these API approaches for [FEATURE]:

Option A: [DESCRIBE]
Option B: [DESCRIBE]

Compare based on:
- REST compliance
- Developer experience
- Performance
- Maintainability
- Flexibility

Recommend one with justification.
```

---

*LLM Prompts for REST API Design v1.0*
