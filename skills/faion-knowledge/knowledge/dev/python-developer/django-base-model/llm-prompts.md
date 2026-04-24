# LLM Prompts for Django Base Model Design

Effective prompts for AI-assisted Django model design. Use with Claude, GPT-4, or other LLMs.

---

## Prompt 1: Design Base Model System

### Initial Assessment

```
I'm starting a new Django project. Help me design a base model system.

Project context:
- Type: [SaaS / E-commerce / Internal tool / API backend]
- Django version: [5.0+ / 5.2 LTS]
- Database: [PostgreSQL / MySQL / SQLite]
- Multi-tenant: [Yes / No]
- Soft delete needed: [Yes / No]
- Audit trail needed: [Yes / No]
- API exposure: [REST / GraphQL / None]

Please recommend:
1. Base model structure (fields, mixins)
2. Manager/QuerySet patterns
3. UUID strategy (separate field vs PK)
4. Any Django 5.x features to leverage
```

### Follow-up for Implementation

```
Based on your recommendations, generate the complete base model code with:
- All mixins as separate classes
- Custom managers with QuerySet pattern
- Type hints on all methods
- Docstrings explaining usage
- Example child model showing inheritance
```

---

## Prompt 2: Soft Delete Implementation

### Basic Request

```
Implement a production-ready soft delete system for Django with:

Requirements:
1. SoftDeleteManager - excludes deleted by default
2. AllObjectsManager - includes deleted for admin
3. delete() - sets deleted_at timestamp
4. hard_delete() - actually removes from DB
5. restore() - undeletes record
6. is_deleted property
7. QuerySet with bulk soft delete/restore
8. Consider unique constraints with deleted records

Provide complete, copy-paste ready code.
```

### Advanced Soft Delete

```
Extend the soft delete implementation to handle:

1. Cascading soft deletes (when parent deleted, soft delete children)
2. Unique constraints that allow same value if one is deleted
   Example: email unique among active users, but deleted users
   can have same email
3. Admin integration showing deleted records with restore action
4. Automatic hard delete after X days via management command

Include all code and migration considerations.
```

---

## Prompt 3: Multi-Tenant Model Design

### Architecture Decision

```
I need to implement multi-tenancy in Django. Help me choose and implement the right approach.

Context:
- Expected tenants: [10-100 / 100-1000 / 1000+]
- Data isolation requirement: [Strict / Moderate]
- Tenant identification: [Subdomain / Header / URL path]
- Database: [PostgreSQL / MySQL]
- Existing models: [Yes, need migration / No, greenfield]

Compare these approaches for my use case:
1. Shared schema with tenant FK
2. Schema per tenant (PostgreSQL)
3. Database per tenant

Then implement the recommended approach with:
- Tenant model
- Tenant-aware base mixin
- Middleware for tenant resolution
- Manager that auto-filters by tenant
```

### Tenant Migration

```
I have an existing Django app that I need to convert to multi-tenant.

Current state:
- [X] models without tenant awareness
- [Database type]
- [Number of existing records]

Provide:
1. Step-by-step migration plan
2. Data migration scripts
3. Code changes needed
4. Testing strategy for tenant isolation
5. Rollback plan
```

---

## Prompt 4: Audit Trail Setup

### Library Selection

```
I need to implement audit trail for Django models. Compare these options for my use case:

Requirements:
- Track: [All fields / Specific fields only]
- History access: [Frequent queries / Rare, mostly compliance]
- Database: [PostgreSQL / MySQL / SQLite]
- Performance priority: [Writes / Reads / Balanced]

Compare:
1. django-simple-history
2. django-auditlog
3. django-reversion
4. pghistory (PostgreSQL only)

Recommend one and explain why, then show implementation.
```

### Implementation

```
Implement django-simple-history for my Django project:

Models to track:
- [Model1]: All fields
- [Model2]: Exclude [field1, field2]
- [Model3]: Only track [field1, field2]

Include:
1. Installation and setup
2. Model configuration with HistoricalRecords
3. Middleware for user tracking
4. Example queries (get history, as_of, diff)
5. Admin integration
6. Performance considerations
7. Storage cleanup strategy
```

---

## Prompt 5: Custom Manager/QuerySet

### Design Pattern

```
Design a custom Manager/QuerySet system for a Django model.

Model: [ModelName]
Common query patterns:
- [Query 1: e.g., "Get active items"]
- [Query 2: e.g., "Filter by date range"]
- [Query 3: e.g., "Get items by status"]
- [Query 4: e.g., "Aggregate by category"]

Requirements:
- Methods should be chainable
- Manager should expose QuerySet methods
- Include type hints
- Support for filtering on related models

Generate the complete implementation with examples of chaining.
```

### Example for E-commerce

```
Create custom Manager/QuerySet for an e-commerce Product model:

Needed methods:
- active() - is_active=True, deleted_at=None, stock > 0
- in_category(category) - filter by category or subcategories
- price_range(min, max) - filter by price
- with_discount() - has discount > 0
- featured() - is_featured=True
- low_stock(threshold=10) - stock below threshold
- recently_added(days=30) - created in last N days
- bestsellers() - order by sales count
- search(query) - search name and description

Show:
1. QuerySet class
2. Manager class
3. Model configuration
4. Usage examples with chaining
```

---

## Prompt 6: Django 5.x Model Features

### GeneratedField Implementation

```
I want to use Django 5.x GeneratedField for computed columns.

Use cases:
1. Full name from first_name + last_name
2. Order total from quantity * unit_price
3. Discount price from price * (1 - discount_percent/100)
4. Age from date_of_birth
5. Status boolean from status enum

For each:
- Show the GeneratedField definition
- Explain db_persist=True vs False
- Note database compatibility
- Show how to query/filter on generated fields
- Migration considerations
```

### db_default Usage

```
Show how to use Django 5.x db_default for:

1. Timestamp (created_at with database NOW())
2. UUID default
3. Status default
4. Counter starting value
5. Computed default from another field

Include:
- Correct syntax
- Difference from Python default
- When to use db_default vs default
- Database-specific considerations
```

---

## Prompt 7: ForeignKey Strategy

### On Delete Decision

```
Help me decide on_delete strategy for my Django models.

Models and relationships:
1. User -> Order (user places orders)
2. Order -> OrderItem (order contains items)
3. OrderItem -> Product (item references product)
4. Task -> User (task assigned to user)
5. Comment -> User (comment author)
6. Comment -> Post (comment on post)
7. [Add your specific relationships]

For each, recommend:
- on_delete choice
- Reasoning
- Alternative if business rules change
- Any null/blank settings needed
```

### Index Optimization

```
Recommend indexes for my Django models based on query patterns.

Model: [ModelName]
Fields: [list fields with types]

Query patterns:
1. [Query 1 with filters/ordering]
2. [Query 2 with filters/ordering]
3. [Query 3 with filters/ordering]

Current indexes: [list any existing]

Recommend:
- Single-column indexes
- Composite indexes (with field order reasoning)
- Covering indexes if beneficial
- Index for unique constraints with soft delete
```

---

## Prompt 8: Model Refactoring

### Legacy to Modern

```
Refactor this legacy Django model to use modern patterns:

```python
[Paste legacy model code here]
```

Apply these improvements:
1. Add UUID for external identification
2. Add timestamps (created_at, updated_at)
3. Convert to proper FK on_delete
4. Add appropriate indexes
5. Improve field choices using TextChoices
6. Add type hints and docstrings
7. Extract common fields to base/mixin
8. Add custom manager if beneficial

Show before/after with explanation of changes.
```

### Add Multi-Tenancy

```
Add multi-tenancy to this existing model:

```python
[Paste model code here]
```

Requirements:
- Add tenant FK
- Update unique constraints to be tenant-scoped
- Add tenant-aware manager
- Keep backward compatibility with existing queries
- Migration strategy for existing data

Show modified code and migration steps.
```

---

## Prompt 9: Testing Base Models

### Test Generation

```
Generate comprehensive tests for this base model system:

```python
[Paste base model code here]
```

Include tests for:
1. UUID generation (unique, immutable)
2. Timestamp auto-population
3. Soft delete (delete, hard_delete, restore)
4. Manager filtering (objects vs all_objects)
5. QuerySet operations (bulk delete, restore)
6. Inheritance works correctly
7. String representation
8. Edge cases (delete already deleted, restore not deleted)

Use pytest with Django fixtures.
```

### Multi-Tenant Tests

```
Generate tests for tenant isolation:

```python
[Paste tenant-aware model code here]
```

Test scenarios:
1. Query returns only current tenant's data
2. Cannot access other tenant's data
3. Create auto-assigns current tenant
4. Admin can access all tenants
5. No tenant context raises error
6. Unique constraints work within tenant
```

---

## Prompt 10: Complete Project Setup

### Full Base Model System

```
Set up a complete base model system for a new Django project.

Project type: [SaaS with user workspaces]
Django: 5.2 LTS
Database: PostgreSQL
Features needed:
- UUID for external IDs
- Automatic timestamps
- Soft delete for user data
- Audit trail for sensitive models
- Multi-tenant by workspace

Generate:
1. File structure (core/models/, etc.)
2. All base models and mixins
3. All managers and querysets
4. Middleware for tenant/user context
5. Example domain model using all features
6. Tests
7. settings.py configuration
8. Initial migration notes
```

---

## Quick Reference: Prompt Patterns

| Need | Prompt Pattern |
|------|----------------|
| Design decision | "Compare X vs Y for my use case: [context]" |
| Implementation | "Generate production-ready code for [feature]" |
| Refactoring | "Improve this code: [paste], apply [patterns]" |
| Testing | "Generate tests for [code], covering [scenarios]" |
| Migration | "Convert [old pattern] to [new pattern], with migration" |
| Troubleshooting | "Debug this issue: [error], code: [paste]" |

---

## Context Variables to Include

Always provide these when asking for model design help:

```
Django version: [4.2 / 5.0 / 5.1 / 5.2]
Database: [PostgreSQL / MySQL / SQLite]
Project type: [SaaS / E-commerce / API / Internal]
Scale: [Small / Medium / Large]
Existing codebase: [Greenfield / Legacy]
Multi-tenant: [Yes / No]
Soft delete: [Yes / No]
Audit trail: [Yes / No]
API type: [REST / GraphQL / None]
Testing framework: [pytest / unittest]
```

---

*Last updated: 2026-01-25*
