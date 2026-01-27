# LLM Prompts for Design Patterns

Effective prompts for LLM-assisted pattern selection, implementation, and review.

## Pattern Selection Prompts

### General Pattern Selection

```
I need to design a solution for [PROBLEM DESCRIPTION].

Context:
- Language/Framework: [e.g., Python/FastAPI, TypeScript/React]
- Scale: [users, requests/sec, data volume]
- Team size: [number of developers]
- Constraints: [performance, memory, testability requirements]

Current implementation has these issues:
- [Issue 1]
- [Issue 2]

Suggest appropriate design patterns and explain:
1. Why each pattern fits this problem
2. Trade-offs of each approach
3. Which pattern you recommend and why
4. Potential anti-patterns to avoid
```

### Creational Pattern Selection

```
I need to create objects with these characteristics:
- [Object complexity: simple/complex]
- [Number of parameters: few/many]
- [Variations: single type/multiple types/family of types]
- [Creation frequency: rare/frequent]
- [Lifecycle: shared instance/new instance each time]

Current approach:
[Describe current object creation code]

Problems with current approach:
- [Problem 1]
- [Problem 2]

Recommend a creational pattern (Factory Method, Abstract Factory, Builder, Prototype, Singleton, or Dependency Injection) and explain your reasoning.
```

### Structural Pattern Selection

```
I have these components that need to work together:
- Component A: [description and interface]
- Component B: [description and interface]

The integration challenge is:
- [e.g., incompatible interfaces, need to add behavior, complex subsystem]

Requirements:
- [Requirement 1]
- [Requirement 2]

Recommend a structural pattern (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, or Proxy) and show how to implement it.
```

### Behavioral Pattern Selection

```
I need to manage this behavior:
- [Describe the behavior or algorithm]

The behavior needs to:
- [ ] Vary at runtime
- [ ] Notify other components of changes
- [ ] Be encapsulated as an object
- [ ] Change based on state
- [ ] Pass through multiple handlers

Current code structure:
[Code snippet or description]

Recommend a behavioral pattern and explain how it solves the problem.
```

## Implementation Prompts

### Pattern Implementation

```
Implement the [PATTERN NAME] pattern for [USE CASE] in [LANGUAGE].

Requirements:
- [Specific requirement 1]
- [Specific requirement 2]

Constraints:
- Follow [coding standards/style guide]
- Include type hints/annotations
- Make it testable
- Follow SOLID principles

Provide:
1. Interface/abstract class definitions
2. Concrete implementations
3. Usage example
4. Unit test example
```

### Pattern Refactoring

```
Refactor this code to use the [PATTERN NAME] pattern:

```[language]
[Current code that needs refactoring]
```

The current code has these problems:
- [Problem 1: e.g., tight coupling]
- [Problem 2: e.g., hard to test]
- [Problem 3: e.g., violates OCP]

Requirements for refactored code:
- Maintain backward compatibility
- Add no external dependencies
- Keep the public API unchanged

Show:
1. Step-by-step refactoring plan
2. Final refactored code
3. Before/after comparison of testability
```

### Multi-Pattern Implementation

```
Design a [FEATURE/SYSTEM] that combines multiple patterns:

Feature requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

I'm considering these patterns:
- [Pattern 1] for [reason]
- [Pattern 2] for [reason]

Questions:
1. Do these patterns work well together?
2. Are there better pattern combinations?
3. How should the patterns interact?
4. What's the implementation order?

Provide a design showing how the patterns integrate.
```

## Code Review Prompts

### Pattern Correctness Review

```
Review this implementation of the [PATTERN NAME] pattern:

```[language]
[Code to review]
```

Check for:
1. Does it correctly implement the pattern's intent?
2. Are there any anti-patterns or misuse?
3. Is it over-engineered or under-engineered?
4. Does it follow the language's idioms?
5. Are there edge cases not handled?

Provide specific improvement suggestions with code examples.
```

### Anti-Pattern Detection

```
Review this code for design pattern anti-patterns:

```[language]
[Code to review]
```

Look for:
- God Object / God Class
- Singleton abuse
- Anemic Domain Model
- Poltergeist / Unnecessary abstraction
- Golden Hammer (forcing patterns where not needed)
- Speculative Generality
- Pattern-itis (overuse of patterns)

For each issue found:
1. Explain why it's problematic
2. Suggest a fix with code example
```

### Architecture Review with Patterns

```
Review this architecture for appropriate pattern usage:

System overview:
[Architecture description or diagram]

Components:
- [Component 1]: [responsibility]
- [Component 2]: [responsibility]

Current patterns used:
- [Pattern 1] in [Component]
- [Pattern 2] in [Component]

Questions:
1. Are the current patterns appropriate?
2. Are there missing patterns that would improve the design?
3. Are any patterns redundant or adding unnecessary complexity?
4. How well do the patterns support the quality attributes (scalability, maintainability, testability)?
```

## Trade-off Analysis Prompts

### Pattern Comparison

```
Compare these patterns for [USE CASE]:

Option A: [Pattern 1]
Option B: [Pattern 2]
Option C: [Pattern 3]

Context:
- [Relevant context about the system]
- [Team experience level]
- [Performance requirements]

Create a comparison table with:
- Complexity (implementation effort)
- Flexibility (ease of extension)
- Performance impact
- Testability
- Maintainability

Recommend the best option with justification.
```

### When NOT to Use a Pattern

```
I'm considering using [PATTERN NAME] for [USE CASE].

Current implementation:
[Simple code that might not need a pattern]

Convince me whether this pattern is:
1. Necessary and beneficial
2. Over-engineering for this case
3. Might be needed later as the system grows

Provide criteria for when this pattern becomes worth the complexity.
```

## Distributed System Pattern Prompts

### Resilience Patterns

```
Design resilience patterns for this distributed system:

Services:
- [Service 1]: [description]
- [Service 2]: [description]

Communication:
- [Sync/Async]
- [Protocol: REST/gRPC/events]

Failure scenarios to handle:
- [Scenario 1: e.g., Service B is slow]
- [Scenario 2: e.g., Service C is down]

Implement these patterns:
1. Circuit Breaker with appropriate thresholds
2. Retry with backoff strategy
3. Fallback responses
4. Bulkhead isolation

Show how they work together in code.
```

### Data Consistency Patterns

```
Design a data consistency strategy for:

Operation: [e.g., "Create order that involves inventory, payment, and shipping"]

Services involved:
1. [Service 1] - owns [data]
2. [Service 2] - owns [data]
3. [Service 3] - owns [data]

Requirements:
- [Consistency requirement: eventual/strong]
- [Failure handling: rollback/compensate]

Design using:
- Saga pattern (orchestration or choreography)
- Outbox pattern for reliable events
- Idempotency handling

Provide sequence diagram and code implementation.
```

## Modern Pattern Prompts

### Cloud-Native Patterns

```
Recommend cloud-native patterns for:

Application type: [e.g., API service, event processor, scheduled job]

Requirements:
- Scale to [X] requests/second
- [X]% availability target
- Deploy to [Kubernetes/serverless/containers]

Address these concerns:
1. Service discovery
2. Configuration management
3. Secrets handling
4. Observability
5. Auto-scaling

For each concern, recommend a pattern and implementation approach.
```

### Event-Driven Patterns

```
Design an event-driven architecture for [SYSTEM]:

Events to handle:
- [Event 1]: [producer] -> [consumers]
- [Event 2]: [producer] -> [consumers]

Requirements:
- Event ordering: [required/not required]
- Delivery guarantee: [at-most-once/at-least-once/exactly-once]
- Event storage: [required for replay/not required]

Include:
1. Event schema design (CloudEvents format)
2. Producer pattern
3. Consumer pattern
4. Dead letter handling
5. Event versioning strategy
```

## Quick Reference Prompts

### "Help me decide" prompts

```
# Quick pattern recommendation
For [brief description], which pattern: [Pattern A] or [Pattern B]?

# Pattern applicability check
Does [Pattern Name] make sense for [brief use case]?

# Simple implementation
Show minimal [Pattern Name] in [Language] for [use case].

# Common mistake check
What are common mistakes when implementing [Pattern Name]?
```

### Problem-to-pattern mapping

```
Match this problem to the right pattern:

Problem: [One sentence description]

Is it:
- Creating objects? -> Creational patterns
- Composing objects? -> Structural patterns
- Managing behavior? -> Behavioral patterns
- Handling distributed systems? -> Distributed patterns

Suggest the most appropriate specific pattern.
```

---

*LLM Prompts for Design Patterns v1.0*
