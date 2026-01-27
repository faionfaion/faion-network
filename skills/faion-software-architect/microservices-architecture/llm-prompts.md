# LLM Prompts for Microservices Design

Practical prompts for AI-assisted microservices architecture.

## Domain Analysis Prompts

### Bounded Context Discovery

```
I'm designing a microservices architecture for [DOMAIN]. Help me identify bounded contexts.

Context:
- Business: [Brief description of the business]
- Key workflows: [List main user journeys]
- Current pain points: [What problems exist]

Analyze this domain and suggest:
1. Potential bounded contexts with clear responsibilities
2. Context relationships (upstream/downstream)
3. Which contexts are Core, Supporting, or Generic
4. Suggested integration patterns between contexts

Format as a table with: Context Name | Responsibility | Type | Key Entities
```

### Event Storming Assistant

```
Help me run an Event Storming session for [FEATURE/DOMAIN].

Starting points:
- Main user goal: [What user wants to achieve]
- Key actors: [Who interacts with the system]
- Known business rules: [Important constraints]

Generate:
1. Domain Events (orange): What happens in the system
2. Commands (blue): What triggers events
3. Aggregates (yellow): What handles commands
4. Read Models (green): What users query
5. External Systems (pink): What integrates

Present as a timeline flow from trigger to outcome.
```

### Service Boundary Validation

```
I've identified these potential services for [DOMAIN]:
[LIST YOUR SERVICES]

For each service, evaluate:
1. Does it have a single business capability?
2. Can it deploy independently?
3. Does it own its data completely?
4. What's the coupling risk with other services?
5. Is it too small (nano-service) or too large (mini-monolith)?

Suggest any boundary adjustments with rationale.
```

## Architecture Design Prompts

### Communication Pattern Selection

```
Help me choose communication patterns for my microservices.

Services:
[LIST YOUR SERVICES WITH BRIEF DESCRIPTIONS]

For each service interaction, recommend:
1. Sync vs Async
2. Protocol (REST, gRPC, Events)
3. Why this choice
4. Failure handling approach

Consider:
- Latency requirements
- Consistency needs
- Failure scenarios
- Scale expectations
```

### API Contract Design

```
Design an API contract for [SERVICE NAME].

Service responsibility: [WHAT IT DOES]

Consumers:
- [LIST SERVICES/CLIENTS THAT WILL USE IT]

Requirements:
- [LIST KEY OPERATIONS NEEDED]

Generate:
1. OpenAPI 3.1 spec with endpoints
2. Request/Response schemas
3. Error response format
4. Versioning strategy recommendation
5. Rate limiting suggestions
```

### Event Schema Design

```
Design event schemas for [SERVICE NAME].

Business operations:
- [LIST OPERATIONS THIS SERVICE HANDLES]

For each significant state change, design:
1. Event name (past tense, e.g., OrderCreated)
2. Event schema with CloudEvents envelope
3. Key fields and their purpose
4. Consumers who might be interested
5. Versioning approach

Consider idempotency and ordering requirements.
```

## Data Architecture Prompts

### Database Selection

```
Help me choose databases for my microservices.

Services and their data needs:
[FOR EACH SERVICE: Name, Data patterns, Query patterns, Scale expectations]

For each service recommend:
1. Database type (relational, document, key-value, etc.)
2. Specific technology (PostgreSQL, MongoDB, Redis, etc.)
3. Why this choice
4. Potential alternatives
5. Migration path if needs change
```

### Saga Pattern Design

```
Design a saga for [CROSS-SERVICE OPERATION].

Services involved:
[LIST SERVICES AND THEIR ROLES]

Happy path flow:
[DESCRIBE EXPECTED SEQUENCE]

For each step:
1. Service responsible
2. Action to take
3. Success condition
4. Compensating action if failure
5. Timeout value

Choose between choreography and orchestration, explain why.
```

### Data Consistency Strategy

```
I need to maintain consistency across these services:
[LIST SERVICES AND SHARED DATA CONCEPTS]

Business requirements:
- Consistency level: [Strong/Eventual]
- Acceptable delay: [Time window]
- Recovery requirements: [What happens on failure]

Recommend:
1. Consistency pattern (saga, event sourcing, CQRS)
2. Implementation approach
3. Conflict resolution strategy
4. Monitoring requirements
```

## Infrastructure Prompts

### Service Mesh Decision

```
Should I use a service mesh for my architecture?

Current state:
- Number of services: [COUNT]
- Team size: [NUMBER]
- Kubernetes: [Yes/No]
- Current pain points: [LIST]

Evaluate:
1. Do I need a service mesh? Why/why not?
2. If yes, Linkerd vs Istio recommendation
3. Minimum viable service mesh features to start
4. Complexity vs benefit tradeoff
5. Migration path from current state
```

### Kubernetes Deployment Strategy

```
Design Kubernetes deployment for [SERVICE NAME].

Service characteristics:
- Language/Runtime: [e.g., Node.js, Go]
- Resource needs: [CPU/Memory patterns]
- Scaling requirements: [Min/Max pods, triggers]
- Dependencies: [Other services, databases]
- SLA: [Availability target]

Generate:
1. Deployment manifest with best practices
2. HPA configuration
3. PDB for availability
4. Resource requests/limits rationale
5. Health check endpoints needed
```

### Observability Setup

```
Design observability strategy for [SERVICE COUNT] microservices.

Current tools: [LIST ANY EXISTING TOOLS]
Budget constraints: [Any cost limits]
Team expertise: [Experience level]

Provide:
1. Logging strategy (format, aggregation, retention)
2. Metrics to collect (service-level, business-level)
3. Distributed tracing approach
4. Alert definitions for key SLOs
5. Dashboard recommendations
6. Tool recommendations with rationale
```

## Migration Prompts

### Monolith Decomposition

```
Help me extract [FEATURE/MODULE] from our monolith.

Current monolith:
- Technology: [STACK]
- Size: [LOC or modules]
- Team: [SIZE]

Module to extract:
- Functionality: [WHAT IT DOES]
- Current coupling: [WHAT IT DEPENDS ON]
- Data: [WHAT DATA IT USES]

Plan:
1. Extraction sequence (Strangler Fig approach)
2. Anti-corruption layer design
3. Data migration strategy
4. Traffic routing approach
5. Rollback plan
6. Success criteria
```

### Legacy Integration

```
Design integration between new [SERVICE] and legacy [SYSTEM].

Legacy system:
- Technology: [STACK]
- Interface: [How it communicates]
- Constraints: [What can't change]
- Data format: [Structure]

New service requirements:
- [LIST REQUIREMENTS]

Design:
1. Anti-corruption layer (ACL) pattern
2. Data transformation approach
3. Error handling
4. Sync vs async integration
5. Migration path when legacy is retired
```

## Review Prompts

### Architecture Review

```
Review my microservices architecture.

Services:
[LIST SERVICES WITH RESPONSIBILITIES]

Communication:
[DESCRIBE HOW THEY COMMUNICATE]

Data:
[DESCRIBE DATABASE STRATEGY]

Infrastructure:
[DESCRIBE DEPLOYMENT APPROACH]

Identify:
1. Potential anti-patterns (distributed monolith, shared DB, etc.)
2. Single points of failure
3. Scaling bottlenecks
4. Security concerns
5. Operational complexity risks

Rate architecture maturity (1-5) and suggest top 3 improvements.
```

### Failure Scenario Analysis

```
Analyze failure scenarios for my microservices architecture.

Architecture:
[DESCRIBE YOUR ARCHITECTURE]

For each service failure:
1. What breaks?
2. What's the blast radius?
3. How does system degrade?
4. What's the recovery path?

Also analyze:
- Database failures
- Message broker failures
- Network partitions
- Cascading failures

Recommend resilience improvements.
```

### Cost Optimization

```
Analyze cost optimization opportunities for my microservices.

Current setup:
- Cloud provider: [AWS/GCP/Azure]
- Services: [LIST WITH RESOURCE ALLOCATION]
- Traffic patterns: [Peak/off-peak]
- Current monthly cost: [AMOUNT]

Identify:
1. Over-provisioned resources
2. Right-sizing opportunities
3. Reserved instance candidates
4. Spot/preemptible opportunities
5. Architecture changes for cost reduction
6. Estimated savings for each recommendation
```

## Best Practices for LLM-Assisted Design

### Providing Context

Always include:
- Business domain description
- Team size and expertise
- Current technical constraints
- Scale expectations
- Timeline/urgency

### Iterative Refinement

```
[After receiving initial design]

I'd like to explore alternatives for [SPECIFIC ASPECT].

Current proposal: [WHAT LLM SUGGESTED]

Constraints I didn't mention:
- [ADDITIONAL CONSTRAINT 1]
- [ADDITIONAL CONSTRAINT 2]

Alternative approaches to consider:
- [ALTERNATIVE 1]
- [ALTERNATIVE 2]

Compare tradeoffs between original and alternatives.
```

### Validation Questions

```
Before implementing [DESIGN DECISION], validate:

1. What assumptions does this design make?
2. What happens if [ASSUMPTION] is wrong?
3. How would we migrate away if this doesn't work?
4. What's the minimum viable version?
5. What metrics would indicate this is failing?
```

## Related Files

- [README.md](README.md) - Architecture overview
- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Code templates

## External Resources

- [microservices.io](https://microservices.io/) - Chris Richardson's patterns
- [Building Microservices](https://samnewman.io/books/building_microservices_2nd_edition/) - Sam Newman
- [DDD Reference](https://www.domainlanguage.com/ddd/reference/) - Eric Evans
