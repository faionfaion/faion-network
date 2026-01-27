# Django Base Model Design Checklist

Step-by-step checklist for designing and implementing base models in Django projects.

---

## Phase 1: Requirements Analysis

### 1.1 Identify Common Fields

- [ ] Do all/most models need timestamps (created_at, updated_at)?
- [ ] Do you need external-facing UUIDs (API exposure)?
- [ ] Do you need soft delete functionality?
- [ ] Do you need audit trail (who changed what, when)?
- [ ] Is this a multi-tenant application?
- [ ] Do you need optimistic locking (version field)?

### 1.2 Determine UUID Strategy

- [ ] **Option A:** Integer PK + separate `uid` field (recommended)
- [ ] **Option B:** UUID as primary key (distributed systems)
- [ ] Document the decision and rationale

### 1.3 Identify Inheritance Pattern

- [ ] **Abstract base class** - shared fields, no DB table
- [ ] **Multi-table inheritance** - separate tables with FK
- [ ] **Proxy model** - same table, different behavior
- [ ] Document which pattern and why

---

## Phase 2: Base Model Design

### 2.1 Create Core Base Model

- [ ] Create `core/models.py` or `common/models.py`
- [ ] Define BaseModel with:
  - [ ] UUID field (if needed)
  - [ ] created_at (auto_now_add=True)
  - [ ] updated_at (auto_now=True)
  - [ ] `class Meta: abstract = True`
  - [ ] Default ordering
  - [ ] `__str__` method

### 2.2 Design Mixin Hierarchy

- [ ] TimestampMixin (if lightweight timestamps needed)
- [ ] UUIDMixin (if UUID separate from timestamps)
- [ ] SoftDeleteMixin (if soft delete needed)
- [ ] AuditMixin (if audit trail needed)
- [ ] TenantMixin (if multi-tenant)
- [ ] Document mixin combination order

### 2.3 Define Custom Managers

- [ ] Default manager (filters deleted if soft delete)
- [ ] AllObjects manager (includes soft deleted)
- [ ] Consider QuerySet.as_manager() pattern
- [ ] Document manager inheritance behavior

---

## Phase 3: Soft Delete Implementation

### 3.1 Soft Delete Manager

- [ ] Create SoftDeleteManager extending models.Manager
- [ ] Override get_queryset() to filter deleted_at__isnull=True
- [ ] Create AllObjectsManager for admin access

### 3.2 Soft Delete Model

- [ ] Add deleted_at field (DateTimeField, null=True, indexed)
- [ ] Override delete() method
- [ ] Implement hard_delete() method
- [ ] Implement restore() method
- [ ] Add is_deleted property

### 3.3 Soft Delete Considerations

- [ ] Handle cascading soft deletes (related models)
- [ ] Update unique constraints (include deleted_at)
- [ ] Handle admin interface (show deleted items)
- [ ] Document restore behavior for FK relations

---

## Phase 4: Audit Trail Setup

### 4.1 Choose Audit Library

- [ ] **django-simple-history** - full snapshots, easy setup
- [ ] **django-auditlog** - JSONB diffs, better performance
- [ ] **pghistory** - PostgreSQL triggers (if Postgres only)
- [ ] Document choice and rationale

### 4.2 Configure Audit Trail

- [ ] Install chosen library
- [ ] Add to INSTALLED_APPS
- [ ] Run migrations
- [ ] Add HistoricalRecords to models
- [ ] Configure user tracking middleware

### 4.3 Audit Trail Verification

- [ ] Test create history entry
- [ ] Test update history entry
- [ ] Test delete history entry
- [ ] Verify user is captured
- [ ] Test history reverting

---

## Phase 5: Multi-Tenant Setup

### 5.1 Choose Tenant Strategy

- [ ] **Shared schema** (row-level) - recommended for most
- [ ] **Schema per tenant** - PostgreSQL schemas
- [ ] **Database per tenant** - maximum isolation
- [ ] Document choice and rationale

### 5.2 Implement Tenant Awareness

- [ ] Create Tenant model
- [ ] Create TenantAwareModel mixin
- [ ] Add tenant FK to tenant-scoped models
- [ ] Create TenantManager with filtering

### 5.3 Tenant Middleware

- [ ] Create middleware to extract tenant from request
- [ ] Store current tenant in thread-local or context
- [ ] Implement get_current_tenant() helper
- [ ] Handle tenant-less requests (public views)

### 5.4 Tenant Security

- [ ] Verify all queries are tenant-filtered
- [ ] Add unique_together constraints with tenant
- [ ] Test cross-tenant data isolation
- [ ] Document admin superuser access

---

## Phase 6: ForeignKey Design

### 6.1 Determine on_delete Behavior

For each ForeignKey:

- [ ] **PROTECT** - for critical data (orders, transactions)
- [ ] **CASCADE** - for child-only-with-parent (order items)
- [ ] **SET_NULL** - for optional references (assigned_to)
- [ ] **SET_DEFAULT** - rarely used
- [ ] **DO_NOTHING** - database handles (use carefully)

### 6.2 Configure Related Names

- [ ] Use descriptive related_name (not default)
- [ ] Use related_query_name if needed
- [ ] Consider '%(class)s_set' for abstract models

### 6.3 Index Optimization

- [ ] Index FK fields (usually automatic)
- [ ] Add composite indexes for common queries
- [ ] Consider covering indexes for read-heavy models

---

## Phase 7: Django 5.x Features

### 7.1 Use db_default Where Appropriate

- [ ] Database-level defaults for timestamps
- [ ] Database-level defaults for UUIDs
- [ ] Database-level defaults for status fields

### 7.2 Use GeneratedField for Computed Columns

- [ ] Identify computed fields (full_name, total, etc.)
- [ ] Choose db_persist=True for PostgreSQL
- [ ] Add indexes if querying computed fields
- [ ] Test migration works correctly

### 7.3 Use CharField without max_length (SQLite)

- [ ] For SQLite projects, max_length optional in 5.2+
- [ ] Keep max_length for PostgreSQL/MySQL

---

## Phase 8: Testing

### 8.1 Unit Tests for Base Model

- [ ] Test UUID generation
- [ ] Test auto timestamps
- [ ] Test __str__ method
- [ ] Test default ordering

### 8.2 Soft Delete Tests

- [ ] Test delete() performs soft delete
- [ ] Test hard_delete() removes from DB
- [ ] Test restore() works correctly
- [ ] Test default manager excludes deleted
- [ ] Test all_objects includes deleted

### 8.3 Manager Tests

- [ ] Test custom queryset methods
- [ ] Test manager methods
- [ ] Test chaining works correctly
- [ ] Test inheritance behavior

### 8.4 Multi-Tenant Tests

- [ ] Test tenant isolation
- [ ] Test cross-tenant access denied
- [ ] Test admin access to all tenants
- [ ] Test tenant auto-assignment on create

---

## Phase 9: Documentation

### 9.1 Code Documentation

- [ ] Docstrings on all base models
- [ ] Docstrings on all managers
- [ ] Docstrings on all mixins
- [ ] Type hints on all methods

### 9.2 Developer Documentation

- [ ] Document inheritance hierarchy
- [ ] Document when to use which base
- [ ] Document FK conventions
- [ ] Document manager usage
- [ ] Add examples for common patterns

### 9.3 Architecture Decision Records

- [ ] ADR for UUID strategy
- [ ] ADR for soft delete approach
- [ ] ADR for multi-tenant architecture
- [ ] ADR for audit trail choice

---

## Phase 10: Migration and Deployment

### 10.1 Pre-Migration

- [ ] Backup database
- [ ] Test migrations on copy of prod data
- [ ] Plan for downtime (if needed)
- [ ] Document rollback procedure

### 10.2 Migration Execution

- [ ] Apply migrations in order
- [ ] Verify indexes created
- [ ] Verify constraints applied
- [ ] Run data migrations (if any)

### 10.3 Post-Migration

- [ ] Verify all models work correctly
- [ ] Run full test suite
- [ ] Check query performance
- [ ] Monitor for errors

---

## Quick Reference: Decision Matrix

| Requirement | Solution |
|-------------|----------|
| External IDs for API | Add `uid` UUIDField (not as PK) |
| Track changes | django-simple-history or django-auditlog |
| Recoverable delete | SoftDeleteMixin with deleted_at |
| Multi-tenant | TenantAwareModel with FK |
| Computed columns | Django 5.x GeneratedField |
| Timestamp audit | auto_now_add + auto_now |
| FK protection | on_delete=PROTECT for important data |

---

## Common Mistakes to Avoid

| Mistake | Prevention |
|---------|------------|
| UUID as PK at scale | Use integer PK + separate uid field |
| No index on uid | Always add db_index=True |
| CASCADE on important data | Use PROTECT for orders, users |
| Exposing integer IDs | Always use uid in API serializers |
| Forgetting soft delete in unique | Add deleted_at to unique_together |
| No manager for deleted | Always provide all_objects manager |
| Tenant leak | Always test cross-tenant isolation |

---

*Last updated: 2026-01-25*
