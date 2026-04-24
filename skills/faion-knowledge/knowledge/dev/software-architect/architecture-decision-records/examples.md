# ADR Examples

Real-world Architecture Decision Record examples across different formats and domains.

## Example 1: Database Selection (Nygard Format)

```markdown
# ADR-001: Use PostgreSQL for Primary Database

**Status:** Accepted
**Date:** 2025-01-15
**Deciders:** Tech Lead, Senior Engineers

## Context

We are building a new e-commerce platform that requires:
- Complex queries with joins across orders, products, and users
- ACID compliance for financial transactions
- Expected load: 10k RPS, 100GB initial data growing to 1TB
- Team has 5 years of relational database experience

We need to select a primary database that will serve as the system of record
for all transactional data.

## Decision

We will use **PostgreSQL 16** as the primary database.

## Consequences

### Positive
- Strong ACID guarantees ensure data consistency
- Excellent JSON support (JSONB) for flexible attributes
- Rich ecosystem with mature tooling (pgAdmin, pgBouncer)
- Team has extensive experience, reducing learning curve
- Strong community support and regular releases
- Native support for full-text search reduces need for Elasticsearch

### Negative
- Horizontal scaling requires more effort (read replicas, Citus)
- Need to manage replication and failover ourselves
- Memory-intensive for large datasets
- Connection pooling required for high concurrency

## Alternatives Considered

### MongoDB
- Good for flexible schema and horizontal scaling
- Native sharding support
- **Rejected:** Our data is highly relational; eventual consistency
  unacceptable for financial transactions; team lacks NoSQL experience

### MySQL 8
- Similar relational capabilities, widely adopted
- Good replication options
- **Rejected:** PostgreSQL has better JSON support, more advanced
  features (CTEs, window functions), and team preference

### CockroachDB
- Distributed SQL with automatic sharding
- Strong consistency across regions
- **Rejected:** Higher operational complexity; overkill for current
  scale; team unfamiliar with distributed databases
```

## Example 2: Architecture Style (MADR Format)

```markdown
# ADR-002: Adopt Modular Monolith Architecture

## Metadata
- **Status:** Accepted
- **Date:** 2025-02-01
- **Deciders:** CTO, Engineering Leads, Architects
- **Technical Story:** [ARCH-123](https://jira.example.com/ARCH-123)

## Context and Problem Statement

We are building a B2B SaaS platform for project management. The team
consists of 12 engineers across 3 squads. We need to decide on the
initial architecture style that balances development velocity with
future scalability.

How should we structure our application to enable independent team
development while maintaining operational simplicity?

## Decision Drivers

- Team is small (12 engineers) with limited DevOps experience
- Time-to-market is critical (MVP in 6 months)
- Expected to grow to 30+ engineers in 2 years
- Must support multiple bounded contexts (Projects, Users, Billing)
- Need to minimize operational overhead initially
- Want option to extract microservices later if needed

## Considered Options

1. **Traditional Monolith** - Single codebase, single deployment
2. **Modular Monolith** - Single deployment with well-defined modules
3. **Microservices** - Separate services per bounded context

## Decision Outcome

Chosen option: **Modular Monolith**, because it provides the right
balance of development velocity, operational simplicity, and future
flexibility for our current team size and timeline.

### Positive Consequences

- Single deployment simplifies DevOps and debugging
- Clear module boundaries enable parallel team development
- Modules can be extracted to microservices when scale demands
- Easier to refactor and move code between modules
- Lower infrastructure costs initially
- Faster local development (single process)

### Negative Consequences

- Requires discipline to maintain module boundaries
- Database schema shared (need conventions for isolation)
- All modules must use same technology stack
- Single point of failure (mitigated by horizontal scaling)
- May need significant refactoring for microservices transition

## Pros and Cons of Options

### Traditional Monolith

| Aspect | Assessment |
|--------|------------|
| Development speed | Good - Simple to build and deploy |
| Team independence | Bad - Merge conflicts, coupled changes |
| Operational complexity | Good - Single deployment |
| Scalability | Neutral - Horizontal scaling possible |
| Future flexibility | Bad - Difficult to extract services |

### Modular Monolith

| Aspect | Assessment |
|--------|------------|
| Development speed | Good - Modules enable parallel work |
| Team independence | Good - Clear ownership boundaries |
| Operational complexity | Good - Single deployment |
| Scalability | Neutral - Horizontal scaling possible |
| Future flexibility | Good - Modules can become services |

### Microservices

| Aspect | Assessment |
|--------|------------|
| Development speed | Bad - Infrastructure overhead |
| Team independence | Good - Full autonomy per service |
| Operational complexity | Bad - K8s, service mesh, observability |
| Scalability | Good - Independent scaling |
| Future flexibility | Good - Already distributed |

## Links

- [Supersedes ADR-001 (rejected microservices approach)](0001-rejected-microservices.md)
- [Module boundary guidelines](../docs/module-boundaries.md)
- [Shopify's Modular Monolith](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity)
```

## Example 3: Authentication Mechanism (MADR Minimal)

```markdown
# ADR-003: Use JWT with Refresh Tokens for API Authentication

**Status:** Accepted
**Date:** 2025-02-15
**Deciders:** Security Team, Backend Lead

## Context and Problem Statement

Our API needs authentication for both web and mobile clients. We need
a stateless authentication mechanism that works across multiple
services while maintaining security.

## Decision Drivers

- Must be stateless for horizontal scaling
- Need to support mobile apps (no cookie support)
- Token revocation capability required
- Should minimize database lookups per request

## Considered Options

1. Session-based authentication (server-side sessions)
2. JWT with short expiry only
3. JWT with refresh tokens
4. OAuth 2.0 with third-party provider

## Decision Outcome

Chosen option: **JWT with refresh tokens**, because it provides
stateless authentication with the ability to revoke access through
refresh token invalidation.

### Implementation Details

- Access token: 15-minute expiry, signed with RS256
- Refresh token: 7-day expiry, stored in database
- Refresh token rotation on each use
- Blacklist compromised refresh tokens

### Positive Consequences

- Stateless access token verification (no DB lookup)
- Token revocation via refresh token invalidation
- Works with web and mobile clients
- Standard approach with library support

### Negative Consequences

- Compromised access tokens valid until expiry (15 min)
- Refresh token storage requires database
- Token refresh logic adds client complexity
- Must secure refresh token storage on clients
```

## Example 4: Y-Statement Format

### Database Selection (Y-Statement)

```markdown
# ADR-004: Database Selection for Session Storage

**Status:** Accepted
**Date:** 2025-03-01

## Decision

In the context of **the e-commerce platform checkout flow**,
facing **the need to maintain shopping cart state across multiple
application instances with sub-10ms latency**,
we decided for **Redis with cluster mode**
and neglected **PostgreSQL sessions, Memcached, and DynamoDB**
to achieve **microsecond read latency, automatic failover, and
native data structure support for cart operations**,
accepting that **we need to manage Redis infrastructure, implement
persistence for cart recovery, and handle cluster topology changes**.
```

### Message Broker Selection (Y-Statement)

```markdown
# ADR-005: Message Broker for Event-Driven Architecture

**Status:** Accepted
**Date:** 2025-03-10

## Decision

In the context of **building an event-driven order processing system**,
facing **the need for reliable, ordered event delivery with high
throughput and exactly-once processing guarantees**,
we decided for **Apache Kafka with Kafka Streams**
and neglected **RabbitMQ, Amazon SQS, and Redis Streams**
to achieve **event replay capability, strong ordering per partition,
built-in stream processing, and proven scalability to millions of
events per second**,
accepting that **operational complexity increases, we need Kafka
expertise on the team, and consumer group rebalancing can cause
temporary processing delays**.
```

## Example 5: Technology Migration (Detailed)

```markdown
# ADR-006: Migrate from REST to GraphQL for Client APIs

## Metadata
- **Status:** Accepted
- **Date:** 2025-03-20
- **Deciders:** Frontend Lead, Backend Lead, Product Manager
- **Technical Story:** [PLAT-456](https://jira.example.com/PLAT-456)
- **Supersedes:** [ADR-012 (REST API design)](0012-rest-api-design.md)

## Context and Problem Statement

Our mobile and web applications currently consume 47 REST endpoints.
Clients often need to make multiple requests to fetch related data,
leading to:
- Over-fetching (getting more data than needed)
- Under-fetching (multiple round trips)
- Tight coupling between clients and backend

Mobile app reports show:
- Average 8 API calls per screen
- 40% of data transferred is unused
- Slow 3G networks result in 6+ second page loads

How can we optimize our API to reduce data transfer and improve
client developer experience?

## Decision Drivers

- Must reduce number of API calls per screen (target: 1-2)
- Must reduce data transfer by 50%+
- Need better developer experience for frontend teams
- Want to enable rapid iteration without backend changes
- Must maintain backwards compatibility during migration
- Should support real-time updates for notifications

## Considered Options

1. **Optimize existing REST APIs** - Add sparse fieldsets, compound documents
2. **Backend for Frontend (BFF)** - Custom endpoints per client type
3. **GraphQL** - Single flexible query language
4. **gRPC** - High-performance RPC with Protocol Buffers

## Decision Outcome

Chosen option: **GraphQL**, because it directly addresses
over-fetching/under-fetching, provides excellent developer tooling,
and enables frontend teams to iterate independently.

### Implementation Strategy

1. Phase 1 (Month 1-2): GraphQL gateway alongside REST
2. Phase 2 (Month 3-4): Migrate mobile app to GraphQL
3. Phase 3 (Month 5-6): Migrate web app to GraphQL
4. Phase 4 (Month 7+): Deprecate unused REST endpoints

### Positive Consequences

- Clients request exactly the data they need
- Single request per screen (reduced from 8)
- Frontend can evolve without backend changes
- Strong typing with schema validation
- Built-in introspection and documentation
- Subscriptions enable real-time features

### Negative Consequences

- Learning curve for team (GraphQL, Apollo)
- Caching more complex than REST
- Need to prevent expensive nested queries (query complexity)
- Two APIs to maintain during migration
- Potential for N+1 query problems (mitigated by DataLoader)
- Monitoring and rate limiting require GraphQL-aware tools

## Pros and Cons of Options

### Optimize REST APIs

- Good: Low effort, team already knows REST
- Good: Established caching patterns
- Bad: Still requires multiple endpoints
- Bad: Sparse fieldsets limited in flexibility
- Bad: Backend must anticipate all client needs

### Backend for Frontend (BFF)

- Good: Optimized for each client type
- Good: No client learning curve
- Bad: Multiple BFFs to maintain
- Bad: Code duplication across BFFs
- Bad: Backend team bottleneck for client changes

### GraphQL

- Good: Single flexible API
- Good: Client-driven data fetching
- Good: Strong ecosystem (Apollo, Relay)
- Bad: Learning curve
- Bad: Caching complexity
- Bad: Query complexity attacks

### gRPC

- Good: High performance
- Good: Strong typing with Protocol Buffers
- Bad: Poor browser support (requires proxy)
- Bad: Not suitable for public APIs
- Bad: Less flexible than GraphQL for varied queries

## Links

- [GraphQL specification](https://spec.graphql.org/)
- [Apollo Federation docs](https://www.apollographql.com/docs/federation/)
- [Query complexity analysis](../docs/graphql-security.md)
- [Migration tracking board](https://jira.example.com/PLAT-456)
```

## Example 6: Infrastructure Decision

```markdown
# ADR-007: Use Kubernetes for Container Orchestration

**Status:** Accepted
**Date:** 2025-04-01
**Deciders:** Platform Team, SRE Lead, CTO

## Context

We are containerizing our applications and need an orchestration
platform. Current state:
- 15 microservices in Docker containers
- Manual deployment via shell scripts
- No auto-scaling or self-healing
- Deployments take 2+ hours with downtime

Requirements:
- Zero-downtime deployments
- Automatic scaling based on load
- Self-healing (restart failed containers)
- Service discovery and load balancing
- Secret management

## Decision

We will use **Amazon EKS (Elastic Kubernetes Service)** for container
orchestration.

## Consequences

### Positive
- Industry-standard orchestration platform
- Rich ecosystem (Helm, ArgoCD, Prometheus)
- Automatic scaling with HPA/VPA
- Built-in service discovery and load balancing
- EKS manages control plane (reduced operational burden)
- Portable skills and configurations

### Negative
- Steep learning curve for team
- EKS costs ($0.10/hour per cluster + EC2)
- Need to manage worker nodes and networking
- YAML configuration complexity
- Debugging distributed systems is harder

## Alternatives Considered

### Amazon ECS
- Simpler than Kubernetes
- Native AWS integration
- **Rejected:** Less portable; fewer community resources;
  limited ecosystem compared to Kubernetes

### Docker Swarm
- Simpler than Kubernetes
- Built into Docker
- **Rejected:** Limited ecosystem; declining adoption;
  fewer features for complex deployments

### Nomad
- Simpler than Kubernetes
- Multi-workload (containers, VMs, binaries)
- **Rejected:** Smaller community; team prefers Kubernetes
  for career growth; less tooling available
```

## Example 7: Superseding an ADR

```markdown
# ADR-008: Migrate from MongoDB to PostgreSQL for User Service

**Status:** Accepted
**Date:** 2025-05-01
**Deciders:** Backend Team, Data Team
**Supersedes:** [ADR-003: Use MongoDB for User Service](0003-mongodb-user-service.md)

## Context

ADR-003 (2023-06-01) selected MongoDB for the User Service based on:
- Expected flexible schema requirements
- Anticipated horizontal scaling needs
- Team experimentation with NoSQL

After 2 years of operation, we've learned:
- Schema is actually stable (rarely changes)
- Joins needed for reporting (implemented in app layer)
- Scaling needs are modest (50k users)
- Aggregation queries are complex and slow
- Team prefers SQL for queries

## Decision

We will migrate the User Service from MongoDB to PostgreSQL.

## Consequences

### Positive
- Joins at database level simplify reporting
- SQL expertise is more common on team
- JSONB covers any flexible data needs
- Consistent with other services (reduces cognitive load)
- Better tooling for analytics

### Negative
- Migration effort (estimated 2 sprints)
- Risk of data loss during migration
- Temporary performance degradation
- Need to update all queries

## Migration Plan

1. Create PostgreSQL schema
2. Implement dual-write (both databases)
3. Backfill historical data
4. Validate data consistency
5. Switch reads to PostgreSQL
6. Remove MongoDB writes
7. Decommission MongoDB

## Links

- **Supersedes:** [ADR-003: Use MongoDB for User Service](0003-mongodb-user-service.md)
- Migration runbook: [USER-SVC-MIGRATION.md](../runbooks/user-svc-migration.md)
```

## Example 8: Rejected ADR

```markdown
# ADR-009: Implement GraphQL Subscriptions for Real-Time Updates

**Status:** Rejected
**Date:** 2025-05-15
**Deciders:** Backend Lead, Frontend Lead, Infrastructure Team

## Context

Product requests real-time notifications for:
- Order status updates
- Chat messages
- Inventory alerts

We evaluated adding GraphQL Subscriptions to our existing
GraphQL API for real-time functionality.

## Decision

We will **NOT** implement GraphQL Subscriptions at this time.

## Rationale for Rejection

1. **Infrastructure complexity**: Subscriptions require WebSocket
   connections, which our current ALB setup doesn't support well.

2. **Limited use cases**: Only 3 features need real-time updates,
   not justifying the infrastructure investment.

3. **Alternative exists**: Server-Sent Events (SSE) can handle our
   use cases with simpler infrastructure.

4. **Team capacity**: Infrastructure team is focused on Kubernetes
   migration; cannot take on WebSocket infrastructure.

## Recommended Alternative

Use Server-Sent Events (SSE) for real-time updates:
- Works over HTTP/1.1 (no WebSocket infrastructure needed)
- Simpler client implementation
- Sufficient for unidirectional server-to-client updates
- Can migrate to Subscriptions later if bidirectional needs arise

See [ADR-010: Use SSE for Real-Time Updates](0010-sse-real-time.md)

## Conditions for Reconsideration

Revisit GraphQL Subscriptions when:
- Bidirectional real-time communication is required
- WebSocket infrastructure is established
- More than 10 features need real-time updates
```

## Example 9: Living ADR (Continuously Updated)

```markdown
# ADR-010: Approved Technology Stack

**Status:** Living
**Last Updated:** 2025-06-01
**Owners:** Architecture Guild

## Purpose

This living ADR documents our approved technology stack. It is
updated quarterly based on technology radar reviews.

## Current Stack (Q2 2025)

### Languages
| Category | Approved | Trial | Hold |
|----------|----------|-------|------|
| Backend | Python, Go | Rust | Java |
| Frontend | TypeScript | - | JavaScript |
| Scripts | Python, Bash | - | Perl |

### Frameworks
| Category | Approved | Trial | Hold |
|----------|----------|-------|------|
| Backend | FastAPI, Django | - | Flask |
| Frontend | React, Next.js | Remix | Vue |
| Mobile | React Native | Flutter | Ionic |

### Databases
| Category | Approved | Trial | Hold |
|----------|----------|-------|------|
| Relational | PostgreSQL | - | MySQL |
| Document | - | MongoDB | - |
| Cache | Redis | - | Memcached |
| Search | Elasticsearch | Meilisearch | Solr |

### Infrastructure
| Category | Approved | Trial | Hold |
|----------|----------|-------|------|
| Containers | Kubernetes (EKS) | - | ECS |
| IaC | Terraform | Pulumi | CloudFormation |
| CI/CD | GitHub Actions | - | Jenkins |

## Change Log

| Date | Change | Rationale |
|------|--------|-----------|
| 2025-06-01 | Added Meilisearch to Trial | Faster search for small datasets |
| 2025-03-01 | Moved Rust to Trial | Performance-critical services |
| 2024-12-01 | Moved Flask to Hold | Standardize on FastAPI |

## Exception Process

To use technology not on the approved list:
1. Write ADR explaining need
2. Get Architecture Guild review
3. Present trade-offs to Tech Lead
4. If approved, technology enters Trial status
```

## Common Patterns Across Examples

| Pattern | Usage |
|---------|-------|
| Clear status | Always explicitly stated |
| Date tracking | Both decision and last-update dates |
| Stakeholder identification | Deciders listed |
| Problem-first context | Why before what |
| Multiple alternatives | At least 3 options considered |
| Explicit trade-offs | Both positive and negative consequences |
| Links to related decisions | Supersedes, references |
| Actionable next steps | Migration plans, implementation details |
