# Distributed System Patterns

Comprehensive guide to patterns for building resilient, consistent, and scalable distributed systems. Covers data consistency, fault tolerance, and coordination patterns essential for microservices architectures.

## Overview

Distributed systems face unique challenges that require specialized patterns:

| Challenge | Patterns |
|-----------|----------|
| Data consistency across services | Saga, CQRS, Event Sourcing, Outbox |
| Service failures | Circuit Breaker, Retry, Timeout |
| Cascading failures | Bulkhead, Rate Limiting |
| Distributed transactions | 2PC, Saga, TCC |
| Coordination | Leader Election, Consensus (Raft/Paxos) |
| Message reliability | Idempotency, Exactly-once delivery |

## Pattern Categories

### 1. Data Consistency Patterns

#### Saga Pattern

Manages distributed transactions as a sequence of local transactions with compensating actions.

**Two Approaches:**

| Approach | Coordination | Coupling | Complexity | Use When |
|----------|--------------|----------|------------|----------|
| **Choreography** | Event-based | Loose | Lower | Simple flows, 3-5 services |
| **Orchestration** | Central coordinator | Tighter | Higher | Complex flows, visibility needed |

**Choreography Flow:**
```
Order Service          Payment Service         Inventory Service
      |                      |                       |
      |--OrderCreated------->|                       |
      |                      |--PaymentProcessed---->|
      |                      |                       |
      |<--------------------|<--InventoryReserved---|
      |                      |                       |
   Complete            (compensate if any step fails)
```

**Orchestration Flow:**
```
              Saga Orchestrator
                     |
    +----------------+----------------+
    |                |                |
    v                v                v
Order Service   Payment Service   Inventory Service
```

**Key Principles:**
- Each step has a compensating action to undo changes
- Compensations must be idempotent
- Use correlation IDs to track saga instances
- Handle out-of-order events gracefully

#### CQRS (Command Query Responsibility Segregation)

Separates read and write models for independent optimization.

```
                    +------------------+
                    |   Write Model    |
   Commands ------> |  (Normalized)    |
                    +--------+---------+
                             |
                             | Events
                             v
                    +------------------+
                    |   Read Model     |
   Queries <------- |  (Denormalized)  |
                    +------------------+
```

**Benefits:**
- Independent scaling of reads vs writes
- Optimized data models for each use case
- Performance improvement: 64% average for read-intensive operations
- Team autonomy through decoupled responsibilities

**When to Use:**
- Read/write ratio significantly imbalanced
- Complex domain logic on writes
- Different read projections needed
- Event Sourcing architecture

#### Event Sourcing

Stores state changes as immutable events instead of current state.

```
Event Store:
+----+-------------------+---------------------------+
| ID | Type              | Data                      |
+----+-------------------+---------------------------+
| 1  | AccountCreated    | {id: "A1", balance: 0}    |
| 2  | MoneyDeposited    | {id: "A1", amount: 100}   |
| 3  | MoneyWithdrawn    | {id: "A1", amount: 30}    |
+----+-------------------+---------------------------+

Current State (derived): {id: "A1", balance: 70}
```

**Benefits:**
- Complete audit trail (100% historical accuracy)
- Temporal queries (state at any point in time)
- Event replay for debugging
- Natural fit for CQRS

**Trade-offs:**
- ~230% more storage than snapshot-based approaches
- Query complexity without read projections
- Event schema evolution challenges

#### Outbox Pattern

Ensures reliable event publishing without distributed transactions.

```
+-------------+    Same Transaction    +-------------+
|  Business   | --------+-----------> |   Outbox    |
|   Table     |         |             |   Table     |
+-------------+         |             +------+------+
                        |                    |
                        v                    | Message Relay
               [Transaction Commits]         | (CDC or Polling)
                                            v
                                   +----------------+
                                   | Message Broker |
                                   +----------------+
```

**Implementation Options:**
- **Polling Publisher:** Periodic queries to outbox table
- **Transaction Log Tailing (CDC):** Debezium, AWS DMS
- **Transactional Messaging:** Database-specific features

**Critical Requirement:** Consumers must be idempotent (messages may be delivered multiple times).

### 2. Transaction Patterns Comparison

| Aspect | 2PC | Saga | TCC |
|--------|-----|------|-----|
| **Consistency** | Strong | Eventual | Eventual |
| **Isolation** | Full | None | Partial |
| **Availability** | Lower | Higher | Higher |
| **Latency** | Higher | Lower | Medium |
| **Complexity** | Medium | Higher | Highest |
| **Scalability** | Limited | High | High |
| **Lock Duration** | Long | Short | Short |
| **Failure Handling** | Coordinator rollback | Compensating transactions | Cancel phase |

**When to Use:**

- **2PC:** Core financial operations, strict audit requirements, short transactions
- **Saga:** Long-running processes, high availability needs, microservices
- **TCC (Try-Confirm-Cancel):** Reservations, inventory holds, time-sensitive operations

### 3. Fault Tolerance Patterns

#### Circuit Breaker

Prevents cascading failures by failing fast when a service is unavailable.

```
States:
          success threshold
              met
         +------------+
         |            |
         v            |
     +--------+  failures  +--------+  timeout  +-----------+
     | CLOSED |----------->|  OPEN  |---------->| HALF-OPEN |
     +--------+            +--------+           +-----------+
         ^                      |                     |
         |                      | immediate fail      |
         |                      v                     |
         +--------success------------------------------+
```

**Configuration Parameters:**
- `failureThreshold`: Failures before opening (e.g., 5)
- `resetTimeout`: Time in OPEN state before testing (e.g., 60s)
- `successThreshold`: Successes in HALF-OPEN to close (e.g., 3)
- `slowCallThreshold`: Slow calls treated as failures

#### Bulkhead Pattern

Isolates failures by partitioning resources.

**Types:**

| Type | Mechanism | Pros | Cons |
|------|-----------|------|------|
| **Semaphore** | Limits concurrent calls | Low overhead, current thread | No timeout for waiting |
| **Thread Pool** | Dedicated thread pools | Full isolation, timeouts | Higher overhead |

**Key Benefit:** One slow/failing service cannot exhaust resources for others.

#### Retry with Exponential Backoff

```
Attempt 1: immediate
Attempt 2: wait 1s
Attempt 3: wait 2s
Attempt 4: wait 4s
...with jitter to prevent thundering herd
```

**Jitter Strategies:**
- **Full Jitter:** `random(0, delay)`
- **Equal Jitter:** `delay/2 + random(0, delay/2)`
- **Decorrelated Jitter:** `min(cap, random(base, prev_delay * 3))`

### 4. Idempotency Patterns

Essential for safe retries in distributed systems.

**HTTP Method Idempotency:**
- GET, PUT, DELETE: Idempotent by design
- POST: Not idempotent (requires explicit handling)
- PATCH: Depends on implementation

**Implementation Strategies:**

| Strategy | Description | Storage |
|----------|-------------|---------|
| **Idempotency Key** | Client-generated UUID per operation | Cache/DB |
| **Natural Key** | Business identifier (order_id + action) | DB |
| **Version/ETag** | Optimistic concurrency control | DB |
| **Deduplication** | Message-level dedup in queues | Queue system |

**Best Practices:**
- Store idempotency records AFTER transaction commits
- Set expiration times for idempotency keys
- Return same response for duplicate requests
- Don't cache 5xx errors (may succeed on retry)

### 5. Coordination Patterns

#### Leader Election

Ensures single active leader among distributed nodes.

**Common Approaches:**
- **Raft/Paxos:** Consensus-based (etcd, Consul)
- **ZooKeeper:** Ephemeral sequential nodes
- **Database:** Row locking with heartbeats
- **Redis:** SETNX with TTL (Redlock algorithm)

#### Consensus Algorithms

| Algorithm | Understandability | Performance | Use Cases |
|-----------|-------------------|-------------|-----------|
| **Raft** | High | Good | etcd, Consul, CockroachDB |
| **Paxos** | Low | Good | Chubby, Megastore |
| **KRaft** | Medium | High | Kafka metadata |

**Raft Key Concepts:**
- Term-based leadership
- Majority quorum for decisions
- Log replication to followers
- Randomized election timeouts

**Recent Improvements (2025):**
- **Dynatune:** Dynamic timeout adaptation (80% faster failure detection)
- **Cabinet:** Dynamic node weights for heterogeneous environments
- **KRaft:** Kafka without ZooKeeper dependency

### 6. Rate Limiting

Protects services from overload.

| Algorithm | Characteristics | Use Case |
|-----------|-----------------|----------|
| **Token Bucket** | Allows bursts, smooth average | API rate limiting |
| **Leaky Bucket** | Fixed output rate | Traffic shaping |
| **Fixed Window** | Simple, edge-case spikes | Basic limiting |
| **Sliding Window** | Smooth, more accurate | Precise rate control |

## Pattern Combinations

Common pattern combinations for production systems:

| Scenario | Patterns |
|----------|----------|
| E-commerce order | Saga + Outbox + Idempotency |
| Real-time analytics | CQRS + Event Sourcing |
| Payment processing | 2PC (core) + Saga (auxiliary) |
| API resilience | Circuit Breaker + Bulkhead + Retry |
| Event streaming | Event Sourcing + CQRS + Outbox |

## Technology Stack (2025)

| Pattern | Tools/Frameworks |
|---------|------------------|
| Saga Orchestration | Temporal, Camunda, AWS Step Functions |
| Event Sourcing | EventStoreDB, Axon, Kafka |
| CQRS | Axon Framework, Eventuate |
| Outbox | Debezium (CDC), custom polling |
| Circuit Breaker | Resilience4j, Polly, Istio |
| Consensus | etcd, Consul, ZooKeeper |
| Rate Limiting | Redis, Envoy, Kong |

## LLM-Assisted Design Tips

When using LLMs for distributed system design:

1. **Provide Context:** Share your consistency requirements (strong vs eventual), SLAs, and scale expectations

2. **Be Specific About Trade-offs:** Ask "What are the trade-offs of using Saga vs 2PC for my payment flow?"

3. **Request Failure Scenarios:** "What happens if the payment service fails after order creation?"

4. **Ask for Compensating Actions:** "Design compensating transactions for each saga step"

5. **Validate Idempotency:** "Is this operation idempotent? How to make it idempotent?"

6. **Consider Edge Cases:** Late-arriving messages, duplicate events, partial failures

## External References

### Documentation
- [Microservices.io Patterns](https://microservices.io/patterns/)
- [Azure Architecture Patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)
- [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/)

### Tools
- [Resilience4j](https://resilience4j.readme.io/)
- [Temporal](https://temporal.io/)
- [Debezium](https://debezium.io/)
- [Axon Framework](https://axoniq.io/)

### Learning Resources
- [Raft Visualization](https://raft.github.io/)
- [ByteByteGo System Design](https://blog.bytebytego.com/)
- [Martin Fowler's Patterns](https://martinfowler.com/articles/patterns-of-distributed-systems/)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Files

- [checklist.md](checklist.md) - Step-by-step implementation checklist
- [examples.md](examples.md) - Real-world system examples
- [templates.md](templates.md) - Copy-paste configurations
- [llm-prompts.md](llm-prompts.md) - Effective prompts for LLM-assisted design

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [event-driven-architecture](../event-driven-architecture/) | Event patterns, message brokers |
| [microservices-architecture](../microservices-architecture/) | Service decomposition |
| [database-selection](../database-selection/) | Storage for patterns |
| [reliability-architecture](../reliability-architecture/) | SLOs, error budgets |
