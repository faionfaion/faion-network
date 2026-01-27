# Quality Attributes Analysis Examples

Real-world examples of quality attribute scenarios, utility trees, ATAM analysis, and trade-off decisions.

---

## Example 1: E-commerce Platform

### Context

- **System**: Online marketplace with 500K daily active users
- **Business drivers**: Black Friday sales, global expansion, mobile-first
- **Key stakeholders**: Product, Engineering, Operations, Security, Finance

### Utility Tree

```
                              UTILITY
                                 │
     ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
     │           │           │       │           │           │
Performance  Availability  Security  Scalability  Maintainability
     │           │           │       │           │           │
     ├─Latency   ├─Uptime    ├─Auth  ├─Elastic   ├─Deploy
     │ (H,M)     │ (H,H)     │(H,M)  │ (H,H)     │ (M,M)
     │           │           │       │           │
     ├─Throughput├─Recovery  ├─Data  ├─Data      ├─Test
     │ (H,H)     │ (H,M)     │(H,H)  │ (M,H)     │ (M,L)
     │           │           │       │           │
     └─Resource  └─Degrade   └─Fraud └─Multi-    └─Observe
       (M,M)       (M,M)       (H,H)   region      (H,M)
                                       (L,H)
```

### Quality Attribute Scenarios

#### Performance Scenarios

**PERF-1: Checkout Response Time (H,M)**
| Part | Value |
|------|-------|
| Source | Customer |
| Stimulus | Submit payment for checkout |
| Environment | Production, Black Friday peak (10x normal) |
| Artifact | Checkout service, payment gateway |
| Response | Complete payment processing |
| Measure | p99 < 3s, p50 < 1s |

**PERF-2: Product Search Throughput (H,H)**
| Part | Value |
|------|-------|
| Source | Customer |
| Stimulus | Search for product with filters |
| Environment | Normal operation, 50K concurrent users |
| Artifact | Search service, Elasticsearch cluster |
| Response | Return paginated results with facets |
| Measure | 5,000 searches/second, p99 < 500ms |

#### Availability Scenarios

**AVAIL-1: System Uptime (H,H)**
| Part | Value |
|------|-------|
| Source | System/Infrastructure |
| Stimulus | Component failure (single AZ outage) |
| Environment | Production, any time |
| Artifact | All customer-facing services |
| Response | Failover to healthy instances |
| Measure | 99.95% uptime (22 min/month downtime max) |

**AVAIL-2: Database Recovery (H,M)**
| Part | Value |
|------|-------|
| Source | Operations team |
| Stimulus | Database corruption detected |
| Environment | Production, business hours |
| Artifact | Order database |
| Response | Restore from backup, replay transactions |
| Measure | RPO < 5 min, RTO < 30 min |

#### Security Scenarios

**SEC-1: Payment Data Protection (H,H)**
| Part | Value |
|------|-------|
| Source | Attacker |
| Stimulus | Attempt to intercept payment data |
| Environment | Any |
| Artifact | Payment processing pipeline |
| Response | Block access, alert security team |
| Measure | 0 successful data breaches, PCI-DSS compliant |

**SEC-2: Fraud Detection (H,H)**
| Part | Value |
|------|-------|
| Source | Fraudulent actor |
| Stimulus | Attempt fraudulent transaction |
| Environment | Production |
| Artifact | Fraud detection service |
| Response | Flag transaction, require verification |
| Measure | Detect 95% fraud, < 0.1% false positives |

#### Scalability Scenarios

**SCALE-1: Elastic Scaling (H,H)**
| Part | Value |
|------|-------|
| Source | Marketing campaign |
| Stimulus | 10x traffic spike within 5 minutes |
| Environment | Production, promotional event |
| Artifact | API gateway, all stateless services |
| Response | Auto-scale to handle load |
| Measure | Scale within 2 min, 0% errors during scaling |

### Sensitivity Points

| ID | Component | Parameter | Sensitivity |
|----|-----------|-----------|-------------|
| SP-1 | Database | Connection pool size | 10% change = 20% latency impact |
| SP-2 | Cache | TTL setting | Shorter TTL = higher DB load |
| SP-3 | Load balancer | Health check interval | Faster = quicker failover, more overhead |
| SP-4 | Search | Index refresh rate | Real-time = CPU intensive |

### Trade-off Points

| ID | Decision | Attributes Affected | Current Choice |
|----|----------|---------------------|----------------|
| TP-1 | Sync vs async inventory | Consistency vs Performance | Async (eventual consistency) |
| TP-2 | Strong vs eventual consistency for cart | Consistency vs Availability | Eventual (AP in CAP) |
| TP-3 | Microservices vs monolith | Scalability vs Complexity | Microservices |
| TP-4 | Multi-region active-active | Availability vs Cost | Active-passive (cost) |

### Risks Identified

| Risk | Description | Severity | Mitigation |
|------|-------------|----------|------------|
| R-1 | Single database SPOF | High | Add read replicas, implement CQRS |
| R-2 | No circuit breakers | High | Implement Resilience4j patterns |
| R-3 | Synchronous payment calls | Medium | Add timeout and retry policies |
| R-4 | No chaos testing | Medium | Implement Chaos Monkey |

### Risk Themes

1. **Resilience gaps**: System lacks fault tolerance patterns (R-1, R-2, R-3)
2. **Operational maturity**: Missing observability and chaos testing (R-4)
3. **Scalability ceiling**: Database scaling strategy undefined (R-1)

---

## Example 2: Healthcare Data Platform

### Context

- **System**: Patient health records and analytics platform
- **Business drivers**: HIPAA compliance, interoperability, data insights
- **Key stakeholders**: Compliance, Clinical, IT, Patients

### Utility Tree

```
                              UTILITY
                                 │
     ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
     │           │           │       │           │           │
  Security   Compliance   Availability  Interop   Performance
     │           │           │          │           │
     ├─Access    ├─HIPAA     ├─Uptime   ├─HL7/FHIR  ├─Query
     │ (H,H)     │ (H,H)     │ (H,H)    │ (H,M)     │ (M,M)
     │           │           │          │           │
     ├─Audit     ├─Retention ├─DR       ├─EHR       ├─Ingest
     │ (H,M)     │ (H,M)     │ (H,H)    │ (H,H)     │ (M,H)
     │           │           │          │           │
     └─Encrypt   └─Consent   └─Backup   └─API       └─Dashboard
       (H,H)       (H,H)       (M,M)      (M,M)       (L,M)
```

### Quality Attribute Scenarios

#### Security Scenarios

**SEC-1: Data Access Control (H,H)**
| Part | Value |
|------|-------|
| Source | Healthcare provider |
| Stimulus | Request access to patient record |
| Environment | Production |
| Artifact | Patient data service, RBAC system |
| Response | Validate role, check consent, grant/deny |
| Measure | 100% access control enforcement, audit every access |

**SEC-2: Data Encryption (H,H)**
| Part | Value |
|------|-------|
| Source | Internal/External |
| Stimulus | Data at rest or in transit |
| Environment | All environments |
| Artifact | All data stores, network |
| Response | Encrypt with AES-256 at rest, TLS 1.3 in transit |
| Measure | 0% unencrypted PHI, annual penetration test passed |

#### Compliance Scenarios

**COMP-1: HIPAA Audit (H,H)**
| Part | Value |
|------|-------|
| Source | External auditor |
| Stimulus | Request access logs for last 6 months |
| Environment | Audit period |
| Artifact | Audit logging system |
| Response | Provide complete, tamper-proof logs |
| Measure | 100% access events logged, logs immutable |

**COMP-2: Data Retention (H,M)**
| Part | Value |
|------|-------|
| Source | Compliance officer |
| Stimulus | Patient requests record deletion |
| Environment | Production |
| Artifact | Data lifecycle management |
| Response | Apply retention policy, anonymize or delete |
| Measure | Comply within 30 days, maintain required records |

#### Availability Scenarios

**AVAIL-1: System Uptime for Clinical (H,H)**
| Part | Value |
|------|-------|
| Source | System |
| Stimulus | Any failure |
| Environment | Production, 24/7 |
| Artifact | Clinical decision support, patient lookup |
| Response | Failover, graceful degradation |
| Measure | 99.99% uptime (4.4 min/month max) |

**AVAIL-2: Disaster Recovery (H,H)**
| Part | Value |
|------|-------|
| Source | Natural disaster |
| Stimulus | Primary datacenter unavailable |
| Environment | Disaster |
| Artifact | Entire system |
| Response | Activate DR site |
| Measure | RPO < 1 hour, RTO < 4 hours |

#### Interoperability Scenarios

**INTER-1: FHIR API Compliance (H,M)**
| Part | Value |
|------|-------|
| Source | External EHR system |
| Stimulus | Request patient data via FHIR R4 |
| Environment | Production |
| Artifact | FHIR server |
| Response | Return conformant FHIR resources |
| Measure | 100% FHIR R4 conformance, SMART on FHIR auth |

**INTER-2: EHR Integration (H,H)**
| Part | Value |
|------|-------|
| Source | Hospital EHR (Epic, Cerner) |
| Stimulus | Real-time patient data sync |
| Environment | Production |
| Artifact | Integration engine |
| Response | Transform, validate, store data |
| Measure | < 5 min sync latency, 99.9% delivery rate |

### Trade-off Decisions

| Decision | Trade-off | Choice | Rationale |
|----------|-----------|--------|-----------|
| Encryption granularity | Security vs Performance | Column-level encryption for PHI | Balance compliance and query speed |
| Audit log retention | Cost vs Compliance | 7 years hot, archive after 2 | HIPAA minimum + buffer |
| Multi-tenancy | Cost vs Isolation | Physical isolation per health system | Regulatory requirements |
| API rate limiting | Availability vs Interoperability | Generous limits with burst | Support clinical workflows |

### Risks and Mitigations

| Risk | Theme | Mitigation |
|------|-------|------------|
| Key management complexity | Security | Use HSM, implement key rotation |
| Consent tracking gaps | Compliance | Implement consent management service |
| Single region deployment | Availability | Plan multi-region DR |
| HL7v2 legacy dependencies | Interoperability | Build translation layer |

---

## Example 3: Real-time Trading Platform

### Context

- **System**: High-frequency trading platform
- **Business drivers**: Ultra-low latency, regulatory compliance, reliability
- **Key stakeholders**: Traders, Risk, Compliance, Technology

### Utility Tree (Prioritized)

```
                              UTILITY
                                 │
     ┌───────────┬───────────┬───┴───┬───────────┐
     │           │           │       │           │
Performance  Reliability  Compliance  Security  Scalability
     │           │           │         │           │
     ├─Latency   ├─Uptime    ├─MiFID   ├─Access    ├─Throughput
     │ (H,H)     │ (H,H)     │ (H,H)   │ (H,M)     │ (H,M)
     │           │           │         │           │
     ├─Jitter    ├─Failover  ├─Audit   ├─Network   ├─Burst
     │ (H,H)     │ (H,H)     │ (H,M)   │ (H,H)     │ (M,H)
     │           │           │         │           │
     └─Determinism└─Recovery └─Report  └─Data      └─Markets
       (H,H)       (M,H)       (M,M)     (M,M)       (M,M)
```

### Quality Attribute Scenarios

#### Performance Scenarios

**PERF-1: Order Execution Latency (H,H)**
| Part | Value |
|------|-------|
| Source | Trading algorithm |
| Stimulus | Submit market order |
| Environment | Normal market hours, peak volume |
| Artifact | Order execution engine |
| Response | Execute order, confirm fill |
| Measure | p99 < 100 microseconds, p50 < 50 microseconds |

**PERF-2: Market Data Processing (H,H)**
| Part | Value |
|------|-------|
| Source | Market data feed |
| Stimulus | Receive price update |
| Environment | Market open, 10M messages/second |
| Artifact | Market data handler |
| Response | Parse, validate, distribute to strategies |
| Measure | < 10 microseconds per message |

**PERF-3: Latency Jitter (H,H)**
| Part | Value |
|------|-------|
| Source | Trading system |
| Stimulus | Any order under any load |
| Environment | All conditions |
| Artifact | End-to-end path |
| Response | Consistent response time |
| Measure | p99/p50 ratio < 2 (low jitter) |

#### Reliability Scenarios

**REL-1: Trading Engine Availability (H,H)**
| Part | Value |
|------|-------|
| Source | System |
| Stimulus | Component failure |
| Environment | Market hours |
| Artifact | Primary trading engine |
| Response | Failover to standby |
| Measure | Failover < 50ms, 0 lost orders |

**REL-2: State Recovery (H,H)**
| Part | Value |
|------|-------|
| Source | Operations |
| Stimulus | System restart required |
| Environment | Pre-market |
| Artifact | Order management system |
| Response | Restore all open orders and positions |
| Measure | Full state recovery < 30 seconds |

#### Compliance Scenarios

**COMP-1: Order Audit Trail (H,H)**
| Part | Value |
|------|-------|
| Source | Regulator |
| Stimulus | Request order reconstruction |
| Environment | Investigation |
| Artifact | Audit system |
| Response | Provide complete order lifecycle |
| Measure | Nanosecond precision, 7-year retention |

**COMP-2: Pre-trade Risk Checks (H,H)**
| Part | Value |
|------|-------|
| Source | Trading algorithm |
| Stimulus | Order submission |
| Environment | All conditions |
| Artifact | Risk engine |
| Response | Validate against limits, approve/reject |
| Measure | < 5 microseconds check, 0 bypass possible |

### Sensitivity Points

| Component | Parameter | Impact |
|-----------|-----------|--------|
| Network | Switch latency | 1 microsecond = competitive disadvantage |
| Memory | NUMA allocation | Wrong node = 100ns penalty |
| GC | Pause time | Any pause = missed opportunities |
| Kernel | Scheduler | Context switch = latency spike |

### Trade-off Analysis

| Trade-off | Options | Decision | Rationale |
|-----------|---------|----------|-----------|
| Language runtime | JVM vs Native | Native (C++/Rust) | Predictable latency, no GC |
| Persistence | Sync vs Async | Async with replication | Latency, replicas for durability |
| Monitoring | Inline vs External | External sampling | Zero latency impact |
| Logging | Sync vs Async | Lock-free async | Cannot block hot path |

### Architecture Decisions

**ADR-001: Memory-Mapped I/O for Market Data**
- **Context**: Need sub-microsecond market data access
- **Decision**: Use memory-mapped files with kernel bypass
- **Consequences**: Complex development, exceptional performance

**ADR-002: FPGA for Order Gateway**
- **Context**: Network latency is competitive differentiator
- **Decision**: Implement order gateway in FPGA
- **Consequences**: Higher development cost, sub-microsecond latency

**ADR-003: Active-Active with Deterministic Replay**
- **Context**: Zero data loss, instant failover required
- **Decision**: Replicate all inputs, deterministic processing
- **Consequences**: Can replay exact state on any node

---

## Example 4: SaaS Analytics Platform

### Context

- **System**: Multi-tenant analytics platform
- **Business drivers**: Fast time-to-insight, data security, cost efficiency
- **Key stakeholders**: Data analysts, IT admins, Finance, Security

### Quality Attribute Scenarios

#### Multi-tenancy Scenarios

**MT-1: Tenant Isolation (H,H)**
| Part | Value |
|------|-------|
| Source | Tenant A |
| Stimulus | Query execution |
| Environment | Shared infrastructure |
| Artifact | Query engine, data storage |
| Response | Access only tenant A data |
| Measure | 0% cross-tenant data access, verified by audit |

**MT-2: Noisy Neighbor Prevention (H,M)**
| Part | Value |
|------|-------|
| Source | Large tenant |
| Stimulus | Resource-intensive query |
| Environment | Shared compute |
| Artifact | Query scheduler |
| Response | Throttle to fair share |
| Measure | No tenant uses > 30% shared resources |

#### Performance Scenarios

**PERF-1: Dashboard Load Time (M,M)**
| Part | Value |
|------|-------|
| Source | Data analyst |
| Stimulus | Open analytics dashboard |
| Environment | Production, 1TB dataset |
| Artifact | Dashboard service, query cache |
| Response | Render interactive dashboard |
| Measure | Initial load < 3s, interaction < 500ms |

**PERF-2: Ad-hoc Query (M,H)**
| Part | Value |
|------|-------|
| Source | Data analyst |
| Stimulus | Run complex aggregation query |
| Environment | Production, 10TB dataset |
| Artifact | Query engine, data warehouse |
| Response | Return results or progress indicator |
| Measure | Simple queries < 10s, complex < 5 min |

#### Cost Efficiency Scenarios

**COST-1: Compute Optimization (H,M)**
| Part | Value |
|------|-------|
| Source | System |
| Stimulus | Low utilization detected |
| Environment | Off-peak hours |
| Artifact | Compute cluster |
| Response | Scale down resources |
| Measure | Average utilization > 60%, scale down within 5 min |

**COST-2: Storage Tiering (M,M)**
| Part | Value |
|------|-------|
| Source | System |
| Stimulus | Data aging policy trigger |
| Environment | Continuous |
| Artifact | Storage manager |
| Response | Move cold data to cheaper tier |
| Measure | Hot:warm:cold ratio optimizes cost by 40% |

### Stakeholder Priorities Matrix

| Stakeholder | Performance | Security | Cost | Usability |
|-------------|-------------|----------|------|-----------|
| Data Analysts | High | Medium | Low | High |
| IT Admins | Medium | High | Medium | Medium |
| Finance | Low | Medium | High | Low |
| Security | Low | High | Low | Low |
| Executives | Medium | High | High | Medium |

### Trade-off Decisions

| Decision | Stakeholder Conflict | Resolution |
|----------|---------------------|------------|
| Shared vs dedicated compute | Cost (Finance) vs Performance (Analysts) | Tiered offering |
| Real-time vs batch | Cost vs Freshness | Near-real-time default, real-time premium |
| Encryption overhead | Security vs Performance | Encrypt at rest, selective in transit |
| Data locality | Compliance vs Performance | Regional deployment with optional global |

---

## Example 5: IoT Fleet Management

### Context

- **System**: Vehicle fleet tracking and management
- **Business drivers**: Real-time visibility, predictive maintenance, fuel optimization
- **Key stakeholders**: Fleet managers, Drivers, Maintenance, Operations

### Quality Attribute Scenarios

#### Reliability Scenarios

**REL-1: Connectivity Loss Handling (H,H)**
| Part | Value |
|------|-------|
| Source | Vehicle device |
| Stimulus | Network connectivity lost |
| Environment | Rural areas, tunnels |
| Artifact | Edge device, data sync service |
| Response | Buffer locally, sync when connected |
| Measure | 0% data loss, sync within 5 min of reconnection |

**REL-2: Device Failure Detection (H,M)**
| Part | Value |
|------|-------|
| Source | Fleet management system |
| Stimulus | No heartbeat from device |
| Environment | Production |
| Artifact | Device monitoring service |
| Response | Alert fleet manager, trigger diagnostics |
| Measure | Detect failure within 2 min, 0 false negatives |

#### Performance Scenarios

**PERF-1: Location Update Latency (H,M)**
| Part | Value |
|------|-------|
| Source | Vehicle device |
| Stimulus | GPS position change |
| Environment | Normal operation, 100K vehicles |
| Artifact | Ingestion pipeline, location service |
| Response | Update map display |
| Measure | End-to-end latency < 5 seconds |

**PERF-2: Geofence Alert (H,H)**
| Part | Value |
|------|-------|
| Source | Vehicle device |
| Stimulus | Enter/exit geofence boundary |
| Environment | Production |
| Artifact | Geofence engine |
| Response | Trigger alert, log event |
| Measure | Alert within 10 seconds of boundary crossing |

#### Scalability Scenarios

**SCALE-1: Fleet Growth (M,H)**
| Part | Value |
|------|-------|
| Source | Business growth |
| Stimulus | Fleet size doubles (100K to 200K vehicles) |
| Environment | Production |
| Artifact | Entire platform |
| Response | Handle increased load |
| Measure | Latency unchanged, linear cost scaling |

### Edge Computing Trade-offs

| Decision | Edge | Cloud | Choice |
|----------|------|-------|--------|
| Location processing | Low latency | Consistent | Edge for geofence, cloud for analytics |
| Data storage | Limited | Unlimited | Edge buffer, cloud permanent |
| ML inference | Real-time | Batch | Edge for anomaly detection |
| Updates | Complex | Simple | Cloud-managed with edge sync |

---

## Summary: Common Patterns

### Frequently Occurring Trade-offs

1. **Consistency vs Availability**: Most systems choose eventual consistency for performance
2. **Security vs Performance**: Encryption overhead is accepted for compliance
3. **Scalability vs Complexity**: Microservices chosen when team size justifies
4. **Cost vs Performance**: Tiered offerings resolve stakeholder conflicts

### Common Risk Themes

1. **Single points of failure**: Database, message queue, authentication
2. **Missing resilience patterns**: No circuit breakers, retries, timeouts
3. **Operational gaps**: Insufficient monitoring, no chaos testing
4. **Scalability ceilings**: Database limits, synchronous calls

### Effective Scenario Patterns

- Always include **normal**, **stress**, and **failure** scenarios
- Quantify measures with **percentiles** (p50, p99) not averages
- Include **business context** in stimulus
- Make scenarios **testable** and **verifiable**
