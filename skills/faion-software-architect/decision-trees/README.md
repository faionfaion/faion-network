# Architecture Decision Trees

Structured decision frameworks for making architecture choices systematically. Decision trees help architects analyze trade-offs and reach optimal outcomes by breaking complex decisions into manageable, sequential questions.

## Overview

Architecture decisions are among the most impactful choices in software development. Poor decisions lead to:
- 40% higher development costs (Gartner 2024)
- 60% longer time-to-market
- Technical debt that compounds over years

This guide provides decision trees for the most common architecture choices, updated for 2025-2026 best practices.

## Decision Tree Categories

| Category | Key Decisions | File |
|----------|---------------|------|
| Architecture Style | Monolith vs Microservices vs Modular Monolith | This file |
| Technology Selection | Framework, language, tools | This file |
| Database Selection | SQL vs NoSQL vs NewSQL vs Vector | [database-selection/](../database-selection/) |
| Cloud Provider | AWS vs Azure vs GCP | This file |
| Build vs Buy | Custom development vs commercial solutions | This file |
| API Design | REST vs GraphQL vs gRPC | [api-gateway-design/](../api-gateway-design/) |
| Caching Strategy | Patterns and invalidation | [caching-architecture/](../caching-architecture/) |

## Core Decision Trees

### 1. Architecture Style Decision Tree

```
Q1: Team size and organization?
    |
    +-- "<10 developers" ----------------------------------------+
    |   Recommendation: Monolith                                 |
    |   Reason: Simplicity, speed, easy debugging                |
    |   Future: Extract services when pain points emerge         |
    |                                                            |
    +-- "10-50 developers" --------------------------------------+
    |   Recommendation: Modular Monolith                         |
    |   Reason: Structure without distribution complexity        |
    |   Pattern: Domain modules with clear interfaces            |
    |   Tools: Packwerk (Ruby), ArchUnit (Java), custom linters  |
    |                                                            |
    +-- "50+ developers" ----------------------------------------+
        Q2: DevOps maturity?
            |
            +-- "High (CI/CD, monitoring, distributed tracing)" -+
            |   Recommendation: Microservices                    |
            |   Preconditions:                                   |
            |   - Bounded contexts are clear                     |
            |   - Teams can own services end-to-end              |
            |   - Platform team exists                           |
            |                                                    |
            +-- "Low to Medium" ---------------------------------+
                Recommendation: Modular Monolith                 |
                Action: Build platform capabilities first        |
```

**Industry Data (2025):**
- 42% of organizations that adopted microservices have consolidated services back (CNCF 2025)
- Amazon Prime Video cut costs 90% migrating from microservices to monolith
- Shopify maintains 2.8M-line Ruby monolith serving millions of merchants

**Decision Thresholds:**
| Metric | Monolith | Modular Monolith | Microservices |
|--------|----------|------------------|---------------|
| Team size | 1-10 | 10-50 | 50+ |
| Revenue | <$1M | $1M-$10M | $10M+ |
| Deployment frequency | Weekly | Daily | Multiple/day |
| DevOps maturity | Low | Medium | High |

---

### 2. Technology Stack Decision Tree

```
Q1: What type of application?
    |
    +-- "Web Application" ---------------------------------------+
    |   Q2: SEO requirements?                                    |
    |       |                                                    |
    |       +-- "Critical (marketing, e-commerce)" --------------+
    |       |   -> Next.js or Astro (SSR/SSG)                    |
    |       |                                                    |
    |       +-- "Not critical (dashboard, internal tool)" -------+
    |           Q3: Team expertise?                              |
    |               +-- "React" -> React + Vite                  |
    |               +-- "Vue" -> Vue + Nuxt                      |
    |               +-- "Angular" -> Angular                     |
    |               +-- "None/New" -> Next.js (largest ecosystem)|
    |                                                            |
    +-- "API/Backend" -------------------------------------------+
    |   Q2: Performance requirements?                            |
    |       |                                                    |
    |       +-- "Standard (<1000 RPS)" --------------------------+
    |       |   Q3: Team expertise?                              |
    |       |       +-- "Python" -> Django or FastAPI            |
    |       |       +-- "JavaScript" -> Node.js + Express/Fastify|
    |       |       +-- "Java/.NET" -> Spring Boot or .NET       |
    |       |       +-- "None" -> FastAPI (Python) or Go         |
    |       |                                                    |
    |       +-- "High performance (>10k RPS)" -------------------+
    |           -> Go, Rust, or C++                              |
    |                                                            |
    +-- "Mobile Application" ------------------------------------+
    |   Q2: Platform requirements?                               |
    |       +-- "Both iOS + Android" -> React Native or Flutter  |
    |       +-- "iOS only" -> Swift/SwiftUI                      |
    |       +-- "Android only" -> Kotlin                         |
    |       +-- "Web + Mobile" -> React Native + Next.js         |
    |                                                            |
    +-- "Data/ML Pipeline" --------------------------------------+
        -> Python (pandas, Spark, dbt, Airflow)
```

**Framework Market Share (2025):**
| Category | Leader | Usage |
|----------|--------|-------|
| Frontend | React | 39% |
| Meta-framework | Next.js | 68% of React devs |
| Backend (Python) | FastAPI | Growing fastest |
| Backend (JS) | Express | 50%+ |
| Mobile | React Native | 42% cross-platform |

---

### 3. Cloud Provider Decision Tree

```
Q1: Current technology investments?
    |
    +-- "Microsoft ecosystem (AD, Office 365, .NET)" ------------+
    |   -> Azure (best integration, hybrid cloud)                |
    |                                                            |
    +-- "Google Workspace, BigQuery, AI/ML focus" ---------------+
    |   -> GCP (best for analytics, Kubernetes, AI)              |
    |                                                            |
    +-- "No strong preference" ----------------------------------+
        Q2: Primary workload type?
            |
            +-- "Enterprise, diverse workloads" -----------------+
            |   -> AWS (broadest services, largest community)    |
            |                                                    |
            +-- "Data analytics, ML/AI" -------------------------+
            |   -> GCP (BigQuery, Vertex AI, TPUs)               |
            |                                                    |
            +-- "Hybrid cloud (on-prem + cloud)" ----------------+
            |   -> Azure (Azure Arc, Stack HCI)                  |
            |                                                    |
            +-- "Kubernetes-native" -----------------------------+
            |   -> GCP (created K8s, GKE is best-in-class)       |
            |                                                    |
            +-- "Cost-sensitive startup" ------------------------+
                -> GCP (sustained use discounts, free tier)
                -> or AWS (most optimization tools)
```

**Market Share (Q2 2025):**
| Provider | Share | Best For |
|----------|-------|----------|
| AWS | 31% | Breadth, enterprise, startups |
| Azure | 25% | Microsoft shops, hybrid, enterprise |
| GCP | 11% | Analytics, AI/ML, Kubernetes |

**Cost Comparison Tips:**
- AWS: Best discounts for reserved instances (up to 72%)
- GCP: Automatic sustained use discounts (up to 30%)
- Azure: Best for existing Microsoft licensing (BYOL)

---

### 4. Build vs Buy Decision Tree

```
Q1: Is this capability a competitive differentiator?
    |
    +-- "Yes (core to business value)" --------------------------+
    |   Q2: Do commercial solutions exist?                       |
    |       +-- "No" -> Build                                    |
    |       +-- "Yes, but inadequate" -> Build or Extend         |
    |       +-- "Yes, fully adequate" -> Q3                      |
    |           Q3: Can you afford the dependency risk?          |
    |               +-- "Yes" -> Buy, focus on differentiation   |
    |               +-- "No" -> Build for strategic control      |
    |                                                            |
    +-- "No (commodity/utility)" --------------------------------+
        Q2: Budget and timeline?
            +-- "Limited budget, fast timeline" -> Buy           |
            +-- "Adequate budget, flexible timeline" -> Q3       |
                Q3: Integration complexity?                      |
                    +-- "High (many custom integrations)" -------+
                    |   -> Build or low-code platform            |
                    +-- "Low (standard integrations)" -----------+
                        -> Buy
```

**2025 Statistics:**
- 67% of failed software implementations stem from incorrect build vs buy decisions (Forrester 2024)
- 35% of large enterprise custom software initiatives are abandoned (Standish Group 2024)
- Organizations with structured decision frameworks report 30-40% fewer implementation failures

**Weighted Scorecard Criteria:**
| Factor | Weight | Build Score | Buy Score |
|--------|--------|-------------|-----------|
| Strategic importance | 30% | High if core | Low if commodity |
| Time to value | 20% | 3-12 months | 1-4 weeks |
| Total cost (3yr) | 20% | Higher upfront | Subscription |
| Integration fit | 15% | Perfect fit | May need adapters |
| Team capability | 15% | Requires skills | Vendor support |

---

### 5. Database Selection Quick Reference

See [database-selection/](../database-selection/) for full decision tree.

**Quick Decision:**
```
Transactional data with joins    -> PostgreSQL
Document-oriented, flexible      -> MongoDB
Key-value, sessions, cache       -> Redis
Time-series metrics              -> TimescaleDB or ClickHouse
Graph relationships              -> Neo4j
Full-text search                 -> Elasticsearch or Meilisearch
Vector embeddings (AI/RAG)       -> Qdrant, Weaviate, or pgvector
Analytics, OLAP                  -> ClickHouse or BigQuery
```

---

## LLM-Assisted Decision Making

### When to Use LLMs

LLMs excel at:
- Generating comprehensive option lists
- Identifying trade-offs you might miss
- Creating structured comparison matrices
- Drafting ADRs from decisions
- Exploring "what if" scenarios

LLMs struggle with:
- Company-specific context (provide it!)
- Current pricing (verify externally)
- Team dynamics and politics
- Predicting future technology trends

### Effective Prompting

**Structure your prompts:**
1. Provide context (team size, budget, existing stack)
2. State the decision clearly
3. List constraints
4. Ask for structured output (table, decision tree, ADR)

See [llm-prompts.md](llm-prompts.md) for copy-paste prompts.

---

## Best Practices

### 1. Document Decisions

Use Architecture Decision Records (ADRs):
- See [architecture-decision-records/](../architecture-decision-records/)
- Store in `/docs/adr/` or `/architecture/decisions/`
- Use MADR format for consistency

### 2. Validate with POC

Before committing to major decisions:
- Build a minimal proof of concept
- Test integration points
- Measure actual performance
- Involve the team in evaluation

### 3. Plan for Evolution

Architecture should allow change:
- Start simple, evolve when needed
- Design for replaceability
- Document assumptions explicitly
- Review decisions periodically

### 4. Consider Total Cost of Ownership

Look beyond initial costs:
- Implementation/development
- Maintenance and operations
- Training and onboarding
- Migration/exit costs
- Opportunity costs

---

## External Resources

### Books
- "Software Architecture: The Hard Parts" - Ford, Richards, Sadalage, Dehghani (2021)
- "Fundamentals of Software Architecture" - Richards, Ford (2020)
- "Building Evolutionary Architectures" - Ford, Parsons, Kua (2017)

### Articles & Guides
- [ADR GitHub Organization](https://adr.github.io/) - ADR templates and tools
- [Architecture Decision Record Examples](https://github.com/joelparkerhenderson/architecture-decision-record) - Comprehensive ADR repository
- [Microsoft Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

### Industry Reports
- [State of Software Architecture Report 2025](https://icepanel.medium.com/state-of-software-architecture-report-2025-12178cbc5f93) - IcePanel
- [O'Reilly Technology Radar](https://www.oreilly.com/radar/)
- CNCF Annual Survey

### Decision Frameworks
- [ATAM (Architecture Tradeoff Analysis Method)](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=513908) - SEI/CMU
- [UK Government ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework)

---

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview document |
| [checklist.md](checklist.md) | Step-by-step decision making checklist |
| [examples.md](examples.md) | Real-world decision tree examples |
| [templates.md](templates.md) | Copy-paste decision tree templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted decisions |

---

## Related Methodologies

| Folder | Relationship |
|--------|--------------|
| [architecture-decision-records/](../architecture-decision-records/) | Document decisions |
| [trade-off-analysis/](../trade-off-analysis/) | Analyze trade-offs |
| [database-selection/](../database-selection/) | Database decisions |
| [cloud-architecture/](../cloud-architecture/) | Cloud decisions |
| [microservices-architecture/](../microservices-architecture/) | Microservices patterns |
| [modular-monolith/](../modular-monolith/) | Modular monolith patterns |

---

*Architecture Decision Trees v2.0 - Updated January 2026*
