# Checklist

## Planning Phase

- [ ] Analyze entity relationships and cardinality
- [ ] Design entity model hierarchy (base classes, inheritance)
- [ ] Plan lazy loading vs eager loading strategies
- [ ] Identify navigation properties and foreign keys
- [ ] Plan composite key scenarios if needed
- [ ] Design soft delete strategy (if applicable)

## Setup Phase

- [ ] Create DbContext class with DbSet properties
- [ ] Create entity classes with proper data annotations
- [ ] Create IEntityTypeConfiguration implementations
- [ ] Register configurations in DbContext.OnModelCreating()
- [ ] Create database migrations
- [ ] Test migrations on fresh database

## Implementation Phase

- [ ] Create repository interfaces with query contracts
- [ ] Implement repositories with IRepository pattern
- [ ] Use AsNoTracking() for read-only queries
- [ ] Implement Include() for eager loading of related entities
- [ ] Use projection (Select) to reduce transferred data
- [ ] Implement paging with Skip/Take
- [ ] Add query filters for soft deletes and multi-tenancy
- [ ] Create unit of work pattern if handling multiple repos

## Testing Phase

- [ ] Test all CRUD operations on each entity
- [ ] Verify relationships work (navigation properties)
- [ ] Test lazy loading behavior and N+1 queries
- [ ] Test query performance with multiple database sizes
- [ ] Verify cascade deletes work as configured
- [ ] Test soft delete functionality
- [ ] Load test with concurrent operations

## Deployment

- [ ] Document entity relationships in architecture
- [ ] Document migration procedures
- [ ] Create scripts for database rollback
- [ ] Monitor query performance in production