# Design Doc Examples

Real-world examples of design documents, RFCs, and architecture decision records from major tech companies and open source projects.

---

## Google-Style Design Doc Examples

### Example 1: Caching Layer for User Service

```markdown
# Design Doc: User Service Caching Layer

**Author:** Alex Chen
**Reviewers:** Sarah Kim, Mike Johnson, Lisa Park
**Status:** Approved
**Last Updated:** 2026-01-15

---

## Overview

This document proposes adding a Redis-based caching layer to the User Service to reduce database load and improve response latency for user profile reads. The User Service currently handles 50,000 requests per second, with 80% being profile reads hitting the database directly.

## Context and Scope

### Background

The User Service was built in 2022 for an expected load of 10,000 RPS. Growth has exceeded projections, and database CPU consistently runs at 85%+ during peak hours. We've observed P99 latencies of 250ms, compared to our SLA target of 100ms.

Previous attempts to address this:
- Database read replicas (2023): Helped but added operational complexity
- Query optimization (2024): 20% improvement, now exhausted

### Goals

1. Reduce P99 latency from 250ms to <50ms for cached requests
2. Decrease database read load by 70%
3. Maintain data freshness within 5 seconds of changes
4. Zero downtime deployment

### Non-Goals

- Caching write operations (out of scope)
- Multi-region cache replication (future consideration)
- Replacing the primary database (separate initiative)

## Design

### System Overview

```
Client → Load Balancer → User Service → Cache (Redis)
                                      ↘ Database (Postgres)
```

Read path:
1. Check Redis cache for user profile
2. If hit: return cached data
3. If miss: query database, cache result, return

### Cache Strategy

**Cache-aside pattern:**
- On read: check cache first, populate on miss
- On write: invalidate cache, write to database
- TTL: 5 minutes (balance freshness vs hit rate)

**Key design:** `user:profile:{user_id}`

### Data Model

Cached object (JSON):
```json
{
  "user_id": "123",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "avatar_url": "https://...",
  "cached_at": "2026-01-15T10:00:00Z"
}
```

### Invalidation

- User profile update: explicit cache delete
- User deletion: explicit cache delete
- Fallback: TTL expiration

## Alternatives Considered

### Alternative 1: Database Query Caching

Use database-level query caching instead of application-level.

- **Pros:** No application code changes
- **Cons:** Less control over invalidation, limited by database cache size
- **Why not chosen:** Insufficient cache hit rates in testing (40% vs projected 85%)

### Alternative 2: CDN Edge Caching

Cache user profiles at the CDN edge.

- **Pros:** Even lower latency, distributed globally
- **Cons:** Complex invalidation, privacy concerns (user data at edge)
- **Why not chosen:** Privacy team concerns about PII at edge nodes

### Alternative 3: Do Nothing

Accept current performance and plan for database upgrade.

- **Pros:** No development effort
- **Cons:** Continued SLA violations, growing database costs
- **Why not chosen:** Database upgrade cost ($50k/month) exceeds cache solution ($5k/month)

## Cross-cutting Concerns

### Security

- Redis cluster isolated in private subnet
- TLS encryption for Redis connections
- No sensitive data in cache keys (only user_id)
- Cache access requires service authentication

### Scalability

- Redis cluster: 3 nodes, can scale horizontally
- Expected 85% cache hit rate reduces DB load proportionally
- Capacity for 100k RPS with current sizing

### Monitoring

New metrics:
- `cache.hit_rate`: Target >80%
- `cache.latency_p99`: Target <5ms
- `cache.memory_usage`: Alert at 70%

Dashboards: Added to existing User Service dashboard

## Timeline and Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| Design approval | Jan 20 | Done |
| Redis cluster setup | Jan 25 | In progress |
| Feature flag rollout (1%) | Jan 30 | Pending |
| Full rollout | Feb 10 | Pending |

## Open Questions

1. **Resolved:** Cache serialization format? → JSON (simpler debugging)
2. **Open:** Should we cache user preferences separately? (Owner: Sarah, Due: Jan 22)

## References

- [User Service Architecture Doc](link)
- [Redis Best Practices](link)
- [ADR-042: Cache Strategy Selection](link)
```

---

## Amazon 6-Pager Example

### Example 2: Customer Return Prediction Service (Narrative Format)

```markdown
# Customer Return Prediction Service

**Author:** Product Team
**Date:** January 2026

---

## Introduction

This document proposes a machine learning service that predicts the likelihood of product returns before purchase completion. By surfacing this information at key decision points, we can reduce return rates, improve customer satisfaction, and decrease operational costs associated with reverse logistics.

## Goals

Our primary goal is to reduce the return rate from 15% to 10% within twelve months of launch, while maintaining or improving customer satisfaction scores. We aim to achieve this by helping customers make better-informed purchase decisions, not by creating friction that reduces legitimate purchases.

A secondary goal is to provide data insights to the product and merchandising teams, enabling them to identify products with systematic fit or quality issues. These insights will inform inventory decisions and vendor conversations.

## Tenets

First, customer trust is paramount. We will never use prediction data to penalize customers or restrict their ability to make purchases or returns. The predictions serve to help customers, not to protect the company from customers.

Second, transparency over opacity. When we surface return risk information, we explain why in clear terms. Customers should understand that suggestions come from data patterns, not judgments about them personally.

Third, accuracy before coverage. We would rather have accurate predictions for a subset of products than inaccurate predictions for all products. We will launch with categories where our models perform well and expand carefully.

## State of the Business

Returns currently cost us $2.3 billion annually in direct costs: shipping, processing, restocking, and lost inventory value. The indirect costs are harder to measure but include customer service burden, environmental impact, and customer frustration with the return process itself.

Our analysis of twelve months of return data reveals that 40% of returns cite "item not as expected" or "fit issues" as the reason. These returns are theoretically preventable with better product information at purchase time. Another 25% cite "changed mind," which may indicate impulse purchases that could be reduced with friction or reflection prompts.

Category analysis shows significant variation. Apparel has a 22% return rate, while books have 3%. Within apparel, shoes have the highest return rate at 28%, driven almost entirely by fit issues. Electronics returns are 12%, often due to compatibility or complexity misunderstandings.

## Lessons Learned

We piloted a size recommendation feature in 2024 for shoes. The feature used customer purchase history and return patterns to suggest sizes. Results were encouraging: customers who engaged with recommendations had 18% fewer returns than control group. However, only 30% of customers engaged with the feature, limiting overall impact.

Key learnings from the pilot:

The recommendation needed to appear earlier in the purchase flow. Customers who had already decided on a size were unlikely to change based on a suggestion at checkout. Moving the suggestion to the product detail page increased engagement to 55%.

Generic recommendations underperformed personalized ones. "Most customers buy a half size up" was less effective than "Based on your purchase of Brand X in size 10, we suggest size 10.5 in Brand Y." Personalization increased recommendation acceptance by 3x.

Customers valued explanation. When we added brief reasoning ("This shoe runs narrow based on customer feedback"), satisfaction scores improved even when customers ignored the recommendation.

## Strategic Priorities

Our first priority is launching the return prediction model for the shoes category by Q2 2026. We will use an A/B test framework to measure impact on return rates, conversion rates, and customer satisfaction. Success criteria are: 20% reduction in return rate with no more than 2% reduction in conversion.

Second, we will expand to apparel and electronics by Q4 2026, applying lessons from shoes. Each category will have category-specific models trained on category-specific features (size charts for apparel, compatibility data for electronics).

Third, we will build a self-service dashboard for merchandising teams to access return prediction insights. This will be delivered by Q1 2027 and will enable teams to identify and address product-level issues proactively.

Fourth, we will explore vendor data sharing partnerships. Vendors could use return prediction data to improve their products or provide better size/compatibility information. This requires legal and privacy review, targeted for Q2 2027.

---

**Appendix A: Model Performance Metrics**

| Category | AUC-ROC | Precision @50% Recall | Coverage |
|----------|---------|----------------------|----------|
| Shoes | 0.82 | 0.71 | 95% |
| Apparel | 0.75 | 0.63 | 88% |
| Electronics | 0.78 | 0.68 | 72% |

**Appendix B: Cost-Benefit Analysis**

[Detailed financial projections...]

**Appendix C: Privacy Review Summary**

[GDPR and privacy considerations...]
```

---

## Uber RFC Example

### Example 3: Service Mesh Migration RFC

```markdown
# RFC: Migration to Istio Service Mesh

**RFC Number:** RFC-2026-042
**Author:** Platform Team
**Status:** Approved
**Created:** 2026-01-10
**Approvers:** [List of principal engineers]

---

## Summary

This RFC proposes migrating our microservices infrastructure from our custom sidecar proxy to Istio service mesh over the next 12 months. This migration will standardize our networking layer, improve observability, and reduce the maintenance burden of our current solution.

## Motivation

Our custom sidecar proxy, built in 2019, served us well but has become a maintenance burden. The team of three engineers maintaining it could instead work on higher-value projects. Additionally, the proxy lacks features now standard in service mesh solutions: distributed tracing integration, advanced traffic management, and mTLS automation.

Industry adoption of Istio has matured significantly. Major companies including Airbnb, eBay, and Salesforce run Istio in production at our scale. The ecosystem of tooling and expertise has grown, reducing our operational risk.

## Proposal

### Overview

We will migrate 200+ services from our custom proxy to Istio sidecars using a gradual rollout strategy. Migration will proceed by service tier: non-critical services first, then mid-tier, then critical path services last.

### Detailed Design

**Phase 1: Infrastructure (Months 1-2)**

Deploy Istio control plane in each cluster. Configure Istio to coexist with existing proxy. Both solutions will run simultaneously during migration.

**Phase 2: Pilot Services (Months 3-4)**

Migrate 10 non-critical services. Establish runbooks and training materials. Validate observability stack integration (Prometheus, Jaeger, Grafana).

**Phase 3: Mid-Tier Services (Months 5-8)**

Migrate 100 mid-tier services. Parallelize with 5 teams, each owning 20 services. Develop automation tools for migration.

**Phase 4: Critical Services (Months 9-11)**

Migrate remaining 90 critical path services. Extra scrutiny and rollback planning. One service at a time with 48-hour bake periods.

**Phase 5: Decommission (Month 12)**

Remove custom proxy from all services. Archive custom proxy codebase. Reassign maintenance team.

### Service SLAs

| Metric | Current | Target (Post-Migration) |
|--------|---------|------------------------|
| Availability | 99.95% | 99.95% |
| P99 Latency Overhead | 5ms | 3ms |
| mTLS Coverage | 60% | 100% |
| Trace Coverage | 40% | 95% |

### Dependencies

- Istio 1.20+ (current stable)
- Kubernetes 1.28+ (already deployed)
- Observability stack upgrade (parallel project)

### Rollout Plan

1. **Week 1-2:** Deploy Istio control plane (non-prod)
2. **Week 3-4:** Deploy Istio control plane (prod)
3. **Week 5-8:** Migrate pilot services
4. **Week 9-32:** Progressive service migration
5. **Week 33-40:** Critical service migration
6. **Week 41-48:** Decommission and cleanup

### Rollback Plan

Each service migration is independently reversible:
1. Disable Istio sidecar injection for namespace
2. Redeploy service without sidecar
3. Automatic routing through old proxy

Cluster-wide rollback: Disable Istio globally, all traffic routes through old proxy (tested monthly).

## Alternatives

### Alternative 1: Upgrade Custom Proxy

Add missing features to our existing solution.

- **Pros:** No migration effort, team expertise exists
- **Cons:** Continued maintenance burden, reinventing solved problems
- **Why rejected:** 18-month effort to reach feature parity, ongoing maintenance still required

### Alternative 2: Linkerd Instead of Istio

Linkerd is simpler and lighter weight.

- **Pros:** Lower resource overhead, simpler operations
- **Cons:** Smaller community, fewer features, less enterprise adoption
- **Why rejected:** We need advanced traffic management features Linkerd lacks

### Alternative 3: AWS App Mesh

Use AWS-native service mesh.

- **Pros:** AWS integration, managed control plane
- **Cons:** Vendor lock-in, limited to AWS, less community innovation
- **Why rejected:** Multi-cloud strategy requires vendor-neutral solution

## Security Considerations

**Improvements:**
- Automatic mTLS between all services
- Centralized certificate management
- Fine-grained authorization policies
- Audit logging for service-to-service calls

**Risks:**
- Istio control plane is critical infrastructure (mitigated by HA deployment)
- Sidecar vulnerabilities (mitigated by automatic updates)

Security team has approved this RFC contingent on completing threat model (due before Phase 3).

## Operational Considerations

**Deployment:** Istio upgrades will follow our standard release train (monthly minors, quarterly majors).

**Monitoring:** New dashboards for mesh health, per-service mesh metrics, control plane health.

**Incident Response:** Runbooks for common issues (sidecar crashes, certificate expiry, control plane failures).

**On-call:** Platform team primary for first 6 months, then shared rotation.

## Timeline

| Phase | Description | Target |
|-------|-------------|--------|
| 1 | Infrastructure | Q1 2026 |
| 2 | Pilot Services | Q2 2026 |
| 3 | Mid-Tier Services | Q2-Q3 2026 |
| 4 | Critical Services | Q4 2026 |
| 5 | Decommission | Q1 2027 |

## Approvals

| Approver | Team | Status | Date |
|----------|------|--------|------|
| Jane Smith | Platform | Approved | 2026-01-12 |
| Bob Lee | SRE | Approved | 2026-01-13 |
| Alice Wang | Security | Approved (conditional) | 2026-01-14 |
| Chris Park | Architecture | Approved | 2026-01-15 |
```

---

## Spotify ADR Example

### Example 4: Architecture Decision Record

```markdown
# ADR-2026-003: Adoption of Event Sourcing for Playlist Service

**Status:** Accepted
**Date:** 2026-01-20
**Deciders:** Playlist Team, Architecture Guild
**Consulted:** Data Platform, Infrastructure
**Informed:** All Engineering

---

## Context

The Playlist Service manages 4 billion playlists with 500 billion tracks. Current CRUD-based architecture struggles with:

1. **Audit requirements:** We cannot answer "what did this playlist look like on date X"
2. **Sync conflicts:** Multiple clients editing same playlist causes data loss
3. **Analytics lag:** Batch ETL takes 6 hours; business needs real-time insights
4. **Recovery difficulty:** Accidental deletions require backup restoration

Playlist is our most important user-facing feature. Degradation directly impacts MAU metrics.

## Decision

We will adopt event sourcing for the Playlist Service.

**What this means:**
- All playlist changes stored as immutable events (AddTrack, RemoveTrack, Rename, etc.)
- Current state derived by replaying events
- Events published to Kafka for downstream consumers
- Snapshots created for performance optimization

**What this does NOT mean:**
- We are not rewriting the entire service
- We are not changing the external API
- Other services are not required to adopt event sourcing

## Consequences

### Positive

- **Complete audit trail:** Every change recorded with timestamp, user, and context
- **Time travel:** Reconstruct any playlist state at any point in time
- **Real-time analytics:** Events available immediately via Kafka
- **Conflict resolution:** Event ordering provides deterministic merge
- **Recovery:** Soft deletes with easy restoration

### Negative

- **Learning curve:** Team needs training on event sourcing patterns
- **Storage growth:** Event log grows faster than state storage (mitigated by retention policy)
- **Query complexity:** Some queries require event replay (mitigated by projections)
- **Eventual consistency:** Strong consistency requires careful design

### Neutral

- **Performance:** Read performance unchanged (served from projections), write path adds ~5ms latency

## Alternatives Considered

### Alternative 1: Temporal Tables (SQL Feature)

Use database temporal tables for history.

- Rejected because: Limited to database-level history, no event semantics, no streaming capability

### Alternative 2: Change Data Capture

Capture database changes and stream to Kafka.

- Rejected because: Captures row changes not domain events, loses semantic meaning, makes conflict resolution harder

### Alternative 3: Audit Log Table

Add separate audit table for changes.

- Rejected because: Duplicate writes, consistency risk, no state reconstruction capability

## Related Decisions

- ADR-2025-042: Kafka as Event Backbone
- ADR-2024-018: Playlist API V2

## Notes

This decision was made after a 4-week RFC process with input from 12 teams. The RFC received 47 comments, all addressed before approval.

Implementation begins Q2 2026 with expected completion Q4 2026.

---

## Change Log

| Date | Change |
|------|--------|
| 2026-01-20 | Initial decision |
```

---

## Open Source RFC Example

### Example 5: Rust-Style RFC (from real projects)

```markdown
- Feature Name: `async_fn_in_trait`
- Start Date: 2022-09-28
- RFC PR: [rust-lang/rfcs#3185](https://github.com/rust-lang/rfcs/pull/3185)
- Rust Issue: [rust-lang/rust#91611](https://github.com/rust-lang/rust/issues/91611)

# Summary

Allow `async fn` to be used in trait definitions and implementations.

# Motivation

Async programming in Rust is increasingly common, but async methods in traits require workarounds like the `async-trait` crate. This adds cognitive overhead, compilation time, and prevents some optimizations.

Making `async fn` work natively in traits would:
- Reduce friction for new Rust async users
- Eliminate need for proc-macro workarounds
- Enable better compiler optimizations
- Align with expected Rust syntax

# Guide-level explanation

[Explains the feature as if teaching it to another programmer...]

After this RFC, you can write:

```rust
trait MyTrait {
    async fn do_something(&self) -> Result<(), Error>;
}
```

instead of the current workaround:

```rust
#[async_trait]
trait MyTrait {
    async fn do_something(&self) -> Result<(), Error>;
}
```

# Reference-level explanation

[Technical specification of the feature...]

# Drawbacks

- Adds complexity to trait system
- Object safety implications need careful design
- May have surprising behavior in edge cases

# Rationale and alternatives

## Alternative: Keep async-trait crate

- Pro: No language changes needed
- Con: Perpetual workaround, proc-macro overhead

## Alternative: Different syntax

- Pro: Clearer about what's happening
- Con: Inconsistent with regular async fn

# Prior art

[Discussion of how other languages handle this...]

# Unresolved questions

1. How to handle object safety?
2. What about `-> impl Trait` returns?
3. Interaction with GATs?

# Future possibilities

- Async drop
- Async closures
- Generator syntax
```

---

## Shopify Engineering Program Example

### Example 6: Mini RFC for Team-Scope Change

```markdown
# Mini RFC: Add Rate Limiting to Checkout API

**Author:** @developer
**Status:** Open for Review
**Deadline:** 2026-01-25
**Scope:** Team-only (no cross-team impact)

---

## Problem Statement

The Checkout API currently has no rate limiting. A single misconfigured client caused 100x normal traffic yesterday, degrading performance for all merchants. We need protection against this.

## Proposed Solution

Add token bucket rate limiting at the API gateway level:
- 1000 requests/minute per merchant
- 429 response when exceeded
- Retry-After header with backoff
- Metrics exposed to Datadog

## Implementation Details

1. Configure Kong rate limiting plugin
2. Set limits in merchant tier configuration
3. Add alerting for merchants hitting limits
4. Document in API changelog

## Success Metrics

- Zero cascading failures from traffic spikes
- <0.1% of requests rate limited under normal operation
- Alert triggers within 1 minute of abuse

## Questions/Concerns

1. Should enterprise tier have higher limits? (Tentatively yes, 5000/min)
2. Need to coordinate with support on merchant communication

---

**If no veto by deadline, author proceeds with implementation.**
```

---

## HashiCorp RFC Template Example

### Example 7: HashiCorp-Style RFC Header

```markdown
# RFC: [Title]

## Overview

[One or two paragraphs explaining the goal of this RFC. A newcomer should understand intent from this section alone.]

## Background

[At least two paragraphs, up to one page. A newcomer to this project should be able to read this section and follow links to get full context.]

Key questions to answer:
- Why is this change necessary?
- What's the current state?
- What have we tried before?

## Proposal

### High-Level Design

[Architecture overview, diagrams, component interactions]

### Detailed Design

[Implementation specifics, APIs, data models]

### Backwards Compatibility

[How existing users/systems are affected]

## Alternatives

### Alternative 1: [Name]

[Description, pros, cons, why rejected]

### Alternative 2: [Name]

[Description, pros, cons, why rejected]

## Trade-offs

What are the disadvantages of your design? What trade-offs are you making because you think the downsides are worth the benefits?

[Be honest about weaknesses. This builds trust with reviewers.]

## Open Questions

1. [Question 1]
2. [Question 2]

## References

- [Related RFC]
- [External resource]
```

---

## Where to Find More Examples

### Public RFC Repositories

| Project | Link | Notes |
|---------|------|-------|
| Rust | [rust-lang/rfcs](https://github.com/rust-lang/rfcs) | Excellent examples of detailed RFCs |
| Ember | [emberjs/rfcs](https://github.com/emberjs/rfcs) | Good frontend-focused examples |
| React | [reactjs/rfcs](https://github.com/reactjs/rfcs) | Sparse but high quality |
| Swift | [apple/swift-evolution](https://github.com/apple/swift-evolution) | Language design RFCs |
| Kubernetes | [kubernetes/enhancements](https://github.com/kubernetes/enhancements) | KEPs (K8s Enhancement Proposals) |
| Uber H3 | [uber/h3 RFCs](https://github.com/uber/h3/tree/master/dev-docs/RFCs) | Geo library RFCs |

### Design Doc Collections

| Resource | Link | Notes |
|----------|------|-------|
| Design Docs Library | [designdocs.dev](https://www.designdocs.dev/) | 1000+ examples from 40+ companies |
| Pragmatic Engineer | [Examples article](https://newsletter.pragmaticengineer.com/p/software-engineering-rfc-and-design) | Curated examples with commentary |

---

*Examples | Design Docs at Big Tech | v2.0*
