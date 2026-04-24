# Database Selection Checklist

Systematic checklist for evaluating and selecting databases.

---

## Phase 1: Requirements Gathering

### Data Model

- [ ] **Data structure**: Relational? Document? Graph? Time-series?
- [ ] **Schema stability**: Fixed schema or frequent changes?
- [ ] **Relationships**: Simple references or complex traversals?
- [ ] **Data types**: Standard types? JSON? Vectors? Geospatial?
- [ ] **Document size**: Average and maximum record size?

### Query Patterns

- [ ] **Read/Write ratio**: Read-heavy? Write-heavy? Balanced?
- [ ] **Query complexity**: Simple lookups? Complex joins? Aggregations?
- [ ] **Access patterns**: Point queries? Range scans? Full-text search?
- [ ] **Real-time requirements**: Sub-millisecond? Seconds? Minutes OK?
- [ ] **Batch processing**: ETL jobs? Analytics queries?

### Consistency Requirements

- [ ] **ACID transactions**: Required? For which operations?
- [ ] **Multi-document transactions**: Needed across collections/tables?
- [ ] **Consistency model**: Strong? Eventual? Causal?
- [ ] **Conflict resolution**: Last-write-wins? Application-level?

### Scale Requirements

- [ ] **Data volume (current)**: GB? TB? PB?
- [ ] **Data volume (3-year projection)**: Expected growth rate?
- [ ] **Request rate**: Queries per second? Writes per second?
- [ ] **Concurrent users**: Peak concurrent connections?
- [ ] **Latency SLA**: p50, p95, p99 requirements?

---

## Phase 2: Infrastructure Constraints

### Deployment Model

- [ ] **Cloud provider**: AWS? GCP? Azure? Multi-cloud?
- [ ] **Region requirements**: Single region? Multi-region? Global?
- [ ] **Managed vs self-hosted**: Ops capacity? Budget constraints?
- [ ] **Containerization**: Docker? Kubernetes? Bare metal?

### Availability Requirements

- [ ] **Uptime SLA**: 99.9%? 99.99%? 99.999%?
- [ ] **Recovery time objective (RTO)**: Minutes? Hours?
- [ ] **Recovery point objective (RPO)**: Zero data loss? Minutes OK?
- [ ] **Disaster recovery**: Cross-region replication?

### Security & Compliance

- [ ] **Encryption at rest**: Required? Key management?
- [ ] **Encryption in transit**: TLS required?
- [ ] **Access control**: RBAC? Row-level security?
- [ ] **Compliance**: GDPR? HIPAA? SOC2? PCI-DSS?
- [ ] **Audit logging**: Required for compliance?
- [ ] **Data residency**: Specific region requirements?

---

## Phase 3: Team & Ecosystem

### Team Expertise

- [ ] **Current skills**: What databases does the team know?
- [ ] **Learning curve**: Acceptable ramp-up time?
- [ ] **Hiring pool**: Can we find engineers for this database?
- [ ] **Documentation quality**: Good docs and tutorials?

### Ecosystem Integration

- [ ] **ORM/Driver support**: For your programming language?
- [ ] **Tooling**: Admin UI? Monitoring? Backup tools?
- [ ] **CI/CD integration**: Easy to automate?
- [ ] **Observability**: Metrics export? Logging?

### Vendor & Community

- [ ] **License**: Open source? Commercial? Hybrid?
- [ ] **Vendor lock-in risk**: Proprietary features used?
- [ ] **Community size**: Active development? Good support?
- [ ] **Long-term viability**: Funding? Adoption trends?

---

## Phase 4: Cost Analysis

### Direct Costs

- [ ] **License fees**: Open source? Enterprise license?
- [ ] **Infrastructure cost**: Instance sizing, storage, network?
- [ ] **Managed service fees**: Fully-loaded monthly cost?
- [ ] **Data transfer costs**: Egress, replication?

### Indirect Costs

- [ ] **Operations overhead**: DBA time, on-call burden?
- [ ] **Development time**: Migration effort? Learning curve?
- [ ] **Tooling costs**: Monitoring, backup, security tools?
- [ ] **Training costs**: Team education?

### Cost Optimization

- [ ] **Reserved instances**: Discount for commitment?
- [ ] **Auto-scaling**: Right-sizing based on load?
- [ ] **Storage tiering**: Hot/warm/cold data management?
- [ ] **Connection pooling**: Reduce connection overhead?

---

## Phase 5: Proof of Concept

### Functional Testing

- [ ] **Data model fit**: Does the schema work?
- [ ] **Query performance**: Meet latency requirements?
- [ ] **Write performance**: Meet throughput requirements?
- [ ] **Complex queries**: Aggregations, joins work correctly?

### Load Testing

- [ ] **Steady state**: Performance under normal load?
- [ ] **Peak load**: Performance at 2x-5x normal?
- [ ] **Sustained load**: Performance over 24+ hours?
- [ ] **Recovery**: Behavior after overload?

### Failure Testing

- [ ] **Node failure**: Automatic failover works?
- [ ] **Network partition**: CAP behavior as expected?
- [ ] **Disk failure**: Data recovery possible?
- [ ] **Backup/Restore**: RTO/RPO met?

### Migration Testing

- [ ] **Data migration**: Import process validated?
- [ ] **Application changes**: Code modifications identified?
- [ ] **Rollback plan**: Can revert if issues?
- [ ] **Downtime estimate**: Migration window acceptable?

---

## Phase 6: Final Decision

### Summary Matrix

| Criterion | Weight | DB Option 1 | DB Option 2 | DB Option 3 |
|-----------|--------|-------------|-------------|-------------|
| Data model fit | 25% | ? | ? | ? |
| Query performance | 20% | ? | ? | ? |
| Scale capability | 15% | ? | ? | ? |
| Team expertise | 15% | ? | ? | ? |
| Total cost (3yr) | 15% | ? | ? | ? |
| Ecosystem/tooling | 10% | ? | ? | ? |
| **Weighted Score** | 100% | ? | ? | ? |

### Decision Criteria

- [ ] **Top scorer**: Which database scored highest?
- [ ] **Deal breakers**: Any critical requirements not met?
- [ ] **Risk assessment**: What could go wrong?
- [ ] **Mitigation plan**: How to address risks?

### Approval & Documentation

- [ ] **Architecture Decision Record**: Document the decision
- [ ] **Stakeholder sign-off**: Technical lead, product owner
- [ ] **Migration plan**: Timeline and resources
- [ ] **Rollback criteria**: When to reconsider?

---

## Quick Decision Checklist

For simpler decisions, use this abbreviated checklist:

```markdown
## Quick Database Selection

### Requirements
- [ ] Data model: _____________ (relational/document/graph/time-series/vector)
- [ ] Primary access pattern: _____________ (OLTP/OLAP/search/cache)
- [ ] Consistency: _____________ (strong/eventual)
- [ ] Scale: _____________ (GB/TB/PB)

### Constraints
- [ ] Cloud provider: _____________
- [ ] Managed preference: _____________ (yes/no/flexible)
- [ ] Team expertise: _____________
- [ ] Budget (monthly): _____________

### Decision
- [ ] Primary database: _____________
- [ ] Rationale: _____________
- [ ] Alternatives considered: _____________
```

---

## Related

- [README.md](README.md) - Database categories and CAP theorem
- [examples.md](examples.md) - Real-world use cases
- [templates.md](templates.md) - Decision matrix templates
- [llm-prompts.md](llm-prompts.md) - AI-assisted selection
