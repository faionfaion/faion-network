# Data Modeling

## Summary

Data modeling is the discipline of designing data structures, their relationships, and constraints at three levels: conceptual (entities and relationships in business terms), logical (normalized attributes, keys, cardinality), and physical (tables, indexes, data types for a specific engine). Always progress conceptual → logical → physical; skipping the logical level leads to unmaintainable physical schemas.

## Why

Access patterns, consistency requirements, and data structure shape determine the correct database paradigm. A relational schema optimized for OLTP becomes a bottleneck for time-series workloads; a Cassandra table designed without query-first thinking becomes unqueryable. Poor physical modeling — wrong data types, missing indexes, no partitioning strategy — is the most common source of production performance failures.

## When To Use

- Designing any new persistent data layer (greenfield or migration)
- Choosing between database paradigms (relational, document, wide-column, graph, time-series)
- Normalizing an existing schema that has update anomalies or data duplication
- Designing analytical schemas (star schema, Data Vault 2.0, SCD)
- Adding an index strategy or partitioning plan before a table grows beyond 10M rows
- Modeling polyglot persistence: assigning each data domain to its optimal store

## When NOT To Use

- Throwaway scripts or single-use data processing where schema design is irrelevant
- Caching layer design (Redis key schema) — use caching-architecture methodology instead
- Event schema design for message buses — use event-driven-architecture methodology
- When a migration-first approach (Alembic, Flyway) is the actual deliverable — this methodology informs *what* to migrate, not *how* to run migrations

## Content

| File | What's inside |
|------|---------------|
| `content/01-levels-and-paradigms.xml` | Three modeling levels (conceptual/logical/physical); six paradigms (relational, document, key-value, wide-column, graph, time-series) with when-to-use |
| `content/02-normalization.xml` | 1NF–3NF rules; denormalization triggers; ER modeling notation; SCD types 0–6 |
| `content/03-physical-design.xml` | Index strategy (B-tree, GIN, BRIN, partial, covering); partitioning; naming conventions; anti-patterns |
| `content/04-advanced-patterns.xml` | Data Vault 2.0 (Hubs/Links/Satellites); polyglot persistence; query-first design for Cassandra; time-series hypertables |

## Templates

| File | Purpose |
|------|---------|
| `templates/pg-standard-table.sql` | PostgreSQL standard table with UUID PK, audit columns, soft delete, updated_at trigger |
| `templates/pg-junction-table.sql` | Many-to-many junction table template with composite PK and reverse lookup index |
| `templates/mongo-schema.js` | MongoDB document schema template with embedded vs referenced patterns and schema validation |
| `templates/cassandra-table.cql` | Cassandra/ScyllaDB table template with partition key, clustering columns, TTL, compaction |
| `templates/data-vault-hub.sql` | Data Vault 2.0 Hub, Link, and Satellite templates with hash key generation functions |
| `templates/scd-type2.sql` | SCD Type 2 dimension table with valid_from/valid_to/is_current and upsert procedure |
