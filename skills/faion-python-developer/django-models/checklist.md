# Django Model Design Checklist

## Pre-Implementation

- [ ] Model inherits from `BaseModel` (or `SoftDeleteModel` if needed)
- [ ] Model belongs to correct app (single responsibility)
- [ ] `constants.py` exists for choices/limits
- [ ] Related models identified (FK, M2M)

## Field Design

### Required Fields
- [ ] All fields have appropriate `max_length` for CharFields
- [ ] `DecimalField` uses `max_digits` and `decimal_places` (not FloatField for money)
- [ ] `blank` and `null` used correctly:
  - String fields: `blank=True`, NOT `null=True`
  - Other fields: `null=True, blank=True` together
- [ ] `default` values set where appropriate
- [ ] `choices` defined in `constants.py` using `TextChoices`/`IntegerChoices`

### ForeignKey Fields
- [ ] `on_delete` explicitly set:
  - `PROTECT` for critical data (user, order)
  - `CASCADE` only when child meaningless without parent
  - `SET_NULL` for optional references
- [ ] `related_name` explicitly set (not auto-generated)
- [ ] `related_query_name` left default (or set to `+` to disable)

### Performance Fields
- [ ] Frequently filtered fields have `db_index=True`
- [ ] UUID fields have `db_index=True`
- [ ] DateTimeField for filtering has `db_index=True`

## Model Meta

- [ ] `db_table` set explicitly (matches naming convention)
- [ ] `ordering` set (usually `['-created_at']`)
- [ ] `verbose_name` and `verbose_name_plural` if needed
- [ ] `get_latest_by` set if using `latest()`

## Indexes

- [ ] Composite indexes for common filter combinations
- [ ] Covering indexes for frequently accessed columns
- [ ] Partial indexes for filtered queries (PostgreSQL)
- [ ] No duplicate indexes (check migrations)

## Constraints

- [ ] `UniqueConstraint` for business rules
- [ ] `CheckConstraint` for data validation
- [ ] Constraints have descriptive names

## Methods

### Required
- [ ] `__str__` returns meaningful representation
- [ ] `clean()` validates cross-field rules

### Optional
- [ ] `save()` override if custom logic needed
- [ ] Properties for computed values (simple only)
- [ ] `get_absolute_url()` if model has detail view

## Validation

- [ ] Field-level validators for format/range
- [ ] `clean()` method for cross-field validation
- [ ] Constraints for database-level enforcement
- [ ] Service layer for complex business rules

## Managers and QuerySets

- [ ] Custom QuerySet for chainable filters
- [ ] Custom Manager for factory methods
- [ ] Combined using `Manager.from_queryset()`
- [ ] Default manager filters appropriately (e.g., soft delete)

## Soft Delete (if applicable)

- [ ] Inherits from `SoftDeleteModel`
- [ ] `objects` manager filters deleted
- [ ] `all_objects` manager includes deleted
- [ ] UniqueConstraints exclude deleted records
- [ ] Related models handle cascade properly

## Migration Safety

- [ ] New required fields have `default` or are nullable initially
- [ ] No data loss in field type changes
- [ ] Large table changes are backwards-compatible
- [ ] Data migrations are separate from schema migrations

## Testing

- [ ] Factory created for model (factory_boy)
- [ ] `clean()` validation tested
- [ ] Constraints tested
- [ ] Manager/QuerySet methods tested
- [ ] Soft delete behavior tested (if applicable)

## Documentation

- [ ] Docstring on model class
- [ ] Complex fields have comments
- [ ] `constants.py` has docstrings

---

## Quick Reference Card

### Field Nullability

| Field Type | Empty Value | Usage |
|------------|-------------|-------|
| CharField | `blank=True` | No null for strings |
| TextField | `blank=True` | No null for strings |
| IntegerField | `null=True, blank=True` | Null means "unknown" |
| ForeignKey | `null=True, blank=True` | Optional relation |
| DateTimeField | `null=True, blank=True` | Null means "not set" |
| BooleanField | `default=False` | Never null |

### on_delete Quick Guide

| Data Importance | on_delete | Example |
|-----------------|-----------|---------|
| Critical | `PROTECT` | User, Order, Payment |
| Owned by parent | `CASCADE` | OrderItem, Comment |
| Optional ref | `SET_NULL` | AssignedTo, LastEditor |
| Has fallback | `SET_DEFAULT` | Category (default=Uncategorized) |

### Index Quick Guide

| Query Pattern | Index Type |
|---------------|------------|
| `filter(field=x)` | `db_index=True` |
| `filter(a=x, b=y)` | `Index(fields=['a', 'b'])` |
| `filter(a=x).order_by('b')` | `Index(fields=['a', 'b'])` |
| Partial filter | `Index(condition=Q(...))` |
| Select specific cols | `Index(include=['col'])` |

### Manager vs QuerySet vs Model Method

| Logic Type | Location | Returns |
|------------|----------|---------|
| Chainable filters | QuerySet | QuerySet |
| Factory (create) | Manager | Model instance |
| Single instance logic | Model method | Varies |
| Database property | Model @property | Value |
| Complex DB property | Selector function | Value |
