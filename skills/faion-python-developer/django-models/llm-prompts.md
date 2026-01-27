# LLM Prompts for Django Model Generation

Prompts for generating Django models with Claude, GPT, or other LLMs.

---

## Model Generation Prompt

### Basic Model

```
Generate a Django model for {ENTITY_NAME} with the following requirements:

Context:
- App name: {APP_NAME}
- Inherits from: BaseModel (provides uid, created_at, updated_at)
- Python version: 3.11+
- Django version: 5.x

Fields:
{LIST_YOUR_FIELDS}

Requirements:
1. Use TextChoices for status/type fields in constants.py
2. Add appropriate indexes for filtered fields
3. Add constraints for business rules
4. Include custom QuerySet with common filters
5. Include Manager with factory methods
6. Add docstrings and type hints
7. Follow HackSoft Django Styleguide patterns

Generate:
1. constants.py with choices
2. models/{entity_name}.py with model, QuerySet, Manager
```

### Example Usage

```
Generate a Django model for Product with the following requirements:

Context:
- App name: catalog
- Inherits from: BaseModel
- Python version: 3.11+
- Django version: 5.x

Fields:
- name (CharField, max 200)
- slug (SlugField, unique)
- description (TextField, optional)
- sku (CharField, max 50, unique)
- price (DecimalField, 10 digits, 2 decimals, min 0.01)
- cost (DecimalField, optional)
- category (FK to Category, PROTECT)
- status: draft, active, discontinued
- stock_quantity (PositiveInteger, default 0)
- is_featured (Boolean, default False)

Requirements:
1. Use TextChoices for status in constants.py
2. Add indexes for: status+category, category+price, is_featured+status
3. Add constraints: price >= 0.01, stock >= 0
4. QuerySet methods: active(), in_category(), in_stock(), price_range()
5. Manager method: create_draft()
6. Properties: is_in_stock, profit_margin
```

---

## Relationship Model Prompt

```
Generate Django models for a {RELATIONSHIP_TYPE} relationship:

Entities:
- {MODEL_A}: {DESCRIPTION_A}
- {MODEL_B}: {DESCRIPTION_B}

Relationship:
- Type: {one-to-many | many-to-many | self-referential}
- Through model (if M2M): {THROUGH_MODEL_NAME}
- Additional fields on relationship: {LIST_FIELDS}

Requirements:
1. Use appropriate on_delete (PROTECT for critical, CASCADE for owned children)
2. Set explicit related_name on all ForeignKeys
3. Add UniqueConstraint for M2M through models
4. Include proper indexes for common query patterns

Generate all necessary models with QuerySets and Managers.
```

### Example Usage

```
Generate Django models for a many-to-many relationship:

Entities:
- Course: Online course with title, instructor (FK to User), description
- User: Already exists in users app

Relationship:
- Type: many-to-many (User can enroll in many Courses, Course has many Users)
- Through model: Enrollment
- Additional fields: enrolled_at, completed_at, progress (0-100), grade

Requirements:
1. Course instructor uses PROTECT
2. Enrollment uses CASCADE (deleted when Course or User deleted)
3. UniqueConstraint: one enrollment per user per course
4. CheckConstraint: progress between 0 and 100
5. QuerySet: by_student(), completed(), in_progress()
```

---

## Soft Delete Model Prompt

```
Generate a Django model with soft delete support for {ENTITY_NAME}:

Context:
- App name: {APP_NAME}
- Inherits from: SoftDeleteModel
- Has relations to: {LIST_RELATED_MODELS}

Fields:
{LIST_YOUR_FIELDS}

Soft Delete Requirements:
1. Default manager excludes deleted records
2. all_objects manager includes deleted
3. Bulk delete support in QuerySet
4. restore() method on model
5. UniqueConstraint should exclude deleted records
6. Related models: {CASCADE_DELETE | PROTECT | SET_NULL}

Generate model with proper soft delete handling for all relationships.
```

---

## Migration Prompt

```
Generate a Django data migration for the following scenario:

Current State:
- Model: {MODEL_NAME}
- App: {APP_NAME}
- Field: {FIELD_NAME} is {CURRENT_STATE}

Target State:
- Field should be: {TARGET_STATE}

Requirements:
1. Must be backwards-compatible
2. No downtime during deployment
3. Handle existing data: {TRANSFORMATION_LOGIC}

Generate:
1. Schema migration (if needed)
2. Data migration with forwards_func and backwards_func
3. Any additional migrations for finalizing the change
```

### Example Usage

```
Generate a Django data migration for the following scenario:

Current State:
- Model: Order
- App: orders
- Field: status is CharField with values 'new', 'processing', 'done'

Target State:
- Field should use new values: 'pending', 'processing', 'completed'
- Map: 'new' -> 'pending', 'done' -> 'completed'

Requirements:
1. Backwards-compatible (old values should still work until fully deployed)
2. Handle existing data by mapping old values to new
3. After migration, only new values should be valid

Generate:
1. Data migration to transform existing values
2. Update to choices in constants.py
```

---

## QuerySet Optimization Prompt

```
Optimize the following Django QuerySet for {USE_CASE}:

Current Query:
```python
{CURRENT_QUERY_CODE}
```

Context:
- Table size: ~{ROW_COUNT} rows
- Common filters: {LIST_FILTERS}
- Performance issue: {DESCRIBE_ISSUE}

Requirements:
1. Reduce N+1 queries
2. Add appropriate indexes
3. Use select_related/prefetch_related
4. Consider database-level optimizations

Generate:
1. Optimized QuerySet method
2. Required index definitions
3. Explanation of optimizations
```

---

## Model Refactoring Prompt

```
Refactor the following Django model following best practices:

Current Model:
```python
{PASTE_CURRENT_MODEL}
```

Issues to Address:
{LIST_ISSUES}

Refactoring Requirements:
1. Extract choices to constants.py
2. Add custom QuerySet for common filters
3. Add Manager with factory methods
4. Improve indexes based on query patterns
5. Add proper constraints
6. Follow HackSoft patterns (thin models, services for logic)

Generate:
1. Refactored constants.py
2. Refactored model with QuerySet and Manager
3. Any services.py functions for business logic
```

---

## Full App Generation Prompt

```
Generate a complete Django app structure for {DOMAIN}:

Domain Description:
{DESCRIBE_THE_DOMAIN}

Entities:
{LIST_ALL_ENTITIES_WITH_RELATIONSHIPS}

Requirements:
1. Follow HackSoft Django Styleguide
2. Use BaseModel for all models
3. Use SoftDeleteModel where appropriate
4. Include constants.py with all choices
5. Include custom QuerySets and Managers
6. Include services.py with business logic
7. Include selectors.py for complex queries

Generate complete file structure with:
- models/__init__.py (imports)
- models/{entity}.py (for each entity)
- constants.py
- services.py
- selectors.py
- admin.py (basic registration)
```

### Example Usage

```
Generate a complete Django app structure for an E-commerce Catalog:

Domain Description:
Product catalog with categories, products, and product variants.
Categories are hierarchical (self-referential).
Products can have multiple variants (size, color).
Products can be featured and have different statuses.

Entities:
1. Category: name, slug, parent (self-ref), level
2. Product: name, slug, description, category (FK), status, is_featured
3. ProductVariant: product (FK, CASCADE), sku, price, stock, attributes (JSON)
4. ProductImage: product (FK, CASCADE), image_url, is_primary, position

Requirements:
1. Category uses CASCADE for children
2. Product uses PROTECT for category
3. ProductVariant and ProductImage use CASCADE
4. SoftDeleteModel for Product only
5. QuerySet methods for filtering and aggregation
6. Services for: product_create, product_update, variant_create
7. Selectors for: get_products_by_category_tree, get_featured_products
```

---

## Prompt Tips

### Be Specific About Versions

```
Django version: 5.x (use GeneratedField, db_default if appropriate)
Python version: 3.11+ (use modern type hints: list[], dict[], X | None)
```

### Specify Patterns

```
Follow HackSoft Django Styleguide:
- Thin models (no business logic in models)
- Services for writes (create, update, delete operations)
- Selectors for complex reads (multiple joins, aggregations)
- Model clean() only for simple cross-field validation
```

### Include Context

```
Existing Models:
- User (in users app)
- BaseModel (in core.models)
- SoftDeleteModel (in core.models)

Existing Constants:
- MAX_PRICE = 999999.99
- DEFAULT_PAGE_SIZE = 20
```

### Request Specific Outputs

```
Generate:
1. constants.py (complete file)
2. models/{name}.py (complete file with imports)
3. __init__.py (with exports)
4. Example usage in services.py
```
