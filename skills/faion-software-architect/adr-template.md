# Architecture Decision Record (ADR) Template

## Standard ADR Format

```markdown
# ADR-{NNN}: {Title}

## Status
{Proposed | Accepted | Deprecated | Superseded by ADR-XXX}

## Context
{What is the issue that we're seeing that motivates this decision?}

## Decision
{What is the change that we're proposing and/or doing?}

## Consequences
### Positive
- {benefit 1}
- {benefit 2}

### Negative
- {trade-off 1}
- {trade-off 2}

### Risks
- {risk 1}: {mitigation}

## Alternatives Considered
### {Alternative 1}
- Pros: {pros}
- Cons: {cons}
- Why rejected: {reason}

## References
- {link 1}
- {link 2}
```

## ADR Examples

### Example 1: Database Selection

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a relational database for our e-commerce platform that handles:
- Product catalog with complex queries
- User accounts and authentication
- Order processing with ACID transactions
- Reporting and analytics

Team has experience with both PostgreSQL and MySQL.

## Decision
Use PostgreSQL 15 as our primary database.

## Consequences
### Positive
- Strong ACID compliance for transactions
- Advanced features (JSONB, full-text search, CTEs)
- Excellent performance for complex queries
- Active community and ecosystem
- Team familiarity

### Negative
- Slightly more complex to set up than MySQL
- Fewer managed hosting options than MySQL
- Write performance slightly lower than MySQL for simple queries

### Risks
- Learning curve for advanced features: Mitigated by team training
- Scaling to >10M rows: Mitigated by read replicas and partitioning plan

## Alternatives Considered

### MySQL
- Pros: Team knows it, simpler setup, many hosting options
- Cons: Fewer advanced features, weaker for complex queries
- Why rejected: We need JSONB and advanced query capabilities

### MongoDB
- Pros: Flexible schema, good for rapid prototyping
- Cons: No ACID transactions, eventual consistency issues
- Why rejected: We need strong consistency for orders and payments

## References
- https://www.postgresql.org/docs/15/
- Internal: docs/database-schema.md
```

### Example 2: Architecture Style

```markdown
# ADR-002: Start with Modular Monolith

## Status
Accepted

## Context
Building a new SaaS product with a small team (3 developers).
Expected to launch MVP in 3 months.
Unclear service boundaries at this stage.

## Decision
Build a modular monolith with clear internal boundaries,
allowing future extraction to microservices if needed.

## Consequences
### Positive
- Faster development with single codebase
- Easier debugging and testing
- Simpler deployment (one service)
- Lower operational overhead
- Clear modules prepare for future microservices

### Negative
- Single point of failure
- All modules share the same runtime
- Cannot independently scale modules

### Risks
- Modules become tightly coupled: Mitigated by strict module boundaries
  and interface contracts
- Difficult to extract later: Mitigated by domain-driven design and
  dependency rules

## Alternatives Considered

### Microservices from Day 1
- Pros: Independent scaling, deployment, tech stack
- Cons: High operational overhead, unclear boundaries, overkill for MVP
- Why rejected: Team too small, boundaries unclear, premature optimization

### Traditional Monolith
- Pros: Simplest approach
- Cons: Hard to extract services later, no clear boundaries
- Why rejected: We want flexibility for future microservices

## References
- https://martinfowler.com/bliki/MonolithFirst.html
- Book: "Monolith to Microservices" by Sam Newman
```

### Example 3: Communication Pattern

```markdown
# ADR-003: Use Async Events for Order Processing

## Status
Accepted

## Context
Order processing involves multiple steps:
1. Validate inventory
2. Process payment
3. Update inventory
4. Send email notification
5. Create shipment

Each step can take 100ms-2s. Don't want to block user while processing.

## Decision
Use asynchronous event-driven architecture for order processing.
- User request creates order (sync)
- Background workers process steps (async)
- RabbitMQ for message queue

## Consequences
### Positive
- Fast response to user (~50ms)
- Steps can be retried independently
- Easy to add new processing steps
- Handles traffic spikes with queue buffering
- Clear separation of concerns

### Negative
- Eventual consistency (order status not immediate)
- More complex to debug (distributed system)
- Need monitoring for queue health

### Risks
- Message loss: Mitigated by RabbitMQ persistence and acknowledgments
- Ordering issues: Mitigated by idempotent handlers and sequence numbers

## Alternatives Considered

### Synchronous Processing
- Pros: Simpler, immediate feedback
- Cons: Slow response (2-5s), blocks user, poor UX
- Why rejected: Unacceptable UX for checkout flow

### Background Jobs (Cron)
- Pros: Simple, no queue needed
- Cons: Delayed processing, no real-time updates
- Why rejected: Need near-real-time processing

## References
- https://www.rabbitmq.com/
- Internal: docs/event-schema.md
```

## ADR Best Practices

### When to Create an ADR

Create an ADR for decisions that:
- Have significant impact on architecture
- Are hard to reverse later
- Affect multiple teams or services
- Involve trade-offs between quality attributes
- Choose between multiple viable options

### When NOT to Create an ADR

Don't create ADRs for:
- Trivial decisions (naming conventions, code style)
- Decisions easily reversed (library choice for small util)
- Decisions with obvious choice (use version control)

### ADR Naming Convention

```
ADR-001-database-selection.md
ADR-002-modular-monolith.md
ADR-003-async-order-processing.md
```

Format: `ADR-{NNN}-{short-title}.md`

### ADR Storage Location

```
docs/architecture/decisions/
├── ADR-001-database-selection.md
├── ADR-002-modular-monolith.md
└── ADR-003-async-order-processing.md
```

Or in project root:
```
.aidocs/architecture/adr/
```

### ADR Status Lifecycle

```
Proposed → Accepted → Deprecated → Superseded
            ↓
        Rejected
```

### Updating ADRs

Never delete ADRs. Instead:
- Change status to "Deprecated" or "Superseded by ADR-XXX"
- Add note at top explaining why it was superseded
- Keep original decision for historical context

---

*Part of faion-software-architect skill*
