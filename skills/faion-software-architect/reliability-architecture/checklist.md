# Reliability Architecture Checklist

Step-by-step checklist for designing reliable systems. Use this during architecture reviews, system design, and reliability audits.

---

## Phase 1: Requirements and SLO Definition

### 1.1 Business Requirements
- [ ] Identify critical business functions
- [ ] Document acceptable downtime (RTO)
- [ ] Document acceptable data loss (RPO)
- [ ] Determine peak traffic patterns and volumes
- [ ] Identify regulatory/compliance requirements
- [ ] Define user expectations for availability

### 1.2 SLI Selection
- [ ] Define availability SLI (successful requests / total requests)
- [ ] Define latency SLI (p50, p95, p99 percentiles)
- [ ] Define error rate SLI
- [ ] Define throughput SLI (if relevant)
- [ ] Define freshness SLI (for data pipelines)
- [ ] Ensure SLIs are measurable from user perspective

### 1.3 SLO Definition
- [ ] Set availability target (99.9%, 99.95%, 99.99%)
- [ ] Set latency targets for each percentile
- [ ] Set error rate threshold
- [ ] Define measurement window (rolling 30 days typical)
- [ ] Calculate error budget based on SLOs
- [ ] Document escalation thresholds (50% budget consumed, etc.)
- [ ] Get stakeholder sign-off on SLOs

### 1.4 Feature Criticality
- [ ] Create feature inventory
- [ ] Classify features by criticality (P0-P3)
- [ ] Define degradation behavior for each priority level
- [ ] Document dependencies between features
- [ ] Identify which features can be disabled under load

---

## Phase 2: Single Points of Failure (SPOF) Analysis

### 2.1 Infrastructure SPOFs
- [ ] Review compute layer (single instance? single zone?)
- [ ] Review network layer (single load balancer? single route?)
- [ ] Review storage layer (single database? single disk?)
- [ ] Review DNS configuration (single provider?)
- [ ] Review CDN configuration
- [ ] Document all identified SPOFs

### 2.2 Application SPOFs
- [ ] Review stateful components
- [ ] Review session management
- [ ] Review cache dependencies
- [ ] Review message queue dependencies
- [ ] Review external API dependencies
- [ ] Identify shared libraries/services that could fail

### 2.3 Data SPOFs
- [ ] Review database replication configuration
- [ ] Review backup locations
- [ ] Review data center distribution
- [ ] Identify data that exists in only one location
- [ ] Review encryption key management (key escrow?)

### 2.4 Operational SPOFs
- [ ] Review deployment pipeline redundancy
- [ ] Review monitoring system redundancy
- [ ] Review on-call coverage
- [ ] Review documentation availability
- [ ] Review credential/secret management
- [ ] Identify bus factor issues (single person knowledge)

---

## Phase 3: Redundancy Design

### 3.1 Compute Redundancy
- [ ] Deploy minimum 2 instances per service
- [ ] Distribute across availability zones
- [ ] Configure auto-scaling policies
- [ ] Set appropriate min/max instance counts
- [ ] Test auto-scaling behavior under load
- [ ] Document scale-up and scale-down times

### 3.2 Data Redundancy
- [ ] Configure database replication (sync/async)
- [ ] Set up read replicas if needed
- [ ] Configure automated backups
- [ ] Test backup restoration process
- [ ] Implement point-in-time recovery
- [ ] Document replication lag monitoring

### 3.3 Network Redundancy
- [ ] Configure multiple load balancers
- [ ] Set up health checks on load balancers
- [ ] Configure DNS failover
- [ ] Implement multi-CDN strategy (if critical)
- [ ] Document network topology

### 3.4 Geographic Redundancy
- [ ] Determine multi-region requirements
- [ ] Choose DR strategy (pilot light, warm standby, etc.)
- [ ] Configure data replication across regions
- [ ] Set up DNS-based routing (latency, geo, failover)
- [ ] Test cross-region failover
- [ ] Document RTO/RPO for regional failures

---

## Phase 4: Fault Tolerance Patterns

### 4.1 Circuit Breaker Implementation
- [ ] Identify all external dependencies
- [ ] Implement circuit breaker for each dependency
- [ ] Configure failure threshold (typically 5-10)
- [ ] Configure success threshold (typically 3-5)
- [ ] Configure timeout duration (typically 30-60s)
- [ ] Define fallback behavior when circuit is open
- [ ] Add circuit state to monitoring dashboard
- [ ] Test circuit breaker behavior under failure

### 4.2 Retry Configuration
- [ ] Identify retryable operations
- [ ] Implement exponential backoff
- [ ] Add jitter to prevent thundering herd
- [ ] Set maximum retry attempts (typically 3-5)
- [ ] Set maximum backoff cap (typically 30-60s)
- [ ] Ensure operations are idempotent OR retry is safe
- [ ] Log retry attempts for debugging
- [ ] Don't retry client errors (4xx except 429)

### 4.3 Timeout Configuration
- [ ] Set connection timeouts (3-5s typical)
- [ ] Set read timeouts (based on operation)
- [ ] Set request timeouts (end-to-end)
- [ ] Implement deadline propagation for distributed calls
- [ ] Calculate timeout budgets for call chains
- [ ] Document timeout values for each service
- [ ] Test behavior when timeouts occur

### 4.4 Bulkhead Implementation
- [ ] Identify services that need isolation
- [ ] Implement thread pool isolation OR semaphore isolation
- [ ] Size pools appropriately (not too small, not too large)
- [ ] Monitor pool utilization and rejection rates
- [ ] Test behavior when bulkhead limit is reached
- [ ] Define fallback for rejected requests

---

## Phase 5: Graceful Degradation

### 5.1 Degradation Strategy
- [ ] Document degradation behavior for each feature
- [ ] Implement feature flags for runtime control
- [ ] Create static fallbacks where appropriate
- [ ] Configure load shedding thresholds
- [ ] Define degradation trigger conditions
- [ ] Test degradation manually and automatically

### 5.2 Load Shedding
- [ ] Implement request prioritization
- [ ] Configure priority-based admission control
- [ ] Define thresholds for each priority level
- [ ] Implement queue depth limits
- [ ] Add metrics for shed/rejected requests
- [ ] Test load shedding under stress

### 5.3 Fallback Strategies
- [ ] Implement static fallbacks (cached data, defaults)
- [ ] Implement degraded responses (simplified data)
- [ ] Configure read-only mode capability
- [ ] Test fallback quality and user experience
- [ ] Document fallback behavior for support team

---

## Phase 6: Health Checks and Probes

### 6.1 Liveness Probe
- [ ] Create /health/live endpoint
- [ ] Keep check lightweight (no external deps)
- [ ] Configure initialDelaySeconds appropriately
- [ ] Set periodSeconds (typically 10-30s)
- [ ] Set timeoutSeconds (typically 1-5s)
- [ ] Set failureThreshold (typically 3)
- [ ] Test that deadlocks trigger liveness failure

### 6.2 Readiness Probe
- [ ] Create /health/ready endpoint
- [ ] Check database connectivity
- [ ] Check cache connectivity
- [ ] Check critical external dependencies
- [ ] Configure periodSeconds (typically 5-10s)
- [ ] Set successThreshold (2-3 for stability)
- [ ] Test that dependency failures trigger readiness failure

### 6.3 Startup Probe
- [ ] Create /health/startup endpoint (can be same as ready)
- [ ] Configure for slow-starting applications
- [ ] Set failureThreshold * periodSeconds > max startup time
- [ ] Test that startup probe prevents premature liveness checks

### 6.4 Health Endpoint Security
- [ ] Protect detailed health info (internal only)
- [ ] Don't expose sensitive data in health responses
- [ ] Rate limit health endpoints if public
- [ ] Consider authentication for detailed endpoints

---

## Phase 7: Disaster Recovery

### 7.1 Backup Configuration
- [ ] Configure automated database backups
- [ ] Set backup frequency based on RPO
- [ ] Configure backup retention period
- [ ] Encrypt backups at rest
- [ ] Store backups in different region
- [ ] Implement 3-2-1 backup rule
- [ ] Document backup schedule and locations

### 7.2 Recovery Procedures
- [ ] Document step-by-step recovery procedures
- [ ] Create runbooks for common failure scenarios
- [ ] Define roles and responsibilities during DR
- [ ] Document communication plan during incidents
- [ ] Test recovery procedures regularly

### 7.3 DR Testing
- [ ] Schedule regular backup restoration tests
- [ ] Perform monthly failover tests (single component)
- [ ] Conduct quarterly DR drills (multi-component)
- [ ] Execute annual full DR exercise
- [ ] Document test results and improvements
- [ ] Update runbooks based on test findings

### 7.4 DR Infrastructure
- [ ] Provision DR environment (pilot light/warm/hot)
- [ ] Configure automated failover (if hot standby)
- [ ] Set up monitoring in DR region
- [ ] Test network connectivity to DR site
- [ ] Document manual vs automatic failover triggers

---

## Phase 8: Chaos Engineering

### 8.1 Preparation
- [ ] Define steady state hypothesis (normal SLI values)
- [ ] Identify critical systems to test
- [ ] Set up observability for chaos experiments
- [ ] Define blast radius limits
- [ ] Get stakeholder approval for experiments
- [ ] Create rollback procedures

### 8.2 Experiment Design
- [ ] Start with simple experiments (instance termination)
- [ ] Progress to network failures (latency, partition)
- [ ] Test resource exhaustion (CPU, memory, disk)
- [ ] Design multi-fault scenarios for mature systems
- [ ] Document expected vs actual outcomes

### 8.3 Execution
- [ ] Run experiments during low-traffic periods initially
- [ ] Monitor SLIs during experiments
- [ ] Have rollback ready
- [ ] Document findings immediately
- [ ] Create follow-up tasks for issues found

### 8.4 Continuous Chaos
- [ ] Automate proven chaos experiments
- [ ] Integrate chaos into CI/CD pipeline
- [ ] Schedule regular chaos runs in production
- [ ] Build chaos dashboards
- [ ] Track improvements over time

---

## Phase 9: Monitoring and Alerting

### 9.1 SLO Monitoring
- [ ] Create SLO dashboard
- [ ] Track error budget consumption
- [ ] Set up error budget alerts (50%, 75%, 90%)
- [ ] Create burn rate alerts for rapid consumption
- [ ] Configure SLO violation alerts

### 9.2 Reliability Metrics
- [ ] Monitor circuit breaker state changes
- [ ] Track retry rates and success rates
- [ ] Monitor timeout rates
- [ ] Track bulkhead rejection rates
- [ ] Monitor health check failures
- [ ] Create reliability scorecard

### 9.3 Alert Configuration
- [ ] Define severity levels for alerts
- [ ] Configure appropriate thresholds (avoid alert fatigue)
- [ ] Set up escalation policies
- [ ] Create runbooks for each alert
- [ ] Test alert delivery to on-call

---

## Phase 10: Documentation and Operations

### 10.1 Architecture Documentation
- [ ] Document reliability architecture decisions (ADRs)
- [ ] Create architecture diagrams showing redundancy
- [ ] Document failure modes and mitigations
- [ ] Keep documentation in version control
- [ ] Review and update quarterly

### 10.2 Runbooks
- [ ] Create runbook for each critical failure scenario
- [ ] Include step-by-step recovery procedures
- [ ] Document escalation paths
- [ ] Include relevant dashboards and logs links
- [ ] Test runbooks during DR drills

### 10.3 On-Call
- [ ] Define on-call rotation schedule
- [ ] Document on-call responsibilities
- [ ] Create incident response procedures
- [ ] Configure appropriate alerting channels
- [ ] Conduct post-incident reviews (blameless)

### 10.4 Continuous Improvement
- [ ] Schedule regular reliability reviews
- [ ] Track reliability metrics over time
- [ ] Conduct post-incident reviews
- [ ] Prioritize reliability improvements
- [ ] Share learnings across teams

---

## Quick Reference: Common Configurations

### Typical SLO Targets

| Service Type | Availability | Latency (p99) | Error Rate |
|--------------|--------------|---------------|------------|
| API (critical) | 99.95% | <500ms | <0.1% |
| API (standard) | 99.9% | <1s | <0.5% |
| Web frontend | 99.9% | <2s | <1% |
| Background jobs | 99.5% | N/A | <1% |
| Data pipeline | 99.9% | <1hr freshness | <0.1% |

### Typical Timeout Values

| Timeout Type | Typical Value |
|--------------|---------------|
| Connection | 3-5 seconds |
| API call | 5-30 seconds |
| Database query | 5-10 seconds |
| File upload | 60-300 seconds |
| Background job | Based on SLA |

### Typical Retry Configuration

| Parameter | Value |
|-----------|-------|
| Max attempts | 3-5 |
| Base delay | 1 second |
| Max delay (cap) | 30-60 seconds |
| Backoff multiplier | 2 (exponential) |
| Jitter | 10-25% of delay |

### Typical Circuit Breaker Configuration

| Parameter | Value |
|-----------|-------|
| Failure threshold | 5-10 failures |
| Success threshold | 3-5 successes |
| Timeout (open state) | 30-60 seconds |
| Failure window | 10-60 seconds |

---

## Checklist Summary

| Phase | Items | Critical? |
|-------|-------|-----------|
| Requirements and SLO Definition | 26 | Yes |
| SPOF Analysis | 20 | Yes |
| Redundancy Design | 20 | Yes |
| Fault Tolerance Patterns | 32 | Yes |
| Graceful Degradation | 14 | Yes |
| Health Checks and Probes | 17 | Yes |
| Disaster Recovery | 18 | Yes |
| Chaos Engineering | 18 | Recommended |
| Monitoring and Alerting | 14 | Yes |
| Documentation and Operations | 18 | Yes |
| **Total** | **197** | - |

Use this checklist as a guide, not a rigid requirement. Prioritize based on your system's criticality and constraints.
