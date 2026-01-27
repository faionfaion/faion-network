# Data Modeling Checklist

Step-by-step checklist for data modeling projects, from requirements gathering to implementation.

## Phase 1: Requirements Gathering

### Business Understanding

- [ ] Identify key business entities and their definitions
- [ ] Document business processes that generate/consume data
- [ ] Understand business rules and constraints
- [ ] Identify regulatory and compliance requirements (GDPR, HIPAA, SOX)
- [ ] Determine data retention policies
- [ ] Document data ownership and stewardship

### Access Patterns

- [ ] List primary read operations (queries)
- [ ] List primary write operations (inserts, updates, deletes)
- [ ] Estimate read/write ratio (e.g., 90/10, 50/50)
- [ ] Identify real-time vs batch access needs
- [ ] Document reporting and analytics requirements
- [ ] Identify search and filtering patterns

### Scale Requirements

- [ ] Estimate current data volume (rows, documents, size)
- [ ] Project growth rate (1 year, 3 years, 5 years)
- [ ] Estimate transaction volume (TPS for reads/writes)
- [ ] Identify peak load patterns
- [ ] Document latency requirements (p50, p95, p99)
- [ ] Determine availability requirements (99.9%, 99.99%)

### Consistency Requirements

- [ ] Identify ACID requirements per entity/operation
- [ ] Determine acceptable eventual consistency windows
- [ ] Document cross-entity transaction needs
- [ ] Identify idempotency requirements
- [ ] Define conflict resolution strategies

---

## Phase 2: Conceptual Modeling

### Entity Identification

- [ ] List all business entities (nouns from requirements)
- [ ] Define each entity in business terms
- [ ] Identify entity boundaries (what belongs where)
- [ ] Distinguish entities from attributes
- [ ] Identify aggregate roots (DDD)

### Relationship Discovery

- [ ] Map relationships between entities
- [ ] Determine cardinality (1:1, 1:N, M:N)
- [ ] Determine optionality (required vs optional)
- [ ] Identify recursive/self-referential relationships
- [ ] Document relationship semantics (verbs)

### Conceptual Diagram

- [ ] Create high-level ERD with entities and relationships
- [ ] Validate with business stakeholders
- [ ] Document assumptions and decisions
- [ ] Get stakeholder sign-off

---

## Phase 3: Logical Modeling

### Attribute Definition

- [ ] List all attributes for each entity
- [ ] Define attribute data types (at logical level)
- [ ] Identify nullable vs required attributes
- [ ] Define default values
- [ ] Document attribute constraints

### Key Design

- [ ] Define primary keys (natural vs surrogate)
- [ ] Identify candidate keys (alternate unique identifiers)
- [ ] Define foreign keys for relationships
- [ ] Document composite key requirements

### Normalization

- [ ] Apply 1NF: Eliminate repeating groups
- [ ] Apply 2NF: Remove partial dependencies
- [ ] Apply 3NF: Remove transitive dependencies
- [ ] Consider BCNF if needed
- [ ] Document normalization decisions

### Denormalization Analysis

- [ ] Identify read-heavy access patterns
- [ ] Analyze join complexity and frequency
- [ ] Determine denormalization candidates
- [ ] Document trade-offs (storage vs performance)
- [ ] Plan data synchronization strategy

### Logical Diagram

- [ ] Create detailed ERD with attributes
- [ ] Include cardinality notation
- [ ] Document domain rules
- [ ] Review with data team

---

## Phase 4: Physical Modeling

### Database Selection

- [ ] Choose database technology (see [database-selection/](../database-selection/))
- [ ] Validate technology against requirements
- [ ] Consider polyglot persistence if needed
- [ ] Document selection rationale (ADR)

### Table/Collection Design

- [ ] Map logical entities to physical tables/collections
- [ ] Define table names (naming convention)
- [ ] Define column names and data types
- [ ] Specify column lengths and precision
- [ ] Set NULL/NOT NULL constraints

### Key Implementation

- [ ] Create primary key columns/constraints
- [ ] Create foreign key constraints (if supported)
- [ ] Define unique constraints
- [ ] Consider composite keys vs single-column

### Index Strategy

- [ ] Identify columns for index creation
- [ ] Design composite indexes based on query patterns
- [ ] Consider partial/filtered indexes
- [ ] Evaluate covering indexes for hot queries
- [ ] Plan index maintenance strategy
- [ ] Document index overhead expectations

### Partitioning

- [ ] Evaluate partitioning need (data volume threshold)
- [ ] Choose partition strategy (range, hash, list)
- [ ] Define partition key
- [ ] Plan partition maintenance (retention, archival)
- [ ] Test cross-partition query performance

---

## Phase 5: Database-Specific Considerations

### Relational (PostgreSQL, MySQL, SQL Server)

- [ ] Finalize table schemas with exact data types
- [ ] Create foreign key relationships with ON DELETE/UPDATE actions
- [ ] Design check constraints
- [ ] Plan triggers if needed (avoid if possible)
- [ ] Consider views for complex queries
- [ ] Plan stored procedures (if used)
- [ ] Define sequences for auto-increment

### Document (MongoDB, DynamoDB)

- [ ] Design document structure (embedding vs referencing)
- [ ] Define collection/table names
- [ ] Plan index strategy (compound, multikey, text)
- [ ] Consider TTL indexes for expiring data
- [ ] Design shard key (if sharding)
- [ ] Document schema validation rules

### Wide-Column (Cassandra, ScyllaDB)

- [ ] Design tables for each query (query-first design)
- [ ] Define partition keys for data distribution
- [ ] Define clustering columns for ordering
- [ ] Plan for data duplication across tables
- [ ] Consider materialized views
- [ ] Define compaction strategy
- [ ] Plan TTL for data expiration

### Graph (Neo4j)

- [ ] Design node labels and properties
- [ ] Design relationship types and properties
- [ ] Plan for index on frequently queried properties
- [ ] Consider full-text indexes
- [ ] Design constraints (uniqueness, existence)
- [ ] Plan for graph projections (GDS)

### Time-Series (TimescaleDB, InfluxDB)

- [ ] Design hypertable/measurement schema
- [ ] Define time partitioning interval
- [ ] Plan tag (indexed) vs field (data) columns
- [ ] Design continuous aggregates/views
- [ ] Define retention policies
- [ ] Plan compression strategy
- [ ] Consider data tiering (hot/warm/cold)

---

## Phase 6: Data Warehouse Specific

### Dimensional Modeling

- [ ] Identify fact tables (events, transactions)
- [ ] Identify dimension tables (descriptive)
- [ ] Design star or snowflake schema
- [ ] Define grain (level of detail) for fact tables
- [ ] Choose SCD type for each dimension attribute
- [ ] Design date dimension with all needed attributes

### Data Vault 2.0

- [ ] Identify business keys for Hubs
- [ ] Design Hub tables with hash keys
- [ ] Identify relationships for Links
- [ ] Design Link tables with hash keys
- [ ] Design Satellites for descriptive data
- [ ] Plan load date and record source tracking
- [ ] Design Point-in-Time tables for performance
- [ ] Design Bridge tables for M:N relationships

### Slowly Changing Dimensions

- [ ] Categorize each dimension attribute by SCD type
- [ ] Implement Type 2 tracking columns (valid_from, valid_to, is_current)
- [ ] Plan ETL logic for SCD handling
- [ ] Consider hash-based change detection
- [ ] Document historical tracking requirements

---

## Phase 7: Data Quality and Governance

### Data Quality Rules

- [ ] Define domain constraints (valid values)
- [ ] Define range constraints (min/max)
- [ ] Define format constraints (email, phone, etc.)
- [ ] Define referential integrity rules
- [ ] Plan data validation in ETL/application

### Metadata Management

- [ ] Document table/column descriptions
- [ ] Define data lineage
- [ ] Create data dictionary
- [ ] Tag sensitive data (PII, PHI)
- [ ] Document data owners

### Security

- [ ] Identify PII/sensitive columns
- [ ] Plan encryption (at rest, in transit)
- [ ] Design access control (RBAC)
- [ ] Plan data masking for non-prod
- [ ] Document compliance requirements

---

## Phase 8: Implementation

### Schema Creation

- [ ] Generate DDL scripts
- [ ] Review scripts with team
- [ ] Execute in development environment
- [ ] Validate schema correctness
- [ ] Document any deviations from logical model

### Data Migration

- [ ] Create migration scripts
- [ ] Plan data transformation logic
- [ ] Test with sample data
- [ ] Plan rollback strategy
- [ ] Document migration runbook

### Testing

- [ ] Test CRUD operations
- [ ] Test complex queries
- [ ] Test with realistic data volumes
- [ ] Benchmark query performance
- [ ] Test concurrent access
- [ ] Test failure scenarios

---

## Phase 9: Operations

### Monitoring

- [ ] Set up query performance monitoring
- [ ] Monitor table/index sizes
- [ ] Track slow queries
- [ ] Monitor connection pools
- [ ] Set up alerting thresholds

### Maintenance

- [ ] Plan index rebuild/reorganize schedule
- [ ] Plan statistics update schedule
- [ ] Plan backup and recovery procedures
- [ ] Document disaster recovery process
- [ ] Plan capacity reviews

### Evolution

- [ ] Document schema change process
- [ ] Plan for backward compatibility
- [ ] Version control database schemas
- [ ] Plan for online schema changes
- [ ] Document deprecation process

---

## Quick Reference: Common Pitfalls

### Avoid These Mistakes

| Pitfall | Solution |
|---------|----------|
| Skipping logical model | Always go conceptual -> logical -> physical |
| Over-normalizing | Balance with access patterns |
| Under-normalizing | At least reach 3NF for OLTP |
| Wrong data types | Use appropriate types (don't over-use TEXT) |
| Missing indexes | Index based on query patterns |
| Too many indexes | Balance read vs write performance |
| Ignoring NULL semantics | Be explicit about nullable columns |
| No naming convention | Establish and enforce standards |
| Skipping documentation | Document as you go |
| No access pattern analysis | Query-first design |

### Red Flags in Reviews

- [ ] Tables with 50+ columns (consider splitting)
- [ ] No primary key defined
- [ ] All columns nullable
- [ ] Missing foreign key relationships
- [ ] Index on every column
- [ ] No index strategy documented
- [ ] Storing formatted data (dates as strings)
- [ ] Using reserved words as names
- [ ] No version control for schemas
- [ ] No data dictionary

---

## Checklist by Database Type

### Relational Database Checklist

```
[ ] Schema design complete
[ ] All tables have primary keys
[ ] Foreign keys defined with appropriate actions
[ ] Indexes created for query patterns
[ ] Constraints (CHECK, UNIQUE) defined
[ ] Data types optimized
[ ] Naming conventions followed
[ ] Documentation complete
```

### Document Database Checklist

```
[ ] Document structure designed
[ ] Embedding vs referencing decisions made
[ ] Indexes created for queries
[ ] Shard key designed (if applicable)
[ ] Schema validation rules defined
[ ] Access patterns documented
[ ] Document size validated
```

### Wide-Column Database Checklist

```
[ ] Query patterns defined first
[ ] Tables designed per query
[ ] Partition keys chosen carefully
[ ] Clustering columns defined
[ ] Data duplication planned
[ ] Compaction strategy chosen
[ ] TTL configured if needed
```

### Graph Database Checklist

```
[ ] Ontology designed first
[ ] Node labels defined
[ ] Relationship types defined
[ ] Properties placed correctly (node vs relationship)
[ ] Indexes on frequently queried properties
[ ] Constraints defined
[ ] Traversal patterns documented
```

### Time-Series Database Checklist

```
[ ] Measurement/hypertable schema designed
[ ] Time partitioning interval chosen
[ ] Tags vs fields categorized
[ ] Retention policies defined
[ ] Compression configured
[ ] Continuous aggregates planned
[ ] Downsampling strategy defined
```
