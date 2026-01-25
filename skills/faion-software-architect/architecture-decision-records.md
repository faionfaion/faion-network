# Architecture Decision Records (ADRs)

Documenting significant architecture decisions.

## What is an ADR?

A short document capturing an important architecture decision:
- **Why** the decision was made
- **What** was decided
- **Consequences** of the decision
- **Alternatives** considered

## When to Write an ADR

- Technology choices (language, framework, database)
- Architecture style (monolith, microservices)
- Significant design patterns
- Third-party service selection
- Breaking changes
- Security decisions

## ADR Template (Lightweight)

```markdown
# ADR-NNN: Title

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Deciders:** [names]

## Context
What is the issue that we're seeing that is motivating this decision?

## Decision
What is the change that we're proposing and/or doing?

## Consequences
What becomes easier or more difficult to do because of this change?

## Alternatives Considered
What other options were evaluated?
```

## ADR Template (Detailed)

```markdown
# ADR-NNN: Title

## Metadata
- **Status:** Proposed | Accepted | Deprecated | Superseded
- **Date:** YYYY-MM-DD
- **Deciders:** [names]
- **Technical Story:** [ticket/issue link]

## Context and Problem Statement
[Describe the context and problem]

## Decision Drivers
- [driver 1]
- [driver 2]

## Considered Options
1. Option A
2. Option B
3. Option C

## Decision Outcome
Chosen option: "[option]", because [justification].

### Positive Consequences
- [e.g., improvement of quality attribute]

### Negative Consequences
- [e.g., compromising quality attribute]

## Pros and Cons of Options

### Option A
- Good, because [argument]
- Bad, because [argument]

### Option B
- Good, because [argument]
- Bad, because [argument]

## Links
- [Link to related ADR]
- [Link to documentation]
```

## Example ADR

```markdown
# ADR-001: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2024-01-15
**Deciders:** Tech Lead, Senior Engineers

## Context
We need a primary database for our new e-commerce platform.
Expected load: 10k RPS, 100GB data, complex queries with joins.

## Decision
Use PostgreSQL 15 as the primary database.

## Consequences

### Positive
- Strong ACID guarantees
- Excellent JSON support (JSONB)
- Rich ecosystem, mature tooling
- Team has experience

### Negative
- Horizontal scaling more complex than NoSQL
- Need to manage replication ourselves

## Alternatives Considered

### MongoDB
- Good for flexible schema
- Better horizontal scaling
- Rejected: Our data is relational, team lacks experience

### MySQL
- Similar capabilities
- Rejected: PostgreSQL has better JSON support, advanced features
```

## ADR Naming Convention

```
decisions/
├── ADR-001-use-postgresql.md
├── ADR-002-adopt-microservices.md
├── ADR-003-jwt-authentication.md
└── ADR-004-kubernetes-deployment.md
```

## Best Practices

1. **Keep them short** - 1-2 pages max
2. **Write when deciding** - Not after the fact
3. **Include context** - Future readers need background
4. **Document alternatives** - Show due diligence
5. **Accept trade-offs** - No perfect solutions
6. **Version control** - Store in repo with code
7. **Review process** - Treat like code review
8. **Never delete** - Supersede instead

## ADR Lifecycle

```
Proposed → Accepted → [Deprecated | Superseded]
                           │
                           └─▶ Reference new ADR
```

## Related

- [trade-off-analysis.md](trade-off-analysis.md) - Evaluating options
- [quality-attributes-analysis.md](quality-attributes-analysis.md) - NFR context
