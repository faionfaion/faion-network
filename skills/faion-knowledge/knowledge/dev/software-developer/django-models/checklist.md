# Checklist

## Planning Phase

- [ ] Identify all entities and relationships
- [ ] Determine field types and constraints for each entity
- [ ] Plan foreign key relationships and on_delete behavior
- [ ] Design model inheritance (if needed: abstract, multi-table, proxy)
- [ ] Identify fields that need indexes
- [ ] Plan timestamped fields (created_at, updated_at)
- [ ] Create database schema diagram

## Model Definition Phase

- [ ] Create BaseModel abstract class with uid, created_at, updated_at
- [ ] Define all models inheriting from BaseModel
- [ ] Add field validators and help_text
- [ ] Define __str__ methods for admin/debugging
- [ ] Create custom QuerySets for common filters
- [ ] Create custom Managers with queryset methods
- [ ] Add Meta options (ordering, indexes, db_table names)

## Relationships Phase

- [ ] Define ForeignKey relationships with on_delete behavior
- [ ] Define OneToOne relationships where applicable
- [ ] Define ManyToMany with through models if needed
- [ ] Use lazy string references ('app.Model') for circular deps
- [ ] Add related_name to all relationships
- [ ] Document relationship cardinality

## Constraints & Validation Phase

- [ ] Add CHECK constraints for valid values
- [ ] Add UNIQUE constraints on appropriate fields
- [ ] Implement clean() method for cross-field validation
- [ ] Add validators for field-level validation
- [ ] Test all constraints work as expected

## Indexing Phase

- [ ] Create indexes on foreign key fields
- [ ] Create indexes on frequently queried fields
- [ ] Create composite indexes for common filter combinations
- [ ] Create partial indexes for soft deletes
- [ ] Verify indexes exist in Meta.indexes

## Migrations & Testing Phase

- [ ] Run makemigrations to create initial migration
- [ ] Review migration file for correctness
- [ ] Test migration on fresh database
- [ ] Test model CRUD operations
- [ ] Test relationship queries and lazy loading
- [ ] Verify custom managers and querysets work

## Documentation Phase

- [ ] Document model relationships in project docs
- [ ] Document custom managers and querysets
- [ ] Document validation rules in code comments
- [ ] Create migrations documentation for team