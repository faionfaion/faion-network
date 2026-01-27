# LLM Prompts for Data Modeling

Effective prompts for LLM-assisted data modeling across different database paradigms.

## Conceptual Modeling Prompts

### Entity Discovery

```
I'm designing a data model for a {domain} application.

Business context:
{brief description of the business domain}

Key use cases:
1. {use case 1}
2. {use case 2}
3. {use case 3}

Please identify:
1. Core business entities
2. Relationships between entities (with cardinality)
3. Key attributes for each entity
4. Any potential aggregates or bounded contexts

Output as a structured list with relationship notation.
```

### Requirements to Entities

```
Convert these business requirements into a conceptual data model:

Requirements:
{paste requirements}

For each entity identified:
- Name and business definition
- Key attributes (no data types yet)
- Relationships to other entities
- Cardinality (1:1, 1:N, M:N)
- Optional vs required relationships

Present as an entity list with relationship diagram notation.
```

---

## Logical Modeling Prompts

### Schema Design from Requirements

```
Design a logical data model for {application type}.

Requirements:
{list key requirements}

Access patterns:
- {query pattern 1}: frequency {high/medium/low}
- {query pattern 2}: frequency {high/medium/low}
- {query pattern 3}: frequency {high/medium/low}

Constraints:
- Database: {database type or "flexible"}
- Read/write ratio: {e.g., 80/20}
- Scale: {expected data volume}

Please provide:
1. Entity definitions with attributes
2. Primary and foreign keys
3. Normalization level (and justification)
4. Denormalization recommendations (if applicable)
5. Index suggestions based on access patterns
```

### Normalization Analysis

```
Analyze this table structure for normalization:

{paste current table structure}

Please:
1. Identify current normal form
2. List any normalization violations
3. Show step-by-step normalization to 3NF
4. Explain the trade-offs of full normalization
5. Recommend whether to keep denormalized for this use case

Use case context: {describe the use case}
```

### Denormalization Strategy

```
I have this normalized schema:

{paste schema}

Query patterns that are slow:
{list slow queries}

Expected load:
- {reads per second}
- {writes per second}

Please recommend:
1. Specific denormalization opportunities
2. What data to duplicate and why
3. Data synchronization strategy
4. Trade-offs (storage vs performance)
5. Implementation approach
```

---

## Physical Modeling Prompts

### PostgreSQL Schema Generation

```
Generate a PostgreSQL schema for {domain}.

Entities and relationships:
{describe entities}

Requirements:
- Support for soft delete: {yes/no}
- Audit columns: {yes/no}
- Multi-tenancy: {none/schema/row-level}
- Expected table sizes: {rough estimates}

Please include:
1. CREATE TABLE statements with appropriate data types
2. Primary and foreign key constraints
3. Indexes based on common query patterns
4. Check constraints for data validation
5. Triggers for updated_at timestamps
6. Comments explaining design decisions
```

### MongoDB Schema Design

```
Design a MongoDB schema for {application}.

Entities:
{list entities}

Access patterns:
1. {query 1 - frequency, latency requirement}
2. {query 2 - frequency, latency requirement}
3. {query 3 - frequency, latency requirement}

Please provide:
1. Document structure (embed vs reference decisions)
2. Collection design
3. Index recommendations
4. Schema validation rules (JSON Schema)
5. Sample documents

Explain embedding vs referencing decisions for each relationship.
```

### Cassandra/ScyllaDB Design

```
Design Cassandra tables for {use case}.

Query requirements (MUST start with queries):
1. {query 1}: Get {data} by {partition}
2. {query 2}: Get {data} filtered by {conditions}
3. {query 3}: Get {data} ordered by {field}

Data characteristics:
- Write volume: {per second}
- Read volume: {per second}
- Retention: {period}
- Data size per partition: {estimate}

Please provide:
1. Table per query (query-first design)
2. Partition key selection with justification
3. Clustering column design
4. Data duplication strategy
5. TTL recommendations
6. CQL CREATE TABLE statements
```

---

## Database Selection Prompts

### Database Technology Selection

```
Help me select the right database for {application}.

Requirements:
- Data type: {structured/semi-structured/unstructured}
- Relationships: {simple/complex/highly connected}
- Consistency: {strong ACID/eventual OK}
- Scale: {current size, growth rate}
- Query patterns: {describe main queries}
- Latency: {p99 requirement}
- Availability: {SLA requirement}

Team context:
- Existing expertise: {databases team knows}
- Ops capability: {managed preferred/self-hosted OK}

Please compare top 3 options with:
1. Fit score for each requirement
2. Pros and cons for this use case
3. Operational complexity
4. Cost considerations
5. Final recommendation with justification
```

### Polyglot Persistence Design

```
Design a polyglot persistence architecture for {application}.

Data domains:
1. {domain 1}: {characteristics, access patterns}
2. {domain 2}: {characteristics, access patterns}
3. {domain 3}: {characteristics, access patterns}

Cross-cutting concerns:
- Search requirements: {describe}
- Analytics requirements: {describe}
- Caching needs: {describe}

Please provide:
1. Database selection for each domain
2. Data flow between databases
3. Synchronization strategy
4. Consistency boundaries
5. Architecture diagram description
```

---

## Time-Series Prompts

### Time-Series Schema Design

```
Design a time-series data model for {use case}.

Data characteristics:
- Metrics: {list metric types}
- Dimensions/tags: {list dimensions}
- Ingestion rate: {points per second}
- Query patterns: {real-time, historical, aggregations}
- Retention: {hot/warm/cold tiers}

Database: {TimescaleDB/InfluxDB/ClickHouse}

Please provide:
1. Table/measurement schema
2. Tag vs field decisions
3. Partitioning strategy
4. Continuous aggregate/materialized view design
5. Retention and compression policies
6. Sample queries
```

---

## Data Warehouse Prompts

### Dimensional Model Design

```
Design a dimensional model for {business domain} analytics.

Business process: {describe the process to analyze}

Grain: {the level of detail for fact table}

Dimensions needed:
{list dimensions with example attributes}

Measures/facts:
{list measures to track}

SCD requirements:
{which dimensions need history tracking, which type}

Please provide:
1. Star schema design
2. Fact table with grain definition
3. Dimension tables with SCD type specification
4. Slowly changing dimension implementation
5. Sample data and queries
```

### Data Vault Design

```
Design a Data Vault 2.0 model for {domain}.

Source systems:
1. {source 1}: {entities it contains}
2. {source 2}: {entities it contains}

Business keys:
{list key business identifiers}

Please provide:
1. Hub definitions with business keys
2. Link definitions for relationships
3. Satellite definitions for descriptive attributes
4. Hash key generation approach
5. Sample loading queries
6. Business vault transformations
```

---

## Graph Database Prompts

### Knowledge Graph Design

```
Design a knowledge graph for {domain}.

Entities (nodes):
{list entity types with key attributes}

Relationships:
{list relationship types between entities}

Query patterns:
1. {traversal query 1}
2. {pattern matching query 2}
3. {path finding query 3}

Please provide:
1. Node label definitions with properties
2. Relationship type definitions with properties
3. Indexes and constraints
4. Cypher queries for common patterns
5. Graph data model diagram description
```

### Graph Migration from Relational

```
Help migrate this relational schema to a graph model:

{paste relational schema}

Current pain points:
{describe join performance issues, query complexity}

Please provide:
1. Node and relationship mapping
2. Property placement decisions
3. Index strategy
4. Migration approach
5. Before/after query comparison
6. Performance expectations
```

---

## Optimization Prompts

### Index Optimization

```
Optimize indexes for these query patterns:

Table schema:
{paste schema}

Queries with execution frequency:
1. {query 1}: {frequency}
2. {query 2}: {frequency}
3. {query 3}: {frequency}

Current indexes:
{list existing indexes}

Write patterns:
{describe insert/update frequency}

Please analyze:
1. Missing indexes for query patterns
2. Unused or redundant indexes
3. Composite index recommendations
4. Partial index opportunities
5. Index maintenance considerations
```

### Query Performance Analysis

```
Analyze this slow query and recommend schema changes:

Query:
{paste query}

Execution plan:
{paste EXPLAIN ANALYZE output}

Current schema:
{paste relevant tables}

Data volumes:
{table sizes}

Please recommend:
1. Schema changes to improve performance
2. Index additions or modifications
3. Query rewriting options
4. Denormalization opportunities
5. Estimated improvement
```

---

## Migration Prompts

### Schema Migration Design

```
Design a migration from:

Current schema:
{paste current schema}

To target schema:
{paste target schema or describe changes}

Constraints:
- Zero downtime: {yes/no}
- Data volume: {size}
- Maximum migration window: {time}

Please provide:
1. Migration strategy (big bang vs gradual)
2. Step-by-step migration plan
3. Rollback strategy
4. Data validation approach
5. Risk mitigation
```

### Cross-Database Migration

```
Plan migration from {source DB} to {target DB}.

Current model:
{describe or paste schema}

Reasons for migration:
{list reasons}

Please provide:
1. Schema translation approach
2. Data type mappings
3. Relationship handling changes
4. Query rewriting examples
5. Data migration strategy
6. Validation checkpoints
```

---

## Review and Validation Prompts

### Schema Review

```
Review this database schema for best practices:

{paste schema}

Context:
- Application type: {type}
- Expected scale: {volume}
- Read/write ratio: {ratio}
- Database: {database type}

Please evaluate:
1. Naming conventions
2. Data type choices
3. Normalization level
4. Index coverage
5. Constraint completeness
6. Potential issues at scale
7. Security considerations

Provide specific recommendations with priority.
```

### Data Model Documentation

```
Generate documentation for this data model:

{paste schema}

Please create:
1. Data dictionary (table and column descriptions)
2. Relationship diagram description (for diagramming tool)
3. Entity explanations for business users
4. Technical notes for developers
5. Sample queries for common use cases
```

---

## Advanced Patterns

### Event Sourcing Schema

```
Design an event sourcing data model for {domain}.

Aggregates:
{list aggregates}

Event types:
{list event types per aggregate}

Requirements:
- Event store: {database}
- Snapshot strategy: {frequency/size threshold}
- Projection needs: {list projections}

Please provide:
1. Event store schema
2. Snapshot storage design
3. Projection table designs
4. Event replay strategy
5. Sample event handling
```

### Multi-Tenant Schema

```
Design a multi-tenant schema for {application}.

Tenancy model: {shared database / schema per tenant / database per tenant}

Requirements:
- Tenant isolation: {data/performance}
- Tenant count: {expected number}
- Tenant size variation: {similar/highly variable}
- Cross-tenant queries: {needed/not needed}

Please provide:
1. Schema design with tenant isolation
2. Row-level security (if applicable)
3. Tenant identification strategy
4. Query patterns with tenant filtering
5. Scaling considerations
```

---

## Prompt Engineering Tips

### Effective Context Providing

1. **Always include:**
   - Database type (PostgreSQL, MongoDB, etc.)
   - Scale expectations (rows, size, growth)
   - Access patterns (read/write ratio, query types)
   - Consistency requirements

2. **For better results:**
   - Provide sample data
   - Include existing schema if modifying
   - Specify constraints and limitations
   - Mention team expertise

3. **Ask for trade-offs:**
   - Request pros and cons
   - Ask about alternatives considered
   - Request justification for decisions

### Iterative Refinement

```
Initial prompt: "Design a user table"

Better: "Design a user table for a SaaS application with:
- Expected 1M users in year 1
- PostgreSQL database
- Need for soft delete
- Multi-tenancy (row-level)
- GDPR compliance (data deletion)
- OAuth integration

Include indexes for email lookup and tenant queries."

Follow-up: "Now add audit logging for user profile changes,
maintaining history of all modifications."
```
