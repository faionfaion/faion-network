# Trade-off Analysis Examples

Real-world examples of trade-off analysis across different decision types.

## Example 1: Database Selection for E-commerce Platform

### Context

A growing e-commerce platform (50K daily users) needs to choose a database for its product catalog. Current MySQL is hitting performance limits.

### Constraints

- Budget: $50K/year for database infrastructure
- Team: Strong SQL skills, limited NoSQL experience
- Timeline: 3 months to migration
- Requirement: Support for 10M products, 1M daily searches

### Options Evaluated

| Option | Description |
|--------|-------------|
| PostgreSQL | Upgrade to optimized PostgreSQL with pgvector |
| MongoDB | Document database for flexible product schemas |
| Elasticsearch + PostgreSQL | Search engine + relational for transactions |
| CockroachDB | NewSQL for horizontal scaling |

### Decision Matrix

| Criteria | Weight | PostgreSQL | MongoDB | ES + PG | CockroachDB |
|----------|--------|------------|---------|---------|-------------|
| Query performance | 5 | 4 (20) | 3 (15) | 5 (25) | 4 (20) |
| Team expertise | 4 | 5 (20) | 2 (8) | 3 (12) | 3 (12) |
| Schema flexibility | 3 | 3 (9) | 5 (15) | 4 (12) | 3 (9) |
| Operational cost | 4 | 5 (20) | 3 (12) | 2 (8) | 3 (12) |
| Future scalability | 3 | 3 (9) | 4 (12) | 4 (12) | 5 (15) |
| Migration effort | 3 | 5 (15) | 2 (6) | 2 (6) | 4 (12) |
| **Total** | | **93** | **68** | **75** | **80** |

### Trade-off Analysis

**Chosen: Elasticsearch + PostgreSQL**

Despite PostgreSQL scoring highest, the team chose ES + PG for search requirements:

| What We Get | What We Lose |
|-------------|--------------|
| Excellent search performance | Increased operational complexity |
| Near real-time search indexing | Two systems to maintain |
| Faceted search capabilities | Data synchronization challenges |
| PostgreSQL ACID for transactions | Higher infrastructure cost |

### Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Data sync between ES and PG | Debezium CDC for real-time sync |
| ES operational complexity | Managed Elasticsearch service |
| Team learning curve | 2-week training, phased rollout |
| Cost overrun | Start with small cluster, scale as needed |

### Outcome (6 months later)

- Search latency: 50ms (was 2s)
- Operational incidents: Higher initially, stabilized after 2 months
- Cost: 40% higher than PostgreSQL-only, but search revenue +25%
- Lesson: Hybrid approach complexity was underestimated

---

## Example 2: Monolith vs Microservices for Fintech Startup

### Context

Series A fintech startup with 8 engineers building a payment processing platform. Need to decide architecture for next 2 years of growth.

### Constraints

- Team: 8 engineers (growing to 20)
- Timeline: MVP in 6 months
- Compliance: PCI-DSS required
- Scale: 10K transactions/day now, projecting 500K in 2 years

### Options Evaluated

| Option | Description |
|--------|-------------|
| Monolith | Single Django application |
| Modular Monolith | Django with strict module boundaries |
| Microservices | Separate services from day one |

### ATAM-Style Scenario Analysis

**Scenario 1: PCI-DSS Audit (Importance: H, Difficulty: H)**

| Architecture | How Supported | Risk |
|--------------|---------------|------|
| Monolith | Single audit scope, but larger blast radius | Medium - all code in scope |
| Modular Monolith | Same as monolith | Medium |
| Microservices | Isolated PCI scope to payment service | Low - minimal scope |

**Scenario 2: Developer Onboarding (Importance: M, Difficulty: L)**

| Architecture | How Supported | Risk |
|--------------|---------------|------|
| Monolith | Single codebase, easy to understand | Low |
| Modular Monolith | Clear structure, moderate complexity | Low |
| Microservices | Multiple repos, complex local setup | High |

**Scenario 3: 50x Traffic Spike (Importance: H, Difficulty: H)**

| Architecture | How Supported | Risk |
|--------------|---------------|------|
| Monolith | Vertical scaling, some horizontal | High - scaling whole app |
| Modular Monolith | Same as monolith | High |
| Microservices | Independent scaling of hot services | Low |

### Trade-off Points Identified

1. **Development Speed vs Future Flexibility**
   - Monolith: Fast now, harder to scale/change later
   - Microservices: Slower now, more flexible later

2. **Operational Simplicity vs Scaling Granularity**
   - Monolith: One deployment, one monitoring setup
   - Microservices: Many deployments, complex observability

3. **PCI Scope vs Development Overhead**
   - Microservices isolate PCI but add operational burden

### Decision

**Chosen: Modular Monolith with extracted Payment Service**

Hybrid approach:
- Core platform as modular monolith
- Payment processing as separate service (PCI isolation)
- Plan to extract more services when team reaches 15+

### Trade-offs Accepted

| What We Get | What We Lose |
|-------------|--------------|
| Fast development velocity | Some future extraction effort |
| Minimal PCI scope | Two deployment pipelines |
| Clear module boundaries | Not full service independence |
| Easier onboarding | Learning modular patterns |

### Architecture Evolution Plan

```
Phase 1 (Now): Modular Monolith + Payment Service
     │
     ▼ Team reaches 15 engineers
Phase 2: Extract Notification Service
     │
     ▼ Team reaches 25 engineers, domains mature
Phase 3: Extract based on team boundaries
```

---

## Example 3: Build vs Buy - Authentication System

### Context

B2B SaaS company needs enterprise authentication features: SSO, SCIM, MFA. Currently using basic email/password auth.

### Constraints

- Budget: $100K implementation budget
- Timeline: 6 months for enterprise tier launch
- Team: 2 engineers can dedicate 50% time
- Requirements: SAML, OIDC, SCIM, MFA, audit logs

### Options Evaluated

| Option | Description |
|--------|-------------|
| Build Custom | In-house authentication system |
| Auth0 | Cloud identity platform |
| Keycloak | Open-source identity server |
| WorkOS | Enterprise auth as a service |

### Cost Analysis (3-Year TCO)

| Cost Factor | Build Custom | Auth0 | Keycloak | WorkOS |
|-------------|--------------|-------|----------|--------|
| Initial development | $200K | $20K | $80K | $15K |
| Annual maintenance | $60K | $0 | $40K | $0 |
| Subscription (1K users) | $0 | $36K/yr | $0 | $30K/yr |
| Infrastructure | $12K/yr | $0 | $24K/yr | $0 |
| **3-Year Total** | **$416K** | **$128K** | **$232K** | **$105K** |

### Strategic Fit Analysis

| Factor | Build | Auth0 | Keycloak | WorkOS |
|--------|-------|-------|----------|--------|
| Is auth core to business? | No | N/A | N/A | N/A |
| Time to market | 12 months | 2 months | 4 months | 1 month |
| Enterprise feature coverage | Unknown | 95% | 80% | 98% |
| Customization flexibility | 100% | 60% | 90% | 50% |
| Vendor lock-in risk | None | High | Low | Medium |

### Trade-off Analysis

**Chosen: WorkOS**

| Evaluating | Build | Auth0 | Keycloak | WorkOS |
|------------|-------|-------|----------|--------|
| **Get** | Full control | Market leader, mature | No vendor lock-in | Fastest to market, enterprise-focused |
| **Lose** | Time, focus | Flexibility, cost at scale | SaaS simplicity | Customization |

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| WorkOS pricing increase | Medium | Medium | Contractual caps, exit clause |
| Feature gap discovered | Low | High | Evaluate alternatives if gap > 10% |
| Vendor discontinuation | Low | High | Data portability clause, SCIM export |

### Exit Strategy

Documented in ADR:
1. All user data exportable via API
2. SAML/OIDC configurations portable
3. Backup plan: migrate to Auth0 (4-week effort)

---

## Example 4: Sync vs Async Communication in Order Processing

### Context

E-commerce platform processing 10K orders/day experiencing timeout issues during payment processing. Order flow: Validate -> Payment -> Inventory -> Notification.

### Current State Issues

- Payment gateway timeouts causing order failures
- Inventory service slow response (2-3s) blocking checkout
- Customer notifications delayed during peak load
- Coupled services creating cascade failures

### Options Evaluated

| Option | Description |
|--------|-------------|
| Optimize sync | Keep sync, optimize each service |
| Full async | All communication via message queue |
| Hybrid | Critical path sync, rest async |
| Saga pattern | Distributed transaction with compensation |

### Quality Attribute Impact

| Attribute | Sync | Full Async | Hybrid | Saga |
|-----------|------|------------|--------|------|
| Consistency | Strong | Eventual | Mixed | Eventual with compensation |
| Latency (user-perceived) | High | Low | Medium | Low |
| Complexity | Low | High | Medium | Very High |
| Reliability | Coupled | Decoupled | Mixed | Decoupled |
| Debugging | Easy | Hard | Medium | Very Hard |

### Scenario Analysis

**Scenario: Payment Gateway 30s Outage**

| Option | Behavior | User Experience |
|--------|----------|-----------------|
| Sync | All checkouts fail | Very Poor |
| Full Async | Orders queued, processed when recovered | Good |
| Hybrid | Orders queued, status updates delayed | Good |
| Saga | Compensation for timeout, retry | Good |

**Scenario: Flash Sale (10x Traffic)**

| Option | Behavior | User Experience |
|--------|----------|-----------------|
| Sync | Timeouts, failures | Very Poor |
| Full Async | Queue builds, eventual processing | Acceptable |
| Hybrid | Checkout fast, processing delayed | Good |
| Saga | Same as hybrid + consistency | Good |

### Decision Matrix

| Criteria | Weight | Sync | Full Async | Hybrid | Saga |
|----------|--------|------|------------|--------|------|
| User experience | 5 | 2 (10) | 3 (15) | 4 (20) | 4 (20) |
| Implementation effort | 4 | 5 (20) | 2 (8) | 3 (12) | 1 (4) |
| Operational complexity | 3 | 5 (15) | 2 (6) | 3 (9) | 1 (3) |
| Reliability | 5 | 2 (10) | 5 (25) | 4 (20) | 5 (25) |
| Data consistency | 4 | 5 (20) | 2 (8) | 3 (12) | 4 (16) |
| **Total** | | **75** | **62** | **73** | **68** |

### Chosen: Hybrid Approach

```
User Request
    │
    ▼
┌─────────────────┐
│ Order Service   │ ──Sync──▶ Validate
│ (orchestrator)  │ ──Sync──▶ Reserve Inventory (2s timeout)
└────────┬────────┘
         │
    Async│(Kafka)
         │
    ┌────┴────┬─────────────┬───────────────┐
    ▼         ▼             ▼               ▼
Payment   Inventory      Shipping      Notification
Service   Deduction      Prep          Service
```

### Trade-offs Documented

| What We Get | What We Lose |
|-------------|--------------|
| Fast checkout response (<500ms) | Immediate payment confirmation |
| Resilience to downstream failures | Strong consistency |
| Independent scaling | Simple debugging |
| Better user experience | Need idempotency everywhere |

### Implementation Notes

1. **Idempotency**: All async handlers must be idempotent
2. **Timeout handling**: 2s sync timeout, then async fallback
3. **Status updates**: WebSocket for real-time order status
4. **Dead letter queue**: For failed processing retry

---

## Example 5: Technical Debt Decision - Refactor vs Ship

### Context

Feature request: Add discount codes to checkout. Current checkout code is messy (technical debt from MVP). Options: refactor first or add feature to existing code.

### Technical Debt Assessment

**Debt Location:** Checkout service
**Debt Type:** Deliberate prudent (MVP speed choice)
**Debt Age:** 8 months
**Developer Pain:** High (2 bugs in last month)

### Options

| Option | Description | Time Estimate |
|--------|-------------|---------------|
| A: Ship on debt | Add discounts to existing messy code | 1 week |
| B: Refactor first | Clean up checkout, then add discounts | 3 weeks |
| C: Parallel refactor | New checkout service, migrate gradually | 4 weeks |
| D: Incremental | Refactor touched code only, Boy Scout style | 2 weeks |

### Business Context

- Marketing campaign launching in 3 weeks (needs discount codes)
- Q4 revenue target depends on campaign
- 2 other features planned for checkout this quarter

### Analysis

| Factor | A: Ship | B: Refactor First | C: Parallel | D: Incremental |
|--------|---------|-------------------|-------------|----------------|
| Meets deadline | Yes | No | No | Yes |
| Adds more debt | Yes | No | No | Slight |
| Future feature velocity | Slower | Faster | Fastest | Moderate |
| Risk of bugs | High | Low | Medium | Medium |

### Decision Framework Applied

1. **Is the deadline real?** Yes - marketing campaign, revenue impact
2. **Will we touch this code again soon?** Yes - 2 more features planned
3. **Current debt budget?** At 25% (above 15-20% target)
4. **Is debt localized?** Yes - checkout service only

### Decision: Option D (Incremental Refactor)

| What We Get | What We Lose |
|-------------|--------------|
| Meet deadline | 1 week longer than shipping dirty |
| Reduce some debt | Not full cleanup |
| Better test coverage | Perfect architecture |
| Team morale | Shipping speed |

### Debt Tracking

```markdown
## Technical Debt Item: DEBT-042

**Location:** checkout/services/order_processor.py
**Type:** Deliberate prudent
**Created:** 2025-01-15
**Severity:** Medium
**Impact:** 2-3 hours/week developer friction

**Description:**
Order calculation logic duplicated, discount logic added incrementally.

**Remediation Plan:**
- Extract PricingService (2 days)
- Add comprehensive unit tests (1 day)
- Refactor order_processor to use PricingService (2 days)

**Trigger for Remediation:**
- Next major checkout feature OR
- Third bug in this area OR
- Q2 2025 (whichever first)

**Status:** Partial remediation in Sprint 24
```

---

## Example 6: Cloud Provider Selection

### Context

Startup expanding from single-region to multi-region deployment. Currently on AWS. Evaluating whether to stay or consider multi-cloud.

### Options

| Option | Description |
|--------|-------------|
| AWS All-in | Expand within AWS, use all native services |
| GCP Migration | Full migration to GCP (better ML tooling) |
| Multi-cloud | Workload-specific cloud placement |
| Cloud-agnostic | Kubernetes-based, portable across clouds |

### Trade-off Matrix

| Factor | AWS All-in | GCP Migration | Multi-cloud | Cloud-agnostic |
|--------|------------|---------------|-------------|----------------|
| Vendor lock-in | High | High | Medium | Low |
| Operational complexity | Low | Medium | Very High | High |
| Cost optimization | Medium | High | High | Medium |
| ML/AI capabilities | Medium | High | High | Medium |
| Team expertise | High | Low | Medium | Medium |
| Migration effort | None | High | Medium | High |

### Cost Analysis (Annual)

| Component | AWS | GCP | Multi-cloud |
|-----------|-----|-----|-------------|
| Compute | $120K | $95K | $100K |
| Data transfer | $40K | $25K | $60K |
| Managed services | $80K | $70K | $90K |
| Operations (FTE) | 0.5 | 1.0 | 2.0 |
| **Total** | **$280K** | **$290K** | **$450K** |

### Decision: AWS All-in with Abstraction Layer

**Rationale:**
- Team expertise in AWS
- Lowest operational complexity
- Added abstraction layer for future portability

### Trade-offs Accepted

| What We Get | What We Lose |
|-------------|--------------|
| Operational simplicity | Best-of-breed ML tools |
| Team velocity | Cloud cost optimization |
| Proven infrastructure | Negotiating leverage |
| Ecosystem depth | Exit flexibility |

### Risk Mitigation

1. **Vendor lock-in:**
   - Containerize all workloads (Kubernetes-ready)
   - Abstract cloud-specific APIs behind interfaces
   - Annual cloud strategy review

2. **Cost:**
   - Reserved instances for baseline
   - Spot instances for batch processing
   - Annual optimization review

---

## Key Lessons from Examples

### Pattern Recognition

| Situation | Common Best Choice |
|-----------|-------------------|
| Small team, unclear requirements | Start simple (monolith, single DB) |
| Time pressure, real deadline | Accept tactical debt, document it |
| Core competitive advantage | Build, don't buy |
| Commodity capability | Buy, don't build |
| Scaling challenges | Add complexity incrementally |

### Common Trade-off Mistakes

1. **Underestimating operational complexity** (Example 1)
2. **Over-engineering for future scale** (Example 2)
3. **Ignoring exit strategy** (Example 3)
4. **Not considering team expertise** (Examples 1, 6)
5. **Binary thinking** (most examples chose hybrid approaches)

### Decision Quality Indicators

Good decisions:
- Explicitly document trade-offs
- Include risk mitigations
- Define evolution path
- Set review checkpoints

Poor decisions:
- Assume no trade-offs exist
- Copy solutions without context
- Ignore team capabilities
- No exit/evolution strategy
