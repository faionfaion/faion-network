# Distributed Patterns Implementation Checklist

Step-by-step checklist for implementing distributed system patterns. Use as a guide during architecture design and code review.

---

## Phase 1: Requirements Analysis

### 1.1 Consistency Requirements

- [ ] Define consistency model needed
  - [ ] Strong consistency (ACID, 2PC)
  - [ ] Eventual consistency (Saga, CQRS)
  - [ ] Causal consistency
- [ ] Identify critical vs non-critical transactions
- [ ] Document acceptable inconsistency window (if eventual)
- [ ] Identify read/write ratio
- [ ] Document latency requirements (p50, p95, p99)

### 1.2 Availability Requirements

- [ ] Define SLA target (99.9%, 99.99%)
- [ ] Identify single points of failure
- [ ] Plan for partial degradation scenarios
- [ ] Document failover requirements
- [ ] Define Recovery Time Objective (RTO)
- [ ] Define Recovery Point Objective (RPO)

### 1.3 Scale Requirements

- [ ] Estimate transaction volume (TPS)
- [ ] Identify burst patterns
- [ ] Plan for 10x growth
- [ ] Document data volume expectations
- [ ] Identify hot spots and bottlenecks

---

## Phase 2: Pattern Selection

### 2.1 Transaction Pattern Selection

```
Decision Tree:

Q1: Do you need strong consistency across all services?
    YES -> Consider 2PC (if supported) or TCC
    NO -> Continue to Q2

Q2: Is the transaction long-running (>few seconds)?
    YES -> Use Saga pattern
    NO -> Continue to Q3

Q3: Do you need to reserve resources?
    YES -> Consider TCC (Try-Confirm-Cancel)
    NO -> Continue to Q4

Q4: How many services involved?
    2-3 services -> Choreography Saga
    4+ services -> Orchestration Saga

Q5: Is full visibility and debugging critical?
    YES -> Orchestration Saga
    NO -> Choreography acceptable
```

- [ ] Document pattern selection with rationale
- [ ] Create ADR for transaction approach
- [ ] Identify all participating services
- [ ] Map transaction boundaries

### 2.2 Data Pattern Selection

- [ ] **CQRS Consideration:**
  - [ ] Read/write ratio > 10:1?
  - [ ] Complex read queries needed?
  - [ ] Different read projections needed?
  - [ ] Independent scaling required?

- [ ] **Event Sourcing Consideration:**
  - [ ] Audit trail required?
  - [ ] Temporal queries needed?
  - [ ] Event replay for debugging useful?
  - [ ] Complex state derivation?

- [ ] **Outbox Pattern Consideration:**
  - [ ] Publishing events after DB writes?
  - [ ] Need atomic DB + message operations?
  - [ ] Cannot use distributed transactions?

### 2.3 Resilience Pattern Selection

- [ ] **Circuit Breaker needed if:**
  - [ ] Calling external/unreliable services
  - [ ] Cascading failures possible
  - [ ] Fast failure preferred over timeout

- [ ] **Bulkhead needed if:**
  - [ ] Multiple independent dependencies
  - [ ] Resource exhaustion concerns
  - [ ] Noisy neighbor isolation needed

- [ ] **Retry needed if:**
  - [ ] Transient failures expected
  - [ ] Operations are idempotent (or can be made so)
  - [ ] Network glitches possible

---

## Phase 3: Saga Implementation

### 3.1 Saga Design

- [ ] List all saga steps in order
- [ ] For each step:
  - [ ] Define the forward action
  - [ ] Define the compensating action
  - [ ] Identify idempotency requirements
  - [ ] Define timeout for the step
- [ ] Design correlation ID strategy
- [ ] Plan for partial compensation scenarios

### 3.2 Choreography Saga Checklist

- [ ] Define events for each state transition
- [ ] Design event schema with versioning
- [ ] Implement event handlers in each service
- [ ] Add correlation ID to all events
- [ ] Implement compensation event handlers
- [ ] Add dead letter queue handling
- [ ] Test out-of-order event handling
- [ ] Implement saga timeout/expiration
- [ ] Add observability (tracing, metrics)

### 3.3 Orchestration Saga Checklist

- [ ] Design saga orchestrator service
- [ ] Implement saga state machine
- [ ] Define step execution order
- [ ] Implement compensation flow
- [ ] Handle orchestrator failures
  - [ ] Persist saga state
  - [ ] Recovery on restart
- [ ] Add saga timeout handling
- [ ] Implement retry logic per step
- [ ] Add observability (tracing, metrics)
- [ ] Consider using Temporal/Camunda/Step Functions

### 3.4 Saga Testing

- [ ] Test happy path end-to-end
- [ ] Test failure at each step
- [ ] Test compensation execution
- [ ] Test concurrent saga instances
- [ ] Test idempotency of steps
- [ ] Test timeout scenarios
- [ ] Load test under expected volume

---

## Phase 4: CQRS/Event Sourcing Implementation

### 4.1 CQRS Implementation

- [ ] Design command model
  - [ ] Command validation logic
  - [ ] Domain invariants
  - [ ] Write-optimized storage
- [ ] Design query model(s)
  - [ ] Read-optimized projections
  - [ ] Denormalized views
  - [ ] Caching strategy
- [ ] Design event schema
  - [ ] Event versioning strategy
  - [ ] Schema evolution plan
- [ ] Implement projection updates
  - [ ] Synchronous vs asynchronous
  - [ ] Handle projection rebuild
- [ ] Plan for eventual consistency handling

### 4.2 Event Sourcing Implementation

- [ ] Choose event store (EventStoreDB, Kafka, custom)
- [ ] Design event schema
  - [ ] Event naming convention
  - [ ] Payload structure
  - [ ] Metadata (timestamp, version, correlation)
- [ ] Implement aggregate root
  - [ ] Load from events
  - [ ] Apply events
  - [ ] Emit new events
- [ ] Implement snapshotting (if needed)
  - [ ] Snapshot frequency
  - [ ] Snapshot storage
- [ ] Plan event schema evolution
  - [ ] Upcasters for old events
  - [ ] Versioning strategy
- [ ] Implement read projections
- [ ] Plan for projection rebuild

### 4.3 CQRS/ES Testing

- [ ] Test command validation
- [ ] Test event generation
- [ ] Test projection updates
- [ ] Test event replay
- [ ] Test schema evolution
- [ ] Test concurrent modifications
- [ ] Performance test event store

---

## Phase 5: Outbox Pattern Implementation

### 5.1 Outbox Design

- [ ] Design outbox table schema
  ```sql
  -- Essential columns:
  -- id (UUID)
  -- aggregate_type
  -- aggregate_id
  -- event_type
  -- payload (JSONB)
  -- created_at
  -- published_at (nullable)
  -- retry_count
  ```
- [ ] Choose relay mechanism
  - [ ] Polling publisher (simpler)
  - [ ] CDC/Log tailing (Debezium, lower latency)
- [ ] Design message format
- [ ] Plan for ordering guarantees

### 5.2 Outbox Implementation

- [ ] Implement outbox table
- [ ] Modify business transactions to write to outbox
- [ ] Ensure same-transaction writes
- [ ] Implement message relay
  - [ ] Polling frequency (if polling)
  - [ ] Batch size
  - [ ] Error handling
- [ ] Implement cleanup/archival
- [ ] Add monitoring for lag

### 5.3 Outbox Consumer Requirements

- [ ] Implement idempotent consumers
- [ ] Handle duplicate messages
- [ ] Implement message deduplication
  - [ ] Dedup by message ID
  - [ ] Time window for dedup
- [ ] Handle out-of-order messages (if applicable)
- [ ] Add dead letter queue

---

## Phase 6: Resilience Implementation

### 6.1 Circuit Breaker Implementation

- [ ] Identify services requiring circuit breakers
- [ ] Configure thresholds
  - [ ] Failure count threshold
  - [ ] Failure rate threshold
  - [ ] Slow call threshold
  - [ ] Slow call duration threshold
- [ ] Configure timeouts
  - [ ] Wait duration in OPEN state
  - [ ] Permitted calls in HALF-OPEN
- [ ] Implement fallback behavior
  - [ ] Cached response
  - [ ] Default response
  - [ ] Degraded functionality
- [ ] Add monitoring and alerting
  - [ ] Circuit state changes
  - [ ] Failure rates
- [ ] Test circuit behavior

### 6.2 Bulkhead Implementation

- [ ] Identify isolation requirements
- [ ] Choose bulkhead type
  - [ ] Semaphore (simpler, current thread)
  - [ ] Thread pool (full isolation)
- [ ] Configure limits
  - [ ] Max concurrent calls
  - [ ] Max wait duration
  - [ ] (Thread pool) Core/max thread count
  - [ ] (Thread pool) Queue capacity
- [ ] Implement rejection handling
- [ ] Add monitoring
  - [ ] Active calls
  - [ ] Rejected calls
  - [ ] Wait times
- [ ] Test under load

### 6.3 Retry Implementation

- [ ] Identify retriable operations
- [ ] Verify idempotency of operations
- [ ] Configure retry policy
  - [ ] Max retry attempts
  - [ ] Backoff strategy (exponential)
  - [ ] Jitter (prevent thundering herd)
  - [ ] Max backoff duration
- [ ] Define retriable exceptions
- [ ] Combine with circuit breaker
- [ ] Add retry metrics

### 6.4 Rate Limiting Implementation

- [ ] Identify rate limit requirements
- [ ] Choose algorithm
  - [ ] Token bucket (allow bursts)
  - [ ] Sliding window (smooth)
- [ ] Configure limits
  - [ ] Requests per second/minute
  - [ ] Burst capacity
- [ ] Implement response for exceeded limits
  - [ ] HTTP 429 Too Many Requests
  - [ ] Retry-After header
- [ ] Consider distributed rate limiting (Redis)
- [ ] Add monitoring

---

## Phase 7: Idempotency Implementation

### 7.1 Idempotency Design

- [ ] Identify non-idempotent operations
- [ ] Choose idempotency strategy
  - [ ] Idempotency key (client-generated)
  - [ ] Natural business key
  - [ ] Version/ETag
- [ ] Design idempotency storage
  - [ ] Cache (Redis) for short-lived
  - [ ] Database for durable
- [ ] Define key expiration policy

### 7.2 Idempotency Implementation

- [ ] Implement idempotency key extraction
- [ ] Implement response caching
- [ ] Handle concurrent requests with same key
- [ ] Store response AFTER transaction commits
- [ ] Do NOT cache 5xx errors
- [ ] Return cached response for duplicates
- [ ] Add TTL for idempotency records
- [ ] Implement cleanup job

### 7.3 Message Idempotency

- [ ] Design message ID strategy
- [ ] Implement deduplication store
- [ ] Handle idempotent processing
- [ ] Consider exactly-once semantics (Kafka)

---

## Phase 8: Leader Election / Consensus

### 8.1 Leader Election Requirements

- [ ] Identify need for leader election
  - [ ] Single writer requirement
  - [ ] Coordinator for distributed tasks
  - [ ] Singleton service requirement
- [ ] Choose implementation
  - [ ] etcd/Consul (recommended)
  - [ ] ZooKeeper
  - [ ] Database-based
  - [ ] Redis (Redlock)

### 8.2 Leader Election Implementation

- [ ] Implement leader registration
- [ ] Implement heartbeat/lease renewal
- [ ] Handle leader failure detection
- [ ] Implement leader change notification
- [ ] Handle split-brain scenarios
- [ ] Test failover scenarios
- [ ] Add monitoring for leader changes

---

## Phase 9: Observability

### 9.1 Distributed Tracing

- [ ] Implement trace ID propagation
- [ ] Add spans for saga steps
- [ ] Add spans for external calls
- [ ] Include compensation in traces
- [ ] Configure sampling rate

### 9.2 Metrics

- [ ] Saga metrics
  - [ ] Saga start/completion rate
  - [ ] Saga duration histogram
  - [ ] Compensation rate
  - [ ] Failure rate by step
- [ ] Circuit breaker metrics
  - [ ] State transitions
  - [ ] Call success/failure rates
- [ ] Bulkhead metrics
  - [ ] Active/rejected calls
  - [ ] Queue depth (thread pool)
- [ ] Outbox metrics
  - [ ] Publishing lag
  - [ ] Retry counts

### 9.3 Alerting

- [ ] Alert on high saga failure rate
- [ ] Alert on circuit breaker opening
- [ ] Alert on high rejection rate (bulkhead)
- [ ] Alert on outbox publishing lag
- [ ] Alert on leader election failures

---

## Phase 10: Testing

### 10.1 Unit Testing

- [ ] Test saga step logic
- [ ] Test compensation logic
- [ ] Test idempotency handling
- [ ] Test circuit breaker state transitions
- [ ] Test retry logic

### 10.2 Integration Testing

- [ ] Test saga end-to-end (happy path)
- [ ] Test saga with failures at each step
- [ ] Test CQRS command/query flow
- [ ] Test event sourcing replay
- [ ] Test outbox publishing

### 10.3 Chaos Testing

- [ ] Test with random service failures
- [ ] Test with network partitions
- [ ] Test with slow services
- [ ] Test with message loss
- [ ] Test with duplicate messages
- [ ] Test leader failover

### 10.4 Load Testing

- [ ] Test at expected load
- [ ] Test at 2x expected load
- [ ] Test with concurrent sagas
- [ ] Measure latency under load
- [ ] Identify breaking points

---

## Phase 11: Documentation

- [ ] Document pattern decisions (ADRs)
- [ ] Document saga flows with diagrams
- [ ] Document compensation procedures
- [ ] Document failure scenarios and handling
- [ ] Document monitoring and alerting
- [ ] Create runbooks for common issues
- [ ] Document recovery procedures

---

## Quick Reference: Pattern Selection Matrix

| Requirement | Recommended Pattern |
|-------------|---------------------|
| Atomic multi-service transaction | Saga (or 2PC if supported) |
| Audit trail | Event Sourcing |
| High read/write ratio | CQRS |
| Reliable event publishing | Outbox Pattern |
| Prevent cascading failures | Circuit Breaker |
| Isolate failures | Bulkhead |
| Handle transient failures | Retry with backoff |
| Single active instance | Leader Election |
| Safe retries | Idempotency |
| Protect from overload | Rate Limiting |

---

## Checklist Completion Tracking

| Phase | Items | Completed |
|-------|-------|-----------|
| 1. Requirements | 15 | [ ] |
| 2. Pattern Selection | 15 | [ ] |
| 3. Saga | 25 | [ ] |
| 4. CQRS/ES | 20 | [ ] |
| 5. Outbox | 15 | [ ] |
| 6. Resilience | 30 | [ ] |
| 7. Idempotency | 15 | [ ] |
| 8. Leader Election | 10 | [ ] |
| 9. Observability | 15 | [ ] |
| 10. Testing | 15 | [ ] |
| 11. Documentation | 7 | [ ] |
| **Total** | **182** | [ ] |
