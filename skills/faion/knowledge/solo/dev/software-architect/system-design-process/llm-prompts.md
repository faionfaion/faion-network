# LLM Prompts for Architecture

Prompts for using LLMs (Claude, GPT, Gemini) in architecture discussions.

## Overview

LLMs are powerful architecture assistants when prompted correctly. This guide provides copy-paste prompts for common architecture tasks.

**Key Principles:**
1. **Provide context first** - system description, constraints, scale
2. **Ask for structured output** - tables, lists, diagrams
3. **Request trade-offs** - pros/cons for every recommendation
4. **Verify with domain knowledge** - LLMs can hallucinate patterns

---

## Requirements Gathering

### Clarifying Questions Prompt

```
I'm designing a [system type] that [brief description].

Act as a senior solutions architect. Ask me clarifying questions to understand:
1. Functional requirements (what it does)
2. Non-functional requirements (scale, latency, availability)
3. Constraints (budget, timeline, team skills)
4. Integration points (external systems)

Ask questions one category at a time. Start with functional requirements.
```

### NFR Checklist Prompt

```
I'm designing a [system description].

Generate a non-functional requirements checklist with:
- Each quality attribute (scalability, availability, latency, security, etc.)
- Specific questions to ask stakeholders
- Typical target values for a [startup/enterprise/high-scale] system
- How to measure each attribute

Format as a table with columns: Attribute | Questions | Typical Targets | Metrics
```

### Scale Estimation Prompt

```
I'm building a [system type] for [use case].

Expected users: [number] DAU
Usage pattern: [description]

Calculate back-of-envelope estimates for:
1. Requests per second (average and peak)
2. Storage growth per day/month/year
3. Bandwidth requirements
4. Cache size recommendations

Show your calculations step by step.
```

---

## Architecture Design

### Architecture Options Prompt

```
System: [description]
Requirements:
- [FR1]
- [FR2]
Scale: [users/RPS/data volume]
Constraints: [budget/team/timeline]

Propose 3 different architecture approaches:
1. Simple/MVP approach
2. Balanced approach
3. Enterprise-grade approach

For each approach, provide:
- Architecture diagram (describe or use ASCII)
- Key components and their responsibilities
- Technology recommendations
- Pros and cons
- When to choose this approach
```

### Database Selection Prompt

```
I need to select a database for [use case].

Data characteristics:
- Volume: [size]
- Read/write ratio: [ratio]
- Query patterns: [description]
- Consistency requirements: [strong/eventual]
- Data structure: [relational/document/key-value/time-series/graph]

Compare the top 3 database options for this use case.
Format as a table: Database | Strengths | Weaknesses | Cost | Scaling Approach

Recommend one option with justification.
```

### Communication Pattern Prompt

```
I have services that need to communicate:
- Service A: [description]
- Service B: [description]
- Requirements: [latency/reliability/ordering]

Compare these communication patterns:
1. Synchronous REST
2. Synchronous gRPC
3. Asynchronous message queue
4. Event streaming (Kafka)

Which pattern fits best? Consider:
- Latency requirements
- Failure handling
- Coupling level
- Debugging complexity
```

### Caching Strategy Prompt

```
System: [description]
Problem: [latency/database load/etc.]

Data patterns:
- Hot data: [% that's frequently accessed]
- Read/write ratio: [ratio]
- Consistency tolerance: [can we serve stale data?]
- Data size: [typical object size]

Recommend a caching strategy:
1. Cache placement (client/CDN/application/database)
2. Cache pattern (cache-aside/read-through/write-through)
3. Eviction policy
4. TTL recommendations
5. Cache invalidation approach

Include Mermaid diagram showing data flow.
```

---

## Trade-off Analysis

### Technology Comparison Prompt

```
I'm choosing between [Option A] and [Option B] for [use case].

Context:
- [Relevant context]
- [Constraints]

Create a detailed comparison:
1. Feature comparison table
2. Performance characteristics
3. Operational complexity
4. Cost analysis
5. Team skill requirements
6. Vendor lock-in risk
7. Community/ecosystem

Conclude with a recommendation and when I might choose the other option.
```

### CAP Theorem Analysis Prompt

```
System: [description]
Requirements:
- Consistency need: [description]
- Availability need: [description]
- Partition scenario: [what happens during network issues]

Analyze this system through CAP theorem:
1. Which two properties should we prioritize?
2. What compromises does this require?
3. How do we handle the sacrificed property?
4. What does graceful degradation look like?

Provide specific examples of user-visible behavior.
```

### Cost-Latency-Reliability Triangle Prompt

```
System: [description]
Current state:
- Cost: [budget]
- Latency: [current p95]
- Reliability: [current SLA]

I want to improve [property] while maintaining others.

Analyze trade-offs:
1. What can we sacrifice to improve [property]?
2. What architectural changes are needed?
3. What's the expected improvement?
4. What are the risks?

Present options from conservative to aggressive.
```

---

## Risk Analysis

### Failure Mode Analysis Prompt

```
System architecture:
[Describe components and their connections]

For each component, analyze:
1. What happens if it fails?
2. What's the blast radius?
3. How is the failure detected?
4. What's the recovery process?
5. What's the MTTR expectation?

Format as a table: Component | Failure Mode | Impact | Detection | Recovery | MTTR

Identify the top 3 risks and recommend mitigations.
```

### Bottleneck Identification Prompt

```
System: [description]
Current scale: [metrics]
Target scale: [metrics]

Architecture:
[Describe current architecture]

Identify potential bottlenecks:
1. Database bottlenecks
2. Network bottlenecks
3. Compute bottlenecks
4. Third-party dependencies

For each bottleneck:
- At what scale does it become a problem?
- What are the warning signs?
- What's the mitigation strategy?

Prioritize by likelihood and impact.
```

### Security Threat Model Prompt

```
System: [description]
Data sensitivity: [PII/financial/healthcare/general]
Attack surface: [web/mobile/API/internal]

Create a threat model using STRIDE:
- Spoofing
- Tampering
- Repudiation
- Information disclosure
- Denial of service
- Elevation of privilege

For each threat category:
1. Specific attack scenarios
2. Likelihood (High/Medium/Low)
3. Impact (High/Medium/Low)
4. Recommended controls

Focus on the top 5 threats by risk score.
```

---

## Documentation Generation

### ADR Generation Prompt

```
Decision: [what we decided]
Context: [why we needed to decide]
Options considered:
1. [Option A]
2. [Option B]
3. [Option C]

Generate an Architecture Decision Record (ADR) in MADR format including:
- Status
- Context (expanded)
- Decision with rationale
- Alternatives with pros/cons table
- Consequences (positive, negative, neutral)
```

### C4 Diagram Prompt

```
System: [description]
Components:
- [Component 1]: [responsibility]
- [Component 2]: [responsibility]
External systems:
- [External 1]: [integration point]

Generate Mermaid C4 diagrams:
1. C4Context - System context showing users and external systems
2. C4Container - Internal containers (services, databases, queues)

Use proper C4 notation: Person, System, System_Ext, Container, ContainerDb, ContainerQueue
Include Rel() for all connections with labels.
```

### API Design Prompt

```
Feature: [description]
Entities: [list of entities]
Operations: [CRUD + custom operations]

Design a REST API:
1. Resource naming (nouns, plurals)
2. HTTP methods for each operation
3. URL structure
4. Request/response schemas (JSON)
5. Error response format
6. Pagination approach
7. Versioning strategy

Format as OpenAPI-style documentation.
```

---

## Review Prompts

### Architecture Review Prompt

```
Review this architecture for [system type]:

[Paste architecture description or diagram]

Requirements:
- [NFR1]
- [NFR2]

Evaluate:
1. Does it meet the stated requirements?
2. What are the single points of failure?
3. What are the scaling bottlenecks?
4. What security concerns exist?
5. What operational complexity issues exist?
6. What would you change?

Rate overall architecture: 1-10 with justification.
```

### Design Document Review Prompt

```
Review this design document:

[Paste design document]

Check for:
1. Completeness - are all sections adequately covered?
2. Clarity - is it understandable by the intended audience?
3. Feasibility - can this be built as described?
4. Risks - are risks identified and mitigated?
5. Alternatives - were alternatives fairly considered?
6. Gaps - what's missing?

Provide specific, actionable feedback.
```

### Code Architecture Alignment Prompt

```
Design document states:
[Paste relevant architecture sections]

Actual code structure:
[Paste directory structure or key code patterns]

Analyze alignment:
1. Where does implementation match design?
2. Where does implementation deviate?
3. Are deviations improvements or regressions?
4. What ADRs should be created for deviations?

Focus on architectural concerns, not code style.
```

---

## Iteration Prompts

### Refine Architecture Prompt

```
Current architecture:
[Describe current state]

Problem: [What's not working]

Constraints:
- Must maintain backward compatibility
- Budget: [limit]
- Timeline: [limit]

Propose incremental improvements:
1. Quick wins (can do this week)
2. Medium-term improvements (this quarter)
3. Long-term evolution (this year)

For each, estimate effort vs impact.
```

### Migration Planning Prompt

```
Current state:
- Architecture: [description]
- Tech stack: [current stack]
- Data: [volume and location]

Target state:
- Architecture: [description]
- Tech stack: [target stack]

Constraints:
- Zero downtime required: [yes/no]
- Rollback capability: [yes/no]
- Team size: [number]

Create a migration plan:
1. Phase breakdown
2. Dependencies between phases
3. Rollback strategy for each phase
4. Risk mitigation for each phase
5. Validation criteria

Use strangler fig pattern where applicable.
```

---

## Meta-Prompts

### Architecture Persona Setup

Use this at the start of architecture conversations:

```
You are a senior solutions architect with 15+ years of experience designing
distributed systems. You have worked at both startups and large enterprises.

Your approach:
1. Always ask clarifying questions before designing
2. Consider operational complexity, not just technical elegance
3. Prefer boring technology unless there's a compelling reason
4. Think about the team that will maintain this
5. Balance ideal solutions with pragmatic constraints

When I describe a system, help me think through the architecture systematically.
Start by summarizing your understanding and asking clarifying questions.
```

### Specification Development

For iterative spec building:

```
I'm building [system description].

Help me develop a complete specification. Ask me questions iteratively until
we've covered:
1. User personas and their goals
2. Core features (must-have vs nice-to-have)
3. Data model and relationships
4. Non-functional requirements
5. Integration points
6. Constraints and assumptions

After each answer, summarize what we've established and ask the next question.
When complete, compile everything into a structured spec.md document.
```

---

## Tips for Effective Prompts

### Do

- Provide specific numbers (users, RPS, data size)
- State constraints explicitly (budget, team, timeline)
- Ask for structured output (tables, lists, diagrams)
- Request trade-offs and alternatives
- Ask for reasoning, not just answers

### Don't

- Ask open-ended "design X for me" without context
- Accept first answer without probing trade-offs
- Assume LLM knows your domain-specific constraints
- Skip validation against your actual requirements
- Trust cost estimates without verification

### Iteration Pattern

```
1. Initial prompt with context
2. Ask "what are the trade-offs?"
3. Ask "what could go wrong?"
4. Ask "what alternatives did you consider?"
5. Ask "how would this change at 10x scale?"
6. Ask "what would you do differently with [constraint]?"
```

---

## References

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Addy Osmani's LLM Coding Workflow](https://addyo.substack.com/p/my-llm-coding-workflow-going-into)
- [Martin Fowler on LLM Engineering Practices](https://martinfowler.com/articles/engineering-practices-llm.html)
- [Eugene Yan's LLM Patterns](https://eugeneyan.com/writing/llm-patterns/)
