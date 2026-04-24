# Architecture Decision Templates

Copy-paste templates for architecture decision trees, decision matrices, and ADRs.

---

## Decision Tree Templates

### Template 1: Architecture Style Decision

```
Q1: Team size?
    |
    +-- "1-10 developers" --------> Monolith
    |   Next: Skip to implementation
    |
    +-- "10-50 developers" -------> Q2
    |
    +-- "50+ developers" ---------> Q3

Q2: Clear domain boundaries?
    |
    +-- "Yes" --------------------> Modular Monolith
    +-- "No" ---------------------> Monolith (refine boundaries first)

Q3: DevOps maturity?
    |
    +-- "High" -------------------> Microservices
    |   (CI/CD, monitoring, distributed tracing)
    |
    +-- "Medium/Low" -------------> Modular Monolith
        Action: Build platform capabilities first
```

### Template 2: Database Selection

```
Q1: Primary data model?
    |
    +-- "Relational (tables, joins)" -------------> Q2
    +-- "Document (nested, flexible)" ------------> Q3
    +-- "Key-value (simple lookups)" -------------> Redis
    +-- "Time-series (metrics, events)" ----------> Q4
    +-- "Graph (relationships)" ------------------> Neo4j
    +-- "Vector (embeddings, AI)" ----------------> Q5
    +-- "Search (full-text)" ---------------------> Elasticsearch

Q2: Scale requirements?
    |
    +-- "Standard (<1TB, <10k QPS)" --------------> PostgreSQL
    +-- "High read (>50k QPS)" -------------------> PostgreSQL + replicas
    +-- "Massive (>100TB)" -----------------------> CockroachDB / TiDB

Q3: Consistency requirements?
    |
    +-- "Strong consistency" ---------------------> MongoDB (w:majority)
    +-- "High availability" ----------------------> DynamoDB / Cassandra

Q4: Query complexity?
    |
    +-- "Simple aggregations" --------------------> InfluxDB
    +-- "SQL-like queries" -----------------------> TimescaleDB
    +-- "Analytics (OLAP)" -----------------------> ClickHouse

Q5: Deployment preference?
    |
    +-- "Managed (cloud)" ------------------------> Pinecone / Weaviate Cloud
    +-- "Self-hosted" ----------------------------> Qdrant / Milvus
    +-- "PostgreSQL extension" -------------------> pgvector
```

### Template 3: Cloud Provider Selection

```
Q1: Existing technology ecosystem?
    |
    +-- "Microsoft (AD, Office 365, .NET)" -------> Azure
    +-- "Google (Workspace, BigQuery)" -----------> GCP
    +-- "None / Mixed" ---------------------------> Q2

Q2: Primary workload type?
    |
    +-- "General enterprise" ---------------------> AWS
    +-- "Data analytics / ML" --------------------> GCP
    +-- "Hybrid cloud" ---------------------------> Azure
    +-- "Kubernetes-native" ----------------------> GCP
    +-- "Government / regulated" -----------------> AWS GovCloud or Azure Gov

Q3: Budget priority?
    |
    +-- "Predictable workloads" ------------------> AWS Reserved
    +-- "Variable workloads" ---------------------> GCP (auto discounts)
    +-- "Microsoft licensing" --------------------> Azure (BYOL)
```

### Template 4: Build vs Buy

```
Q1: Is this a competitive differentiator?
    |
    +-- "Yes (core to business)" -----------------> Q2
    +-- "No (commodity/utility)" -----------------> Q4

Q2: Do adequate solutions exist?
    |
    +-- "No" -------------------------------------> Build
    +-- "Yes, but inadequate" --------------------> Build or Extend
    +-- "Yes, fully adequate" --------------------> Q3

Q3: Can you afford vendor dependency?
    |
    +-- "Yes" ------------------------------------> Buy
    +-- "No" -------------------------------------> Build

Q4: Time and budget constraints?
    |
    +-- "Tight" ----------------------------------> Buy
    +-- "Flexible" -------------------------------> Q5

Q5: Integration complexity?
    |
    +-- "High (many custom integrations)" --------> Build or Low-code
    +-- "Low (standard integrations)" ------------> Buy
```

### Template 5: API Style Selection

```
Q1: Who is the primary consumer?
    |
    +-- "External developers" --------------------> REST + OpenAPI
    +-- "Internal services" ----------------------> Q2
    +-- "Frontend (web/mobile)" ------------------> Q3
    +-- "Multiple consumer types" ----------------> Multi-API strategy

Q2: Performance critical?
    |
    +-- "Yes (low latency, high throughput)" -----> gRPC
    +-- "No" -------------------------------------> REST

Q3: Data requirements?
    |
    +-- "Complex, varied queries" ----------------> GraphQL
    +-- "Simple CRUD" ----------------------------> REST
    +-- "Real-time updates" ----------------------> WebSocket / SSE
```

### Template 6: Frontend Framework Selection

```
Q1: SEO requirements?
    |
    +-- "Critical" -------------------------------> SSR/SSG framework (Next.js, Nuxt, Astro)
    +-- "Not critical" ---------------------------> Q2

Q2: Team expertise?
    |
    +-- "React" ----------------------------------> Next.js or React + Vite
    +-- "Vue" ------------------------------------> Nuxt
    +-- "Angular" --------------------------------> Angular
    +-- "None / new team" ------------------------> Next.js (largest ecosystem)

Q3: Application type?
    |
    +-- "Content site" ---------------------------> Astro
    +-- "Full-stack app" -------------------------> Next.js / Nuxt
    +-- "Admin dashboard" ------------------------> React + Vite
    +-- "Highly interactive" ---------------------> React / Vue / Svelte
```

---

## Decision Matrix Templates

### Template: Weighted Decision Matrix

```markdown
## Decision: [Title]

### Evaluation Criteria

| Criteria | Weight | Rationale |
|----------|--------|-----------|
| [Criteria 1] | X% | [Why this weight] |
| [Criteria 2] | X% | [Why this weight] |
| [Criteria 3] | X% | [Why this weight] |
| [Criteria 4] | X% | [Why this weight] |
| [Criteria 5] | X% | [Why this weight] |
| **Total** | **100%** | |

### Scoring Guide

| Score | Meaning |
|-------|---------|
| 1 | Poor / Does not meet requirements |
| 2 | Below average / Partially meets requirements |
| 3 | Average / Meets basic requirements |
| 4 | Good / Exceeds requirements |
| 5 | Excellent / Best in class |

### Decision Matrix

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| [Criteria 1] | X% | [1-5] | [1-5] | [1-5] |
| [Criteria 2] | X% | [1-5] | [1-5] | [1-5] |
| [Criteria 3] | X% | [1-5] | [1-5] | [1-5] |
| [Criteria 4] | X% | [1-5] | [1-5] | [1-5] |
| [Criteria 5] | X% | [1-5] | [1-5] | [1-5] |
| **Weighted Total** | 100% | **X.X** | **X.X** | **X.X** |

### Calculation

Option A: (C1 * W1) + (C2 * W2) + ... = X.X
Option B: (C1 * W1) + (C2 * W2) + ... = X.X
Option C: (C1 * W1) + (C2 * W2) + ... = X.X

### Recommendation

**Selected:** [Option]

**Rationale:**
1. [Key reason 1]
2. [Key reason 2]
3. [Key reason 3]
```

### Template: Technology Comparison Matrix

```markdown
## Technology Comparison: [Category]

| Feature | [Tech A] | [Tech B] | [Tech C] |
|---------|----------|----------|----------|
| **Performance** |
| Throughput | | | |
| Latency | | | |
| Scalability | | | |
| **Operations** |
| Deployment complexity | | | |
| Monitoring | | | |
| Maintenance burden | | | |
| **Development** |
| Learning curve | | | |
| Documentation | | | |
| Ecosystem/plugins | | | |
| **Business** |
| License | | | |
| Cost (at scale) | | | |
| Vendor support | | | |
| Community size | | | |
| **Fit** |
| Team expertise | | | |
| Integration with stack | | | |
| Use case alignment | | | |
```

### Template: Total Cost of Ownership

```markdown
## TCO Analysis: [Decision]

### 3-Year Cost Projection

| Cost Category | Option A | Option B |
|---------------|----------|----------|
| **Initial Costs** |
| Licensing/Purchase | $ | $ |
| Implementation | $ | $ |
| Training | $ | $ |
| Migration | $ | $ |
| **Subtotal Initial** | **$** | **$** |
| **Annual Costs (x3)** |
| Licensing/Subscription | $ | $ |
| Infrastructure | $ | $ |
| Maintenance/Support | $ | $ |
| Operations (FTE) | $ | $ |
| **Subtotal Annual x3** | **$** | **$** |
| **Hidden Costs** |
| Integration effort | $ | $ |
| Technical debt | $ | $ |
| Opportunity cost | $ | $ |
| **Subtotal Hidden** | **$** | **$** |
| **TOTAL 3-YEAR TCO** | **$** | **$** |

### Assumptions
- [List key assumptions]
```

---

## ADR Templates

### Template: MADR (Markdown Any Decision Record)

```markdown
# ADR-XXXX: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded by ADR-YYYY]

## Context

[What is the issue that we're seeing that motivates this decision or change?]

## Decision Drivers

- [Driver 1]
- [Driver 2]
- [Driver 3]

## Considered Options

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome

Chosen option: "[Option X]", because [justification].

### Consequences

**Good:**
- [Positive consequence 1]
- [Positive consequence 2]

**Bad:**
- [Negative consequence 1]
- [Negative consequence 2]

### Confirmation

[How will we confirm that the decision is implemented correctly?]

## Pros and Cons of the Options

### [Option 1]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]

### [Option 2]

- Good, because [argument a]
- Bad, because [argument b]
- Bad, because [argument c]

### [Option 3]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]

## More Information

[Links to relevant documentation, research, or discussions]
```

### Template: Nygard's ADR (Lightweight)

```markdown
# ADR-XXXX: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Context

[The issue motivating this decision, and any context that influences or constrains the decision.]

## Decision

[The change that we're proposing and/or doing.]

## Consequences

[What becomes easier or more difficult to do because of this change.]
```

### Template: Y-Statement ADR

```markdown
# ADR-XXXX: [Title]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Decision

In the context of **[use case/user story]**,
facing **[concern]**,
we decided for **[option]**
and against **[other options]**,
to achieve **[quality/goal]**,
accepting **[downside/trade-off]**.

## Full Context

[Expanded context if needed]

## Considered Alternatives

1. **[Alternative 1]**: [Brief description and why rejected]
2. **[Alternative 2]**: [Brief description and why rejected]

## Consequences

[What becomes easier or more difficult to do because of this change]

## Related Decisions

- [ADR-XXXX: Related Decision]
```

---

## Quick Reference Cards

### Architecture Style Selection Card

```
+------------------+-------------+-------------------+----------------+
|                  | Monolith    | Modular Monolith  | Microservices  |
+------------------+-------------+-------------------+----------------+
| Team Size        | 1-10        | 10-50             | 50+            |
| Deployment       | Single      | Single            | Independent    |
| Scaling          | Vertical    | Vertical          | Horizontal     |
| Complexity       | Low         | Medium            | High           |
| DevOps Maturity  | Low         | Low-Medium        | High           |
| Data Consistency | ACID        | ACID              | Eventual       |
| Best For         | MVP, small  | Growing products  | Large orgs     |
+------------------+-------------+-------------------+----------------+
```

### Database Selection Card

```
+------------------+---------------+---------------------+
| Use Case         | Primary       | Alternative         |
+------------------+---------------+---------------------+
| Transactional    | PostgreSQL    | MySQL               |
| Document         | MongoDB       | DynamoDB            |
| Key-value/Cache  | Redis         | Memcached           |
| Time-series      | TimescaleDB   | ClickHouse          |
| Analytics (OLAP) | ClickHouse    | BigQuery            |
| Search           | Elasticsearch | Meilisearch         |
| Graph            | Neo4j         | Amazon Neptune      |
| Vector (AI)      | Qdrant        | pgvector            |
+------------------+---------------+---------------------+
```

### Cloud Provider Card

```
+------------------+-------------+-------------+-------------+
|                  | AWS         | Azure       | GCP         |
+------------------+-------------+-------------+-------------+
| Market Share     | 31%         | 25%         | 11%         |
| Best For         | Breadth     | Microsoft   | Data/ML     |
|                  | Enterprise  | Hybrid      | Kubernetes  |
| Compute          | EC2, Lambda | VMs, Funcs  | GCE, Cloud  |
|                  |             |             | Run         |
| Kubernetes       | EKS         | AKS         | GKE (best)  |
| Database         | RDS, Aurora | SQL, Cosmos | Cloud SQL,  |
|                  |             |             | Spanner     |
| AI/ML            | SageMaker   | Azure ML    | Vertex AI   |
| Discount Model   | Reserved    | Reserved    | Sustained   |
|                  | (up to 72%) | + BYOL      | (auto 30%)  |
+------------------+-------------+-------------+-------------+
```

### API Style Card

```
+------------------+-------------+-------------+-------------+
|                  | REST        | GraphQL     | gRPC        |
+------------------+-------------+-------------+-------------+
| Best For         | Public APIs | Frontend    | Internal    |
|                  | CRUD        | flexibility | services    |
| Performance      | Good        | Medium      | Excellent   |
| Caching          | HTTP native | Custom      | Custom      |
| Schema           | OpenAPI     | SDL         | Protobuf    |
| Learning Curve   | Low         | Medium      | Medium      |
| Tooling          | Excellent   | Good        | Good        |
+------------------+-------------+-------------+-------------+
```

---

## Blank Templates

### Blank Decision Tree

```
Q1: [First question]?
    |
    +-- "[Answer A]" ---------> [Outcome or Q2]
    |
    +-- "[Answer B]" ---------> [Outcome or Q3]
    |
    +-- "[Answer C]" ---------> [Outcome]

Q2: [Follow-up question]?
    |
    +-- "[Answer A]" ---------> [Outcome]
    +-- "[Answer B]" ---------> [Outcome]

Q3: [Follow-up question]?
    |
    +-- "[Answer A]" ---------> [Outcome]
    +-- "[Answer B]" ---------> [Outcome]
```

### Blank Decision Document

```markdown
# Decision: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | In Progress | Decided
**Decision Maker:** [Name/Role]
**Stakeholders:** [Names/Roles]

## Problem Statement

[Clear description of what needs to be decided]

## Constraints

- [Constraint 1]
- [Constraint 2]
- [Constraint 3]

## Options

### Option 1: [Name]

**Description:** [What this option entails]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Cost/Effort:** [High/Medium/Low or specific estimate]

### Option 2: [Name]

[Same structure as Option 1]

### Option 3: [Name]

[Same structure as Option 1]

## Decision Matrix

| Criteria | Weight | Option 1 | Option 2 | Option 3 |
|----------|--------|----------|----------|----------|
| [Criteria] | X% | X | X | X |
| **Total** | 100% | **X.X** | **X.X** | **X.X** |

## Recommendation

**Selected Option:** [Option X]

**Rationale:**
[Explanation of why this option was chosen]

## Next Steps

1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

## Appendix

[Supporting research, data, or references]
```

---

*Architecture Decision Templates v2.0 - Updated January 2026*
