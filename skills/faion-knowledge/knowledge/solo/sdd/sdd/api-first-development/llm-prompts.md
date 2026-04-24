# LLM Prompts for API Design

Effective prompts for using LLMs in API-first development workflows.

## API Specification Generation

### Generate OpenAPI from Requirements

```
You are an API architect. Generate an OpenAPI 3.1 specification based on these requirements:

**Domain:** [e.g., Task Management]
**Resources:** [e.g., Tasks, Projects, Users]
**Authentication:** [e.g., JWT Bearer tokens]

Requirements:
1. [List specific requirements]
2. [...]

Generate a complete OpenAPI 3.1 specification including:
- info section with description, contact
- servers (production, staging, local)
- security schemes
- all CRUD endpoints for each resource
- reusable components (schemas, parameters, responses)
- proper error responses (400, 401, 403, 404, 500)
- pagination for list endpoints
- examples for all request/response bodies

Use these conventions:
- operationId: camelCase (e.g., createTask, listTasks)
- paths: kebab-case plurals (e.g., /user-profiles)
- schemas: PascalCase (e.g., CreateTaskRequest)
- nullable fields: use type array ['string', 'null']
```

### Generate API from Existing Database Schema

```
Given this database schema:

```sql
[Paste CREATE TABLE statements]
```

Generate an OpenAPI 3.1 specification that:
1. Creates CRUD endpoints for each table
2. Maps database types to JSON Schema types
3. Handles foreign key relationships appropriately
4. Includes proper validation constraints from DB constraints
5. Generates appropriate request/response schemas

Conventions:
- snake_case DB columns -> camelCase in API
- Primary keys are read-only in create requests
- Foreign keys use UUID format
- Include timestamps (createdAt, updatedAt) from DB
```

### Extend Existing API Spec

```
Here is my current OpenAPI specification:

```yaml
[Paste existing spec]
```

I need to add the following functionality:
- [New requirement 1]
- [New requirement 2]

Generate the additions to the specification that:
1. Follow existing naming conventions
2. Reuse existing components where possible
3. Create new reusable components if needed
4. Maintain consistency with existing patterns
5. Add appropriate documentation

Return only the new/modified sections with clear comments indicating where they go.
```

## Code Generation from OpenAPI

### Generate Server Implementation

```
Given this OpenAPI specification:

```yaml
[Paste OpenAPI spec]
```

Generate a [Python/TypeScript/Go] server implementation using [FastAPI/Express/Gin]:

Requirements:
1. Implement all endpoints defined in the spec
2. Generate type definitions/models from schemas
3. Add input validation matching schema constraints
4. Implement proper error handling with defined error responses
5. Use dependency injection for database/services
6. Add authentication middleware based on security schemes
7. Include TODO comments where business logic is needed

Structure:
- models/ - Pydantic/Zod/struct definitions
- routes/ - Endpoint handlers
- middleware/ - Auth, error handling
- services/ - Business logic stubs
```

### Generate Client SDK

```
Given this OpenAPI specification:

```yaml
[Paste OpenAPI spec]
```

Generate a [TypeScript/Python] client SDK that:

1. Creates typed methods for each operation
2. Uses operationId for method names
3. Handles authentication (Bearer token)
4. Implements proper error handling
5. Supports request/response interceptors
6. Includes JSDoc/docstrings from descriptions
7. Uses async/await patterns

Example usage should look like:
```typescript
const client = new ApiClient({ baseUrl, token });
const tasks = await client.listTasks({ page: 1, limit: 20 });
const task = await client.createTask({ title: "New task" });
```
```

### Generate Type Definitions Only

```
Given this OpenAPI specification:

```yaml
[Paste OpenAPI spec]
```

Generate [TypeScript/Python/Go] type definitions for:
1. All schemas in components/schemas
2. Request body types for each operation
3. Response types for each operation
4. Query parameter types

Use these conventions:
- TypeScript: interfaces with optional properties using `?`
- Python: Pydantic models with Optional[] types
- Go: structs with json tags and pointers for optional fields

Include:
- Type comments from descriptions
- Validation decorators where applicable
```

## API Design Review

### Review Specification for Best Practices

```
Review this OpenAPI specification for best practices and potential issues:

```yaml
[Paste OpenAPI spec]
```

Check for:

**Naming:**
- [ ] Consistent plural nouns for collections
- [ ] Consistent casing (kebab-case paths, camelCase operationIds)
- [ ] Meaningful operationIds

**Design:**
- [ ] RESTful resource design
- [ ] Proper HTTP method usage
- [ ] Consistent pagination pattern
- [ ] Proper use of HTTP status codes

**Documentation:**
- [ ] All operations have summary and description
- [ ] All parameters documented
- [ ] Examples provided for complex types
- [ ] Error responses documented

**Security:**
- [ ] Authentication defined
- [ ] Sensitive data not in URL
- [ ] Rate limiting mentioned

**Maintainability:**
- [ ] Reusable components used
- [ ] No duplicate schemas
- [ ] Proper use of $ref

Provide specific recommendations with examples for each issue found.
```

### Suggest Breaking Changes for v2

```
Given this v1 OpenAPI specification:

```yaml
[Paste v1 spec]
```

And these requirements for v2:
- [Requirement 1]
- [Requirement 2]

Analyze and recommend:

1. **Breaking changes needed:**
   - List each breaking change
   - Explain why it's necessary
   - Suggest migration path for consumers

2. **Non-breaking additions:**
   - New endpoints
   - New optional fields
   - New response fields

3. **Deprecations:**
   - What to deprecate in v1
   - Suggested sunset timeline

4. **Migration guide outline:**
   - Step-by-step migration instructions
   - Code examples for common patterns

Generate the complete v2 specification with:
- Clear comments on breaking changes
- Deprecated annotations where applicable
```

## Testing and Validation

### Generate Test Cases from Spec

```
Given this OpenAPI specification:

```yaml
[Paste OpenAPI spec]
```

Generate comprehensive test cases for [Jest/Pytest/Go testing]:

1. **Happy path tests:**
   - Test each endpoint with valid data
   - Test pagination
   - Test filtering/sorting

2. **Validation tests:**
   - Test required field validation
   - Test type validation
   - Test constraint validation (min/max, pattern)

3. **Error handling tests:**
   - Test 401 without auth
   - Test 404 for missing resources
   - Test 400 for invalid input

4. **Edge cases:**
   - Empty lists
   - Maximum pagination limits
   - Unicode characters in strings

Use the examples from the spec as test data.
```

### Generate Mock Data

```
Given this OpenAPI schema:

```yaml
[Paste schema section]
```

Generate realistic mock data for testing:

1. **Valid examples:**
   - 5 different valid instances of each schema
   - Cover edge cases (min/max lengths, all enum values)
   - Include optional fields in some instances

2. **Invalid examples:**
   - Missing required fields
   - Type mismatches
   - Constraint violations

Format as JSON that can be used in tests or mock server configuration.
```

## Documentation Generation

### Generate API Documentation

```
Given this OpenAPI specification:

```yaml
[Paste OpenAPI spec]
```

Generate human-readable API documentation in Markdown:

1. **Overview section:**
   - API purpose and capabilities
   - Authentication guide
   - Rate limiting info
   - Base URLs

2. **Quick start:**
   - cURL examples for common operations
   - SDK installation
   - First API call walkthrough

3. **Endpoint reference:**
   - Group by tags
   - Include request/response examples
   - Document all parameters
   - Show error responses

4. **Schemas reference:**
   - Field descriptions
   - Validation rules
   - Example JSON

5. **Error handling guide:**
   - Error response format
   - Common error codes
   - Troubleshooting tips
```

### Generate Changelog from Spec Diff

```
Compare these two OpenAPI specifications:

**Previous version (v1.0.0):**
```yaml
[Paste old spec]
```

**New version (v1.1.0):**
```yaml
[Paste new spec]
```

Generate a changelog entry that includes:

1. **New Features:**
   - New endpoints
   - New optional fields
   - New response fields

2. **Changes:**
   - Modified behaviors
   - Updated validation rules

3. **Deprecations:**
   - Deprecated endpoints
   - Deprecated fields

4. **Breaking Changes:** (if any)
   - List with migration instructions

Format as a standard CHANGELOG.md entry.
```

## Prompt Tips for API Design

### Context Setting

Always include:
- Domain context (what the API is for)
- Tech stack constraints
- Existing conventions to follow
- Target audience (internal/external developers)

### Specificity

Be specific about:
- Naming conventions (camelCase, snake_case, kebab-case)
- Authentication method
- Error response format
- Pagination style (offset, cursor)

### Iteration

Use follow-up prompts to:
- Add missing endpoints
- Refine schemas
- Add examples
- Improve documentation

### Validation

Always ask the LLM to:
- Validate against OpenAPI 3.1 spec
- Check for consistency
- Identify potential issues
- Suggest improvements

## Example Workflow

```
Step 1: Generate initial spec from requirements
Step 2: Review for best practices
Step 3: Add missing components
Step 4: Generate server stubs
Step 5: Generate client SDK
Step 6: Generate test cases
Step 7: Generate documentation
```

Use separate prompts for each step, feeding the output of previous steps as context.
