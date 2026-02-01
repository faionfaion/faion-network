# Data Modeling

Designing database schemas and data structures for optimal performance, scalability, and maintainability.

## Overview

Data modeling is the process of creating a visual representation of data structures, their relationships, and constraints. It bridges business requirements and technical implementation, ensuring data is organized, consistent, and accessible.

## Three Levels of Data Modeling

| Level | Purpose | Audience | Detail |
|-------|---------|----------|--------|
| **Conceptual** | What entities exist | Business stakeholders | High-level, no technical details |
| **Logical** | How data is organized | Data architects, analysts | Attributes, relationships, normalization |
| **Physical** | How data is stored | DBAs, developers | Tables, columns, indexes, data types |

### Conceptual Model

Focuses on business entities and their relationships without technical implementation details.

```
Customer --- places ---> Order
Order --- contains ---> Product
Product --- belongs to ---> Category
```

**Key characteristics:**
- Entity names only (no attributes)
- High-level relationships
- Technology-agnostic
- Stakeholder communication tool

### Logical Model

Adds structure: attributes, keys, normalization, and detailed relationships.

**Key characteristics:**
- Entities with full attribute lists
- Primary and foreign keys defined
- Normalized to 3NF (typically)
- Cardinality specified (1:1, 1:N, M:N)
- Still technology-agnostic

### Physical Model

Database-specific implementation with data types, indexes, and constraints.

**Key characteristics:**
- Table and column names
- Data types and lengths
- Indexes and constraints
- Storage parameters
- Partitioning strategy

## Data Modeling Paradigms

### Relational (SQL)

Traditional normalized approach for transactional systems.

| Strength | Weakness |
|----------|----------|
| ACID compliance | Complex joins at scale |
| Data integrity | Vertical scaling limits |
| Mature tooling | Schema rigidity |

**When to use:** OLTP systems, financial data, structured data with complex relationships.

### Document (NoSQL)

Flexible schema, stores data as JSON/BSON documents.

| Strength | Weakness |
|----------|----------|
| Schema flexibility | Denormalization complexity |
| Horizontal scaling | No cross-document transactions (some DBs) |
| Developer-friendly | Query limitations |

**When to use:** Content management, user profiles, catalogs, event logging.

### Key-Value

Simplest model: unique keys mapped to values.

| Strength | Weakness |
|----------|----------|
| Extreme performance | No complex queries |
| Easy horizontal scaling | Value opacity |
| Low latency | No relationships |

**When to use:** Session storage, caching, real-time leaderboards.

### Wide-Column

Column families with flexible schemas per row.

| Strength | Weakness |
|----------|----------|
| High write throughput | Query-driven design required |
| Horizontal scaling | Learning curve |
| Time-series optimized | Limited ad-hoc queries |

**When to use:** Time-series data, IoT, analytics, high-write workloads.

### Graph

Nodes and edges for highly connected data.

| Strength | Weakness |
|----------|----------|
| Relationship traversal | Not for bulk analytics |
| Pattern matching | Scaling complexity |
| Flexible schema | Learning curve |

**When to use:** Social networks, fraud detection, recommendation engines, knowledge graphs.

### Time-Series

Optimized for timestamped data points.

| Strength | Weakness |
|----------|----------|
| Time-based queries | Limited for non-time data |
| Compression | Specific use case |
| Aggregation functions | May need companion DB |

**When to use:** Monitoring, IoT sensors, financial ticks, application metrics.

## Core Concepts

### Normalization (Relational)

| Form | Rule | Purpose |
|------|------|---------|
| 1NF | Atomic values, no repeating groups | Eliminate multi-valued columns |
| 2NF | 1NF + No partial dependencies | Remove dependencies on partial key |
| 3NF | 2NF + No transitive dependencies | Remove indirect dependencies |
| BCNF | Every determinant is a candidate key | Stricter 3NF |
| 4NF | No multi-valued dependencies | Handle independent multi-valued facts |
| 5NF | No join dependencies | Lossless decomposition |

**Practical guidance:** 3NF is sufficient for most OLTP systems. Over-normalization creates join overhead.

### Denormalization

Intentionally adding redundancy to improve read performance.

**When to denormalize:**
- Read-heavy workloads (>90% reads)
- Frequent expensive joins
- Reporting/analytics requirements
- Real-time query needs

**Denormalization techniques:**
- Store calculated fields
- Duplicate reference data
- Pre-aggregate statistics
- Flatten hierarchies

### Entity-Relationship (ER) Modeling

| Relationship | Notation | Example |
|--------------|----------|---------|
| One-to-One (1:1) | User --- Profile | Each user has exactly one profile |
| One-to-Many (1:N) | User --< Orders | User places many orders |
| Many-to-Many (M:N) | Students >--< Courses | Requires junction table |

### Cardinality and Optionality

- **Cardinality:** How many (one, many)
- **Optionality:** Required or optional (0..1, 1..*)

## Advanced Patterns

### Slowly Changing Dimensions (SCD)

Handling historical changes in dimension tables.

| Type | Strategy | Use Case |
|------|----------|----------|
| Type 0 | Never change | Date of birth, original values |
| Type 1 | Overwrite | Error corrections, no history needed |
| Type 2 | Add row with versioning | Full history tracking |
| Type 3 | Add previous column | Limited history (current + previous) |
| Type 4 | Separate history table | Performance optimization |
| Type 6 | Hybrid (1+2+3) | Current value + full history |

### Data Vault 2.0

Modern data warehouse methodology for enterprise data.

**Core components:**
- **Hubs:** Business keys (Customer ID, Product ID)
- **Links:** Relationships between hubs
- **Satellites:** Descriptive attributes with history

**Benefits:**
- Audit-ready with full lineage
- Agile and incremental loading
- Parallel development
- Source-system agnostic

### Polyglot Persistence

Using multiple database technologies in one system.

```
E-commerce Example:
- PostgreSQL     -> Orders, inventory (ACID)
- Redis          -> Session, cache
- Elasticsearch  -> Product search
- Neo4j          -> Recommendations
- ClickHouse     -> Analytics
```

**Design principles:**
- Match data to optimal storage
- Define clear boundaries
- Plan for data synchronization
- Consider operational complexity

## Database-Specific Modeling

### PostgreSQL / MySQL (Relational)

- Normalize to 3NF for OLTP
- Use appropriate data types (don't use TEXT for everything)
- Design indexes based on query patterns
- Consider partitioning for large tables

### MongoDB (Document)

- Design for access patterns, not entities
- Embed data that's accessed together
- Reference data that changes independently
- Avoid deeply nested documents (16MB limit)

### Cassandra / ScyllaDB (Wide-Column)

- Query-first design: know your queries before modeling
- Partition keys for data distribution
- Clustering columns for sorting
- Denormalize: no joins available
- One table per query pattern

### Neo4j (Graph)

- Start with ontology, not CSV structure
- Nodes for nouns, relationships for verbs
- Store properties on relationships when relevant
- Design for traversal patterns
- Keep relationship types semantic

### TimescaleDB / InfluxDB (Time-Series)

- Hypertables/measurements for time partitioning
- Choose appropriate time intervals
- Consider retention policies
- Pre-aggregate for historical queries
- Tag vs field design (indexed vs data)

## LLM-Assisted Data Modeling

### Effective Approaches

1. **Start with requirements:** Provide business context before asking for schemas
2. **Iterate incrementally:** Build conceptual -> logical -> physical
3. **Specify constraints:** Mention scale, access patterns, consistency needs
4. **Request alternatives:** Ask for trade-off analysis
5. **Validate with examples:** Provide sample data or queries

### LLM Strengths

- Rapid schema generation
- Pattern recognition and suggestions
- Normalization/denormalization analysis
- Index recommendations
- Migration script generation
- Documentation creation

### LLM Limitations

- Cannot validate against real data volumes
- May suggest outdated patterns
- Needs domain context for good designs
- Cannot benchmark actual performance
- May miss subtle business rules

## Tools and Resources

### Data Modeling Tools

| Tool | Type | Best For |
|------|------|----------|
| [dbdiagram.io](https://dbdiagram.io) | Web | Quick ERD creation |
| [Hackolade](https://hackolade.com) | Desktop | Multi-database modeling |
| [SqlDBM](https://sqldbm.com) | Web | Cloud-first teams |
| [pgModeler](https://pgmodeler.io) | Desktop | PostgreSQL specialists |
| [DBeaver](https://dbeaver.io) | Desktop | Multi-database, free |
| [Lucidchart](https://lucidchart.com) | Web | Collaborative diagrams |

### Design Validation

- Query pattern testing
- Load testing with realistic data volumes
- Access pattern simulation
- Index effectiveness analysis

## Decision Framework

### Choosing a Data Model

```
1. What are the primary access patterns?
   - Point lookups -> Key-Value or Document
   - Complex queries -> Relational or Graph
   - Time-based -> Time-Series
   - Write-heavy -> Wide-Column

2. What consistency requirements exist?
   - Strong ACID -> Relational
   - Eventual consistency acceptable -> NoSQL

3. What is the data structure?
   - Highly structured -> Relational
   - Semi-structured -> Document
   - Highly connected -> Graph
   - Time-series -> Time-Series DB

4. What is the scale?
   - Vertical scaling OK -> Relational
   - Horizontal scaling needed -> NoSQL
```


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step data modeling checklist |
| [examples.md](examples.md) | Real-world data model examples |
| [templates.md](templates.md) | Copy-paste patterns and schemas |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted modeling |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [database-selection/](../database-selection/) | Choosing the right database |
| [caching-architecture/](../caching-architecture/) | Performance layer design |
| [system-design-process/](../system-design-process/) | Overall system design |

## External References

- [Data Modeling Best Practices 2025](https://datacrossroads.nl/2025/07/09/data-architecture-and-modeling-trends-in-2025/)
- [Data Vault 2.0 Guide](https://coalesce.io/data-insights/data-vault-2-0-the-complete-implementation-guide/)
- [NoSQL Data Architecture Patterns](https://www.geeksforgeeks.org/dbms/nosql-data-architecture-patterns/)
- [Slowly Changing Dimensions Guide](https://www.datacamp.com/tutorial/mastering-slowly-changing-dimensions-scd)
- [Neo4j Knowledge Graph Design](https://medium.com/@vdondeti.naidu/designing-a-knowledge-graph-with-neo4j-ontology-data-modeling-and-real-world-graph-thinking-77b29a02a217)
- [Time-Series Database Comparison 2025](https://markaicode.com/time-series-data-influxdb-timescaledb-comparison/)
- [Polyglot Persistence Patterns](https://medium.com/@rachoork/polyglot-persistence-a-strategic-approach-to-modern-data-architecture-e2a4f957f50b)
