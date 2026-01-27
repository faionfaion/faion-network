# Architecture Decision Tree Examples

Real-world examples of architecture decisions using decision trees. Each example shows the complete decision process, trade-offs considered, and final outcome.

---

## Example 1: Architecture Style for E-commerce Startup

### Context

**Company:** FastCart (fictional)
**Stage:** Series A startup, $5M funding
**Team:** 12 developers, 2 DevOps engineers
**Current State:** Legacy PHP monolith, planning rewrite
**Goal:** Build scalable platform for 10x growth

### Decision Tree Walkthrough

```
Q1: Team size? -> "12 developers" (10-50 range)
    |
    Recommendation: Modular Monolith
    |
Q2: But we need to scale 10x - shouldn't we use microservices?
    |
    Analysis:
    - 10x traffic != 10x complexity
    - Horizontal scaling works for monoliths too
    - 42% of orgs consolidated microservices back (CNCF 2025)
    |
Q3: DevOps maturity?
    |
    Assessment: Medium
    - CI/CD exists but basic
    - No distributed tracing
    - Limited Kubernetes experience
    |
    Confirmation: Modular Monolith is correct choice
```

### Decision Matrix

| Criteria | Weight | Microservices | Modular Monolith | Monolith |
|----------|--------|---------------|------------------|----------|
| Development speed | 25% | 2 | 4 | 5 |
| Scalability | 20% | 5 | 4 | 3 |
| Operational complexity | 20% | 2 | 4 | 5 |
| Team fit | 15% | 2 | 4 | 4 |
| Future flexibility | 20% | 5 | 4 | 2 |
| **Weighted Score** | 100% | **3.0** | **4.0** | **3.8** |

### Decision

**Chosen:** Modular Monolith

**Rationale:**
1. Team size (12) is in the "sweet spot" for modular monolith
2. DevOps maturity insufficient for microservices complexity
3. Clear module boundaries can be extracted later if needed
4. Shopify serves millions of merchants with a modular monolith

**Module Structure:**
```
fastcart/
├── modules/
│   ├── catalog/        # Product catalog domain
│   ├── cart/           # Shopping cart domain
│   ├── checkout/       # Order processing
│   ├── payments/       # Payment integration
│   ├── users/          # User management
│   └── notifications/  # Email, SMS, push
├── shared/
│   └── kernel/         # Shared utilities
└── infrastructure/
```

### Outcome (12 months later)

- Successfully launched platform
- Handles 50k daily orders
- 3 modules extracted to services (payments, notifications)
- No major architectural regrets

---

## Example 2: Database Selection for SaaS Analytics Platform

### Context

**Company:** DataPulse (fictional)
**Product:** Real-time analytics dashboard
**Requirements:**
- 10M events/day ingestion
- Sub-second query response for dashboards
- 90-day data retention
- Multi-tenant architecture

### Decision Tree Walkthrough

```
Q1: Primary access pattern?
    |
    -> "Time-series + Analytics"
    |
Q2: Query complexity?
    |
    -> "Complex aggregations, GROUP BY, window functions"
    |
Q3: Real-time requirements?
    |
    -> "Near real-time (< 5 second delay acceptable)"
    |
Options:
    - TimescaleDB (PostgreSQL extension)
    - ClickHouse
    - Apache Druid
    - BigQuery
```

### Options Analysis

**Option 1: TimescaleDB**
- Pros: PostgreSQL compatibility, joins, mature ecosystem
- Cons: Slower at scale (>1B rows), higher operational cost
- Best for: <1B rows, need SQL joins

**Option 2: ClickHouse**
- Pros: Fastest analytical queries, column compression, open-source
- Cons: Limited joins, learning curve, self-managed
- Best for: Pure analytics, high volume, cost-conscious

**Option 3: Apache Druid**
- Pros: Real-time ingestion, sub-second queries
- Cons: Complex operations, smaller community
- Best for: Real-time analytics, streaming

**Option 4: BigQuery**
- Pros: Serverless, auto-scaling, low ops
- Cons: Cost at scale, cold start latency, vendor lock-in
- Best for: Variable workloads, Google Cloud shops

### Decision Matrix

| Criteria | Weight | TimescaleDB | ClickHouse | Druid | BigQuery |
|----------|--------|-------------|------------|-------|----------|
| Query performance | 25% | 3 | 5 | 5 | 4 |
| Operational complexity | 20% | 4 | 3 | 2 | 5 |
| Cost (at scale) | 20% | 3 | 5 | 4 | 2 |
| Team familiarity | 15% | 4 | 2 | 2 | 4 |
| Ecosystem/tooling | 20% | 5 | 4 | 3 | 5 |
| **Weighted Score** | 100% | **3.7** | **3.9** | **3.2** | **3.9** |

### Decision

**Chosen:** ClickHouse

**Rationale:**
1. Best query performance for analytical workloads
2. Excellent compression (10-20x) reduces storage costs
3. Open-source, no vendor lock-in
4. Growing ecosystem and community
5. ClickHouse Cloud available if ops becomes burden

**Architecture:**
```
Event Sources -> Kafka -> ClickHouse -> API -> Dashboard
                    |
                    +-> S3 (long-term archive)
```

### Implementation Notes

- Used ClickHouse's MaterializedViews for pre-aggregation
- Implemented multi-tenant via tenant_id in partition key
- Achieved 50ms p95 query latency
- Cost: 70% lower than BigQuery estimate

---

## Example 3: Cloud Provider Selection for FinTech Startup

### Context

**Company:** PayFlow (fictional)
**Product:** B2B payment processing
**Requirements:**
- PCI DSS compliance
- Multi-region deployment (US, EU)
- Real-time payment processing
- Existing team has AWS experience

### Decision Tree Walkthrough

```
Q1: Current technology investments?
    |
    -> "Team has AWS experience, no Microsoft/Google dependencies"
    |
Q2: Primary workload type?
    |
    -> "Transaction processing (fintech)"
    |
Q3: Compliance requirements?
    |
    -> "PCI DSS Level 1, SOC 2, GDPR"
    |
All three providers meet compliance needs. Continue...
    |
Q4: Regional requirements?
    |
    -> "US + EU, data residency requirements"
    |
All three have US + EU regions. Continue...
    |
Q5: Specific service needs?
    |
    -> "Managed Kubernetes, PostgreSQL, Redis, Kafka"
```

### Options Analysis

**AWS:**
- Pros: Team experience, broadest services, most mature
- Cons: Complex pricing, networking costs
- FinTech relevance: Most payment companies use AWS

**Azure:**
- Pros: Strong enterprise features, hybrid cloud
- Cons: No team experience, learning curve
- FinTech relevance: Good but less common in payments

**GCP:**
- Pros: Best Kubernetes (GKE), transparent pricing
- Cons: Smaller service catalog, less FinTech adoption
- FinTech relevance: Growing but smaller market share

### Decision Matrix

| Criteria | Weight | AWS | Azure | GCP |
|----------|--------|-----|-------|-----|
| Team expertise | 25% | 5 | 2 | 2 |
| Compliance certifications | 20% | 5 | 5 | 4 |
| FinTech ecosystem | 15% | 5 | 3 | 3 |
| Cost (estimated) | 15% | 3 | 3 | 4 |
| Managed services quality | 15% | 4 | 4 | 5 |
| Multi-region support | 10% | 5 | 5 | 4 |
| **Weighted Score** | 100% | **4.35** | **3.35** | **3.25** |

### Decision

**Chosen:** AWS

**Rationale:**
1. Team already proficient in AWS (25% weight)
2. Strongest PCI DSS compliance track record in payments industry
3. Most payment processors and banking partners on AWS (easier integration)
4. EKS, RDS PostgreSQL, ElastiCache, MSK all production-ready

**Architecture:**
```
Multi-Region Active-Active:
- us-east-1 (primary US)
- eu-west-1 (primary EU)
- us-west-2 (DR)

Services: EKS, RDS Multi-AZ, ElastiCache Cluster, MSK
```

### Cost Optimization

- Reserved Instances for baseline (40% savings)
- Spot Instances for batch processing (70% savings)
- S3 Intelligent Tiering for logs
- Estimated monthly: $45k (vs $65k on-demand)

---

## Example 4: Build vs Buy - Authentication System

### Context

**Company:** TeamCollab (fictional)
**Product:** Enterprise collaboration SaaS
**Requirements:**
- SSO (SAML, OIDC)
- MFA
- SCIM provisioning
- SOC 2 compliance
- 500+ enterprise customers

### Decision Tree Walkthrough

```
Q1: Is authentication a competitive differentiator?
    |
    -> "No, it's a necessity but not our core value"
    |
Q2: Do commercial solutions exist?
    |
    -> "Yes, many: Auth0, Okta, Clerk, WorkOS"
    |
Q3: Can we afford the dependency risk?
    |
    -> Analysis needed...
```

### Build Option Analysis

**Effort Estimate:**
- Initial build: 6-9 months (3 engineers)
- SSO implementation: 2 months
- MFA implementation: 1 month
- SCIM implementation: 2 months
- SOC 2 compliance: 1-2 months
- Ongoing maintenance: 0.5 FTE

**Total Cost (3 years):**
- Development: $300k (9 months x 3 engineers)
- Maintenance: $225k (0.5 FTE x 3 years)
- Security audits: $50k/year = $150k
- **Total: ~$675k**

### Buy Option Analysis

**Auth0 (Enterprise):**
- $23k/year base + $0.03/MAU
- At 100k MAU: $23k + $36k = $59k/year
- 3-year cost: ~$177k
- All features included (SSO, MFA, SCIM)

**WorkOS:**
- $0.10/MAU for enterprise features
- At 100k MAU: $120k/year
- 3-year cost: ~$360k
- Best-in-class SSO

**Clerk:**
- $0.02/MAU
- At 100k MAU: $24k/year
- 3-year cost: ~$72k
- Developer-focused, newer

### Decision Matrix

| Criteria | Weight | Build | Auth0 | WorkOS | Clerk |
|----------|--------|-------|-------|--------|-------|
| Total cost (3yr) | 25% | 2 | 4 | 3 | 5 |
| Time to market | 25% | 1 | 5 | 5 | 5 |
| Feature completeness | 20% | 3 | 5 | 5 | 4 |
| Maintenance burden | 15% | 2 | 5 | 5 | 5 |
| Flexibility | 15% | 5 | 3 | 3 | 3 |
| **Weighted Score** | 100% | **2.3** | **4.4** | **4.1** | **4.5** |

### Decision

**Chosen:** Auth0

**Rationale:**
1. 3-year TCO is 74% lower than build ($177k vs $675k)
2. Time to market: weeks vs 9 months
3. Enterprise features (SSO, SCIM) battle-tested
4. SOC 2 compliance included
5. Flexibility less important since auth is not differentiator

**Trade-off Accepted:**
- Vendor dependency (mitigated by standard protocols)
- Less customization (acceptable for non-core feature)

### Implementation Notes

- Integrated in 2 weeks
- Custom branding via Auth0 Universal Login
- SSO available to enterprise customers immediately
- Engineering team focused on core product features

---

## Example 5: Frontend Framework Selection

### Context

**Company:** InsightBoard (fictional)
**Product:** Data visualization dashboard
**Requirements:**
- Complex interactive charts
- Real-time updates (WebSocket)
- SEO for marketing pages
- Team of 4 frontend developers

### Decision Tree Walkthrough

```
Q1: SEO requirements?
    |
    -> "Critical for marketing pages, not for app"
    |
    Implication: Need SSR/SSG for marketing, SPA acceptable for app
    |
Q2: Team expertise?
    |
    -> "3 React devs, 1 Vue dev"
    |
Q3: Complexity of UI?
    |
    -> "High - complex charts, drag-drop, real-time"
    |
Options:
    - Next.js (React, SSR/SSG)
    - Remix (React, SSR)
    - Vue + Nuxt
    - SvelteKit
```

### Options Analysis

**Next.js:**
- Pros: Team knows React, largest ecosystem, Vercel support
- Cons: App Router complexity, bundle size
- Best for: Full-stack React apps with SEO needs

**Remix:**
- Pros: Better data loading patterns, simpler mental model
- Cons: Smaller ecosystem, less familiar
- Best for: Data-heavy apps with nested routes

**Nuxt:**
- Pros: Great DX, good SSR
- Cons: Only 1 Vue dev, smaller ecosystem
- Best for: Vue teams

**SvelteKit:**
- Pros: Smallest bundle, best performance
- Cons: No team experience, smallest ecosystem
- Best for: Performance-critical, willing to invest in learning

### Decision Matrix

| Criteria | Weight | Next.js | Remix | Nuxt | SvelteKit |
|----------|--------|---------|-------|------|-----------|
| Team expertise | 30% | 5 | 4 | 2 | 1 |
| Ecosystem | 25% | 5 | 3 | 4 | 3 |
| Performance | 20% | 3 | 4 | 3 | 5 |
| DX | 15% | 4 | 5 | 5 | 5 |
| Hiring pool | 10% | 5 | 3 | 4 | 2 |
| **Weighted Score** | 100% | **4.4** | **3.7** | **3.2** | **2.9** |

### Decision

**Chosen:** Next.js 14 (App Router)

**Rationale:**
1. 75% of team already proficient in React
2. Largest ecosystem for charting (Recharts, Visx, etc.)
3. SSG for marketing pages, RSC for app
4. Easiest to hire for (68% JS devs use Next.js)

**Architecture:**
```
/                   # Marketing (SSG)
/pricing            # Marketing (SSG)
/blog/*             # Blog (SSG)
/app/*              # Dashboard (RSC + Client Components)
/api/*              # API routes (tRPC)
```

### Implementation Notes

- Used Turbopack for fast dev builds
- Partial prerendering for dashboard shell
- WebSocket via Socket.io for real-time charts
- Recharts for visualization (React-native)

---

## Example 6: API Design Style Selection

### Context

**Company:** DevHub (fictional)
**Product:** Developer tools platform
**Consumers:**
- Public API for third-party integrations
- Internal services
- Web and mobile clients

### Decision Tree Walkthrough

```
Q1: Who are the API consumers?
    |
    Multiple: External developers, internal services, frontend
    |
    Implication: May need different APIs for different consumers
    |
Q2: For external developers?
    |
    -> "Public API, need stability, documentation"
    -> REST with OpenAPI
    |
Q3: For internal services?
    |
    -> "Performance critical, type safety needed"
    -> gRPC
    |
Q4: For frontend?
    |
    -> "Complex data requirements, varying queries"
    -> GraphQL or BFF pattern
```

### Decision

**Chosen:** Multi-API Strategy

```
External Developers  ->  REST API (OpenAPI 3.1)
                            |
Internal Services    ->  gRPC (Protocol Buffers)
                            |
Frontend (Web/Mobile) -> GraphQL (Federation)
                            |
                     Core Domain Services
```

**Rationale:**
1. REST for external: Universal, well-documented, cacheable
2. gRPC for internal: Performance (10x faster), type safety, streaming
3. GraphQL for frontend: Flexible queries, reduces over-fetching

**Implementation:**

```yaml
# REST (external)
/api/v1/projects
/api/v1/projects/{id}
/api/v1/projects/{id}/builds

# gRPC (internal)
service BuildService {
  rpc TriggerBuild(BuildRequest) returns (BuildResponse);
  rpc StreamLogs(LogRequest) returns (stream LogEntry);
}

# GraphQL (frontend)
type Query {
  project(id: ID!): Project
  viewer: User
}
```

---

## Summary: Decision Patterns

### Pattern 1: Start Simple, Evolve

Most examples show a preference for simpler solutions:
- Modular monolith over microservices
- Managed services over self-hosted
- Buy over build for non-core features

### Pattern 2: Team Expertise Matters

Team familiarity consistently weighted 15-30% in decisions:
- AWS chosen partly due to existing expertise
- Next.js chosen for React team
- Learning curve is a real cost

### Pattern 3: Total Cost of Ownership

Look beyond initial costs:
- Build vs Buy: 3-year TCO comparison
- Cloud: Reserved instances, egress costs
- Open source: Operational overhead

### Pattern 4: Reversibility

Consider how easy it is to change:
- Modular monolith -> microservices: Moderate effort
- Cloud provider switch: High effort
- Framework switch: Very high effort

---

*Architecture Decision Tree Examples v2.0 - Updated January 2026*
