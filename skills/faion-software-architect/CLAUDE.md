# Software Architect

> **Entry point:** `/faion-net` — invoke for automatic routing.

System design, technology selection, Architecture Decision Records (ADRs), quality attributes.

**Methodologies:** 33 | **Agents:** 2

## When to Use

- Designing system architecture
- Technology selection decisions
- Architecture style selection (monolith, microservices, etc.)
- Database selection and data modeling
- Creating Architecture Decision Records (ADRs)
- Quality attributes analysis (scalability, performance, security)
- Communication patterns (REST, GraphQL, gRPC, async)

## Key Decision Trees

**Architecture Style:**
```
Small team / MVP → Monolith or Modular Monolith
Large team / Independent deploy → Microservices
Unclear boundaries → Modular Monolith (extract later)
```

**Database:**
```
Relational → PostgreSQL / MySQL
Document → MongoDB / DynamoDB
Key-value → Redis
Time-series → TimescaleDB
Graph → Neo4j
Search → Elasticsearch
```

**Communication:**
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

## Files

| File | Purpose |
|------|---------|
| [SKILL.md](SKILL.md) | Navigation hub with decision reference |
| [system-design-process.md](system-design-process.md) | System design workflow |
| [architecture-decision-records.md](architecture-decision-records.md) | ADR methodology |
| [adr-template.md](adr-template.md) | ADR template & examples |
| [c4-model.md](c4-model.md) | C4 model guide |

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [faion-software-developer](../faion-software-developer/CLAUDE.md) | Implements the architecture |
| [faion-devops-engineer](../faion-devops-engineer/CLAUDE.md) | Implements infrastructure |
| [faion-product-manager](../faion-product-manager/CLAUDE.md) | Provides product requirements |
| [faion-business-analyst](../faion-business-analyst/CLAUDE.md) | Provides business requirements |
| [faion-sdd](../faion-sdd/CLAUDE.md) | Uses architecture in design docs |
