# Quality Attributes Checklist

Comprehensive step-by-step checklist for defining, analyzing, and validating quality attributes.

---

## Phase 1: Discovery and Elicitation

### 1.1 Stakeholder Identification

- [ ] Identify all stakeholder groups (users, operators, developers, business)
- [ ] Document stakeholder quality concerns
- [ ] Prioritize stakeholders by influence and interest
- [ ] Schedule quality attribute workshops

### 1.2 Business Driver Analysis

- [ ] Document primary business goals
- [ ] Identify revenue-critical features
- [ ] Understand regulatory/compliance requirements
- [ ] Capture competitive differentiation needs
- [ ] Define acceptable risk levels

### 1.3 Context Understanding

- [ ] Document expected user base size
- [ ] Identify peak usage patterns
- [ ] Understand geographic distribution
- [ ] Analyze existing system constraints
- [ ] Identify integration requirements

---

## Phase 2: Quality Attribute Prioritization

### 2.1 Utility Tree Construction

- [ ] List all relevant quality attributes
- [ ] Create hierarchy (attribute -> sub-attribute -> scenarios)
- [ ] Rate importance (H/M/L) for each scenario
- [ ] Rate difficulty (H/M/L) for each scenario
- [ ] Identify (H,H) scenarios as highest priority

### 2.2 Trade-off Identification

- [ ] Document known trade-offs between attributes
- [ ] Identify sensitivity points (single attribute impact)
- [ ] Identify trade-off points (multiple attribute impact)
- [ ] Get stakeholder consensus on trade-off decisions
- [ ] Document rationale for trade-off decisions

### 2.3 Priority Matrix

Use this matrix to prioritize quality attributes:

| Attribute | Business Impact | Technical Risk | Priority |
|-----------|-----------------|----------------|----------|
| Performance | H/M/L | H/M/L | |
| Scalability | H/M/L | H/M/L | |
| Availability | H/M/L | H/M/L | |
| Security | H/M/L | H/M/L | |
| Maintainability | H/M/L | H/M/L | |
| Testability | H/M/L | H/M/L | |
| Observability | H/M/L | H/M/L | |
| Cost | H/M/L | H/M/L | |

---

## Phase 3: Performance Requirements

### 3.1 Latency Requirements

- [ ] Define p50 latency target (median)
- [ ] Define p95 latency target (tail)
- [ ] Define p99 latency target (worst case)
- [ ] Specify latency per operation type
- [ ] Document latency under normal load
- [ ] Document latency under peak load
- [ ] Define Time to First Byte (TTFB) targets

### 3.2 Throughput Requirements

- [ ] Define requests per second (RPS) targets
- [ ] Specify concurrent user capacity
- [ ] Document transactions per second (TPS)
- [ ] Define data processing volume/time
- [ ] Specify batch processing requirements

### 3.3 Resource Utilization

- [ ] Define CPU utilization limits
- [ ] Specify memory usage limits
- [ ] Document storage I/O requirements
- [ ] Define network bandwidth needs
- [ ] Set cost per request/user targets

### 3.4 Performance Tactics Checklist

- [ ] Caching strategy defined (browser, CDN, application, database)
- [ ] Database indexing reviewed
- [ ] Query optimization performed
- [ ] Connection pooling configured
- [ ] Async processing for heavy operations
- [ ] Compression enabled (gzip/brotli)
- [ ] Static assets on CDN
- [ ] Database read replicas considered

---

## Phase 4: Scalability Requirements

### 4.1 Load Projections

- [ ] Current load documented
- [ ] 6-month growth projection
- [ ] 1-year growth projection
- [ ] Peak vs average load ratio defined
- [ ] Seasonal patterns identified

### 4.2 Scaling Strategy

- [ ] Vertical scaling limits defined
- [ ] Horizontal scaling approach selected
- [ ] Auto-scaling triggers defined
- [ ] Scaling response time requirements
- [ ] Maximum scale limits set

### 4.3 Scalability Tactics Checklist

- [ ] Stateless service design
- [ ] Load balancing strategy selected
- [ ] Database sharding plan (if needed)
- [ ] Message queue integration
- [ ] Microservices decomposition considered
- [ ] Event-driven architecture evaluated
- [ ] Data partitioning strategy defined

---

## Phase 5: Availability Requirements

### 5.1 Uptime Targets

- [ ] SLA percentage defined (99%, 99.9%, 99.99%)
- [ ] Planned maintenance windows documented
- [ ] Maximum single outage duration defined
- [ ] Monthly downtime budget calculated
- [ ] Business hours vs 24/7 requirements

### 5.2 Failure Scenarios

- [ ] Single component failure handling
- [ ] Data center failure handling
- [ ] Network partition handling
- [ ] Dependent service failure handling
- [ ] Data corruption recovery

### 5.3 Recovery Requirements

- [ ] Recovery Time Objective (RTO) defined
- [ ] Recovery Point Objective (RPO) defined
- [ ] Backup frequency specified
- [ ] Backup retention policy defined
- [ ] DR site requirements

### 5.4 Availability Tactics Checklist

- [ ] Multi-AZ deployment configured
- [ ] Multi-region considered (if needed)
- [ ] Load balancer health checks
- [ ] Database replication setup
- [ ] Circuit breakers implemented
- [ ] Retry with exponential backoff
- [ ] Graceful degradation strategies
- [ ] Failover automation
- [ ] Auto-healing mechanisms

---

## Phase 6: Reliability Requirements

### 6.1 Fault Tolerance

- [ ] MTBF target defined
- [ ] MTTR target defined
- [ ] Acceptable failure rate specified
- [ ] Failure detection mechanisms
- [ ] Automatic recovery procedures

### 6.2 Data Integrity

- [ ] Transaction consistency requirements
- [ ] Data validation rules
- [ ] Corruption detection mechanisms
- [ ] Data reconciliation procedures

### 6.3 Reliability Tactics Checklist

- [ ] Heartbeat monitoring configured
- [ ] Exception detection and handling
- [ ] Voting mechanisms (if distributed)
- [ ] Active redundancy configured
- [ ] Passive redundancy configured
- [ ] Rollback mechanisms tested
- [ ] State checkpoint procedures
- [ ] Process monitoring active

---

## Phase 7: Security Requirements

### 7.1 Authentication

- [ ] Authentication method selected (OAuth2, OIDC, SAML)
- [ ] Multi-factor authentication requirements
- [ ] Session management policy
- [ ] Password policy defined
- [ ] API authentication (API keys, JWT)

### 7.2 Authorization

- [ ] Authorization model selected (RBAC, ABAC)
- [ ] Role definitions documented
- [ ] Permission matrix created
- [ ] Least privilege principle applied
- [ ] Privilege escalation prevention

### 7.3 Data Protection

- [ ] Encryption at rest requirements
- [ ] Encryption in transit requirements
- [ ] Key management strategy
- [ ] Data classification completed
- [ ] PII handling procedures

### 7.4 Compliance

- [ ] Regulatory requirements identified (GDPR, HIPAA, PCI-DSS, SOC2)
- [ ] Audit logging requirements
- [ ] Data retention policies
- [ ] Right to deletion requirements
- [ ] Compliance certification needs

### 7.5 Security Tactics Checklist

- [ ] Input validation on all endpoints
- [ ] Output encoding implemented
- [ ] Rate limiting configured
- [ ] WAF deployed
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] CORS policy defined
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Secrets management (Vault, AWS Secrets Manager)
- [ ] Network segmentation
- [ ] Zero trust architecture considered
- [ ] Threat modeling completed (STRIDE)
- [ ] Penetration testing scheduled

---

## Phase 8: Maintainability Requirements

### 8.1 Code Quality

- [ ] Coding standards defined
- [ ] Code review process established
- [ ] Static analysis tools configured
- [ ] Code complexity limits set
- [ ] Technical debt tracking

### 8.2 Modifiability

- [ ] Change deployment frequency target
- [ ] Change failure rate target
- [ ] Time to implement feature estimates
- [ ] Backward compatibility requirements
- [ ] API versioning strategy

### 8.3 Documentation

- [ ] Architecture documentation requirements
- [ ] API documentation standards
- [ ] Runbook requirements
- [ ] Code documentation standards
- [ ] Change log maintenance

### 8.4 Maintainability Tactics Checklist

- [ ] Clear module boundaries (bounded contexts)
- [ ] Design patterns applied (SOLID)
- [ ] Dependency injection used
- [ ] Feature flags implemented
- [ ] Blue-green deployment capability
- [ ] Rollback procedures tested
- [ ] Configuration externalized
- [ ] Database migration strategy

---

## Phase 9: Testability Requirements

### 9.1 Test Coverage

- [ ] Unit test coverage target (e.g., 80%)
- [ ] Integration test coverage target
- [ ] E2E test coverage for critical paths
- [ ] Performance test coverage
- [ ] Security test coverage

### 9.2 Test Environment

- [ ] Test environment parity with production
- [ ] Test data management strategy
- [ ] Test isolation requirements
- [ ] Parallel test execution capability

### 9.3 Testability Tactics Checklist

- [ ] Dependency injection for mocking
- [ ] Interface segregation for stubs
- [ ] Deterministic operations (no random/time)
- [ ] Observable state for assertions
- [ ] Contract testing for APIs
- [ ] Test doubles strategy (mocks, fakes, stubs)
- [ ] Test data factories
- [ ] CI/CD test integration

---

## Phase 10: Observability Requirements

### 10.1 Logging

- [ ] Log levels defined (DEBUG, INFO, WARN, ERROR)
- [ ] Structured logging format (JSON)
- [ ] Log retention policy
- [ ] Sensitive data masking
- [ ] Centralized log aggregation

### 10.2 Metrics

- [ ] RED metrics (Rate, Errors, Duration)
- [ ] USE metrics (Utilization, Saturation, Errors)
- [ ] Business metrics defined
- [ ] Custom application metrics
- [ ] Metric retention period

### 10.3 Tracing

- [ ] Distributed tracing enabled
- [ ] Trace sampling strategy
- [ ] Trace correlation with logs
- [ ] External service tracing
- [ ] Database query tracing

### 10.4 Alerting

- [ ] Alert severity levels defined
- [ ] Alert routing rules
- [ ] On-call procedures
- [ ] Escalation policy
- [ ] Alert fatigue prevention

### 10.5 Observability Tactics Checklist

- [ ] Structured logging implemented
- [ ] OpenTelemetry integration
- [ ] Health check endpoints (/health, /ready)
- [ ] SLI dashboards created
- [ ] SLO alerts configured
- [ ] Error budget tracking
- [ ] Runbooks for common alerts
- [ ] Incident response procedures

---

## Phase 11: Cost Requirements

### 11.1 Budget Constraints

- [ ] Monthly infrastructure budget
- [ ] Cost per user/request target
- [ ] Cost optimization priorities
- [ ] Reserved vs on-demand strategy

### 11.2 Cost Tactics Checklist

- [ ] Right-sizing instances
- [ ] Spot/preemptible instances considered
- [ ] Reserved instance commitments
- [ ] Auto-scaling to reduce idle resources
- [ ] Storage tiering (hot/warm/cold)
- [ ] Data transfer optimization
- [ ] Caching to reduce compute
- [ ] Serverless for variable loads

---

## Phase 12: Validation and Documentation

### 12.1 Quality Attribute Validation

- [ ] All quality attribute scenarios documented
- [ ] Each scenario has measurable response
- [ ] Scenarios reviewed by stakeholders
- [ ] Trade-offs documented and approved
- [ ] Architectural decisions recorded (ADRs)

### 12.2 Testing Validation

- [ ] Performance tests created for latency targets
- [ ] Load tests created for throughput targets
- [ ] Chaos engineering tests for availability
- [ ] Security tests for vulnerabilities
- [ ] Compliance audits scheduled

### 12.3 Monitoring Validation

- [ ] SLIs mapped to quality attributes
- [ ] SLOs defined for each SLI
- [ ] Dashboards created
- [ ] Alerts configured
- [ ] Error budgets established

### 12.4 Documentation Checklist

- [ ] Quality attribute specification document
- [ ] Trade-off analysis document
- [ ] Architecture Decision Records (ADRs)
- [ ] SLO documentation
- [ ] Runbooks for operations

---

## Quick Reference: Quality Attribute Questions

Use these questions during stakeholder interviews:

| Attribute | Key Questions |
|-----------|---------------|
| **Performance** | What response time is acceptable? What's peak load? |
| **Scalability** | How much growth expected? What's the scaling strategy? |
| **Availability** | What's acceptable downtime? What hours matter most? |
| **Reliability** | What happens if X fails? How fast must we recover? |
| **Security** | What data is sensitive? Who needs access? Compliance? |
| **Maintainability** | How often do we release? How complex are changes? |
| **Testability** | What's critical to test? What coverage is needed? |
| **Observability** | How do we know it's working? What alerts matter? |
| **Cost** | What's the budget? What's cost per user target? |

---

*Part of [quality-attributes](README.md) | [faion-software-architect](../CLAUDE.md)*
