# LLM Prompts for Quality Attributes

Effective prompts for LLM-assisted quality attribute analysis, trade-off decisions, and NFR documentation.

---

## Quality Attribute Elicitation Prompts

### System-Wide Quality Analysis

```
Analyze quality attribute requirements for a {system type} with:
- Users: {number and type}
- Scale: {transactions/day, data volume}
- Compliance: {regulations if any}
- Budget: {constraints}

For each quality attribute (Performance, Scalability, Availability, Security,
Maintainability, Testability, Observability), provide:

1. Relevant scenarios using SEI 6-part format
2. Measurable targets (SLIs/SLOs)
3. Recommended architectural tactics
4. Trade-offs to consider
5. Priority (Critical/High/Medium/Low) with rationale
```

### Specific Attribute Deep Dive

```
I need detailed quality requirements for {attribute} in my {system type}.

Context:
- Current state: {metrics if known}
- Business requirements: {goals}
- Technical constraints: {limitations}
- Budget: {range}

Provide:
1. 3-5 quality attribute scenarios (SEI format)
2. Specific SLI/SLO definitions with PromQL/metrics
3. Architectural tactics with trade-offs
4. Implementation recommendations (tools, patterns)
5. Monitoring and alerting strategy
6. Cost implications
```

### Quality Requirements Interview Guide

```
Generate interview questions to elicit quality requirements for {system type}
from {stakeholder type: business/technical/operations}.

For each question, include:
- The question
- Why it matters
- Follow-up probing questions
- How to translate answers into measurable requirements

Focus on: {specific quality attributes or all}
```

---

## Performance Analysis Prompts

### Performance Requirements Definition

```
Define performance requirements for:
- System: {description}
- Key operations: {list critical user actions}
- Expected load: {concurrent users, requests/second}
- SLA tier: {99%, 99.9%, 99.99%}

Provide:
1. Latency targets (p50, p95, p99) per operation
2. Throughput requirements
3. Resource utilization limits
4. Performance testing strategy
5. Monitoring dashboards (Grafana JSON snippet)
6. Alert thresholds
```

### Performance Optimization Analysis

```
Analyze performance bottlenecks for this architecture:

{paste architecture description or diagram}

Current metrics:
- Latency p95: {value}
- Error rate: {value}
- Throughput: {value}

Target metrics:
- Latency p95: {target}
- Error rate: {target}
- Throughput: {target}

Identify:
1. Top 5 likely bottlenecks
2. Quick wins (< 1 week effort)
3. Medium-term improvements (1-4 weeks)
4. Architectural changes needed
5. Expected impact of each recommendation
```

### Caching Strategy Design

```
Design a caching strategy for {system type}:

Data characteristics:
- Read/write ratio: {e.g., 80:20}
- Data freshness requirements: {staleness tolerance}
- Cache hit rate target: {percentage}
- Data size: {approximate}

Consider:
1. Cache layers (browser, CDN, application, database)
2. Cache invalidation strategy
3. Cache key design
4. TTL recommendations
5. Redis/Memcached configuration
6. Cache-aside vs write-through patterns
```

---

## Scalability Analysis Prompts

### Capacity Planning

```
Help me plan capacity for {system type}:

Current state:
- Users: {number}
- Data volume: {size}
- Peak RPS: {value}

Growth projections:
- 6 months: {multiplier}
- 1 year: {multiplier}
- 3 years: {multiplier}

Provide:
1. Scaling strategy (vertical/horizontal/elastic)
2. Database scaling approach
3. Caching layer sizing
4. Message queue capacity
5. Cost projection at each milestone
6. When to consider architectural changes
```

### Database Scaling Decision

```
I need to scale my {database type} database:

Current:
- Size: {GB/TB}
- Read QPS: {value}
- Write QPS: {value}
- Latency p95: {value}

Problems:
- {describe current issues}

Options I'm considering:
1. Vertical scaling
2. Read replicas
3. Sharding
4. Different database

Analyze each option with:
- Pros/cons
- Implementation complexity
- Cost implications
- Migration risks
- Recommended approach
```

---

## Availability and Reliability Prompts

### High Availability Design

```
Design high availability for {system type}:

Requirements:
- SLA: {99.9% / 99.99% / 99.999%}
- RTO: {minutes/hours}
- RPO: {minutes/hours}
- Budget: {range}

Current architecture:
{describe or paste diagram}

Provide:
1. Multi-AZ/multi-region strategy
2. Load balancing configuration
3. Database replication setup
4. Failover automation
5. Health check design
6. Chaos engineering test plan
7. Estimated downtime budget and alerts
```

### Disaster Recovery Planning

```
Create a disaster recovery plan for {system type}:

Business context:
- Revenue impact: {$/hour of downtime}
- Compliance requirements: {if any}
- Data sensitivity: {classification}

Infrastructure:
- Primary region: {AWS/GCP region}
- Current backup strategy: {description}

Define:
1. DR site location and setup
2. Data replication strategy (sync/async)
3. Failover procedures (automated/manual)
4. Failback procedures
5. Testing schedule
6. Runbook for DR activation
7. RTO/RPO validation tests
```

### Failure Mode Analysis

```
Analyze failure modes for {component/system}:

Architecture:
{paste architecture description}

Dependencies:
- {list external services}
- {list databases}
- {list third-party APIs}

For each potential failure:
1. Failure scenario description
2. Impact assessment (users affected, data at risk)
3. Detection mechanism
4. Automated response
5. Manual intervention needed
6. Recovery procedure
7. Preventive measures
```

---

## Security Analysis Prompts

### Security Requirements Elicitation

```
Define security requirements for {system type}:

Context:
- Data types: {PII, financial, health, etc.}
- Compliance: {GDPR, HIPAA, PCI-DSS, SOC2}
- Threat actors: {external hackers, insiders, competitors}
- Risk tolerance: {low/medium/high}

Provide:
1. Authentication requirements (protocols, MFA)
2. Authorization model (RBAC/ABAC)
3. Data protection (encryption, masking)
4. Network security (firewall, WAF)
5. Audit logging requirements
6. Incident response requirements
7. Security testing requirements
```

### Threat Modeling (STRIDE)

```
Perform STRIDE threat modeling for {system/feature}:

System description:
{paste architecture or feature description}

Trust boundaries:
- {list trust boundaries}

Data flows:
- {list data flows}

For each STRIDE category (Spoofing, Tampering, Repudiation,
Information Disclosure, Denial of Service, Elevation of Privilege):

1. Identify threats
2. Assess likelihood (H/M/L)
3. Assess impact (H/M/L)
4. Propose mitigations
5. Map to controls (OWASP, CIS)
```

### Security Architecture Review

```
Review security architecture for:

{paste architecture description}

Authentication:
- {current approach}

Authorization:
- {current approach}

Data protection:
- {current approach}

Evaluate:
1. Authentication strength and gaps
2. Authorization model completeness
3. Data protection adequacy
4. Network security posture
5. Secrets management
6. Logging and monitoring
7. Compliance gaps (for {specify regulations})
8. Top 5 security improvements prioritized
```

---

## Trade-off Analysis Prompts

### ATAM-Style Analysis

```
Perform architecture trade-off analysis for {decision}:

Context:
{describe the architectural decision to make}

Quality attributes at stake:
- {QA1}: {importance}
- {QA2}: {importance}
- {QA3}: {importance}

Options:
1. {Option 1 description}
2. {Option 2 description}
3. {Option 3 description}

For each option, analyze:
1. Impact on each quality attribute (+/-/neutral)
2. Sensitivity points (single QA impact)
3. Trade-off points (multiple QA impact)
4. Risks and mitigations
5. Cost implications
6. Recommendation with rationale
```

### Technology Selection Trade-offs

```
Compare {technology options} for {use case}:

Requirements:
- Performance: {requirements}
- Scalability: {requirements}
- Cost: {constraints}
- Team expertise: {current skills}

For each option, evaluate:
1. Fit for requirements (1-10 score)
2. Quality attribute impact matrix
3. Learning curve
4. Operational complexity
5. Total cost of ownership
6. Vendor lock-in risk
7. Community/support quality
8. Recommendation with trade-off summary
```

### CAP Theorem Decision

```
Help me make a CAP theorem trade-off decision:

System: {description}
Use case: {describe consistency and availability needs}

Scenarios:
1. Normal operation: {requirements}
2. Network partition: {requirements}
3. Node failure: {requirements}

Questions:
- Can we tolerate stale reads? {yes/no/sometimes}
- Can we tolerate unavailability? {yes/no/sometimes}
- What's the consistency model needed? {strong/eventual/causal}

Recommend:
1. CP vs AP decision
2. Database selection implications
3. Replication strategy
4. Conflict resolution approach
5. How to communicate trade-offs to stakeholders
```

---

## SLO Definition Prompts

### SLO Design

```
Design SLOs for {service/system}:

Service type: {request-driven/pipeline/storage}
Users: {internal/external}
Business criticality: {low/medium/high/critical}

Current metrics (if known):
- Availability: {percentage}
- Latency p95: {value}
- Error rate: {percentage}

Define:
1. SLIs with exact measurement method (PromQL)
2. SLO targets with rationale
3. Error budget calculation
4. Error budget policy (what happens when depleted)
5. Alert thresholds (burn rate based)
6. Dashboard design
7. Review cadence
```

### Error Budget Policy

```
Create an error budget policy for {team/service}:

SLO: {target, e.g., 99.9%}
Error budget: {calculated, e.g., 43.8 min/month}

Define actions at these thresholds:
1. > 75% budget remaining
2. 50-75% budget remaining
3. 25-50% budget remaining
4. 10-25% budget remaining
5. < 10% budget remaining
6. Budget exhausted

Include:
- Development velocity impact
- Release process changes
- On-call expectations
- Stakeholder communication
- Post-budget-exhaustion recovery plan
```

---

## NFR Documentation Prompts

### NFR Specification Generation

```
Generate NFR specification document for {project}:

System type: {description}
Stakeholders: {list}
Compliance: {requirements}
Timeline: {phase/release}

Generate complete NFR document with:
1. Performance requirements (with metrics)
2. Scalability requirements (with growth targets)
3. Availability requirements (with SLAs)
4. Security requirements (with controls)
5. Maintainability requirements
6. Testability requirements
7. Observability requirements
8. Cost requirements

Format as a formal requirements document with:
- Unique IDs (NFR-XXX)
- Priority levels
- Verification methods
- Traceability to business goals
```

### Quality Attribute Scenario Writing

```
Write quality attribute scenarios for {requirement}:

Requirement: {description}
Quality attribute: {type}
Criticality: {level}

Write 3 scenarios covering:
1. Normal conditions
2. Peak/stress conditions
3. Failure/edge conditions

Each scenario should include:
- Source (who/what triggers)
- Stimulus (the event)
- Environment (system state)
- Artifact (component affected)
- Response (what happens)
- Response measure (how to verify)
- Priority (business/technical: H/M/L)
```

---

## Architecture Review Prompts

### Quality-Focused Architecture Review

```
Review this architecture for quality attributes:

{paste architecture description or diagram}

Context:
- Scale: {users, data, transactions}
- Environment: {cloud/on-prem/hybrid}
- Team size: {number}
- Budget: {range}

Evaluate each quality attribute:
1. Performance: strengths, weaknesses, recommendations
2. Scalability: strengths, weaknesses, recommendations
3. Availability: strengths, weaknesses, recommendations
4. Security: strengths, weaknesses, recommendations
5. Maintainability: strengths, weaknesses, recommendations

Provide:
- Overall quality score (1-10)
- Top 3 risks
- Top 3 improvement priorities
- Quick wins vs long-term investments
```

### Pre-Production Readiness

```
Assess production readiness for {service}:

Current state:
- Development complete: {yes/no}
- Testing complete: {describe}
- Documentation: {describe}

Checklist against quality attributes:

Performance:
- [ ] Load testing completed
- [ ] Latency targets met
- [ ] Resource limits configured

Availability:
- [ ] Health checks implemented
- [ ] Redundancy configured
- [ ] Failover tested

Security:
- [ ] Security review completed
- [ ] Secrets management configured
- [ ] Authentication/authorization tested

Observability:
- [ ] Logging configured
- [ ] Metrics exposed
- [ ] Alerts configured
- [ ] Dashboards created
- [ ] Runbooks written

For each unchecked item, provide:
1. Risk of shipping without it
2. Minimum viable implementation
3. Recommended timeline
```

---

## Prompt Chaining Strategy

For complex quality analysis, chain prompts in this order:

1. **Discovery:** Elicit requirements from stakeholders
2. **Prioritization:** Build utility tree, identify (H,H) scenarios
3. **Analysis:** Deep dive into critical attributes
4. **Trade-offs:** Analyze competing concerns
5. **Design:** Define SLIs/SLOs and architectural tactics
6. **Documentation:** Generate formal NFR specification
7. **Review:** Validate architecture against requirements

---

## Context Templates

Include these context blocks in prompts for better results.

### Minimal Context

```
System: {type, e.g., "B2B SaaS project management tool"}
Scale: {users, data volume}
Stack: {key technologies}
Constraints: {budget, timeline, team size}
```

### Full Context

```
## System Context
- Type: {description}
- Industry: {sector}
- Compliance: {regulations}

## Scale
- Current users: {number}
- Growth target: {6mo/1yr}
- Data volume: {current/projected}
- Peak traffic: {RPS}

## Technical Stack
- Backend: {languages, frameworks}
- Database: {type, version}
- Infrastructure: {cloud provider, services}
- CI/CD: {tools}

## Team
- Size: {number}
- Expertise: {strengths}
- Gaps: {areas needing support}

## Constraints
- Budget: {range}
- Timeline: {deadline}
- Technical debt: {known issues}
```

---

*Part of [quality-attributes](README.md) | [faion-software-architect](../CLAUDE.md)*
