# LLM Prompts for Database Selection

Prompts for AI-assisted database selection and architecture discussions.

---

## Requirements Analysis Prompts

### Extract Database Requirements

```
Analyze the following feature/system description and extract database requirements:

[PASTE FEATURE DESCRIPTION OR PRD]

For each data entity identified, provide:
1. Data structure (relational, document, graph, time-series, vector)
2. Estimated volume and growth rate
3. Access patterns (read/write ratio, query types)
4. Consistency requirements (ACID, eventual)
5. Latency requirements
6. Relationships with other entities

Format as a structured table.
```

### Identify Access Patterns

```
Given this system description:

[PASTE SYSTEM DESCRIPTION]

Identify and categorize all data access patterns:

1. **Point queries** (single record by ID)
2. **Range queries** (date ranges, pagination)
3. **Aggregations** (counts, sums, averages)
4. **Joins** (cross-table/collection queries)
5. **Full-text search** (keyword search)
6. **Graph traversals** (relationship navigation)
7. **Vector similarity** (semantic search, recommendations)

For each pattern, estimate:
- Frequency (requests per second)
- Latency requirement (ms)
- Criticality (P0/P1/P2)
```

---

## Database Comparison Prompts

### Compare Databases for Use Case

```
Compare the following databases for [USE CASE]:

Databases: [DATABASE 1], [DATABASE 2], [DATABASE 3]

Requirements:
- Data model: [DESCRIBE]
- Scale: [VOLUME, THROUGHPUT]
- Consistency: [STRONG/EVENTUAL]
- Latency: [REQUIREMENTS]
- Budget: [RANGE]
- Team expertise: [CURRENT SKILLS]

Provide a comparison matrix covering:
1. Data model fit
2. Query capabilities
3. Scalability
4. Consistency guarantees
5. Operational complexity
6. Cost (managed and self-hosted)
7. Ecosystem and tooling
8. Team learning curve

Conclude with a recommendation and rationale.
```

### Vector Database Selection

```
Help me select a vector database for a RAG application with these requirements:

- Embedding model: [MODEL, e.g., OpenAI text-embedding-3-large]
- Embedding dimensions: [DIMENSIONS, e.g., 1536]
- Number of vectors: [CURRENT] growing to [PROJECTED]
- Metadata filtering needs: [DESCRIBE FILTERS]
- Hybrid search: [YES/NO - keyword + semantic]
- Deployment: [Cloud managed / Self-hosted / Either]
- Budget: [MONTHLY BUDGET]

Compare: Qdrant, Weaviate, Pinecone, Milvus, pgvector

Consider:
1. Performance at my scale
2. Filtering capabilities
3. Hybrid search support
4. Operational complexity
5. Cost at scale
6. Integration with [MY STACK]
```

### NewSQL vs Traditional SQL

```
Should I use a distributed NewSQL database (CockroachDB, TiDB, Spanner)
or stick with PostgreSQL/MySQL for:

[DESCRIBE YOUR APPLICATION]

Requirements:
- Geographic distribution: [SINGLE REGION / MULTI-REGION / GLOBAL]
- Transaction volume: [TPS]
- Data volume: [SIZE]
- Consistency requirements: [DESCRIBE]
- Current stack: [POSTGRES/MYSQL/OTHER]
- Team size and expertise: [DESCRIBE]

Analyze:
1. When NewSQL provides clear value
2. When PostgreSQL + replicas is sufficient
3. Migration complexity
4. Cost comparison (3-year TCO)
5. Operational complexity difference
6. Risk assessment
```

---

## Architecture Design Prompts

### Polyglot Persistence Design

```
Design a database architecture for:

[PASTE SYSTEM DESCRIPTION]

The system has these components:
- [Component 1]: [Description]
- [Component 2]: [Description]
- [Component 3]: [Description]

For each component, recommend:
1. Primary database choice
2. Rationale for selection
3. Data flow between databases
4. Synchronization strategy
5. Failure handling

Provide an architecture diagram in text format showing data flow.
```

### Time-Series Database Selection

```
I need to select a time-series database for:

Use case: [IOT / MONITORING / FINANCIAL / LOGS]

Requirements:
- Ingestion rate: [EVENTS PER SECOND]
- Query patterns: [REAL-TIME / HISTORICAL / BOTH]
- Retention period: [DAYS/MONTHS/YEARS]
- Aggregation needs: [DESCRIBE]
- Integration: [PROMETHEUS / GRAFANA / CUSTOM]

Compare: TimescaleDB, InfluxDB, ClickHouse, QuestDB

Consider the "Smart Factory Pattern" if applicable:
- Hot tier (real-time alerting)
- Warm tier (dashboards)
- Cold tier (historical analytics)
```

### Graph Database Evaluation

```
Evaluate whether I need a dedicated graph database for:

[DESCRIBE YOUR USE CASE]

Current approach: [HOW YOU HANDLE RELATIONSHIPS NOW]

Questions to answer:
1. What types of relationship queries do I need?
2. How deep do traversals go? (1-hop, 2-hop, N-hop)
3. What's the query frequency?
4. Can PostgreSQL with recursive CTEs handle this?
5. Would Neo4j / Neptune / Dgraph provide measurable benefits?

If graph DB is recommended, which one fits best for:
- Query language preference: [CYPHER / GREMLIN / GRAPHQL]
- Deployment: [MANAGED / SELF-HOSTED]
- Integration with: [MY STACK]
```

---

## Migration Planning Prompts

### Assess Migration Complexity

```
Assess the complexity of migrating from [SOURCE DB] to [TARGET DB]:

Current setup:
- Data volume: [SIZE]
- Number of tables/collections: [COUNT]
- Daily transactions: [VOLUME]
- Downtime tolerance: [ZERO / MINIMAL / MAINTENANCE WINDOW]
- Application stack: [DESCRIBE]

Identify:
1. Schema differences and mapping required
2. Data type incompatibilities
3. Application code changes needed
4. Query rewrites required
5. Feature gaps to address
6. Recommended migration strategy (big-bang vs phased)
7. Estimated effort (person-weeks)
8. Key risks and mitigations
```

### Plan Database Modernization

```
Create a database modernization roadmap for:

Current state:
- Primary database: [CURRENT DB]
- Pain points: [LIST ISSUES]
- Growth projections: [DESCRIBE]

Goals:
- [GOAL 1]
- [GOAL 2]
- [GOAL 3]

Provide a phased approach:
1. Quick wins (0-3 months)
2. Medium-term improvements (3-12 months)
3. Long-term architecture (1-3 years)

For each phase, specify:
- Changes to make
- Resources required
- Risks and dependencies
- Success metrics
```

---

## Cost Optimization Prompts

### Analyze Database Costs

```
Analyze and optimize database costs for:

Current setup:
- Database: [DB NAME AND VERSION]
- Instance: [SIZE/TYPE]
- Storage: [SIZE AND TYPE]
- Monthly cost: [AMOUNT]
- Utilization: [CPU/MEMORY/IOPS UTILIZATION]

Usage patterns:
- Peak hours: [TIMES]
- Off-peak utilization: [PERCENTAGE]
- Read/write ratio: [RATIO]

Suggest optimizations:
1. Right-sizing recommendations
2. Reserved instance analysis
3. Storage optimization
4. Connection pooling benefits
5. Read replica strategy
6. Caching layer ROI

Calculate potential savings for each recommendation.
```

### Compare Managed vs Self-Hosted

```
Compare managed database service vs self-hosted for:

Database: [DATABASE NAME]
Scale: [DATA SIZE, THROUGHPUT]
Team: [SIZE, DB EXPERTISE]
Compliance: [REQUIREMENTS]

Calculate 3-year TCO for:

**Managed option:** [e.g., AWS RDS, MongoDB Atlas]
- Instance costs
- Storage costs
- Backup costs
- Support costs

**Self-hosted option:** [e.g., EC2, Kubernetes]
- Infrastructure costs
- DBA time (hours/week * hourly rate)
- On-call burden
- Tooling costs
- Training costs

Provide recommendation with break-even analysis.
```

---

## Interview & Review Prompts

### Review Database Design

```
Review this database design:

[PASTE SCHEMA / DESIGN DOCUMENT]

Evaluate against:
1. Normalization / denormalization appropriateness
2. Index strategy
3. Partitioning / sharding approach
4. Consistency model choice
5. Scalability considerations
6. Operational concerns

Identify:
- Potential issues at 10x scale
- Missing indexes
- Over-indexing
- Query anti-patterns
- Suggested improvements

Rate overall design: [1-5] with detailed feedback.
```

### Prepare for Database Discussion

```
Prepare me for a technical discussion about database selection for:

[DESCRIBE PROJECT/SYSTEM]

Stakeholders: [WHO WILL BE IN THE MEETING]

Prepare:
1. Key questions to ask about requirements
2. Common objections and responses
3. Comparison data to have ready
4. Risk discussion points
5. Cost talking points
6. Migration complexity discussion

Provide a meeting agenda and key slides/diagrams needed.
```

---

## Quick Decision Prompts

### Quick Database Recommendation

```
Quick database recommendation:

Use case: [ONE SENTENCE DESCRIPTION]
Scale: [SMALL/MEDIUM/LARGE]
Team experience: [DATABASES TEAM KNOWS]
Budget: [LOW/MEDIUM/HIGH]
Managed preference: [YES/NO/FLEXIBLE]

Give me:
1. Top recommendation
2. Runner-up alternative
3. One-sentence rationale each
```

### Should I Add This Database?

```
I'm considering adding [NEW DATABASE] to my stack that currently uses [CURRENT DATABASES].

Use case for new database: [DESCRIBE]

Answer:
1. Can current databases handle this? (with effort level)
2. Is a dedicated database justified?
3. What's the operational cost of adding this?
4. Recommendation: Add / Don't add / Consider alternative
```

---

## Prompt Engineering Tips

### Be Specific About Scale

```
Instead of: "I have a lot of data"
Say: "10 million records, growing 1M/month, 1000 reads/sec, 100 writes/sec"
```

### Specify Constraints Clearly

```
Instead of: "I need good performance"
Say: "p99 latency < 50ms for reads, p99 < 100ms for writes"
```

### Include Team Context

```
Add: "Team of 5 engineers, strong PostgreSQL experience,
no graph database experience, can invest 2 weeks in learning"
```

### State Non-Negotiables

```
Add: "Must support: GDPR compliance, encryption at rest,
row-level security. Nice to have: GraphQL support"
```

---

## Related

- [README.md](README.md) - Database categories overview
- [checklist.md](checklist.md) - Selection checklist
- [examples.md](examples.md) - Real-world use cases
- [templates.md](templates.md) - Decision matrix templates
