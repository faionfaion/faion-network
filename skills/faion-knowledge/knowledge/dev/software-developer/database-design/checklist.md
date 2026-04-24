# Checklist

## Schema Design Phase

- [ ] Identify all entities and attributes
- [ ] Define entity relationships
- [ ] Create entity-relationship diagram
- [ ] Normalize to 3NF (normalize first, denormalize for perf)
- [ ] Define primary keys (UUIDs preferred)
- [ ] Define foreign keys and constraints
- [ ] Create schema design document

## Field Definition Phase

- [ ] Define appropriate field types
- [ ] Set field constraints (NOT NULL, CHECK)
- [ ] Add unique constraints where appropriate
- [ ] Set default values
- [ ] Add timestamps (created_at, updated_at)
- [ ] Define field lengths/precision

## Index Strategy Phase

- [ ] Create indexes on foreign keys
- [ ] Create indexes on frequently queried fields
- [ ] Create composite indexes for common filters
- [ ] Create partial indexes for soft deletes
- [ ] Analyze query patterns before indexing
- [ ] Avoid over-indexing

## Data Integrity Phase

- [ ] Define referential integrity (foreign keys)
- [ ] Define on_delete behavior (RESTRICT, CASCADE, SET_NULL)
- [ ] Add CHECK constraints for valid values
- [ ] Add UNIQUE constraints
- [ ] Implement domain constraints
- [ ] Test constraint enforcement

## Partitioning Strategy Phase

- [ ] Identify tables needing partitioning
- [ ] Choose partitioning strategy (range, hash, list)
- [ ] Define partition boundaries
- [ ] Plan partition maintenance
- [ ] Test partitioning behavior

## Soft Delete Strategy Phase

- [ ] Add deleted_at column for soft deletes
- [ ] Create views for active records
- [ ] Add partial indexes for active records
- [ ] Update queries to filter soft deletes
- [ ] Document soft delete behavior

## Audit/History Phase

- [ ] Design audit table structure
- [ ] Create triggers for audit logging
- [ ] Track changes (old/new values)
- [ ] Record who changed what and when
- [ ] Test audit logging works

## Denormalization Phase

- [ ] Identify performance bottlenecks
- [ ] Add computed/redundant columns if needed
- [ ] Use triggers to maintain denormalized data
- [ ] Document denormalization rationale
- [ ] Test denormalization consistency

## Views and Materialized Views Phase

- [ ] Create views for common queries
- [ ] Create materialized views for aggregations
- [ ] Plan refresh strategy
- [ ] Add indexes to materialized views
- [ ] Test view performance

## Migration Strategy Phase

- [ ] Use migration tools (Alembic, Liquibase)
- [ ] Create reversible migrations
- [ ] Test migrations on test database
- [ ] Plan migration for large tables
- [ ] Document migration procedures

## Testing Phase

- [ ] Test all constraints work
- [ ] Test relationships and cascades
- [ ] Test queries with proper indexes
- [ ] Load test with realistic data volume
- [ ] Test query performance
- [ ] Test soft deletes work correctly
- [ ] Test audit logging

## Documentation Phase

- [ ] Document schema and relationships
- [ ] Document indexing strategy
- [ ] Document constraints and rules
- [ ] Create schema diagrams
- [ ] Document migration procedures
- [ ] Document performance considerations

## Deployment

- [ ] Plan zero-downtime migrations
- [ ] Back up production database
- [ ] Run migrations in staging first
- [ ] Monitor migration performance
- [ ] Have rollback plan ready
- [ ] Document what was changed