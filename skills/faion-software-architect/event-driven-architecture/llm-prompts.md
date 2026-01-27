# LLM Prompts for Event-Driven Architecture

Prompts for AI-assisted event-driven architecture design and implementation.

---

## Architecture Design Prompts

### EDA Assessment

```
Assess whether event-driven architecture is appropriate for this system:

CONTEXT:
- System: [System name and purpose]
- Current architecture: [Monolith/Microservices/Other]
- Team size: [Number]
- Scale: [Users/requests per day]

REQUIREMENTS:
- [List key requirements]

CONSTRAINTS:
- [List constraints: budget, timeline, team skills]

Analyze:
1. Benefits EDA would provide
2. Challenges and risks
3. Recommended patterns (pub/sub, event sourcing, CQRS)
4. Migration strategy if applicable
5. Decision recommendation with rationale
```

### Pattern Selection

```
Help me select the right event-driven pattern for this use case:

USE CASE: [Describe the business scenario]

REQUIREMENTS:
- Consistency: [Strong/Eventual]
- Audit: [Yes/No - need full history?]
- Scale: [Read-heavy/Write-heavy/Balanced]
- Latency: [Real-time/Near-real-time/Batch OK]

CURRENT STATE:
- Database: [Type]
- Existing events: [Yes/No]
- Team experience: [Event-driven experience level]

Evaluate these patterns for fit:
1. Simple Pub/Sub
2. Event Sourcing
3. CQRS
4. Event Sourcing + CQRS

For each, explain:
- Fit score (1-10)
- Pros for this use case
- Cons/challenges
- Implementation complexity
```

### Message Broker Selection

```
Help me choose a message broker for this event-driven system:

REQUIREMENTS:
- Throughput: [events/second]
- Latency: [p95 target]
- Retention: [How long to keep events]
- Replay: [Need to replay events?]
- Ordering: [Global/Per-key/None]
- Delivery: [At-least-once/Exactly-once]

ENVIRONMENT:
- Cloud provider: [AWS/GCP/Azure/On-prem]
- Team ops capacity: [High/Medium/Low]
- Budget: [Range or constraint]
- Existing infrastructure: [What's already in use]

Compare these options:
1. Apache Kafka
2. Apache Pulsar
3. RabbitMQ
4. AWS SQS/SNS
5. [Any other relevant option]

For each:
- Score against requirements
- Operational considerations
- Cost estimate
- Migration path
- Recommendation
```

---

## Event Design Prompts

### Event Schema Design

```
Design a CloudEvents-compliant event schema for this domain event:

DOMAIN: [e.g., E-commerce, Banking, Healthcare]
BOUNDED CONTEXT: [e.g., Orders, Payments, Users]
EVENT: [What happened - e.g., "Order was placed"]

BUSINESS CONTEXT:
- What triggers this event?
- Who produces it?
- Who consumes it?
- What decisions depend on it?

REQUIREMENTS:
- Must include: [Required data points]
- Privacy: [Any PII considerations]
- Compliance: [Any regulatory requirements]

Provide:
1. Full CloudEvents JSON schema
2. JSON Schema for validation
3. Versioning strategy
4. Example event instance
5. Consumer contract considerations
```

### Event Naming Convention

```
Establish event naming conventions for this system:

DOMAIN: [Domain name]
SERVICES: [List of services]

CURRENT EVENTS (if any):
[List existing event names]

Create:
1. Naming convention rules
2. Type hierarchy structure
3. Examples for common event types:
   - Entity created
   - Entity updated
   - Entity deleted
   - Status changed
   - Integration events
4. Anti-patterns to avoid
5. Documentation template
```

### Event Storming Output to Schema

```
Convert this Event Storming output into event schemas:

AGGREGATE: [Aggregate name]

EVENTS FROM EVENT STORMING:
1. [Event 1 - orange sticky]
2. [Event 2 - orange sticky]
3. [Event 3 - orange sticky]

COMMANDS THAT TRIGGER THEM:
1. [Command 1 - blue sticky]
2. [Command 2 - blue sticky]

POLICIES/REACTIONS:
1. [Policy 1 - purple sticky]

For each event, generate:
1. CloudEvents schema
2. Data payload schema
3. Producer identification
4. Consumer identification
5. Event flow diagram
```

---

## Implementation Prompts

### Producer Implementation

```
Generate an event producer implementation:

LANGUAGE: [Python/TypeScript/Java/Go]
BROKER: [Kafka/RabbitMQ/Pulsar/SQS]
FRAMEWORK: [Django/FastAPI/Express/Spring/etc.]

EVENT TO PUBLISH:
[Event schema or description]

REQUIREMENTS:
- [ ] CloudEvents format
- [ ] Idempotent publishing
- [ ] Retry with backoff
- [ ] Correlation ID propagation
- [ ] Error handling
- [ ] Metrics/logging
- [ ] Transactional outbox (if applicable)

Generate:
1. Producer class/module
2. Event creation helper
3. Publishing logic
4. Error handling
5. Integration tests
6. Usage example
```

### Consumer Implementation

```
Generate an event consumer implementation:

LANGUAGE: [Python/TypeScript/Java/Go]
BROKER: [Kafka/RabbitMQ/Pulsar/SQS]
FRAMEWORK: [Django/FastAPI/Express/Spring/etc.]

EVENT TO CONSUME:
[Event schema]

PROCESSING LOGIC:
[What should happen when event is received]

REQUIREMENTS:
- [ ] Idempotent handling
- [ ] At-least-once delivery handling
- [ ] Out-of-order handling
- [ ] Dead letter queue
- [ ] Graceful shutdown
- [ ] Metrics/logging

Generate:
1. Consumer class/module
2. Event handler interface
3. Idempotency implementation
4. Error handling with DLQ
5. Integration tests
6. Health check endpoint
```

### Saga Implementation

```
Design and implement a saga for this distributed transaction:

TRANSACTION: [Describe what needs to happen]

SERVICES INVOLVED:
1. [Service 1]: [What it does in this transaction]
2. [Service 2]: [What it does]
3. [Service 3]: [What it does]

FAILURE SCENARIOS:
- What if [Service 1] fails?
- What if [Service 2] fails?
- What if [Service 3] fails?

REQUIREMENTS:
- Saga type: [Choreography/Orchestration]
- Language: [Python/TypeScript/Java/Go]
- Broker: [Kafka/RabbitMQ/etc.]

Generate:
1. Saga state machine diagram
2. Event definitions (forward and compensating)
3. Saga orchestrator/participant code
4. Compensation handlers
5. Timeout handling
6. Testing strategy
```

---

## Troubleshooting Prompts

### Consumer Lag Analysis

```
Help me diagnose and fix consumer lag issues:

SYMPTOMS:
- Consumer group: [Name]
- Current lag: [Number of messages]
- Lag trend: [Increasing/Stable/Variable]
- Processing time: [Average/p95]

INFRASTRUCTURE:
- Broker: [Kafka/etc.]
- Partitions: [Count]
- Consumer instances: [Count]
- Consumer resources: [CPU/Memory]

PROCESSING:
- What does the consumer do?
- Any external dependencies?
- Database operations?

Analyze:
1. Likely root causes
2. Diagnostic queries/commands
3. Short-term mitigation
4. Long-term solutions
5. Monitoring improvements
```

### Event Schema Evolution

```
Help me evolve this event schema without breaking consumers:

CURRENT SCHEMA:
```json
[Current event schema]
```

REQUIRED CHANGES:
- Add field: [Field name and type]
- Remove field: [Field name]
- Rename field: [Old name to new name]
- Change type: [Field and type change]

CONSUMERS:
- [List of known consumers]
- Can coordinate deployment: [Yes/No]

Provide:
1. Compatibility analysis (backward/forward)
2. Schema versioning approach
3. Migration strategy
4. New schema version
5. Consumer update guide
6. Rollback plan
```

### Duplicate Event Handling

```
I'm seeing duplicate events being processed. Help me diagnose and fix:

SYMPTOMS:
- Event type: [Type]
- Duplicate rate: [Percentage or count]
- Pattern: [Always/Sometimes/Under load]

CURRENT IMPLEMENTATION:
- Producer: [How events are published]
- Consumer: [How events are processed]
- Idempotency: [Current approach if any]

INFRASTRUCTURE:
- Broker: [Type]
- Delivery guarantee: [Setting]
- Consumer group: [Settings]

Analyze:
1. Possible causes of duplicates
2. Where duplicates originate (producer/broker/consumer)
3. Idempotency implementation strategy
4. Code changes needed
5. Testing approach for verification
```

---

## Architecture Review Prompts

### EDA Review Checklist

```
Review this event-driven architecture design:

DESIGN DOCUMENT:
[Paste design or describe architecture]

Review against:

1. EVENT DESIGN
   - Are events immutable?
   - Is naming consistent (past tense)?
   - Are schemas versioned?
   - Is CloudEvents format used?

2. PRODUCER PATTERNS
   - Transactional outbox implemented?
   - Retry logic present?
   - Correlation ID propagated?

3. CONSUMER PATTERNS
   - Idempotency implemented?
   - Dead letter queue configured?
   - Out-of-order handling addressed?

4. INFRASTRUCTURE
   - Broker selection appropriate?
   - Partitioning strategy sound?
   - Retention configured correctly?

5. OBSERVABILITY
   - Distributed tracing enabled?
   - Consumer lag monitored?
   - Error rates tracked?

6. RESILIENCE
   - What happens if broker is down?
   - What happens if consumer crashes?
   - How are poison messages handled?

Provide:
- Score for each category (1-5)
- Critical issues
- Recommendations
- Risks and mitigations
```

### Event Catalog Review

```
Review this event catalog for completeness and consistency:

EVENT CATALOG:
[List of events with descriptions]

SERVICES:
[List of services]

Review:
1. Coverage - are all domain events captured?
2. Naming consistency
3. Ownership clarity (producer per event)
4. Consumer documentation
5. Schema availability
6. Versioning approach
7. Deprecation handling

Provide:
- Missing events (based on domain)
- Inconsistencies found
- Documentation gaps
- Improvement recommendations
- Event catalog template suggestion
```

---

## Migration Prompts

### Monolith to EDA Migration

```
Plan migration from monolith to event-driven architecture:

CURRENT STATE:
- Monolith description: [Architecture overview]
- Key modules: [List]
- Database: [Type and size]
- Current integrations: [List]

TARGET STATE:
- Services to extract: [List]
- Events to introduce: [Key events]
- Timeline: [Constraint]

CONSTRAINTS:
- Zero downtime required: [Yes/No]
- Team size: [Number]
- Budget: [Constraint]

Create migration plan:
1. Phase 1: Introduce event infrastructure
2. Phase 2: Strangler fig pattern steps
3. Phase 3: Service extraction order
4. Dual-write strategy
5. Rollback plans per phase
6. Success metrics
7. Risk register
```

### Broker Migration

```
Plan migration from [Current Broker] to [Target Broker]:

CURRENT STATE:
- Broker: [Current]
- Topics/queues: [Count and names]
- Throughput: [Messages/second]
- Consumers: [Count and types]
- Retention: [Current settings]

TARGET:
- Broker: [Target]
- Reason for migration: [Why]
- Timeline: [Constraint]

REQUIREMENTS:
- Zero message loss
- Minimal downtime
- Rollback capability

Create:
1. Migration strategy (big bang vs gradual)
2. Dual-publish approach
3. Consumer migration steps
4. Data migration for historical events
5. Validation approach
6. Rollback procedure
7. Post-migration verification
```

---

## Documentation Prompts

### Event Documentation

```
Generate comprehensive documentation for this event:

EVENT: [Event type]
PRODUCER: [Service name]
SCHEMA: [JSON schema]

Generate:
1. Event overview (purpose, when emitted)
2. Schema documentation with field descriptions
3. Example payloads (happy path, edge cases)
4. Consumer guide
5. Troubleshooting guide
6. Changelog template
```

### ADR for EDA Decision

```
Write an Architecture Decision Record for this EDA decision:

DECISION: [What was decided]
CONTEXT: [Why this decision was needed]
OPTIONS CONSIDERED:
1. [Option 1]
2. [Option 2]
3. [Option 3]

Generate ADR with:
1. Title
2. Status
3. Context
4. Decision
5. Consequences (positive and negative)
6. Alternatives considered
7. References
```

---

## Quick Reference Prompts

### Event Type Generator

```
Generate event types for [domain/aggregate]:

Events needed:
- Creation event
- Update events (for key fields)
- Status change events
- Deletion/archival event
- Integration events

Output: List with naming, description, and key payload fields
```

### Consumer Group Strategy

```
Design consumer group strategy for:
- Topic: [Name]
- Partitions: [Count]
- Consumers: [Types and purposes]
- Ordering requirements: [Describe]

Output: Consumer group names, partition assignment, scaling strategy
```

### Dead Letter Queue Handler

```
Design DLQ handling for:
- Event type: [Type]
- Failure reasons: [Common failures]
- SLA: [Max time in DLQ]

Output: DLQ topic design, retry logic, alerting, manual intervention process
```

---

## Prompt Chaining for Complex Designs

### Full EDA Design Flow

```
STEP 1: Event Storming → Event List
"Run event storming for [domain]. Output: list of domain events"

STEP 2: Event List → Schemas
"Convert these events to CloudEvents schemas: [events]"

STEP 3: Schemas → Producer/Consumer
"Generate producer and consumer for: [schema]"

STEP 4: Implementation → Tests
"Generate integration tests for: [implementation]"

STEP 5: Tests → Documentation
"Document this event system: [all outputs]"
```

---

## Usage Tips

1. **Be specific about constraints** - Include team skills, timeline, budget
2. **Provide existing context** - Current architecture, tech stack
3. **State requirements clearly** - Consistency, latency, scale needs
4. **Ask for alternatives** - Get multiple options compared
5. **Request rationale** - Understand why, not just what
6. **Include examples** - Provide sample data when asking about schemas
7. **Iterate** - Start broad, then drill into specifics
