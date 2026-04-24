# LLM Prompts for Architecture Workflows

Effective prompts for LLM-assisted architecture design, review, and documentation.

## Table of Contents

1. [System Design Prompts](#1-system-design-prompts)
2. [Architecture Review Prompts](#2-architecture-review-prompts)
3. [ADR Writing Prompts](#3-adr-writing-prompts)
4. [Technology Evaluation Prompts](#4-technology-evaluation-prompts)
5. [ATAM Assessment Prompts](#5-atam-assessment-prompts)
6. [Migration Planning Prompts](#6-migration-planning-prompts)
7. [Design Document Prompts](#7-design-document-prompts)

---

## 1. System Design Prompts

### Requirements Clarification

```
I'm designing a [system type] that needs to [primary function].

Help me identify:
1. Key functional requirements (5-7 core features)
2. Non-functional requirements with specific targets
3. Potential constraints to consider
4. Edge cases and failure scenarios

Context:
- Expected users: [number]
- Industry: [industry]
- Budget constraints: [yes/no/unknown]
```

### Scale Estimation

```
Help me estimate the scale for a system with:
- [X] daily active users
- [Y] actions per user per day
- [Z] bytes per record

Calculate:
1. Requests per second (average and peak)
2. Storage requirements (1 year, 5 years)
3. Bandwidth requirements
4. Any capacity concerns to flag

Show your calculations step by step.
```

### High-Level Design Generation

```
Design a high-level architecture for [system] with these requirements:
- Functional: [list requirements]
- Non-functional: [list requirements]
- Scale: [RPS, storage, users]

Provide:
1. C4 Container diagram (in Mermaid format)
2. List of major components with responsibilities
3. Data flow description
4. Technology recommendations for each component
5. Key design decisions with rationale
```

### Component Deep Dive

```
I'm designing the [component name] for [system type].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Provide detailed design including:
1. Internal architecture
2. Data model/schema
3. API contracts
4. Error handling strategy
5. Scaling considerations
6. Key design decisions
```

### Trade-off Analysis

```
I'm deciding between [Option A] and [Option B] for [component/decision].

Context:
- System requirements: [requirements]
- Constraints: [constraints]
- Team skills: [skills]

Analyze trade-offs across:
1. Performance
2. Scalability
3. Reliability
4. Complexity
5. Cost
6. Time to implement

Recommend one option with clear rationale.
```

### System Design Interview Preparation

```
Act as a senior software architect conducting a system design interview.

I need to design [system name, e.g., "a URL shortener like bit.ly"].

Guide me through the design process:
1. Start by asking clarifying questions
2. Help me estimate scale
3. Prompt me to draw high-level design
4. Ask probing questions about my choices
5. Point out potential issues
6. Suggest improvements

Behave like a real interviewer - don't give me the answer directly, help me discover it.
```

---

## 2. Architecture Review Prompts

### Architecture Analysis

```
Review this architecture description:

[Paste architecture description, diagrams, or documentation]

Analyze:
1. Strengths of the current design
2. Potential weaknesses or risks
3. Scalability concerns
4. Security considerations
5. Single points of failure
6. Recommendations for improvement

Format as a structured review report.
```

### Risk-Storming Facilitation

```
Help me conduct a risk-storming session for [system name].

Current architecture:
[Describe architecture]

For each major component, identify:
1. What could fail?
2. How likely is failure?
3. What's the blast radius?
4. How would we detect it?
5. How would we recover?

Categorize risks as: Critical, High, Medium, Low
```

### Quality Attribute Assessment

```
Assess this architecture against these quality attributes:

Architecture:
[Describe architecture]

Evaluate (1-5 scale with justification):
1. Performance: [target latency, throughput]
2. Scalability: [target load]
3. Availability: [target uptime]
4. Security: [key concerns]
5. Maintainability: [key concerns]
6. Testability: [key concerns]

For each, provide:
- Current capability estimate
- Gap analysis
- Improvement recommendations
```

### Design Review Questions

```
Generate design review questions for a [system type] architecture.

Focus areas:
- [Focus area 1]
- [Focus area 2]
- [Focus area 3]

Provide:
1. 5 critical questions (must be answered)
2. 5 probing questions (reveal hidden issues)
3. 5 forward-looking questions (future concerns)

For each question, explain what a good answer looks like.
```

### Architecture Anti-pattern Detection

```
Analyze this architecture for common anti-patterns:

[Paste architecture description]

Check for:
1. Distributed monolith
2. Chatty services
3. Shared database anti-pattern
4. Circular dependencies
5. God services
6. Lack of boundaries
7. Missing resilience patterns
8. Inadequate observability

For each detected issue, suggest remediation.
```

---

## 3. ADR Writing Prompts

### ADR Generation from Discussion

```
Create an ADR from this decision discussion:

[Paste meeting notes, Slack conversation, or decision summary]

Format as MADR with:
1. Title (clear, descriptive)
2. Status
3. Context and Problem Statement
4. Decision Drivers
5. Considered Options (with pros/cons)
6. Decision Outcome
7. Consequences (positive and negative)

Keep it concise but complete.
```

### ADR from Technical Decision

```
I've decided to use [technology/approach] for [problem/component].

Reasons:
- [Reason 1]
- [Reason 2]

Alternatives I considered:
- [Alternative 1]
- [Alternative 2]

Create a complete ADR in Nygard format that:
1. Explains the context clearly
2. States the decision definitively
3. Lists realistic consequences
4. Would be useful to someone reading it in 2 years
```

### ADR Review

```
Review this ADR for completeness and clarity:

[Paste ADR]

Check:
1. Is the context clear to someone unfamiliar with the project?
2. Is the decision stated clearly and definitively?
3. Are alternatives fairly represented?
4. Are consequences realistic (both positive and negative)?
5. Is the rationale convincing?
6. Are there missing considerations?

Suggest specific improvements.
```

### Superseding ADR

```
I need to write an ADR that supersedes [ADR-XXX].

Original decision: [describe original decision]
Why it's changing: [describe new context]
New decision: [describe new decision]

Create an ADR that:
1. References the original ADR
2. Explains what changed
3. Documents the new decision
4. Notes what happens to existing implementations
```

### ADR Backfill

```
We have an existing system with undocumented decisions. Help me backfill ADRs.

System: [describe system]
Known decisions:
1. [Decision 1]
2. [Decision 2]
3. [Decision 3]

For each decision:
1. Reconstruct likely context (what problem was being solved)
2. Infer alternatives that were probably considered
3. Document consequences we've observed
4. Flag any decisions that might need revisiting

Format as individual ADRs.
```

---

## 4. Technology Evaluation Prompts

### Technology Comparison

```
Compare [Technology A] vs [Technology B] for [use case].

Our requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Team context:
- Team size: [X]
- Existing experience: [technologies]
- Budget: [range]

Compare across:
1. Feature fit
2. Performance characteristics
3. Scalability
4. Learning curve
5. Community and support
6. Total cost of ownership
7. Risk factors

Recommend one with clear rationale.
```

### Evaluation Criteria Definition

```
I'm evaluating [technology category] options for [use case].

Help me define evaluation criteria:
1. Identify must-have requirements (deal-breakers)
2. Identify nice-to-have requirements
3. Suggest appropriate weights for each criterion
4. Define scoring rubric (what does 1-5 mean for each criterion)

Consider both technical and organizational factors.
```

### POC Scope Definition

```
I need to run a proof of concept for [technology] to evaluate it for [use case].

Key concerns to validate:
- [Concern 1]
- [Concern 2]

Help me define:
1. POC scope (what to build)
2. Success criteria (measurable)
3. Time box (recommended duration)
4. Risks to watch for
5. Go/no-go decision framework
```

### Vendor Evaluation

```
Evaluate these vendors/options for [category]:
- [Vendor/Option 1]
- [Vendor/Option 2]
- [Vendor/Option 3]

Requirements:
- [Requirement 1]
- [Requirement 2]

Create a comparison matrix including:
1. Feature comparison
2. Pricing models
3. Support options
4. Integration capabilities
5. Vendor stability/risk
6. Lock-in concerns
```

### TCO Analysis

```
Calculate total cost of ownership for [technology/approach].

Setup assumptions:
- Scale: [describe]
- Timeline: [X years]
- Team: [size and rates]

Include:
1. Infrastructure costs (compute, storage, network)
2. Licensing costs
3. Development effort (initial + ongoing)
4. Operations effort
5. Training costs
6. Opportunity costs
7. Hidden costs

Compare to [alternative] if applicable.
```

---

## 5. ATAM Assessment Prompts

### Quality Attribute Scenario Generation

```
Generate quality attribute scenarios for [system type].

Business context:
- [Context 1]
- [Context 2]

For each quality attribute (Performance, Availability, Security, Scalability, Modifiability), generate 2-3 scenarios in this format:

Source: [Who/what generates stimulus]
Stimulus: [What condition arrives]
Artifact: [What part is affected]
Environment: [Conditions when it occurs]
Response: [How system should respond]
Measure: [How to measure response]
Priority: (Importance, Difficulty)
```

### Utility Tree Creation

```
Create a quality attribute utility tree for [system].

Business goals:
- [Goal 1]
- [Goal 2]

Known constraints:
- [Constraint 1]
- [Constraint 2]

Build a utility tree with:
1. Quality attributes as first level
2. Refinements as second level
3. Specific scenarios as leaves
4. Priority ratings (H/M/L) for importance and difficulty

Focus on the most architecturally significant scenarios.
```

### Trade-off Point Analysis

```
Analyze trade-offs in this architecture:

[Describe architecture]

Identify where improving one quality attribute would harm another:
1. List each trade-off point
2. Explain the conflict
3. Describe how the current design balances it
4. Suggest alternative balances if applicable
5. Recommend how to document this for stakeholders
```

### Sensitivity Point Identification

```
Identify sensitivity points in this architecture:

[Describe architecture]

For each major component/decision:
1. Which quality attributes does it significantly impact?
2. How sensitive is the overall system to changes here?
3. What happens if this component fails or underperforms?
4. Are there alternative approaches with different sensitivity profiles?
```

### ATAM Risk Brainstorm

```
Brainstorm architectural risks for [system].

Current design:
[Describe architecture]

Quality requirements:
[List key quality attributes and targets]

Identify:
1. Risks (architectural decisions that might cause problems)
2. Non-risks (decisions that seem safe)
3. Risk themes (patterns across multiple risks)

For each risk:
- Severity (Critical/High/Medium/Low)
- Likelihood
- Mitigation options
```

---

## 6. Migration Planning Prompts

### Migration Strategy Selection

```
I need to migrate from [current state] to [target state].

Current system:
- [Describe current architecture]
- [Pain points]
- [Constraints]

Target system:
- [Describe target architecture]
- [Key benefits expected]

Help me choose between:
1. Strangler Fig (incremental)
2. Blue-Green (parallel)
3. Big Bang (complete switchover)

Consider: risk tolerance, team capacity, business continuity, timeline.
```

### Component Prioritization

```
Help me prioritize components for migration.

Components to migrate:
1. [Component A] - [brief description]
2. [Component B] - [brief description]
3. [Component C] - [brief description]
[etc.]

For each, assess:
- Business value of migrating
- Technical risk
- Dependencies on/from other components
- Effort estimate (T-shirt: S/M/L/XL)

Provide prioritized order with rationale.
```

### Migration Risk Assessment

```
Assess risks for migrating [component] from [old] to [new].

Current implementation:
[Describe]

Target implementation:
[Describe]

Identify risks in:
1. Data migration
2. Functionality parity
3. Performance impact
4. Integration points
5. Rollback complexity
6. Team capability

For each risk, suggest mitigation.
```

### Rollback Plan Generation

```
Create a rollback plan for migrating [component].

Migration approach:
[Describe migration steps]

Current traffic routing:
[Describe how traffic currently flows]

Define:
1. Rollback triggers (what conditions trigger rollback)
2. Rollback steps (specific actions)
3. Data reconciliation (if writes occurred)
4. Communication plan
5. Post-rollback actions
```

### Migration Validation Strategy

```
Define validation strategy for [component] migration.

Old system behavior:
[Describe expected behavior]

New system implementation:
[Describe implementation]

Create validation plan including:
1. Functional tests (happy path, edge cases)
2. Performance benchmarks
3. Comparison testing approach
4. Production validation (canary criteria)
5. Monitoring requirements
6. Success criteria for each migration phase
```

---

## 7. Design Document Prompts

### Design Document Outline

```
Create an outline for a design document for [feature/system].

Requirements:
- [Requirement 1]
- [Requirement 2]

Constraints:
- [Constraint 1]

Audience: [Who will read this]

Generate outline with:
1. All necessary sections
2. Key questions each section should answer
3. Suggested diagrams to include
4. Level of detail appropriate for audience
```

### Design Document Review

```
Review this design document:

[Paste design document]

Evaluate:
1. Completeness (are all necessary sections present?)
2. Clarity (can someone implement from this?)
3. Technical soundness (are the choices reasonable?)
4. Risks identified (are concerns addressed?)
5. Testability (is testing strategy clear?)

Provide feedback categorized as:
- Blocking (must fix before approval)
- Important (should fix)
- Minor (nice to fix)
- Questions (need clarification)
```

### Design Document from Requirements

```
Generate a technical design document from these requirements:

[Paste requirements or PRD]

Include:
1. Overview and goals
2. Non-goals (what's explicitly out of scope)
3. Proposed solution with architecture
4. Data model
5. API contracts
6. Security considerations
7. Testing strategy
8. Rollout plan
9. Open questions

Use diagrams where helpful (Mermaid format).
```

### Design Critique

```
Act as a senior architect reviewing this design:

[Paste design]

Provide critique:
1. What's good about this design?
2. What concerns do you have?
3. What questions would you ask the author?
4. What alternatives might be worth considering?
5. What risks should be called out?

Be constructive but thorough.
```

### Design Evolution Documentation

```
Document how this design has evolved:

Original design: [describe or paste]
Current design: [describe or paste]

Create documentation that:
1. Summarizes key changes
2. Explains why changes were made
3. Notes what we learned
4. Updates relevant ADRs
5. Flags any technical debt created
```

---

## Prompt Engineering Tips

### For Better Architecture Responses

1. **Provide Context**
   - Business goals and constraints
   - Scale requirements
   - Team capabilities
   - Existing systems

2. **Be Specific About Output**
   - Request specific formats (ADR, checklist, diagram)
   - Ask for reasoning, not just answers
   - Request trade-off analysis

3. **Iterate**
   - Start with high-level, then deep dive
   - Ask follow-up questions
   - Challenge recommendations

4. **Validate**
   - Ask LLM to critique its own output
   - Request alternative perspectives
   - Compare against known patterns

### Common Prompt Patterns

```
# For analysis:
"Analyze [X] for [concerns]. Consider [context]."

# For generation:
"Generate [artifact type] for [subject] given [requirements]."

# For comparison:
"Compare [A] vs [B] for [use case] across [criteria]."

# For review:
"Review [artifact] for [quality criteria]. Suggest improvements."

# For planning:
"Create a plan for [activity] considering [constraints]."
```

---

*Part of faion-software-architect skill*
