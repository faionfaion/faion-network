# Quality Attributes Framework

## Overview

Quality attributes (also called non-functional requirements or "-ilities") are measurable properties that define how well a system performs its functions. They determine whether a system will succeed or fail regardless of functional correctness.

**Key principle:** A system that meets all functional requirements but fails quality attributes (performance, security, scalability) will inevitably fail in production.

## ISO/IEC 25010 Quality Model

The [ISO/IEC 25010](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) standard provides a comprehensive framework for software quality evaluation with two dimensions.

### Product Quality Model (9 Characteristics)

| Characteristic | Sub-characteristics | Key Question |
|----------------|---------------------|--------------|
| **Functional Suitability** | Completeness, Correctness, Appropriateness | Does it do what users need? |
| **Performance Efficiency** | Time behavior, Resource utilization, Capacity | How fast and efficient? |
| **Compatibility** | Co-existence, Interoperability | Works with other systems? |
| **Usability** | Learnability, Operability, User error protection | Easy to use? |
| **Reliability** | Maturity, Availability, Fault tolerance, Recoverability | Can we depend on it? |
| **Security** | Confidentiality, Integrity, Non-repudiation, Accountability, Authenticity | Is it protected? |
| **Maintainability** | Modularity, Reusability, Analyzability, Modifiability, Testability | Easy to change? |
| **Portability** | Adaptability, Installability, Replaceability | Runs elsewhere? |
| **Safety** | Operational constraint, Risk identification, Fail safe, Hazard warning | Prevents harm? |

### Quality in Use Model (5 Characteristics)

| Characteristic | Description |
|----------------|-------------|
| **Effectiveness** | Accuracy and completeness with which users achieve goals |
| **Efficiency** | Resources expended in relation to effectiveness |
| **Satisfaction** | User attitudes toward use of the system |
| **Freedom from Risk** | Economic, health/safety, environmental risk mitigation |
| **Context Coverage** | Effectiveness across different contexts of use |

## Core Quality Attributes for Architecture

### Performance

**Definition:** Response time, throughput, and resource utilization under load.

| Metric | Description | Target Examples |
|--------|-------------|-----------------|
| Latency (p50) | Median response time | < 100ms |
| Latency (p95) | 95th percentile | < 300ms |
| Latency (p99) | 99th percentile | < 1s |
| Throughput | Requests per second | > 10,000 RPS |
| TTFB | Time to first byte | < 200ms |

**Architectural Tactics:**
- Caching (Redis, CDN, browser)
- Connection pooling
- Async processing
- Query optimization
- Compression (gzip, brotli)
- Database indexing
- Read replicas

### Scalability

**Definition:** Ability to handle increased load by adding resources.

| Type | Description | When to Use |
|------|-------------|-------------|
| **Vertical** | Add CPU/RAM to existing machines | Simple, limited ceiling |
| **Horizontal** | Add more machines | Complex, unlimited ceiling |
| **Elastic** | Auto-scale based on demand | Cloud-native, cost-optimal |

**Architectural Tactics:**
- Stateless services
- Load balancing
- Database sharding
- Event-driven architecture
- Microservices decomposition
- Message queues (Kafka, RabbitMQ)

### Availability

**Definition:** System uptime and ability to serve requests.

| SLA Level | Downtime/Year | Downtime/Month | Use Case |
|-----------|---------------|----------------|----------|
| 99% | 3.65 days | 7.2 hours | Development |
| 99.9% | 8.76 hours | 43.8 minutes | Standard production |
| 99.95% | 4.38 hours | 21.9 minutes | Business critical |
| 99.99% | 52.56 minutes | 4.32 minutes | High availability |
| 99.999% | 5.26 minutes | 25.9 seconds | Mission critical |

**Architectural Tactics:**
- Redundancy (multi-AZ, multi-region)
- Load balancer health checks
- Database replication
- Circuit breakers
- Graceful degradation
- Failover mechanisms
- Auto-healing

### Reliability

**Definition:** System's ability to perform under stated conditions for a specified period.

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **MTBF** | Mean Time Between Failures | Total uptime / Number of failures |
| **MTTR** | Mean Time To Recovery | Total downtime / Number of failures |
| **MTTF** | Mean Time To Failure | Total operational time / Number of failures |
| **Failure Rate** | Failures per time unit | 1 / MTBF |

**Architectural Tactics:**
- Fault detection (heartbeat, voting, exception detection)
- Fault recovery (redundancy, rollback, retry with backoff)
- Fault prevention (removal from service, transactions, process monitor)

### Security

**Definition:** Protection against unauthorized access, data breaches, and attacks.

| Attribute | Description |
|-----------|-------------|
| **Confidentiality** | Data accessible only to authorized parties |
| **Integrity** | Data not modified by unauthorized parties |
| **Availability** | System accessible to authorized users |
| **Authentication** | Verify identity of users/systems |
| **Authorization** | Grant permissions to verified users |
| **Non-repudiation** | Actions cannot be denied |
| **Accountability** | Actions traceable to actors |

**Architectural Tactics:**
- Defense in depth
- Zero trust architecture
- Encryption (at rest, in transit)
- Authentication (OAuth2, JWT, MFA)
- Authorization (RBAC, ABAC)
- Input validation
- Rate limiting
- WAF (Web Application Firewall)
- Security headers (CSP, HSTS)

### Maintainability

**Definition:** Ease of modifying, fixing, and enhancing the system.

| Sub-attribute | Description | Metrics |
|---------------|-------------|---------|
| **Modularity** | Degree of discrete components | Coupling, cohesion |
| **Reusability** | Components usable in other systems | Shared libraries count |
| **Analyzability** | Ease of diagnosing issues | Code complexity |
| **Modifiability** | Ease of making changes | Change failure rate |
| **Testability** | Ease of testing | Code coverage |

**Architectural Tactics:**
- Clear module boundaries
- Design patterns (SOLID)
- API versioning
- Feature flags
- Comprehensive testing
- Documentation
- CI/CD pipelines

### Testability

**Definition:** Degree to which a system supports testing.

| Level | Scope | Tools |
|-------|-------|-------|
| Unit | Single function/method | pytest, Jest |
| Integration | Component interactions | pytest, Supertest |
| E2E | Full user flows | Playwright, Cypress |
| Performance | Load/stress | k6, Locust |
| Security | Vulnerabilities | OWASP ZAP, Burp |

**Architectural Tactics:**
- Dependency injection
- Interface segregation
- Test doubles (mocks, stubs)
- Observable state
- Separate concerns
- Contract testing

### Observability

**Definition:** Ability to understand internal state from external outputs.

| Pillar | Description | Tools |
|--------|-------------|-------|
| **Logs** | Event records | ELK, Loki, CloudWatch |
| **Metrics** | Numerical measurements | Prometheus, Datadog |
| **Traces** | Request flow tracking | Jaeger, Tempo |

**Architectural Tactics:**
- Structured logging (JSON)
- Distributed tracing
- Custom metrics
- Health endpoints
- SLI/SLO monitoring
- Alerting rules
- Dashboards

## Quality Attribute Trade-offs

Quality attributes often conflict. Improving one may degrade another.

### Common Trade-offs

| Trade-off | Description | Example |
|-----------|-------------|---------|
| Performance vs Security | Security checks add latency | Encryption overhead |
| Performance vs Cost | Better performance requires more resources | Larger instances |
| Scalability vs Simplicity | Distributed systems are complex | Microservices overhead |
| Consistency vs Availability | CAP theorem | Database replication lag |
| Security vs Usability | More security = more friction | MFA vs UX |
| Flexibility vs Performance | Abstraction has overhead | ORM vs raw SQL |

### Trade-off Analysis

Use the [Architecture Tradeoff Analysis Method (ATAM)](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) to:

1. Identify business drivers
2. Create quality attribute utility tree
3. Analyze architectural approaches
4. Identify sensitivity points (affect single attribute)
5. Identify trade-off points (affect multiple attributes)
6. Prioritize scenarios
7. Document decisions as ADRs

## SLI/SLO/SLA Framework

### Definitions

| Term | Definition | Owner |
|------|------------|-------|
| **SLI** (Service Level Indicator) | Metric you measure | Engineering |
| **SLO** (Service Level Objective) | Target for SLI | Product/Engineering |
| **SLA** (Service Level Agreement) | Contract with penalties | Business/Legal |

### Relationship

```
SLI (measure) --> SLO (target) --> SLA (contract)

Example:
- SLI: 99.2% of requests < 200ms
- SLO: 99.5% of requests < 200ms (internal target)
- SLA: 99.0% of requests < 200ms (contractual minimum)
```

### Error Budget

```
Error Budget = 100% - SLO Target

Example: 99.9% SLO = 0.1% error budget
- Monthly: 43.8 minutes downtime allowed
- When exhausted: focus on reliability over features
```

### Common SLIs by Service Type

| Service Type | SLIs |
|--------------|------|
| **Request-driven** | Availability, Latency, Throughput |
| **Pipeline** | Freshness, Correctness, Coverage |
| **Storage** | Durability, Throughput, Latency |

## LLM Usage Tips

### When to Use This Framework

1. **System design** - Define quality requirements upfront
2. **Architecture review** - Evaluate existing systems
3. **Trade-off decisions** - Make informed compromises
4. **NFR documentation** - Specify measurable requirements
5. **SLO definition** - Set reliability targets

### Effective Prompting Strategies

1. **Be specific about context** - Include system type, scale, constraints
2. **Request measurable targets** - Ask for specific numbers, not vague descriptions
3. **Ask for trade-offs** - Quality attributes compete; understand the costs
4. **Request tactics** - Ask for specific architectural decisions
5. **Include scenarios** - Use the 6-part quality attribute scenario format

### Quality Attribute Scenario Format

Every quality requirement should follow this structure:

```
Source: Who/what generates the stimulus (user, external system, attacker)
Stimulus: The event or condition (request, attack, failure)
Environment: System state (normal, peak load, degraded)
Artifact: Component being stimulated (API, database, service)
Response: What happens (process, reject, log)
Response Measure: How to verify (latency < 200ms, 99.9% success)
```

## Files in This Folder

| File | Purpose |
|------|---------|
| [README.md](README.md) | This overview and LLM tips |
| [checklist.md](checklist.md) | Step-by-step quality requirements checklist |
| [examples.md](examples.md) | Real quality attribute implementations |
| [templates.md](templates.md) | Copy-paste quality requirement templates |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted quality analysis |

## External References

### Standards and Frameworks

- [ISO/IEC 25010:2023](https://iso25000.com/index.php/en/iso-25000-standards/iso-25010) - Software product quality model
- [SEI Quality Attribute Resources](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/) - CMU/SEI research
- [ATAM](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) - Architecture Tradeoff Analysis Method
- [arc42 Quality Model](https://quality.arc42.org/standards/iso-25010) - Practical quality attributes

### SRE and Operations

- [Google SRE Book](https://sre.google/sre-book/service-level-objectives/) - SLO best practices
- [Azure Well-Architected](https://learn.microsoft.com/en-us/azure/well-architected/reliability/metrics) - Reliability metrics
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/) - Quality pillars

### Best Practices

- [Perforce NFR Guide](https://www.perforce.com/blog/alm/what-are-non-functional-requirements-examples) - NFR documentation
- [Codacy ISO 25010 Guide](https://blog.codacy.com/iso-25010-software-quality-model) - Quality model exploration
- [InformIT Quality Attributes](https://www.informit.com/articles/article.aspx?p=1959673&seqNum=5) - Architectural tactics

---

*Part of [faion-software-architect](../CLAUDE.md) skill | 605+ methodologies*
