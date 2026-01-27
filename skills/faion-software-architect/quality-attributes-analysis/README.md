# Quality Attributes Analysis

Systematic analysis of non-functional requirements (NFRs) and quality attributes for architecture decisions using ATAM, utility trees, and quality attribute scenarios.

## Overview

Quality Attributes Analysis is the process of identifying, prioritizing, and evaluating the non-functional requirements that drive architectural decisions. Unlike functional requirements (what the system does), quality attributes define how well the system performs its functions.

### Why Quality Attributes Matter

- **Architecture drivers**: 80% of architectural decisions stem from quality attributes, not features
- **Early detection**: Quality issues found in design cost 10-100x less to fix than in production
- **Trade-off clarity**: Makes explicit the conflicts between competing quality goals
- **Stakeholder alignment**: Creates shared understanding of system priorities

### ISO/IEC 25010:2023 Quality Model

The latest ISO standard defines nine product quality characteristics:

| Characteristic | Definition | Key Sub-characteristics |
|---------------|------------|------------------------|
| **Functional Suitability** | Functions meet stated needs | Completeness, correctness, appropriateness |
| **Performance Efficiency** | Performance vs resources | Time behavior, resource utilization, capacity |
| **Compatibility** | Exchange info with other systems | Co-existence, interoperability |
| **Interaction Capability** | Operated by specified users | Usability, accessibility, user error protection |
| **Reliability** | Functions under stated conditions | Availability, fault tolerance, recoverability |
| **Security** | Protection of information | Confidentiality, integrity, authenticity |
| **Maintainability** | Effectiveness of modifications | Modularity, reusability, modifiability, testability |
| **Flexibility** | Adaptability to changes | Adaptability, scalability, installability |
| **Safety** | Avoid states that cause harm | Operational constraint, risk identification |

---

## Core Concepts

### Quality Attribute Scenario

A testable statement that defines a quality requirement with six parts:

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUALITY ATTRIBUTE SCENARIO                   │
├─────────────────────────────────────────────────────────────────┤
│  Source          →  Who/what generates the stimulus            │
│  Stimulus        →  What event or condition triggers response  │
│  Environment     →  Context: normal, overload, attack, etc.    │
│  Artifact        →  What part of system is affected            │
│  Response        →  How system should behave                   │
│  Response Measure →  Quantifiable success criteria             │
└─────────────────────────────────────────────────────────────────┘
```

**Example Performance Scenario:**
- **Source**: Marketing campaign
- **Stimulus**: 10x traffic spike (1M concurrent users)
- **Environment**: Production, peak hours
- **Artifact**: API gateway, checkout service
- **Response**: Auto-scale, queue excess requests
- **Measure**: p99 latency < 500ms, 0% errors, scale within 60s

### Utility Tree

Hierarchical representation of quality requirements used to prioritize architectural drivers:

```
                           UTILITY
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
     Performance         Security           Availability
          │                   │                   │
    ┌─────┴─────┐      ┌─────┴─────┐      ┌─────┴─────┐
    │           │      │           │      │           │
 Latency   Throughput Auth     Encrypt   Uptime   Recovery
    │           │      │           │      │           │
 (H,M)       (M,H)   (H,H)      (M,M)   (H,H)      (M,H)
```

**Priority notation**: (Importance, Difficulty)
- H = High, M = Medium, L = Low
- (H,H) = High importance, Hard to achieve → Critical architectural driver

### ATAM (Architecture Tradeoff Analysis Method)

SEI Carnegie Mellon's method for evaluating architectures against quality goals.

**Nine ATAM Steps:**

| Phase | Step | Activity |
|-------|------|----------|
| **Phase 1** | 1 | Present ATAM to stakeholders |
| | 2 | Present business drivers |
| | 3 | Present architecture |
| | 4 | Identify architectural approaches |
| | 5 | Generate utility tree |
| | 6 | Analyze architectural approaches |
| **Phase 2** | 7 | Brainstorm and prioritize scenarios |
| | 8 | Analyze architectural approaches (refined) |
| | 9 | Present results |

**ATAM Outputs:**

| Output | Description |
|--------|-------------|
| **Risks** | Architecture decisions that may cause problems |
| **Non-risks** | Sound decisions that are well-understood |
| **Sensitivity Points** | Parameters where small changes have big impact |
| **Tradeoff Points** | Decisions affecting multiple quality attributes |
| **Risk Themes** | Patterns of risk across the architecture |

---

## Quality Attribute Tactics

Tactics are proven design decisions that influence a specific quality attribute.

### Performance Tactics

| Tactic | Description | Example |
|--------|-------------|---------|
| **Increase resources** | More CPU, memory, bandwidth | Vertical scaling |
| **Introduce concurrency** | Parallel processing | Thread pools, async I/O |
| **Reduce overhead** | Minimize per-request work | Connection pooling |
| **Manage sampling rate** | Process subset of data | Monitoring aggregation |
| **Bound queue sizes** | Limit pending work | Backpressure |
| **Schedule resources** | Prioritize important work | Priority queues |

### Availability Tactics

| Tactic | Description | Example |
|--------|-------------|---------|
| **Ping/Echo** | Health checking | Load balancer probes |
| **Heartbeat** | Periodic liveness signal | Service mesh |
| **Exception handling** | Graceful error recovery | Try-catch, circuit breakers |
| **Voting** | Consensus among replicas | Raft, Paxos |
| **Active redundancy** | Hot standby | Multi-AZ deployment |
| **Passive redundancy** | Warm/cold standby | DR region |
| **Rollback** | Restore previous state | Database PITR |

### Security Tactics

| Tactic | Description | Example |
|--------|-------------|---------|
| **Authenticate** | Verify identity | OAuth 2.0, OIDC |
| **Authorize** | Verify permissions | RBAC, ABAC |
| **Encrypt** | Protect data | TLS, AES-256 |
| **Limit access** | Reduce attack surface | Firewalls, VPC |
| **Limit exposure** | Minimize data exposure | Data masking |
| **Detect intrusion** | Monitor for attacks | SIEM, WAF |
| **Verify integrity** | Detect tampering | HMAC, signatures |

### Modifiability Tactics

| Tactic | Description | Example |
|--------|-------------|---------|
| **Split module** | Separate concerns | Microservices |
| **Encapsulate** | Hide implementation | APIs, interfaces |
| **Use intermediary** | Decouple components | Message queues |
| **Restrict dependencies** | Limit coupling | Dependency injection |
| **Defer binding** | Late configuration | Feature flags |
| **Abstract services** | Hide platform details | Adapters |

### Scalability Tactics

| Tactic | Description | Example |
|--------|-------------|---------|
| **Horizontal scaling** | Add more instances | Auto-scaling groups |
| **Data partitioning** | Shard databases | Hash/range sharding |
| **Load balancing** | Distribute requests | L4/L7 load balancers |
| **Stateless design** | No session affinity | JWT tokens |
| **Caching** | Reduce load on backends | Redis, CDN |
| **Async processing** | Decouple request/response | Message queues |

---

## Stakeholder Analysis

Different stakeholders prioritize different quality attributes:

| Stakeholder | Primary Concerns | Quality Focus |
|-------------|------------------|---------------|
| **End Users** | Fast, reliable experience | Performance, Availability, Usability |
| **Operations** | Easy to deploy and monitor | Maintainability, Observability |
| **Security Team** | Protected from threats | Security, Compliance, Auditability |
| **Business** | Cost-effective scaling | Scalability, Cost efficiency |
| **Developers** | Easy to understand and change | Modifiability, Testability |
| **Architects** | Long-term sustainability | Flexibility, Interoperability |

### Stakeholder Concern Matrix

```
                    Performance  Availability  Security  Modifiability  Cost
End Users              ●●●          ●●●          ●○○         ○○○        ○○○
Operations             ●●○          ●●●          ●●○         ●●●        ●●○
Security Team          ○○○          ●●○          ●●●         ●○○        ○○○
Business               ●●○          ●●●          ●●○         ○○○        ●●●
Developers             ●○○          ○○○          ●○○         ●●●        ○○○

Legend: ●●● = Critical, ●●○ = Important, ●○○ = Relevant, ○○○ = Low priority
```

---

## Common Trade-offs

Quality attributes often conflict. Understanding trade-offs is essential:

| Decision | Favors | Sacrifices | Example |
|----------|--------|------------|---------|
| Strong consistency | Correctness | Performance, Availability | ACID databases |
| Eventual consistency | Performance, Availability | Immediate accuracy | NoSQL, caches |
| Microservices | Scalability, Team autonomy | Complexity, Latency | Netflix, Uber |
| Monolith | Simplicity, Performance | Independent scaling | Early startups |
| Encryption everywhere | Security | Performance | Zero trust |
| Feature flags | Modifiability, Safety | Complexity | Trunk-based dev |
| Caching | Performance | Consistency | Read-heavy workloads |
| Async processing | Scalability, Resilience | Complexity, Latency | Event-driven |

### CAP Theorem Trade-offs

During network partitions, choose two of three:

| Choice | What You Get | What You Sacrifice | Use Case |
|--------|--------------|-------------------|----------|
| **CP** | Consistency + Partition tolerance | Availability | Financial transactions |
| **AP** | Availability + Partition tolerance | Consistency | Social feeds, shopping cart |
| **CA** | Consistency + Availability | Partition tolerance | Single-node systems only |

---

## LLM Usage Tips

### When to Use LLM for QA Analysis

| Task | LLM Effectiveness | Notes |
|------|-------------------|-------|
| Generate scenarios | High | Provide domain context |
| Identify trade-offs | High | Ask for multiple perspectives |
| Suggest tactics | High | Specify constraints |
| Prioritize attributes | Medium | Combine with stakeholder input |
| Validate scenarios | Medium | Cross-check with domain experts |
| Quantify measures | Low | Requires real performance data |

### Effective Prompting Patterns

**Context-rich requests:**
```
"For a fintech payment processing system handling 10K TPS
with 99.99% availability requirement, analyze trade-offs
between strong consistency and performance."
```

**Structured output:**
```
"Generate 5 quality attribute scenarios for scalability
using this format: Source, Stimulus, Environment, Artifact,
Response, Response Measure"
```

**Trade-off exploration:**
```
"Compare microservices vs modular monolith for a 10-person
startup. Consider: team size, deployment complexity,
performance, and time-to-market."
```

### Anti-patterns to Avoid

- Asking for specific SLO numbers without real data
- Accepting generic scenarios without domain customization
- Skipping stakeholder validation of priorities
- Using LLM output as final decision (always validate)

---

## Related Methodologies

| Methodology | Focus | When to Use |
|-------------|-------|-------------|
| [ATAM](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) | Trade-off analysis | Major architectural decisions |
| [SAAM](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=12558) | Modifiability analysis | Change impact evaluation |
| [ARID](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=5722) | Active reviews for design | Early design validation |
| [QAW](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=6795) | Quality attribute workshop | Requirements elicitation |
| [CBAM](https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=5914) | Cost-benefit analysis | Economic justification |

---

## External Resources

### Official Standards and Methods

- [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html) - Product quality model
- [SEI ATAM Collection](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) - Official ATAM resources
- [arc42 Quality Model](https://quality.arc42.org/standards/iso-25010) - ISO 25010 practical guide

### Books and Papers

- "Software Architecture in Practice" (4th ed.) - Bass, Clements, Kazman
- "Documenting Software Architectures" - Clements et al.
- "Risk Themes Discovered Through Architecture Evaluations" - CMU/SEI-2006-TR-012

### Online Resources

- [Quality Attribute Scenarios (Design Practice Repository)](https://socadk.github.io/design-practice-repository/artifact-templates/DPR-QualityAttributeScenario.html)
- [Utility Trees and Quality Attributes](https://arnon.me/2012/04/utility-trees-quality-attributes/)
- [ATAM Overview (CIO Wiki)](https://cio-wiki.org/wiki/Architecture_Tradeoff_Analysis_Method_(ATAM))
- [Quality Attributes Tactics](https://bohutskyi.com/Quality_Attributes_Tactics.html)

---

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step QA analysis checklist |
| [examples.md](examples.md) | Real-world QA analysis examples |
| [templates.md](templates.md) | Copy-paste analysis templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted analysis |

## Related Skill Files

| File | Purpose |
|------|---------|
| [trade-off-analysis/](../trade-off-analysis/) | Decision framework for trade-offs |
| [quality-attributes/](../quality-attributes/) | ISO 25010 quality framework |
| [system-design-process/](../system-design-process/) | Overall design workflow |
| [reliability-architecture/](../reliability-architecture/) | Reliability deep dive |
| [performance-architecture/](../performance-architecture/) | Performance deep dive |
| [security-architecture/](../security-architecture/) | Security deep dive |
