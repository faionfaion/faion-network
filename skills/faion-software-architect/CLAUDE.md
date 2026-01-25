# faion-software-architect

<<<<<<< HEAD
Software architecture skill for system design, technology selection, and architecture decision records.

## Overview

| Metric | Value |
|--------|-------|
| Methodologies | 28 |
| Agents | 2 |

## Directory Structure

```
faion-software-architect/
├── SKILL.md                    # Main skill definition
├── CLAUDE.md                   # This file
├── decision-trees.md           # Architecture decision trees
└── patterns.md                 # Design patterns reference
```

## When to Use

| Trigger | Action |
|---------|--------|
| "Design architecture for..." | System design workflow |
| "Should we use X or Y?" | Technology selection |
| "How to scale to...?" | Quality attributes analysis |
| "Document why we chose..." | Create ADR |
| "Review this architecture" | Design review |

## Key Decision Trees

### Architecture Style

=======
> **Entry Point:** Invoked via [/faion-net](../faion-net/CLAUDE.md) or directly as `/faion-software-architect`

## When to Use

- Designing system architecture
- Technology selection decisions
- Architecture style selection (monolith, microservices, etc.)
- Database selection and data modeling
- Creating Architecture Decision Records (ADRs)
- Quality attributes analysis (scalability, performance, security)
- Communication patterns (REST, GraphQL, gRPC, async)
- Design reviews and architecture audits

## Overview

Software architecture skill for system design, technology selection, and architecture decision records.

**Methodologies:** 28 | **Agents:** 2

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Navigation hub with decision reference |
| [system-design-process.md](system-design-process.md) | System design workflow |
| [architecture-decision-records.md](architecture-decision-records.md) | ADR methodology |
| [adr-template.md](adr-template.md) | ADR template & examples |
| [c4-model.md](c4-model.md) | C4 model guide |

## Key Decision Trees

**Architecture Style:**
>>>>>>> claude
```
Small team / MVP → Monolith or Modular Monolith
Large team / Independent deploy → Microservices
Unclear boundaries → Modular Monolith (extract later)
```

<<<<<<< HEAD
### Database Selection

```
Relational data → PostgreSQL / MySQL
Document data → MongoDB / DynamoDB
=======
**Database:**
```
Relational → PostgreSQL / MySQL
Document → MongoDB / DynamoDB
>>>>>>> claude
Key-value → Redis
Time-series → TimescaleDB
Graph → Neo4j
Search → Elasticsearch
```

<<<<<<< HEAD
### Communication Pattern

=======
**Communication:**
>>>>>>> claude
```
Sync internal → gRPC or REST
Sync external → REST or GraphQL
Async ordered → Kafka
Async unordered → RabbitMQ / SQS
Real-time → WebSockets or SSE
```

## Quality Attributes

| Attribute | Key Question |
|-----------|--------------|
| Scalability | Handle 10x load? |
| Performance | Latency p95 < 200ms? |
| Availability | 99.9% or 99.99%? |
| Security | Threat model done? |
| Maintainability | Deploy daily? |

<<<<<<< HEAD
## ADR Template (Quick)

```markdown
# ADR-NNN: Title
## Status: Proposed/Accepted
## Context: Why is this decision needed?
## Decision: What we decided
## Consequences: Trade-offs
## Alternatives: What else was considered
```

=======
>>>>>>> claude
## Related Skills

| Skill | Relationship |
|-------|--------------|
<<<<<<< HEAD
| faion-software-developer | Implements the architecture |
| faion-devops-engineer | Implements infrastructure |
| faion-product-manager | Provides requirements |

---

*faion-software-architect v1.0*
=======
| [faion-net](../faion-net/CLAUDE.md) | Parent orchestrator |
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Implements the architecture |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | Implements infrastructure |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Provides product requirements |
| [faion-business-analyst](../faion-business-analyst/CLAUDE.md) | Provides business requirements |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Uses architecture in design docs |

---

*faion-software-architect v1.1*
>>>>>>> claude
