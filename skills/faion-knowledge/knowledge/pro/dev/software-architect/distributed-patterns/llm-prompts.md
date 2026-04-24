# LLM Prompts for Distributed Patterns Design

Effective prompts for AI-assisted distributed system architecture discussions.

---

## Prompt Categories

1. [Pattern Selection](#1-pattern-selection-prompts)
2. [Saga Design](#2-saga-design-prompts)
3. [CQRS/Event Sourcing](#3-cqrsevent-sourcing-prompts)
4. [Consistency & Transactions](#4-consistency--transaction-prompts)
5. [Resilience Patterns](#5-resilience-pattern-prompts)
6. [Idempotency](#6-idempotency-prompts)
7. [Failure Analysis](#7-failure-analysis-prompts)
8. [Code Review](#8-code-review-prompts)

---

## 1. Pattern Selection Prompts

### 1.1 General Pattern Selection

```
I'm designing a distributed system with the following characteristics:
- [Number] services involved
- Transaction type: [long-running/short/mixed]
- Consistency requirement: [strong/eventual/causal]
- Availability SLA: [99.9%/99.99%/other]
- Expected load: [TPS]
- Key operations: [list main operations]

Which distributed transaction pattern(s) should I use?
Compare Saga, 2PC, and TCC for my use case with trade-offs.
```

### 1.2 Saga vs 2PC Decision

```
Help me choose between Saga and Two-Phase Commit for this scenario:

Business Context:
- Operation: [describe the business transaction]
- Services involved: [list services]
- Transaction duration: [typical duration]
- Rollback frequency expectation: [rare/occasional/common]

Technical Constraints:
- Database types: [relational/NoSQL/mixed]
- Message broker: [Kafka/RabbitMQ/SQS/none]
- Existing transaction support: [yes/no]

Requirements:
- Consistency: [must be immediate / eventual OK]
- Audit requirements: [strict/moderate/minimal]
- Latency budget: [ms]

Provide recommendation with justification.
```

### 1.3 Choreography vs Orchestration

```
I need to implement a Saga pattern for [use case]. Help me decide between choreography and orchestration.

Saga Flow:
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]
...

Considerations:
- Team structure: [single team / multiple teams]
- Visibility/debugging requirements: [high/medium/low]
- Coupling tolerance: [loose preferred / tight acceptable]
- Existing event infrastructure: [yes/no]

Recommend the approach and explain the decision criteria.
```

---

## 2. Saga Design Prompts

### 2.1 Complete Saga Design

```
Design a complete Saga for [business transaction, e.g., "e-commerce order placement"].

Services involved:
- [Service 1]: [responsibility]
- [Service 2]: [responsibility]
- [Service 3]: [responsibility]

For each step, provide:
1. Action description
2. Compensating action
3. Idempotency strategy
4. Failure scenarios
5. Timeout recommendation

Also include:
- State machine diagram (text representation)
- Event schema for choreography (if applicable)
- Orchestrator pseudo-code (if applicable)
```

### 2.2 Compensation Design

```
I have a Saga with the following steps:
1. [Step 1 - already completed]
2. [Step 2 - already completed]
3. [Step 3 - FAILED HERE]

Design the compensation flow considering:
- Side effects already produced: [list any notifications, external calls]
- Data changes: [what was modified]
- External system states: [any third-party integrations]

Questions to address:
1. What compensations are needed in what order?
2. How to handle compensation failures?
3. How to make compensations idempotent?
4. What if some steps can't be compensated?
```

### 2.3 Saga Edge Cases

```
Analyze edge cases for this Saga:

[Describe the saga flow]

Consider and provide handling strategies for:
1. Duplicate events arriving
2. Out-of-order events
3. Orphaned sagas (never completed)
4. Concurrent sagas for same entity
5. Compensation timeout
6. Partial compensation success
7. Network partition during compensation
```

---

## 3. CQRS/Event Sourcing Prompts

### 3.1 CQRS Architecture Design

```
Design a CQRS architecture for [domain, e.g., "inventory management"].

Read Requirements:
- Query patterns: [list main queries]
- Latency requirements: [ms for each]
- Data freshness tolerance: [real-time / seconds / minutes]

Write Requirements:
- Command patterns: [list main commands]
- Validation complexity: [simple/complex]
- Concurrency handling: [optimistic/pessimistic]

Provide:
1. Command model design
2. Read model(s) design
3. Event schema
4. Projection update strategy (sync/async)
5. Eventual consistency handling for UI
```

### 3.2 Event Sourcing Design

```
Design an event-sourced aggregate for [entity, e.g., "Order"].

Entity Lifecycle:
- Created -> [states] -> [final states]

For each state transition:
1. Event name and schema
2. Aggregate validation rules
3. Side effects (if any)

Additional requirements:
- Snapshotting strategy
- Event versioning approach
- Projection rebuild strategy
- Storage estimate for [expected volume]
```

### 3.3 Event Schema Evolution

```
I have an existing event sourced system with this event:

```json
{
  "type": "OrderCreated",
  "version": 1,
  "data": {
    [current schema]
  }
}
```

I need to:
- [Add field X]
- [Rename field Y to Z]
- [Remove field W]
- [Change type of field V]

Design:
1. New event version schema
2. Upcaster for old events
3. Migration strategy
4. Backward compatibility approach
5. Rollback plan if issues arise
```

---

## 4. Consistency & Transaction Prompts

### 4.1 Consistency Analysis

```
Analyze the consistency requirements for this system:

Operations:
1. [Operation A] - [description]
2. [Operation B] - [description]
3. [Operation C] - [description]

For each operation:
- Does it require strong consistency?
- What's the acceptable inconsistency window?
- What are the consequences of stale reads?
- What invariants must be maintained?

Recommend consistency model per operation with justification.
```

### 4.2 Distributed Transaction Design

```
Design a distributed transaction for this cross-service operation:

Operation: [description]

Services and their responsibilities:
- Service A: [action + database]
- Service B: [action + database]
- Service C: [action + external API]

Constraints:
- Service C external API has no rollback capability
- Service A and B use different database types
- Operation must complete within [X] seconds

Design the transaction strategy covering:
1. Coordination mechanism
2. Commit protocol
3. Failure recovery
4. Timeout handling
5. Idempotency at each step
```

### 4.3 Outbox Pattern Implementation

```
Design an Outbox pattern implementation for [service name].

Requirements:
- Database: [PostgreSQL/MySQL/MongoDB]
- Message broker: [Kafka/RabbitMQ/SQS]
- Message volume: [messages/second]
- Ordering requirements: [strict per aggregate / relaxed]

Provide:
1. Outbox table schema
2. Transaction code pattern
3. Relay implementation (polling vs CDC)
4. Cleanup/archival strategy
5. Monitoring approach
6. Consumer idempotency requirements
```

---

## 5. Resilience Pattern Prompts

### 5.1 Circuit Breaker Configuration

```
Configure a Circuit Breaker for [service/operation].

Characteristics:
- Normal response time: [ms]
- Acceptable slow call threshold: [ms]
- Current failure rate: [%]
- Request volume: [requests/minute]
- Recovery behavior: [fast/gradual]

Provide:
1. Configuration values with rationale:
   - Failure threshold
   - Slow call threshold
   - Wait duration in OPEN
   - Half-open test calls
2. Fallback strategy
3. Monitoring metrics
4. Alert thresholds
```

### 5.2 Bulkhead Design

```
Design bulkhead isolation for this API Gateway:

Downstream services:
- [Service A]: [criticality: high/medium/low], [response time], [reliability]
- [Service B]: [criticality], [response time], [reliability]
- [Service C]: [criticality], [response time], [reliability]

Total available resources:
- Thread pool size: [N]
- Connection pool size: [M]

Design:
1. Bulkhead allocation per service
2. Semaphore vs Thread Pool choice per service
3. Queue capacity (if using thread pool)
4. Rejection handling strategy
5. Resource adjustment recommendations based on observed behavior
```

### 5.3 Retry Strategy Design

```
Design a retry strategy for [operation type].

Operation characteristics:
- Idempotent: [yes/no/can be made]
- Average duration: [ms]
- Known transient failures: [list]
- Permanent failure indicators: [list]

Constraints:
- SLA timeout: [seconds]
- Resource constraints: [any]
- Downstream protection needs: [yes/no]

Design:
1. Retry policy (max attempts, delays)
2. Backoff algorithm with justification
3. Jitter strategy
4. Retriable vs non-retriable exception classification
5. Integration with circuit breaker
```

### 5.4 Combined Resilience Stack

```
Design a complete resilience stack for calling [external service].

Service characteristics:
- Availability: [%]
- Average latency: [ms]
- Failure modes: [timeout/5xx/network errors]
- Rate limits: [if any]

Design a layered resilience approach with:
1. Timeout configuration
2. Retry policy
3. Circuit breaker settings
4. Bulkhead configuration
5. Rate limiter (if needed)
6. Fallback strategy

Show the order of application and interaction between patterns.
```

---

## 6. Idempotency Prompts

### 6.1 Idempotency Strategy Design

```
Design idempotency for this API endpoint:

Endpoint: [method] [path]
Operation: [description of what it does]
Side effects:
- [Database changes]
- [External API calls]
- [Notifications]

Current flow:
[Describe current implementation]

Design:
1. Idempotency key strategy (client-generated vs natural key)
2. Storage approach (cache vs database)
3. TTL recommendation
4. Handling concurrent requests with same key
5. Response caching strategy
6. Error scenarios and handling
```

### 6.2 Message Consumer Idempotency

```
Design idempotent message processing for this consumer:

Message type: [event/command name]
Processing involves:
- [Database operations]
- [External service calls]
- [Side effects]

Characteristics:
- Message broker: [Kafka/RabbitMQ/SQS]
- Delivery guarantee: [at-least-once/exactly-once]
- Processing time: [typical duration]
- Message ordering: [required/not required]

Design:
1. Deduplication strategy
2. Processing state tracking
3. Handling redelivered messages
4. Interaction with transaction boundaries
5. Cleanup of deduplication records
```

### 6.3 Making Operations Idempotent

```
This operation is NOT idempotent. Help me make it idempotent:

Current implementation:
```[language]
[code snippet]
```

Operation: [describe what it does]
Problem: [why it's not idempotent]

Provide:
1. Idempotent redesign
2. Required schema changes (if any)
3. Client contract changes (if any)
4. Migration strategy from current to idempotent version
```

---

## 7. Failure Analysis Prompts

### 7.1 Failure Scenario Analysis

```
Analyze failure scenarios for this distributed operation:

[Describe the operation flow]

For each of these failure points:
1. [Service A fails after step X]
2. [Network partition between A and B]
3. [Database timeout during step Y]
4. [Message broker unavailable]
5. [Duplicate message delivery]

Provide:
- What state is the system left in?
- How is this detected?
- What is the recovery procedure?
- How long until consistency is restored?
```

### 7.2 Saga Failure Analysis

```
Analyze what happens when this Saga fails at each step:

Saga: [Name]
Steps:
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

For failure at each step:
1. What compensations trigger?
2. What if compensation fails?
3. What's the final system state?
4. Human intervention needed?
5. Data reconciliation required?
```

### 7.3 Split-Brain Analysis

```
Analyze split-brain scenarios for this distributed system:

Architecture:
[Describe the distributed architecture]

Leader election: [mechanism used]
Data replication: [sync/async, factor]

Scenarios to analyze:
1. Network partition isolating leader
2. Slow network causing false leader detection
3. Multiple leaders elected simultaneously
4. Partition heals with conflicting writes

For each:
- How is it detected?
- What's the resolution strategy?
- What data loss/duplication is possible?
- How to prevent or minimize impact?
```

---

## 8. Code Review Prompts

### 8.1 Distributed Pattern Code Review

```
Review this implementation of [pattern name]:

```[language]
[code to review]
```

Check for:
1. Correct pattern implementation
2. Error handling completeness
3. Idempotency
4. Race conditions
5. Resource leaks
6. Timeout handling
7. Observability (logging, metrics, tracing)
8. Testability

Provide specific issues and fixes.
```

### 8.2 Saga Implementation Review

```
Review this Saga implementation:

```[language]
[saga code]
```

Verify:
1. All steps have compensation
2. Compensations are idempotent
3. Correlation ID propagation
4. Timeout handling
5. State persistence
6. Failure detection
7. Concurrent saga handling
8. Observability

List issues by severity (critical/major/minor).
```

### 8.3 Circuit Breaker Review

```
Review this Circuit Breaker configuration and usage:

Configuration:
```yaml
[config]
```

Code:
```[language]
[code]
```

Check:
1. Appropriate thresholds for the service
2. Correct exception handling
3. Fallback implementation
4. State monitoring
5. Integration with other resilience patterns
6. Thread safety
7. Resource cleanup

Suggest improvements with rationale.
```

---

## Prompt Templates for Specific Technologies

### Temporal/Cadence

```
Design a Temporal workflow for [use case].

Requirements:
- [List requirements]

Provide:
1. Workflow definition
2. Activity definitions with retry policies
3. Signal handling (if needed)
4. Query handlers (if needed)
5. Error handling and compensation
6. Testing strategy
```

### Kafka Event Processing

```
Design Kafka consumer for [event type] with:
- Exactly-once processing requirement
- [Other requirements]

Provide:
1. Consumer configuration
2. Offset management strategy
3. Partition assignment strategy
4. Error handling
5. Dead letter topic handling
6. Idempotency implementation
```

### Redis Distributed Patterns

```
Implement [pattern] using Redis for [use case].

Requirements:
- Cluster mode: [yes/no]
- Persistence: [required/optional]
- Performance: [ops/second]

Provide:
1. Data structure design
2. Lua scripts for atomicity
3. Cluster considerations
4. Failure handling
5. Monitoring approach
```

---

## Best Practices for LLM Prompts

### DO

- Provide specific context about your system
- List concrete requirements and constraints
- Ask for trade-off analysis, not just solutions
- Request failure scenario handling
- Ask for monitoring and observability recommendations
- Specify technology stack when relevant

### DON'T

- Ask generic "how to implement X" without context
- Ignore scale and performance requirements
- Forget to mention consistency requirements
- Skip failure scenario analysis
- Assume single-node behavior applies to distributed

### Follow-up Questions to Ask

After receiving initial design:

1. "What happens if [specific failure]?"
2. "How does this scale to [10x load]?"
3. "What are the monitoring requirements?"
4. "How do we test this in isolation?"
5. "What's the migration path from current state?"
6. "What are the operational runbooks needed?"

---

## Example Complete Prompt

```
I'm designing a payment processing system and need help with distributed transaction patterns.

CONTEXT:
- We're building a SaaS payment gateway
- ~10,000 transactions/minute at peak
- Services: PaymentAPI, FraudCheck, BankIntegration, NotificationService
- Using PostgreSQL and Kafka
- 99.99% availability requirement

CURRENT FLOW:
1. PaymentAPI receives request
2. FraudCheck validates (can reject)
3. BankIntegration processes charge (external API, no rollback)
4. NotificationService sends confirmation

CHALLENGES:
- Bank API has no rollback - only refund after successful charge
- FraudCheck is slow (500ms p95)
- Notifications are best-effort

QUESTIONS:
1. Should I use Saga or 2PC? Why?
2. How to handle the Bank API's lack of rollback?
3. Design the compensation flow for each failure point
4. How to make the system idempotent for retry safety?
5. What resilience patterns for FraudCheck latency?

Please provide:
- Pattern recommendation with justification
- Complete saga/transaction design
- Failure scenario analysis
- Idempotency strategy
- Monitoring recommendations
```

---

## Related Files

- [README.md](README.md) - Pattern overview
- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Code templates
