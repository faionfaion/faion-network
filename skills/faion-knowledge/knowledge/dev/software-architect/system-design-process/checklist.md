# System Design Checklist

Step-by-step checklist from requirements to architecture.

## Phase 1: Understand Requirements

### Functional Requirements

- [ ] **Users identified**: Who uses the system? (personas, roles)
- [ ] **Core features listed**: What must the MVP include?
- [ ] **User flows mapped**: How do users accomplish their goals?
- [ ] **Data entities defined**: What data does the system manage?
- [ ] **Integrations listed**: What external systems connect?
- [ ] **Edge cases captured**: What happens in unusual scenarios?

### Non-Functional Requirements

- [ ] **Scale targets set**:
  - [ ] DAU (daily active users): _____
  - [ ] Peak RPS (requests per second): _____
  - [ ] Data growth rate: _____ GB/month
  - [ ] Storage retention: _____ months/years

- [ ] **Availability target defined**:
  - [ ] SLA: _____ % (99.9% = 8.76h downtime/year)
  - [ ] RTO (recovery time objective): _____
  - [ ] RPO (recovery point objective): _____

- [ ] **Latency requirements set**:
  - [ ] p50: _____ ms
  - [ ] p95: _____ ms
  - [ ] p99: _____ ms

- [ ] **Consistency model chosen**:
  - [ ] Strong consistency (banking, inventory)
  - [ ] Eventual consistency (social feeds, analytics)
  - [ ] Causal consistency (collaborative editing)

- [ ] **Security requirements identified**:
  - [ ] Authentication method: _____
  - [ ] Authorization model: _____
  - [ ] Data encryption: at-rest / in-transit / both
  - [ ] Compliance: GDPR / SOC2 / HIPAA / PCI-DSS / None

## Phase 2: Define Scope

- [ ] **In scope** documented (features for this version)
- [ ] **Out of scope** documented (explicitly excluded)
- [ ] **MVP vs full** defined (phased approach if needed)
- [ ] **Success metrics** identified (how to measure success)
- [ ] **Constraints** listed:
  - [ ] Budget: _____
  - [ ] Timeline: _____
  - [ ] Team size/skills: _____
  - [ ] Tech stack restrictions: _____

## Phase 3: High-Level Design

### Architecture Selection

- [ ] **Architecture style chosen**:
  - [ ] Monolith
  - [ ] Modular Monolith
  - [ ] Microservices
  - [ ] Serverless
  - [ ] Event-driven
  - [ ] Hybrid

- [ ] **Rationale documented** (why this style?)

### Component Identification

- [ ] **Major components listed**:
  - [ ] Frontend (web, mobile, API clients)
  - [ ] Backend services
  - [ ] Databases
  - [ ] Caches
  - [ ] Message queues
  - [ ] External APIs

- [ ] **C4 Context diagram created** (system + actors)
- [ ] **C4 Container diagram created** (apps, DBs, services)

### Data Architecture

- [ ] **Primary database selected**:
  - [ ] Relational: PostgreSQL / MySQL
  - [ ] Document: MongoDB / DynamoDB
  - [ ] Key-value: Redis / Memcached
  - [ ] Time-series: TimescaleDB / InfluxDB
  - [ ] Graph: Neo4j / Neptune
  - [ ] Search: Elasticsearch / Algolia

- [ ] **Data model designed**:
  - [ ] Entity relationships defined
  - [ ] Indexes planned
  - [ ] Partitioning strategy (if needed)

- [ ] **Caching strategy defined**:
  - [ ] Cache-aside / Read-through / Write-through
  - [ ] Cache invalidation approach
  - [ ] TTL policies

### API Design

- [ ] **API style chosen**:
  - [ ] REST
  - [ ] GraphQL
  - [ ] gRPC
  - [ ] WebSocket (real-time)

- [ ] **API contracts defined**:
  - [ ] Endpoints/operations listed
  - [ ] Request/response schemas
  - [ ] Error handling conventions
  - [ ] Versioning strategy

## Phase 4: Deep Dive

### Critical Paths

- [ ] **Hot paths identified** (most frequent operations)
- [ ] **Latency-sensitive paths optimized**
- [ ] **Data-intensive operations analyzed**

### Scalability Design

- [ ] **Horizontal scaling points identified**:
  - [ ] Stateless services
  - [ ] Read replicas
  - [ ] Sharding strategy

- [ ] **Vertical scaling limits known**
- [ ] **Auto-scaling policies defined**

### Reliability Design

- [ ] **Single points of failure (SPOF) identified**
- [ ] **Redundancy added** for critical components
- [ ] **Failure modes documented**:
  - [ ] What happens if component X fails?
  - [ ] Graceful degradation strategy
  - [ ] Circuit breaker patterns

- [ ] **Backup strategy defined**:
  - [ ] Backup frequency
  - [ ] Backup retention
  - [ ] Recovery testing plan

### Security Design

- [ ] **Authentication implemented**:
  - [ ] OAuth 2.0 / OIDC
  - [ ] JWT tokens
  - [ ] API keys
  - [ ] MFA

- [ ] **Authorization implemented**:
  - [ ] RBAC / ABAC
  - [ ] Resource-level permissions

- [ ] **Data protection**:
  - [ ] Encryption at rest (AES-256)
  - [ ] Encryption in transit (TLS 1.3)
  - [ ] PII handling

- [ ] **Threat model completed**:
  - [ ] Attack vectors identified
  - [ ] Mitigations documented

## Phase 5: Validate Design

### Review Checklist

- [ ] **Requirements coverage**: All FRs addressed
- [ ] **NFR targets achievable**: Scale, availability, latency
- [ ] **Cost estimation**: Within budget
- [ ] **Team capability**: Can build with current skills
- [ ] **Timeline feasibility**: Achievable in given time

### Bottleneck Analysis

- [ ] **Database bottlenecks**: Read/write scaling plan
- [ ] **Network bottlenecks**: CDN, edge caching
- [ ] **Compute bottlenecks**: Horizontal scaling
- [ ] **Third-party limits**: API rate limits, quotas

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| _____ | High/Med/Low | High/Med/Low | _____ |
| _____ | High/Med/Low | High/Med/Low | _____ |

## Phase 6: Document

### Required Documentation

- [ ] **Architecture Decision Records (ADRs)**:
  - [ ] ADR-001: Architecture style selection
  - [ ] ADR-002: Database selection
  - [ ] ADR-003: Communication patterns
  - [ ] (additional ADRs as needed)

- [ ] **C4 Diagrams**:
  - [ ] Level 1: System Context
  - [ ] Level 2: Container
  - [ ] Level 3: Component (optional, for complex containers)

- [ ] **Data Model Documentation**:
  - [ ] ER diagram
  - [ ] Data dictionary

- [ ] **API Documentation**:
  - [ ] OpenAPI/Swagger spec (REST)
  - [ ] GraphQL schema
  - [ ] gRPC proto files

### Design Document Structure

```markdown
# System Design: [Name]

## 1. Overview
Brief description, goals, success metrics

## 2. Requirements
### Functional
### Non-Functional
### Constraints

## 3. High-Level Architecture
C4 Context diagram, major components

## 4. Detailed Design
### Component A
### Component B
### Data Model
### API Design

## 5. Scalability & Reliability
Scaling strategy, failure handling

## 6. Security
Authentication, authorization, data protection

## 7. Trade-offs & Alternatives
What was considered, why rejected

## 8. Open Questions
Unresolved items for future discussion
```

## Quick Reference: Scale Cheat Sheet

| Scale | Users | RPS | Data | Architecture |
|-------|-------|-----|------|--------------|
| Small | < 10K | < 100 | < 100GB | Monolith, single DB |
| Medium | 10K-1M | 100-10K | 100GB-10TB | Monolith + replicas, caching |
| Large | 1M-100M | 10K-1M | 10TB-1PB | Microservices, sharding |
| Massive | > 100M | > 1M | > 1PB | Distributed systems, specialized DBs |

## Quick Reference: Latency Numbers

| Operation | Latency |
|-----------|---------|
| L1 cache | 1 ns |
| L2 cache | 4 ns |
| RAM | 100 ns |
| SSD random read | 16 us |
| HDD seek | 2 ms |
| Same datacenter round trip | 0.5 ms |
| Cross-region round trip | 50-150 ms |
| Cross-continent round trip | 100-300 ms |

## Related

- [README.md](README.md) - Process overview
- [templates.md](templates.md) - ADR and diagram templates
- [examples.md](examples.md) - Real-world case studies
