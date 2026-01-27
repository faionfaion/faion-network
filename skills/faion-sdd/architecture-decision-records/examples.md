# ADR Examples

Real-world Architecture Decision Record examples from open-source projects and practical scenarios.

## Example 1: Database Selection (Nygard Format)

From a typical web application project:

```markdown
# ADR-0003: Use PostgreSQL as Primary Database

**Status:** Accepted
**Date:** 2025-09-15
**Deciders:** Alice Chen, Bob Smith, Carol Wang

## Context

Our e-commerce platform needs a relational database to store:
- User accounts and authentication data
- Product catalog (10k+ products)
- Order history and transactions
- Inventory management

The team has experience with MySQL and PostgreSQL. We need ACID compliance
for financial transactions. Expected load is 1000 concurrent users initially,
scaling to 10,000 within two years.

## Decision

We will use PostgreSQL 16 as our primary database.

## Alternatives Considered

### MySQL 8.0
- **Pros:** Familiar to 3/5 team members, good tooling, widely deployed
- **Cons:** Less advanced JSON support, weaker full-text search
- **Why rejected:** PostgreSQL's JSONB and full-text search better fit our
  product catalog requirements

### MongoDB
- **Pros:** Flexible schema, horizontal scaling, JSON-native
- **Cons:** No ACID transactions across collections, team unfamiliar
- **Why rejected:** ACID compliance critical for payment processing

## Consequences

### Positive
- Strong ACID compliance for financial transactions
- Advanced JSONB support for flexible product attributes
- Built-in full-text search eliminates need for Elasticsearch initially
- Excellent geospatial support if we add location features

### Negative
- 2/5 team members need PostgreSQL training
- Horizontal scaling more complex than MongoDB (may need Citus later)
- Slightly higher operational complexity than MySQL

### Neutral
- Will use pgAdmin for administration
- Deployment via Docker with official postgres image
```

## Example 2: API Design (MADR Format)

Adapted from MADR template:

```markdown
# Use REST over GraphQL for Public API

* Status: accepted
* Deciders: API Team, Platform Architects
* Date: 2025-10-20

## Context and Problem Statement

We need to design a public API for third-party integrations. Should we use
REST, GraphQL, or gRPC?

## Decision Drivers

* Developer experience for API consumers
* Caching capabilities
* Team expertise
* API documentation tooling
* Mobile app requirements (bandwidth considerations)

## Considered Options

* REST with OpenAPI
* GraphQL
* gRPC

## Decision Outcome

Chosen option: "REST with OpenAPI", because:
- Better caching at HTTP level
- Wider ecosystem adoption for third-party developers
- Excellent OpenAPI tooling for documentation
- Team has extensive REST experience

### Consequences

* Good, because HTTP caching reduces server load
* Good, because extensive tooling ecosystem (Swagger, Postman)
* Good, because familiar to most third-party developers
* Bad, because over-fetching/under-fetching issues for complex queries
* Bad, because multiple round-trips for related resources

### Confirmation

We will validate this decision by:
1. Building MVP API endpoints
2. Gathering feedback from beta partners
3. Measuring API response times and payload sizes
4. Reassessing after 6 months of production use

## Pros and Cons of the Options

### REST with OpenAPI

* Good, because industry standard, well understood
* Good, because excellent caching
* Good, because simpler to implement and maintain
* Bad, because fixed response structure
* Bad, because versioning can be complex

### GraphQL

* Good, because flexible queries, no over-fetching
* Good, because strong typing with schema
* Good, because single endpoint simplicity
* Bad, because caching is complex
* Bad, because learning curve for consumers
* Bad, because security considerations (query complexity)

### gRPC

* Good, because high performance, strongly typed
* Good, because excellent for microservice communication
* Bad, because poor browser support
* Bad, because less familiar to third-party developers
* Bad, because binary protocol harder to debug

## More Information

See also:
- ADR-0005: API Versioning Strategy
- ADR-0008: Rate Limiting Implementation
```

## Example 3: Frontend Framework (Y-Statement Format)

```markdown
# ADR-0007: Frontend Framework Selection

**Status:** Accepted
**Date:** 2025-11-01
**Deciders:** Frontend Team

## Y-Statement

In the context of building a customer-facing dashboard,
facing the need for fast initial load times and SEO optimization,
we decided for Next.js with React Server Components
and against Create React App or Vite SPA,
to achieve better Core Web Vitals and search engine indexing,
accepting that the team needs to learn Server Components patterns
and that deployment requires a Node.js runtime instead of static hosting.

## Extended Context

The marketing dashboard needs:
- Public-facing landing pages (SEO critical)
- Authenticated user dashboard (SPA-like experience)
- Shared component library with marketing site

## Alternatives Rejected

| Option | Why Rejected |
|--------|--------------|
| Create React App | No SSR, poor SEO, deprecated by React team |
| Vite + React | Excellent DX but no built-in SSR |
| Remix | Good option but smaller ecosystem than Next.js |
| Astro | Great for content sites but less suited for apps |

## Consequences

- (+) SEO-optimized landing pages
- (+) Fast initial page loads via SSR
- (+) Incremental adoption of Server Components
- (+) Vercel deployment integration
- (-) Team learning curve for RSC patterns
- (-) More complex caching strategy
- (-) Server runtime costs vs static hosting
```

## Example 4: Authentication Strategy (Extended Format)

```markdown
# ADR-0012: Authentication and Authorization Strategy

**Status:** Accepted
**Date:** 2025-08-20
**Deciders:** Security Team, Backend Team, Product Owner
**Technical Story:** SEC-123

## Context

### Current State
Our application currently uses session-based authentication with cookies.
As we expand to mobile apps and third-party API access, we need a more
flexible authentication strategy.

### Requirements
- Support web, mobile, and API clients
- Enable third-party integrations via API keys
- Comply with SOC 2 requirements
- Support MFA for sensitive operations
- Enable SSO for enterprise customers

### Constraints
- Must maintain backward compatibility during migration
- Budget: No additional SaaS costs > $500/month
- Timeline: Must be production-ready within Q1 2026
- Team has limited OAuth2/OIDC experience

## Decision

We will implement JWT-based authentication with the following approach:

1. **Access tokens**: Short-lived JWTs (15 minutes) for API authentication
2. **Refresh tokens**: Long-lived tokens (7 days) stored securely
3. **Identity provider**: Auth0 for SSO and enterprise features
4. **API keys**: For server-to-server integrations
5. **MFA**: TOTP-based, required for admin operations

## Alternatives Considered

### Option 1: Keep Session-Based Auth
- **Description:** Enhance current session auth with API token support
- **Pros:**
  - No migration needed
  - Team already familiar
  - Simpler implementation
- **Cons:**
  - Doesn't scale well for mobile/API
  - No built-in SSO support
  - Session storage becomes bottleneck
- **Estimated effort:** Low
- **Risk:** High (technical debt, scalability issues)

### Option 2: JWT with Self-Hosted Identity Server
- **Description:** Use Keycloak or similar for identity management
- **Pros:**
  - Full control over auth infrastructure
  - No per-user SaaS costs
  - OIDC compliant
- **Cons:**
  - Significant operational overhead
  - Security expertise required
  - Higher initial implementation cost
- **Estimated effort:** High
- **Risk:** Medium (operational complexity)

### Option 3: JWT with Auth0 (Chosen)
- **Description:** Use Auth0 for identity, custom JWT validation
- **Pros:**
  - Enterprise SSO out of the box
  - MFA included
  - SOC 2 compliant
  - Reduced security responsibility
- **Cons:**
  - Per-user pricing at scale
  - Vendor lock-in risk
  - External dependency
- **Estimated effort:** Medium
- **Risk:** Low

## Decision Matrix

| Criterion | Weight | Session | Keycloak | Auth0 |
|-----------|--------|---------|----------|-------|
| Mobile support | 5 | 2 | 5 | 5 |
| SSO capability | 4 | 1 | 5 | 5 |
| Team expertise | 3 | 5 | 2 | 3 |
| Operational overhead | 4 | 5 | 2 | 4 |
| Cost (3 years) | 3 | 5 | 4 | 3 |
| Time to implement | 4 | 5 | 2 | 4 |
| **Weighted Score** | | 3.4 | 3.2 | 4.0 |

## Consequences

### Positive
- Enterprise-ready SSO capability
- Compliant authentication for SOC 2
- Reduced security maintenance burden
- Better mobile/API support
- Built-in MFA

### Negative
- Auth0 costs ~$300/month initially, scaling with users
- Vendor dependency for critical auth path
- Team needs OAuth2/OIDC training
- Migration period with dual auth support

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Auth0 outage | Low | High | Implement JWT caching, graceful degradation |
| Cost overrun | Medium | Medium | Monitor MAU, implement usage alerts |
| Migration issues | Medium | Medium | Parallel auth systems during transition |
| Vendor lock-in | Low | Medium | Abstract auth behind service layer |

## Implementation Plan

1. **Phase 1** (Month 1): Set up Auth0, implement for new API endpoints
2. **Phase 2** (Month 2): Migrate web authentication
3. **Phase 3** (Month 3): Mobile app integration
4. **Phase 4** (Month 4): Enterprise SSO rollout

## Related Decisions

- ADR-0005: API Design (defines authentication headers)
- ADR-0015: Session Management (superseded by this ADR)
- ADR-0018: Rate Limiting (uses JWT claims)

## Notes

- Auth0 contract negotiated with 20% discount for annual commitment
- Security team approved after penetration testing
- Compliance officer confirmed SOC 2 alignment

## References

- [Auth0 Architecture Scenarios](https://auth0.com/docs/architecture-scenarios)
- [OWASP Authentication Cheatsheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc8725)
```

## Example 5: Microservices Communication

```markdown
# ADR-0021: Inter-Service Communication Pattern

**Status:** Accepted
**Date:** 2025-12-05
**Deciders:** Platform Team

## Context

As we decompose our monolith into microservices, we need to decide how
services will communicate. Current services:
- User Service
- Order Service
- Inventory Service
- Notification Service

Requirements:
- Handle 10,000 orders/hour at peak
- Eventual consistency acceptable for non-critical paths
- Strong consistency required for inventory deductions
- Services may be temporarily unavailable

## Decision

We will use a hybrid approach:

1. **Synchronous (REST):** For queries and user-facing operations requiring
   immediate response
2. **Asynchronous (RabbitMQ):** For events and operations that can be
   eventually consistent
3. **Saga pattern:** For distributed transactions (order + inventory)

## Communication Matrix

| From | To | Method | Use Case |
|------|----|--------|----------|
| API Gateway | User Service | REST | Authentication, profile |
| API Gateway | Order Service | REST | Create order, get order |
| Order Service | Inventory Service | REST | Reserve inventory (sync) |
| Order Service | RabbitMQ | Event | Order created event |
| Notification Service | RabbitMQ | Subscribe | Send order confirmation |
| Inventory Service | RabbitMQ | Event | Stock level changed |

## Consequences

### Positive
- Clear separation of sync vs async concerns
- Resilient to service failures (async path)
- Scalable event processing
- Audit trail via message queue

### Negative
- Increased infrastructure complexity
- Debugging distributed transactions harder
- Message ordering challenges
- Need for idempotency in consumers

## Related ADRs

- ADR-0019: Service Decomposition Strategy
- ADR-0022: Message Queue Selection (RabbitMQ vs Kafka)
- ADR-0025: Distributed Tracing Implementation
```

## Example 6: Superseding an ADR

```markdown
# ADR-0030: Migrate from REST to GraphQL for Mobile BFF

**Status:** Accepted
**Date:** 2026-01-10
**Deciders:** Mobile Team, API Team
**Supersedes:** ADR-0003 (for mobile clients only)

## Context

ADR-0003 established REST as our API standard. After 18 months in production,
mobile team reports:
- Average 4-5 API calls per screen (performance issue)
- 60% of payload data unused (bandwidth waste)
- Difficult to iterate on mobile UI without backend changes

## Decision

We will implement GraphQL as a Backend-for-Frontend (BFF) specifically for
mobile clients, while maintaining REST for:
- Third-party API consumers
- Web application (where current approach works well)
- Server-to-server communication

## Why This Doesn't Fully Supersede ADR-0003

ADR-0003's decision for REST remains valid for:
- Public API (third-party developers prefer REST)
- Web frontend (caching benefits outweigh flexibility needs)
- Internal services (REST simpler for service-to-service)

GraphQL is being added as a complementary approach for mobile only.

## Consequences

### Positive
- Mobile screens load with single request
- Mobile team can iterate UI independently
- Reduced mobile data usage
- Better mobile app performance

### Negative
- Two API paradigms to maintain
- Additional infrastructure (GraphQL server)
- Team needs GraphQL training
- More complex API monitoring

## Notes

This is a targeted addition, not a wholesale replacement. We will revisit
after 12 months to assess whether GraphQL should expand to other clients.
```

## Open Source Project Examples

### From MADR Project

The MADR project itself uses ADRs. See their decisions at:
[github.com/adr/madr/tree/develop/docs/decisions](https://github.com/adr/madr/tree/develop/docs/decisions)

### From JabRef

Reference management software with extensive ADR history:
[github.com/JabRef/jabref/tree/main/docs/decisions](https://github.com/JabRef/jabref)

### From Backstage (Spotify)

Developer portal with well-documented decisions:
[backstage.io/docs/architecture-decisions](https://backstage.io/docs/architecture-decisions/)

### From AWS ParallelCluster

Uses Log4brains for ADR management:
[aws.github.io/aws-parallelcluster-ui/log4brains/adr](https://aws.github.io/aws-parallelcluster-ui/log4brains/adr/)

## Key Takeaways from Examples

| Aspect | Best Practice |
|--------|---------------|
| **Length** | 1-2 pages, focused on decision |
| **Alternatives** | Always show 2+ options with honest pros/cons |
| **Consequences** | Include both positive AND negative |
| **Context** | Enough for someone unfamiliar to understand |
| **Decision** | Clear statement using "We will..." |
| **Links** | Reference related ADRs |
| **Status** | Always include, update when superseded |
