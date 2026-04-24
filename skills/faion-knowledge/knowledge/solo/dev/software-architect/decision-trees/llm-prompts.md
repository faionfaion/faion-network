# LLM Prompts for Architecture Decisions

Effective prompts for using LLMs (Claude, GPT-4, Gemini) to assist with architecture decision making. Each prompt is designed to produce structured, actionable output.

---

## How to Use These Prompts

### Best Practices

1. **Provide context** - Always include team size, budget, existing stack
2. **Be specific** - Vague questions get vague answers
3. **Ask for structure** - Request tables, decision trees, pros/cons
4. **Verify externally** - LLMs may have outdated pricing or features
5. **Iterate** - Use follow-up prompts to dive deeper

### Prompt Structure

```
[Context/Background]
[Specific Question]
[Desired Output Format]
[Constraints/Requirements]
```

---

## Architecture Style Decision Prompts

### Prompt 1: Architecture Style Selection

```
I need help deciding on an architecture style for a new project.

**Context:**
- Company: [Company name/type]
- Product: [Brief product description]
- Team size: [Number of developers]
- Current DevOps maturity: [Low/Medium/High - describe CI/CD, monitoring capabilities]
- Budget: [Rough budget or constraints]
- Timeline: [Deadline or time constraints]
- Expected scale: [Users, requests/second, data volume]

**Question:**
Should we use a Monolith, Modular Monolith, or Microservices architecture?

**Please provide:**
1. A decision tree analysis based on our context
2. Recommendation with clear rationale
3. Pros and cons for top 2 options
4. Risk factors and mitigation strategies
5. Migration path if we need to evolve later
```

### Prompt 2: Monolith to Microservices Assessment

```
We're considering migrating from a monolith to microservices.

**Current State:**
- Monolith size: [Lines of code, number of modules]
- Team size: [Number of developers]
- Deployment frequency: [How often we deploy]
- Pain points: [What problems we're trying to solve]
- DevOps capabilities: [CI/CD, monitoring, K8s experience]

**Questions:**
1. Are we ready for microservices? What's missing?
2. Which services should be extracted first?
3. What's the recommended migration approach (strangler fig, parallel run, etc.)?
4. What infrastructure investments are needed?
5. What are the expected benefits and when will we see them?

Please provide a phased migration plan with specific recommendations.
```

### Prompt 3: Modular Monolith Design

```
Help me design a modular monolith architecture.

**Product:** [Product description]

**Domain Areas:**
- [Domain 1]: [Brief description]
- [Domain 2]: [Brief description]
- [Domain 3]: [Brief description]

**Tech Stack:** [Language, framework]

**Please provide:**
1. Recommended module structure with boundaries
2. Communication patterns between modules (sync vs async, events)
3. Database strategy (shared vs separate schemas)
4. Code organization and folder structure
5. Tools for enforcing module boundaries
6. Criteria for when to extract a module to a service
```

---

## Technology Selection Prompts

### Prompt 4: Tech Stack Evaluation

```
Help me evaluate technology options for [specific need].

**Context:**
- Project type: [Web app, API, mobile, etc.]
- Team expertise: [List current skills]
- Performance requirements: [Latency, throughput targets]
- Scale expectations: [Users, data volume, growth]
- Budget: [Cost constraints]
- Timeline: [Deadline]

**Options I'm considering:**
1. [Option 1]
2. [Option 2]
3. [Option 3]

**Please provide:**
1. Comparison table with key criteria
2. Decision matrix with weighted scores
3. Your recommendation with rationale
4. Hidden gotchas or considerations I might miss
5. Learning resources for the recommended option
```

### Prompt 5: Framework Selection

```
I need to choose a [frontend/backend/mobile] framework.

**Requirements:**
- Type: [SPA, SSR, API, etc.]
- SEO importance: [Critical/Not important]
- Real-time features: [Yes/No, describe]
- Integrations needed: [List key integrations]
- Team background: [Current skills and experience]
- Performance targets: [Specific metrics]

**Constraints:**
- Must support: [Specific features]
- Cannot use: [Any excluded options]
- Budget for tools/hosting: [Amount]

Please create a decision tree and recommend the best framework with detailed justification.
```

### Prompt 6: Language Selection for New Service

```
We're building a new service and need to choose a programming language.

**Service Purpose:** [What the service does]

**Requirements:**
- Performance: [Latency/throughput needs]
- Concurrency: [Number of concurrent operations]
- Team skills: [Current language expertise]
- Ecosystem needs: [Required libraries, integrations]
- Deployment: [Container, serverless, VM]

**Current Stack:** [What we already use]

**Please provide:**
1. Top 3 language recommendations with pros/cons
2. Performance comparison for our use case
3. Ecosystem assessment (libraries, tools)
4. Team ramp-up time estimates
5. Long-term maintainability considerations
```

---

## Database Selection Prompts

### Prompt 7: Database Selection

```
Help me select a database for [application/feature].

**Data Characteristics:**
- Data model: [Relational, document, key-value, time-series, graph]
- Write volume: [Writes per second]
- Read volume: [Reads per second]
- Data size: [Current and projected]
- Query patterns: [Simple lookups, complex joins, aggregations, full-text search]
- Consistency requirements: [Strong, eventual]

**Non-Functional Requirements:**
- Latency: [Target p95/p99]
- Availability: [Target uptime]
- Durability: [Data loss tolerance]

**Constraints:**
- Budget: [Monthly budget]
- Team expertise: [What databases team knows]
- Cloud provider: [AWS/Azure/GCP/On-prem]

Please provide a decision tree analysis and recommendation with specific product suggestions.
```

### Prompt 8: Multi-Database Strategy

```
We're designing a system that may need multiple databases.

**Use Cases:**
1. [Use case 1]: [Data type, access pattern, volume]
2. [Use case 2]: [Data type, access pattern, volume]
3. [Use case 3]: [Data type, access pattern, volume]

**Questions:**
1. Which databases should we use for each use case?
2. How should data flow between databases?
3. How do we handle transactions across databases?
4. What's the operational complexity of this approach?
5. Is there a simpler single-database solution?

Please provide a data architecture diagram with database recommendations.
```

---

## Cloud Provider Selection Prompts

### Prompt 9: Cloud Provider Comparison

```
Help me choose between AWS, Azure, and GCP for our workload.

**Workload Type:** [Web app, data analytics, ML, etc.]

**Requirements:**
- Regions needed: [Geographic requirements]
- Compliance: [PCI, HIPAA, SOC2, etc.]
- Existing investments: [Microsoft licenses, Google Workspace, etc.]
- Key services needed: [Kubernetes, serverless, databases, ML]

**Team Expertise:**
- AWS experience: [None/Some/Expert]
- Azure experience: [None/Some/Expert]
- GCP experience: [None/Some/Expert]

**Budget Sensitivity:** [High/Medium/Low]

Please provide:
1. Feature comparison for our specific needs
2. Cost comparison for estimated workload
3. Pros/cons for each provider
4. Your recommendation with justification
5. Migration/lock-in considerations
```

### Prompt 10: Multi-Cloud Strategy Assessment

```
We're considering a multi-cloud strategy.

**Current State:**
- Primary cloud: [Current provider]
- Workloads: [What runs where]
- Pain points: [Why considering multi-cloud]

**Goals:**
- [Goal 1: e.g., avoid vendor lock-in]
- [Goal 2: e.g., best-of-breed services]
- [Goal 3: e.g., disaster recovery]

**Questions:**
1. Is multi-cloud right for us, or is the complexity not worth it?
2. If yes, what's the recommended approach (active-active, DR, best-of-breed)?
3. How do we manage networking, identity, and data across clouds?
4. What tools and practices do we need?
5. What's the cost and operational overhead?

Please provide an honest assessment with specific recommendations.
```

---

## Build vs Buy Prompts

### Prompt 11: Build vs Buy Analysis

```
Help me decide whether to build or buy [capability/feature].

**Capability Needed:** [Detailed description]

**Requirements:**
- Functional: [List key features needed]
- Non-functional: [Performance, security, compliance]
- Integration: [What systems it needs to connect to]
- Customization: [How much customization is needed]

**Team Context:**
- Team size: [Developers available]
- Relevant expertise: [Skills match]
- Current priorities: [What else team is working on]

**Business Context:**
- Strategic importance: [Is this a differentiator?]
- Timeline: [When do we need this?]
- Budget: [Available budget]

**Commercial Options Considered:**
1. [Product 1]: [Price range]
2. [Product 2]: [Price range]
3. [Product 3]: [Price range]

Please provide:
1. Build effort estimate (team, time, cost)
2. Buy cost comparison (3-year TCO)
3. Weighted decision matrix
4. Risk analysis for each option
5. Your recommendation with confidence level
```

### Prompt 12: Vendor Evaluation

```
Help me evaluate vendors for [category].

**Our Requirements:**
- Must have: [Critical features]
- Nice to have: [Desired features]
- Deal breakers: [Non-negotiables]

**Vendors to Evaluate:**
1. [Vendor 1]
2. [Vendor 2]
3. [Vendor 3]

**Evaluation Criteria:**
- Features/Functionality
- Pricing model
- Support quality
- Integration capabilities
- Security/Compliance
- Company stability
- [Any other criteria]

Please create a detailed comparison matrix and provide a recommendation.
```

---

## API Design Prompts

### Prompt 13: API Style Selection

```
Help me choose an API style for [use case].

**Context:**
- Consumers: [Who will use the API - internal, external, frontend]
- Data complexity: [Simple CRUD, complex nested data, etc.]
- Performance needs: [Latency, throughput requirements]
- Real-time requirements: [Streaming, subscriptions, webhooks]

**Current Stack:**
- Backend: [Languages, frameworks]
- Frontend: [If applicable]
- Existing APIs: [What styles already in use]

**Questions:**
1. Should we use REST, GraphQL, gRPC, or a combination?
2. How should we handle versioning?
3. What authentication/authorization approach?
4. How should we handle errors and pagination?

Please provide an API design recommendation with examples.
```

---

## Decision Documentation Prompts

### Prompt 14: Generate ADR

```
Help me write an Architecture Decision Record.

**Decision:** [What was decided]

**Context:**
[Background information, what prompted this decision]

**Options Considered:**
1. [Option 1]
2. [Option 2]
3. [Option 3]

**Decision Rationale:**
[Why we chose what we chose]

**Known Trade-offs:**
[What we're accepting]

Please generate a complete ADR in MADR format, including:
- Status
- Context
- Decision Drivers
- Considered Options with pros/cons
- Decision Outcome
- Consequences (positive and negative)
```

### Prompt 15: Decision Review

```
Review this architecture decision and identify potential issues.

**Decision:** [Paste the decision or ADR]

**Context:**
- Team size: [Size]
- Stage: [Startup/Growth/Enterprise]
- Industry: [Industry]

**Please analyze:**
1. Are there any red flags or anti-patterns?
2. What assumptions might be wrong?
3. What risks weren't considered?
4. What alternatives should have been explored?
5. What questions should we have asked?
6. Is this decision reversible, and what's the cost to change later?
```

---

## Trade-off Analysis Prompts

### Prompt 16: Trade-off Analysis

```
Help me analyze the trade-offs for [decision].

**Options:**
1. [Option 1]
2. [Option 2]

**Quality Attributes to Consider:**
- Performance
- Scalability
- Security
- Maintainability
- Cost
- Time to market
- [Add any others relevant]

**Constraints:**
- [Constraint 1]
- [Constraint 2]

Please provide:
1. Trade-off matrix showing how each option affects each quality attribute
2. Sensitivity analysis - which trade-offs matter most for our context
3. Risk assessment for each option
4. Recommendation with confidence level
```

### Prompt 17: Technical Debt Assessment

```
Evaluate whether this technical decision will create technical debt.

**Proposed Decision:** [Description]

**Context:**
- Why we're considering this: [Drivers]
- Time pressure: [Deadline]
- Alternative approaches: [What else we could do]

**Questions:**
1. Is this creating technical debt, or is it a reasonable trade-off?
2. If it's debt, what's the "interest rate" (ongoing cost)?
3. When should we pay it back?
4. What's the cost of paying it back later vs doing it right now?
5. What guardrails can we put in place to prevent it from getting worse?
```

---

## Follow-up Prompt Templates

### Diving Deeper

```
Thanks for that analysis. I'd like to explore [specific aspect] further.

Specifically:
1. [Detailed question 1]
2. [Detailed question 2]
3. [Detailed question 3]

Please provide more detail on these points.
```

### Challenging Assumptions

```
Your recommendation was [recommendation], but I'm concerned about [concern].

Can you:
1. Address this specific concern
2. Explain what would change if [alternative assumption]
3. Provide evidence or case studies supporting your recommendation
4. Describe scenarios where your recommendation would be wrong
```

### Getting Implementation Details

```
I've decided to go with [decision]. Now help me with implementation.

Please provide:
1. Step-by-step implementation plan
2. Key decisions during implementation
3. Common pitfalls to avoid
4. Success metrics to track
5. Timeline milestones
```

---

## Prompts for Specific Decisions

### Prompt 18: Microservices Decomposition

```
Help me decompose a monolith into microservices.

**Current Monolith:**
- Size: [Lines of code, modules]
- Domains: [List major domains/features]
- Pain points: [Why decomposing]

**Please provide:**
1. Recommended service boundaries based on domain-driven design
2. Priority order for extraction (start with which service?)
3. Communication patterns between services
4. Data ownership and synchronization strategy
5. Shared libraries vs duplication trade-offs
```

### Prompt 19: Event-Driven Architecture Design

```
Help me design an event-driven architecture for [system].

**Use Case:** [What the system does]

**Events to Handle:**
- [Event 1]: [Description, volume, latency needs]
- [Event 2]: [Description, volume, latency needs]
- [Event 3]: [Description, volume, latency needs]

**Requirements:**
- Ordering: [Is order important?]
- Exactly-once: [Is it required?]
- Retention: [How long to keep events?]

**Questions:**
1. What event broker should we use (Kafka, RabbitMQ, SQS, etc.)?
2. What event schema format (JSON, Avro, Protobuf)?
3. How should we handle failures and retries?
4. How should we do event versioning?
5. What monitoring and observability do we need?
```

### Prompt 20: Caching Strategy

```
Help me design a caching strategy for [application].

**Current Situation:**
- Database: [Type, current load]
- Read/write ratio: [e.g., 90/10]
- Hot data: [What data is accessed most]
- Latency requirements: [Target p95]

**Questions:**
1. What should we cache (and what should we NOT cache)?
2. What caching pattern should we use (cache-aside, write-through, etc.)?
3. What's the right TTL strategy?
4. How do we handle cache invalidation?
5. What cache technology should we use?

Please provide a caching architecture with specific recommendations.
```

---

## Quick Reference: Prompt Patterns

### Decision Prompt Pattern

```
Help me decide [specific decision].

**Context:** [Background]
**Options:** [List options]
**Constraints:** [Limitations]
**Criteria:** [What matters]

Please provide: [Desired output format]
```

### Analysis Prompt Pattern

```
Analyze [specific thing].

**Details:** [Information about the thing]
**Questions:**
1. [Specific question]
2. [Specific question]

Please provide: [Desired output format]
```

### Design Prompt Pattern

```
Help me design [specific system/component].

**Requirements:** [What it needs to do]
**Constraints:** [Limitations]
**Existing Context:** [What already exists]

Please provide: [Architecture diagram, code structure, etc.]
```

---

*LLM Prompts for Architecture Decisions v2.0 - Updated January 2026*
