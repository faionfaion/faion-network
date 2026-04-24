# Event-Driven Architecture Checklist

Step-by-step checklist for designing and implementing event-driven systems.

---

## 1. Requirements Analysis

### Business Requirements

- [ ] Identify async communication needs
- [ ] Define consistency requirements (eventual vs strong)
- [ ] Determine audit/compliance requirements
- [ ] Identify replay/recovery requirements
- [ ] Define SLAs for event processing latency
- [ ] Understand peak load characteristics

### Technical Requirements

- [ ] Estimate event volume (events/second)
- [ ] Define event retention period
- [ ] Identify ordering requirements
- [ ] Determine delivery guarantee needs
- [ ] Assess existing infrastructure constraints

---

## 2. Pattern Selection

### Event-Driven vs Request-Response

| Factor | Favor Event-Driven | Favor Request-Response |
|--------|-------------------|----------------------|
| Coupling | Loose coupling needed | Tight integration ok |
| Latency | Eventual consistency ok | Immediate response needed |
| Scale | Independent scaling | Coupled scaling ok |
| Failures | Resilience critical | Simple error handling ok |

- [ ] Document pattern selection rationale
- [ ] Verify team familiarity with chosen patterns

### Event Sourcing Decision

- [ ] Is complete audit trail required?
- [ ] Is time-travel/replay valuable?
- [ ] Can team handle eventual consistency?
- [ ] Is the domain naturally event-based?
- [ ] Are there regulatory requirements for event history?

**Proceed with event sourcing only if 3+ answers are "yes"**

### CQRS Decision

- [ ] Different read/write scaling requirements?
- [ ] Complex read queries vs simple writes?
- [ ] Read/write ratio significantly unbalanced?
- [ ] Need different data models for reads?

### Saga Pattern Decision

- [ ] Distributed transaction across services?
- [ ] Need to maintain data consistency?
- [ ] Can define compensating actions?
- [ ] Acceptable eventual consistency?

**Saga Type Selection:**
| Criteria | Choreography | Orchestration |
|----------|--------------|---------------|
| Participants | 2-4 services | 5+ services |
| Complexity | Simple flow | Complex flow |
| Visibility | Decentralized ok | Central monitoring needed |
| Failure | No SPOF | Orchestrator backup needed |

---

## 3. Message Broker Selection

### Selection Criteria

| Requirement | Kafka | Pulsar | RabbitMQ | SQS |
|-------------|-------|--------|----------|-----|
| High throughput | Yes | Yes | Limited | Limited |
| Event replay | Yes | Yes | No | No |
| Complex routing | Limited | Yes | Yes | No |
| Multi-tenancy | Manual | Native | Manual | Native |
| Operations | Complex | Complex | Simple | None |
| AWS-native | No | No | No | Yes |

- [ ] Throughput requirements assessed
- [ ] Latency requirements assessed
- [ ] Replay requirements assessed
- [ ] Routing complexity assessed
- [ ] Operational capacity assessed
- [ ] Cloud provider alignment checked
- [ ] Cost estimated

### Broker Configuration

- [ ] Partitioning strategy defined (if applicable)
- [ ] Replication factor configured
- [ ] Retention policy configured
- [ ] Consumer group strategy defined
- [ ] Dead letter queue configured
- [ ] Monitoring and alerting setup

---

## 4. Event Schema Design

### CloudEvents Compliance

- [ ] Using CloudEvents format?
- [ ] Required attributes present:
  - [ ] `specversion`
  - [ ] `id`
  - [ ] `source`
  - [ ] `type`
- [ ] Optional attributes considered:
  - [ ] `time`
  - [ ] `datacontenttype`
  - [ ] `dataschema`
  - [ ] `subject`

### Event Structure

- [ ] Event naming follows past tense convention
- [ ] Type hierarchy defined (reverse domain notation)
- [ ] Correlation ID included
- [ ] Causation ID included (for event chains)
- [ ] Version field included
- [ ] Timestamp in ISO 8601 / RFC 3339 format
- [ ] Payload size reasonable (< 1MB recommended)

### Schema Management

- [ ] Schema registry selected (Confluent, AWS Glue, etc.)
- [ ] Compatibility mode defined (backward/forward/full)
- [ ] Schema versioning strategy documented
- [ ] Breaking change policy established
- [ ] Schema validation in CI/CD

---

## 5. Producer Implementation

### Event Publishing

- [ ] Events published asynchronously
- [ ] Retry logic with exponential backoff
- [ ] Circuit breaker for broker failures
- [ ] Correlation ID propagated from request
- [ ] Event timestamp set at creation
- [ ] Unique event ID generated

### Transactional Outbox Pattern

- [ ] Local transaction includes event storage
- [ ] Outbox table for pending events
- [ ] Background publisher for outbox
- [ ] Deduplication on consumer side
- [ ] Outbox cleanup strategy

```
Transaction:
1. Update domain state
2. Write event to outbox table
3. Commit transaction

Background:
4. Read from outbox
5. Publish to broker
6. Mark as published
```

### Producer Checklist

- [ ] Idempotent event creation
- [ ] Ordering key strategy (if needed)
- [ ] Batch publishing for efficiency
- [ ] Error handling and logging
- [ ] Metrics: publish rate, failures, latency

---

## 6. Consumer Implementation

### Event Processing

- [ ] Idempotent handler implementation
- [ ] Deduplication mechanism (event ID tracking)
- [ ] Out-of-order handling strategy
- [ ] Timeout and retry configuration
- [ ] Dead letter queue handling
- [ ] Graceful shutdown handling

### Idempotency Checklist

- [ ] Event ID stored on processing
- [ ] Duplicate check before processing
- [ ] Conditional database updates
- [ ] Idempotency window defined

### Consumer Group Strategy

- [ ] Consumer group naming convention
- [ ] Partition assignment strategy
- [ ] Rebalancing handling
- [ ] Offset commit strategy (manual vs auto)
- [ ] Consumer lag monitoring

### Error Handling

- [ ] Transient error retry (with backoff)
- [ ] Poison message detection
- [ ] Dead letter queue routing
- [ ] Alert on DLQ growth
- [ ] Manual intervention process

---

## 7. Saga Implementation

### Choreography Checklist

- [ ] Events trigger next step
- [ ] Compensating events defined
- [ ] Saga state tracked per participant
- [ ] Timeout handling for steps
- [ ] Distributed tracing enabled

### Orchestration Checklist

- [ ] Orchestrator service defined
- [ ] State machine for saga steps
- [ ] Retry policy per step
- [ ] Compensation logic per step
- [ ] Saga timeout handling
- [ ] Orchestrator HA/failover

### Compensation Design

| Step | Forward Action | Compensation |
|------|---------------|--------------|
| 1 | Create order | Cancel order |
| 2 | Reserve inventory | Release inventory |
| 3 | Charge payment | Refund payment |
| 4 | Ship order | Cancel shipment |

- [ ] All steps have compensations
- [ ] Compensations are idempotent
- [ ] Partial compensation handled
- [ ] Compensation order defined (usually reverse)

---

## 8. Observability

### Logging

- [ ] Structured logging (JSON)
- [ ] Event ID in all log entries
- [ ] Correlation ID in all log entries
- [ ] Log levels appropriate
- [ ] Sensitive data masked

### Metrics

- [ ] Publish rate (events/sec)
- [ ] Consume rate (events/sec)
- [ ] Consumer lag
- [ ] Processing latency (p50, p95, p99)
- [ ] Error rate
- [ ] Dead letter queue depth
- [ ] Retry count

### Tracing

- [ ] Distributed tracing enabled (Jaeger, Zipkin, etc.)
- [ ] Trace context propagated in events
- [ ] Span per event processing
- [ ] Parent-child relationships tracked

### Alerting

- [ ] Consumer lag threshold
- [ ] DLQ growth rate
- [ ] Processing error rate
- [ ] Broker connectivity
- [ ] Partition imbalance

---

## 9. Testing

### Unit Testing

- [ ] Event serialization/deserialization
- [ ] Handler logic (mocked dependencies)
- [ ] Idempotency logic
- [ ] Compensation logic

### Integration Testing

- [ ] Event publish to real/test broker
- [ ] Event consumption from broker
- [ ] End-to-end event flow
- [ ] Saga completion scenarios

### Chaos Testing

- [ ] Broker unavailability
- [ ] Consumer crash during processing
- [ ] Network partition
- [ ] Out-of-order delivery
- [ ] Duplicate delivery

### Contract Testing

- [ ] Producer-consumer contract defined
- [ ] Schema compatibility verified
- [ ] Breaking change detection

---

## 10. Operations

### Deployment

- [ ] Rolling deployment strategy
- [ ] Consumer drain before shutdown
- [ ] Blue-green deployment support
- [ ] Feature flags for new event types

### Data Management

- [ ] Retention policy implemented
- [ ] Compaction strategy (if applicable)
- [ ] Archive strategy for old events
- [ ] GDPR/data deletion handling

### Disaster Recovery

- [ ] Broker cluster redundancy
- [ ] Cross-region replication (if needed)
- [ ] Consumer state backup
- [ ] Event replay procedures documented
- [ ] Recovery runbooks

### Documentation

- [ ] Event catalog maintained
- [ ] Producer/consumer ownership documented
- [ ] Schema registry documented
- [ ] Runbooks for common issues
- [ ] Architecture decision records (ADRs)

---

## Quick Reference: Decision Matrix

### When to Use Event-Driven Architecture

| Scenario | Recommendation |
|----------|----------------|
| Microservices communication | Strongly recommended |
| Audit requirements | Event sourcing |
| High read/write ratio | CQRS |
| Distributed transactions | Saga pattern |
| Simple CRUD | Likely overkill |
| Strong consistency required | Consider alternatives |

### Broker Quick Selection

```
High throughput + replay needed → Kafka
Multi-tenant + streaming/queuing → Pulsar
Complex routing + low latency → RabbitMQ
AWS serverless + simple queue → SQS
Lightweight + cloud-native → NATS
```

---

## Checklist Summary

| Phase | Items |
|-------|-------|
| Requirements | 11 items |
| Pattern Selection | 15 items |
| Broker Selection | 13 items |
| Schema Design | 16 items |
| Producer | 15 items |
| Consumer | 18 items |
| Saga | 14 items |
| Observability | 18 items |
| Testing | 12 items |
| Operations | 14 items |
| **Total** | **146 items** |
