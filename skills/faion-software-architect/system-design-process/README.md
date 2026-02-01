# System Design Process

Practical guide to designing software systems, from requirements to architecture.

## Overview

This methodology adapts the system design interview approach for real-world projects. Instead of whiteboard exercises, you produce actionable artifacts: specs, ADRs, C4 diagrams, and implementation plans.

**Key Insight:** LLMs have transformed architecture work. Use them for trade-off analysis, pattern selection, and documentation generation while maintaining human judgment on critical decisions.

## Process Phases

```
1. UNDERSTAND  →  2. SCOPE  →  3. DESIGN  →  4. VALIDATE  →  5. DOCUMENT
   (What)          (Boundaries)  (How)        (Verify)        (Record)
```

| Phase | Output | LLM Assistance |
|-------|--------|----------------|
| Understand | Requirements list | Clarifying questions, NFR checklist |
| Scope | In/out of scope doc | MVP vs full feature analysis |
| Design | Architecture diagrams | Pattern suggestions, trade-off analysis |
| Validate | Review feedback | Risk identification, bottleneck analysis |
| Document | ADRs, C4 diagrams | Template generation, diagram code |

## Requirements Gathering

### Functional Requirements (FR)

What the system **does**:

- User stories with acceptance criteria
- Use cases with actors and flows
- API contracts and data models
- Integration points

**Questions to Ask:**
1. Who are the users? What are their goals?
2. What are the core features vs nice-to-have?
3. What data does the system handle?
4. What external systems does it integrate with?

### Non-Functional Requirements (NFR)

How the system **performs**:

| Attribute | Question | Typical Metrics |
|-----------|----------|-----------------|
| **Scalability** | How many users/requests? | DAU, RPS, concurrent users |
| **Availability** | What uptime is required? | 99.9% (8.76h/year down), 99.99% (52min/year) |
| **Latency** | How fast must it respond? | p50 < 100ms, p95 < 200ms, p99 < 500ms |
| **Durability** | Can we lose data? | RPO (recovery point), RTO (recovery time) |
| **Consistency** | Strong or eventual? | CAP trade-off (CP vs AP) |
| **Security** | What threats exist? | Threat model, compliance (GDPR, SOC2) |

### Scale Estimation

Back-of-envelope calculations for capacity planning:

```
# Traffic
DAU = Daily Active Users
RPS = DAU * requests_per_user / 86400
Peak_RPS = RPS * 3 (typical peak multiplier)

# Storage
Storage/day = objects/day * avg_object_size
Storage/year = Storage/day * 365 * replication_factor

# Bandwidth
Bandwidth = RPS * avg_response_size

# Cache
Cache_size = hot_data_percentage * total_data (typically 20%)
```

## LLM-Assisted Design

### How LLMs Help

1. **Trade-off Analysis**: Present options, get structured comparison
2. **Pattern Selection**: Describe problem, get pattern recommendations
3. **Risk Identification**: Share design, get potential failure modes
4. **Documentation**: Generate ADRs, diagrams, specs from conversations
5. **Code Review**: Validate architecture alignment in implementations

### Workflow with LLMs

```
1. Define spec.md with LLM (iterative Q&A until complete)
2. Brainstorm architecture options (ask for 3+ alternatives)
3. Evaluate trade-offs (structured comparison)
4. Generate C4 diagrams (Mermaid code)
5. Create ADRs (capture decisions)
6. Review implementation plan (identify gaps)
```

### When to Override LLM Suggestions

- Domain-specific constraints not in training data
- Organizational preferences (tech stack, vendors)
- Cost/budget limitations
- Team skill constraints
- Regulatory/compliance requirements

## Architecture Styles Decision Tree

```
Project Type?
├── MVP / Small team → Monolith
│   └── Growing? → Modular Monolith
├── Multiple teams / Independent deploy → Microservices
├── Event-driven workflows → Event Sourcing + CQRS
├── Real-time data processing → Streaming (Kafka, Flink)
└── Unclear boundaries → Modular Monolith (extract later)
```

## Common Design Patterns

| Pattern | Use Case | Trade-off |
|---------|----------|-----------|
| **Load Balancer** | Distribute traffic | + Scalability, - Single point of failure |
| **CDN** | Static content | + Latency, - Cache invalidation complexity |
| **Cache** (Redis) | Reduce DB load | + Speed, - Data staleness |
| **Message Queue** | Async processing | + Decoupling, - Eventual consistency |
| **Database Replication** | Read scaling | + Availability, - Replication lag |
| **Sharding** | Write scaling | + Throughput, - Cross-shard queries |
| **Rate Limiting** | Abuse protection | + Security, - User experience |
| **Circuit Breaker** | Fault tolerance | + Resilience, - Complexity |

## C4 Model Overview

The C4 model provides four levels of abstraction:

| Level | Name | Shows | Audience |
|-------|------|-------|----------|
| 1 | Context | System + actors | Everyone |
| 2 | Container | Apps, DBs, services | Tech leads |
| 3 | Component | Modules within container | Developers |
| 4 | Code | Classes, functions | Developers |

**Rule:** Start at Context, zoom in as needed. Most projects need L1-L2 only.

See [templates.md](templates.md) for Mermaid C4 diagram examples.

## Quality Gates

Before finalizing architecture:

- [ ] All NFRs have measurable targets
- [ ] Scale estimates calculated
- [ ] Single points of failure identified
- [ ] Data model supports all use cases
- [ ] API contracts defined
- [ ] Security threat model completed
- [ ] Cost estimation done
- [ ] Migration path defined (if replacing existing system)

## Files in This Directory

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview |
| [checklist.md](checklist.md) | Step-by-step system design checklist |
| [examples.md](examples.md) | Case studies: Twitter, Uber, Netflix |
| [templates.md](templates.md) | ADR templates, C4 diagrams in Mermaid |
| [llm-prompts.md](llm-prompts.md) | Prompts for architecture discussions |

## External Resources

### Essential Reading

- [System Design Primer](https://github.com/donnemartin/system-design-primer) - Comprehensive GitHub resource
- [ByteByteGo](https://bytebytego.com/) - Visual system design guides by Alex Xu
- [Designing Data-Intensive Applications](https://dataintensive.net/) - Martin Kleppmann's book

### Architecture Documentation

- [C4 Model](https://c4model.com/) - Simon Brown's visualization approach
- [ADR GitHub](https://adr.github.io/) - Architecture Decision Records
- [arc42](https://arc42.org/) - Software architecture documentation template

### Tools

- [Structurizr](https://structurizr.com/) - C4 diagrams as code
- [Mermaid](https://mermaid.js.org/syntax/c4.html) - Diagrams in markdown
- [Excalidraw](https://excalidraw.com/) - Whiteboard-style diagrams


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Methodologies

- [architecture-decision-records.md](../architecture-decision-records.md) - ADR deep dive
- [c4-model.md](../c4-model.md) - C4 visualization guide
- [quality-attributes-analysis.md](../quality-attributes-analysis.md) - NFR analysis
- [trade-off-analysis.md](../trade-off-analysis.md) - Decision making framework
