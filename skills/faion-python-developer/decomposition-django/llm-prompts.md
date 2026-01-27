# LLM Prompts for Django Decomposition

Effective prompts for Django development with LLM coding agents.

---

## General Principles

### Decomposition for LLM Agents

LLM coding agents work best with:

1. **Small, focused files** (50-150 lines)
2. **Clear task boundaries** - one feature per prompt
3. **Incremental changes** - build on previous context
4. **Test-driven approach** - write tests alongside code

**Anti-pattern:** Asking for "entire user management system"
**Pattern:** Breaking into discrete tasks (model, service, views, tests)

---

## Codebase Analysis Prompts

### Initial Audit

```
Analyze this Django project structure and identify:
1. Files over 200 lines that need splitting
2. Business logic in views that should move to services
3. Repeated query patterns that should become selectors
4. Circular import risks
5. Missing test coverage

Focus on the {app_name} app first.
```

### Dependency Mapping

```
Map the dependencies in the {app_name} Django app:
1. Model relationships (ForeignKey, ManyToMany)
2. Import chains between modules
3. Signal connections
4. Celery task dependencies

Output as a dependency graph showing which files depend on which.
```

### Code Quality Check

```
Review {file_path} and identify:
1. Functions over 30 lines
2. Classes with too many responsibilities
3. Missing type hints
4. Missing docstrings
5. N+1 query risks

Suggest specific refactoring for each issue.
```

---

## Model Decomposition Prompts

### Split Models File

```
Split {app_name}/models.py into a models/ package:
1. Create models/__init__.py with re-exports
2. One file per model (or closely related models)
3. Keep managers in same file as model
4. Preserve all imports and relationships
5. Verify no circular imports

Current structure:
{paste current models.py}
```

### Extract Model Mixins

```
Extract reusable patterns from these models into mixins:

{paste models}

Create:
1. TimeStampedMixin (created_at, updated_at)
2. SoftDeleteMixin (is_deleted, deleted_at)
3. Any domain-specific mixins you identify

Place in models/mixins.py
```

### Add Type Hints to Model

```
Add type hints to this Django model following PEP 484:

{paste model}

Include:
1. Field type annotations where useful
2. Method return types
3. Property return types
4. Manager return types (QuerySet[Model])
```

---

## Service Layer Prompts

### Extract Service from View

```
Extract business logic from this view into a service:

{paste view code}

Create:
1. Input dataclass for the operation
2. Service class/function with the logic
3. Proper transaction handling
4. Type hints throughout
5. Docstrings with examples

The view should only handle request parsing and response formatting.
```

### Create Service Layer

```
Create a service layer for the {app_name} app following HackSoft pattern:

Services needed:
- {entity}_service.py: CRUD and business operations
- {related}_service.py: Related domain operations

Each service should:
1. Use dataclasses for input/output
2. Use @transaction.atomic for writes
3. Raise domain exceptions (not HTTP errors)
4. Have no knowledge of HTTP/requests
5. Be fully type-hinted
```

### Service with Dependencies

```
Create {service_name} service with dependency injection:

Dependencies:
- {dependency_1}: {description}
- {dependency_2}: {description}

The service should:
1. Accept dependencies in __init__
2. Use Protocol for dependency types
3. Be testable with mock dependencies
4. Handle errors gracefully
```

---

## Selector Prompts

### Extract Selectors

```
Extract query logic from these views/services into selectors:

{paste code with queries}

Create selectors for:
1. get_by_id / get_by_slug
2. get_all / get_active
3. Search/filter operations
4. Pagination helpers

Each selector should:
1. Return QuerySet for further filtering
2. Include proper select_related/prefetch_related
3. Have clear type hints
4. Be a plain function (not class)
```

### Optimize Queries

```
Review these selectors for N+1 query issues:

{paste selectors}

For each function:
1. Identify related data accessed
2. Add appropriate select_related
3. Add appropriate prefetch_related
4. Consider using only()/defer() for large models
```

---

## View Decomposition Prompts

### Split ViewSet

```
Split this monolithic ViewSet into focused views:

{paste viewset}

Create:
1. {Resource}ListView - list endpoint
2. {Resource}DetailView - retrieve endpoint
3. {Resource}CreateView - create endpoint
4. {Resource}UpdateView - update endpoint
5. {Resource}ActionViews - custom actions

Each view should:
1. Use service for business logic
2. Use selector for queries
3. Be under 80 lines
4. Have proper permissions
```

### Thin View Refactor

```
Refactor this view to be "thin" (only HTTP handling):

{paste view}

Move to service layer:
- All business logic
- All database operations
- All side effects (emails, notifications)

The view should only:
1. Parse request data
2. Call service
3. Format response
```

---

## Serializer Prompts

### Split Serializers

```
Split {app_name}/serializers.py into:
1. serializers/user_read.py - List and Detail serializers
2. serializers/user_write.py - Create and Update serializers
3. serializers/user_nested.py - Embedded serializers

Keep serializers focused:
- No business logic in create()/update()
- Clear naming: {Model}{Action}Serializer
- Type hints on all custom methods
```

### Create Write Serializer

```
Create input serializer for {operation}:

Required fields: {list fields}
Optional fields: {list fields}

The serializer should:
1. Validate input only (no mutations)
2. Use clear field types
3. Include helpful error messages
4. Be separate from read serializers
```

---

## Testing Prompts

### Generate Service Tests

```
Generate pytest tests for this service:

{paste service}

Cover:
1. Happy path for each method
2. Edge cases and error handling
3. Transaction rollback scenarios
4. Input validation

Use factory_boy for fixtures.
Structure: arrange-act-assert pattern.
```

### Generate Selector Tests

```
Generate tests for these selectors:

{paste selectors}

Test:
1. Return correct results
2. Filtering works correctly
3. Pagination works
4. Empty results handled
5. Performance (no N+1)
```

### API Integration Tests

```
Generate API integration tests for:

{paste view or describe endpoint}

Test:
1. Authentication/authorization
2. Valid request returns correct data
3. Invalid request returns proper errors
4. Status codes are correct
5. Response format matches serializer
```

---

## Incremental Refactoring Prompts

### Phase 1: Models

```
Phase 1 of {app_name} decomposition - Models:

1. Convert models.py to models/ package
2. Extract base model mixins to core/
3. Add type hints to all models
4. Ensure no migrations needed

Keep backward compatibility - no table changes.
```

### Phase 2: Services

```
Phase 2 of {app_name} decomposition - Services:

Building on Phase 1, create service layer:
1. Identify all write operations in views
2. Create {entity}_service.py for each entity
3. Move business logic to services
4. Add tests for services

Views should still work - just delegate to services.
```

### Phase 3: Selectors

```
Phase 3 of {app_name} decomposition - Selectors:

Building on Phase 2, extract queries:
1. Find repeated queries in views/services
2. Create {entity}_selectors.py
3. Move all read operations to selectors
4. Optimize with select_related/prefetch_related

Services and views should use selectors for all reads.
```

### Phase 4: Views

```
Phase 4 of {app_name} decomposition - Views:

Building on Phase 3, thin the views:
1. Convert views.py to views/ package
2. Split by resource or action type
3. Remove all business logic (use services)
4. Remove all queries (use selectors)
5. Update URL configuration
```

---

## DRF-Specific Prompts

### Create REST Endpoint

```
Create a REST endpoint for {resource}:

Requirements:
- {list requirements}

Include:
1. ViewSet or APIView (choose appropriate)
2. Serializers (read/write separate)
3. Permissions
4. URL configuration
5. Tests

Follow HackSoft pattern: views call services, services use selectors.
```

### API Versioning

```
Add API versioning for {app_name}:

1. Create api/v1/{app_name}/ structure
2. Move current views to v1
3. Update URL configuration
4. Create version-specific serializers if needed
5. Document breaking changes
```

### Pagination Setup

```
Implement cursor pagination for {endpoint}:

Requirements:
1. Cursor-based (not offset) for large datasets
2. Configurable page size
3. Include next/previous links
4. Handle edge cases

Return format:
{
  "results": [...],
  "next": "cursor_token",
  "previous": "cursor_token"
}
```

---

## CLAUDE.md Generation Prompts

### Generate App Documentation

```
Generate CLAUDE.md for the {app_name} Django app:

Include:
1. App purpose and domain
2. Directory structure table
3. Key services and their methods
4. Key selectors and their purposes
5. API endpoints summary
6. Testing notes
```

### Update Root CLAUDE.md

```
Update the project CLAUDE.md with:

1. New {app_name} structure after decomposition
2. Service layer conventions
3. Selector patterns
4. Testing approach

Keep existing content, add new section for {app_name}.
```

---

## Debugging Prompts

### Fix Circular Import

```
Fix circular import between:
- {file_1}
- {file_2}

Options to consider:
1. Move shared code to new module
2. Use lazy imports
3. Restructure dependencies
4. Use string annotations for type hints

Maintain all functionality while resolving the cycle.
```

### Fix N+1 Query

```
This code has N+1 query problem:

{paste code}

Identify:
1. Where the N+1 occurs
2. Which related objects cause it
3. Fix with select_related or prefetch_related
4. Verify fix with django-debug-toolbar
```

### Migration Issue

```
After decomposition, migrations fail:

Error: {paste error}

Original structure: {describe}
New structure: {describe}

Fix the migration without data loss.
Consider: db_table, rename operations, data migrations.
```

---

## Best Practices for LLM Prompts

### Do

- Provide existing code when asking for changes
- Specify exact file paths
- Request one logical change at a time
- Ask for tests alongside implementation
- Specify Django/DRF version

### Don't

- Ask for "entire app" at once
- Skip providing context
- Accept generated code without review
- Skip incremental testing
- Ignore type hints in prompts

### Prompt Template

```
Context:
- Django {version}, DRF {version}
- App: {app_name}
- File: {file_path}

Current code:
{paste code}

Task:
{specific task}

Requirements:
1. {requirement 1}
2. {requirement 2}

Output:
- Modified code
- New files if needed
- Tests
```

---

## Related

- [README.md](README.md) - Overview and patterns
- [checklist.md](checklist.md) - Step-by-step checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Code templates
