# LLM Prompts for Behavioral Patterns

Effective prompts for LLM-assisted behavioral pattern design, implementation, and review.

## Pattern Selection Prompts

### Problem-First Analysis

```
I need help choosing the right behavioral pattern for this problem:

**Context:**
[Describe your system/module]

**Problem:**
[What are you trying to solve?]

**Requirements:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Constraints:**
- Language: [Python/TypeScript/Go]
- Framework: [Django/React/etc.]
- Team size: [small/medium/large]

Please recommend:
1. The most appropriate behavioral pattern
2. Why this pattern fits
3. Alternative patterns considered
4. Potential drawbacks to watch for
```

### Pattern Comparison

```
Compare these behavioral patterns for my use case:

**Use case:** [Describe the scenario]

**Patterns to compare:**
1. [Pattern A]
2. [Pattern B]

For each pattern, explain:
- How it would solve the problem
- Implementation complexity
- Testability
- Extensibility
- Performance implications

Which would you recommend and why?
```

### Complexity Validation

```
I'm considering using the [Pattern Name] pattern for:

[Describe the problem in 2-3 sentences]

Current solution: [Describe current approach]

Questions:
1. Is this pattern overkill for my use case?
2. What's the simplest solution that would work?
3. At what point would the pattern become necessary?
4. What's the migration path from simple to pattern-based?
```

## Implementation Prompts

### Strategy Pattern

```
Implement a Strategy pattern for [domain] with these strategies:

1. [Strategy A]: [Description]
2. [Strategy B]: [Description]
3. [Strategy C]: [Description]

Requirements:
- Language: [Python/TypeScript/Go]
- Strategies should be [runtime-swappable/compile-time fixed]
- Need [validation/logging/metrics] in context
- Consider [thread safety/async support] if applicable

Include:
- Strategy interface/protocol
- All concrete strategies
- Context class
- Factory method for strategy selection
- Unit tests for each strategy
```

### Observer Pattern

```
Implement an Observer/Event system with these specifications:

**Events:**
- [Event 1]: [When triggered, what data]
- [Event 2]: [When triggered, what data]

**Requirements:**
- Language: [Python/TypeScript/Go]
- [Typed events / Generic events]
- Memory management: [Weak references / Manual unsubscribe / GC-safe]
- Threading: [Single-threaded / Thread-safe / Async]

Include:
- Subject/EventEmitter interface
- Observer interface
- Concrete implementation
- Unsubscribe mechanism
- Example usage
```

### Command Pattern

```
Implement a Command pattern for [use case] with:

**Commands:**
1. [Command 1]: [What it does]
2. [Command 2]: [What it does]
3. [Command 3]: [What it does]

**Requirements:**
- Language: [Python/TypeScript/Go]
- Undo support: [Yes/No]
- Redo support: [Yes/No]
- Command history: [In-memory / Persistent]
- Composition: [Support macro commands / Single commands only]

Include:
- Command interface with execute/undo
- Invoker with history management
- All concrete commands
- Composite command (if needed)
```

### State Pattern

```
Implement a State Machine for [entity] with these states:

**States:**
- [State 1]: [Description, allowed actions]
- [State 2]: [Description, allowed actions]
- [State 3]: [Description, allowed actions]

**Transitions:**
- [State 1] -> [State 2]: On [event/action]
- [State 2] -> [State 3]: On [event/action]
- [etc.]

**Requirements:**
- Language: [Python/TypeScript/Go]
- [Entry/exit actions / No hooks]
- [Guard conditions / Simple transitions]
- [Type-safe / Dynamic states]

Include:
- State interface
- All state implementations
- Context class
- Transition validation
- State diagram as comment/doc
```

### Chain of Responsibility

```
Implement a handler chain for [processing pipeline]:

**Handlers (in order):**
1. [Handler 1]: [What it checks/processes]
2. [Handler 2]: [What it checks/processes]
3. [Handler 3]: [What it checks/processes]

**Chain behavior:**
- [Stop on first handler / Continue through all]
- [Can modify request / Read-only]
- [Return value / Side effects only]

**Requirements:**
- Language: [Python/TypeScript/Go]
- Error handling: [Return error / Throw / Error handler]
- Async support: [Yes/No]

Include:
- Handler interface
- Base handler with chain logic
- All concrete handlers
- Chain builder/factory
- Usage example with request flow
```

### Template Method

```
Implement a Template Method pattern for [process]:

**Algorithm steps:**
1. [Step 1]: [Required/Optional], [Customizable/Fixed]
2. [Step 2]: [Required/Optional], [Customizable/Fixed]
3. [Step 3]: [Required/Optional], [Customizable/Fixed]

**Concrete implementations:**
1. [Implementation A]: [How steps differ]
2. [Implementation B]: [How steps differ]

**Requirements:**
- Language: [Python/TypeScript/Go]
- [Abstract class / Interface + default implementation]
- Hook methods: [Yes/No]

Include:
- Abstract base with template method
- All abstract/hook methods clearly marked
- Concrete implementations
- Example showing algorithm flow
```

## Code Review Prompts

### Pattern Implementation Review

```
Review this [Pattern Name] implementation:

```[language]
[Paste code here]
```

Please analyze:
1. Does this correctly implement the pattern?
2. Are there any SOLID principle violations?
3. Is the interface properly designed?
4. Are there memory leaks or resource issues?
5. Is it testable?
6. Is it thread-safe (if applicable)?
7. What improvements would you suggest?

Focus on [language] best practices and idioms.
```

### Pattern Modernization

```
Modernize this [Pattern Name] implementation to [language] best practices (2025):

```[language]
[Paste older/basic code here]
```

Improvements to consider:
- Use modern language features ([protocols/generics/etc.])
- Improve type safety
- Better error handling
- Async support if applicable
- Testing improvements
- Performance optimizations

Show the refactored code with comments explaining changes.
```

### Anti-Pattern Detection

```
Review this code for behavioral pattern anti-patterns:

```[language]
[Paste code here]
```

Check for:
1. God classes masquerading as mediators
2. Observer memory leaks
3. State pattern without proper transitions
4. Over-complicated strategy selection
5. Command pattern without proper undo support
6. Missing unsubscribe mechanisms
7. Thread safety issues

For each issue found, suggest a fix.
```

## Refactoring Prompts

### Extract Pattern

```
Refactor this code to use the [Pattern Name] pattern:

**Current code:**
```[language]
[Paste code with smell]
```

**Problems with current approach:**
- [Problem 1]
- [Problem 2]

**Goals:**
- [What should improve after refactoring]

Show:
1. Step-by-step refactoring plan
2. Final refactored code
3. How to migrate existing callers
```

### Pattern Migration

```
Help me migrate from [Pattern A] to [Pattern B]:

**Current [Pattern A] implementation:**
```[language]
[Paste current code]
```

**Why migrate:**
- [Reason 1]
- [Reason 2]

**Constraints:**
- [Must maintain backward compatibility / Can break API]
- [Gradual migration / Big bang]

Provide:
1. Migration strategy
2. New implementation
3. Adapter/bridge code (if needed)
4. Updated tests
```

## Testing Prompts

### Pattern Unit Tests

```
Generate comprehensive unit tests for this [Pattern Name] implementation:

```[language]
[Paste implementation]
```

Test scenarios needed:
- Normal operation
- Edge cases
- Error conditions
- [State transitions / Strategy switching / etc.]
- [Pattern-specific scenarios]

Use [pytest/jest/testing-go] with:
- Clear test names describing behavior
- Arrange-Act-Assert structure
- Appropriate mocking
```

### Integration Testing

```
Create integration tests for this [Pattern Name] in context:

**Pattern code:**
```[language]
[Paste pattern implementation]
```

**Integration context:**
- [Where pattern is used]
- [External dependencies]
- [Expected behavior in system]

Tests should verify:
1. Pattern integrates correctly with [components]
2. Error handling propagates properly
3. Performance is acceptable
4. [Context-specific requirements]
```

## Architecture Discussion Prompts

### Pattern Trade-offs

```
I'm designing a [system/feature] and considering behavioral patterns.

**Architecture context:**
- [Monolith/Microservices/Serverless]
- [Sync/Async/Event-driven]
- [Languages/frameworks used]

**Current design question:**
[Describe the specific decision point]

**Options I'm considering:**
1. [Option A with pattern X]
2. [Option B with pattern Y]
3. [Option C without pattern]

Discuss trade-offs for each option regarding:
- Complexity vs. benefit
- Team learning curve
- Testing difficulty
- Debugging experience
- Performance impact
- Future extensibility
```

### Pattern Composition

```
How should I combine these behavioral patterns effectively?

**Patterns to combine:**
- [Pattern A]: [Purpose]
- [Pattern B]: [Purpose]

**Use case:**
[Describe what you're building]

Questions:
1. Do these patterns work well together?
2. What's the recommended composition approach?
3. Are there interaction pitfalls to avoid?
4. Show an example of clean composition
```

## Domain-Specific Prompts

### E-commerce Patterns

```
Design behavioral patterns for an e-commerce [component]:

**Component:** [Order processing / Payment / Inventory / etc.]

**Requirements:**
- [Business requirement 1]
- [Business requirement 2]

**Constraints:**
- Must handle [concurrent orders / refunds / etc.]
- Integration with [payment gateway / warehouse / etc.]

Recommend appropriate behavioral patterns and show implementation.
```

### API/Middleware Patterns

```
Implement behavioral patterns for API middleware:

**Middleware needs:**
1. [Authentication]
2. [Rate limiting]
3. [Logging]
4. [Validation]
5. [Error handling]

**Framework:** [Express/FastAPI/Gin/etc.]

Show:
1. Which patterns apply
2. How they compose
3. Implementation code
4. Configuration examples
```

### Event-Driven Systems

```
Design behavioral patterns for event-driven architecture:

**Events:**
- [Event 1]: [Producer, data]
- [Event 2]: [Producer, data]

**Consumers:**
- [Consumer A]: Handles [events]
- [Consumer B]: Handles [events]

**Requirements:**
- [Eventual consistency / Strong consistency]
- [At-least-once / Exactly-once delivery]
- [Ordered / Unordered processing]

Show patterns for:
1. Event publishing
2. Event handling
3. Error recovery
4. Dead letter handling
```

## Quick Reference Prompts

### Pattern Summary

```
Give me a quick reference for [Pattern Name]:

Include:
1. One-sentence description
2. When to use (3 bullet points)
3. When NOT to use (2 bullet points)
4. Minimal code example in [language]
5. Common mistakes to avoid
```

### Pattern Comparison Table

```
Create a comparison table for these behavioral patterns:
[Pattern 1, Pattern 2, Pattern 3]

Compare:
| Aspect | Pattern 1 | Pattern 2 | Pattern 3 |
|--------|-----------|-----------|-----------|
| Purpose | | | |
| Complexity | | | |
| Testing | | | |
| Use when | | | |
| Avoid when | | | |
```

### Decision Flowchart

```
Create a decision flowchart for choosing between behavioral patterns:

Starting question: [What problem are you solving?]

Include decision points for:
- Strategy vs State
- Observer vs Mediator
- Command vs direct calls
- Chain of Responsibility vs simple conditionals
- Template Method vs Strategy

Output as text-based flowchart or Mermaid diagram.
```

## Tips for Better Prompts

### Be Specific About Context

- Always mention the programming language
- Specify frameworks and libraries in use
- Describe team experience level
- Note any constraints (performance, legacy code)

### Describe the Problem, Not the Solution

Bad: "Implement Strategy pattern"
Good: "I have 5 payment methods with different validation rules..."

### Include Success Criteria

- What should the code do?
- How should it be tested?
- What edge cases matter?

### Request Trade-off Analysis

- Ask for alternatives
- Ask what could go wrong
- Ask about complexity vs. benefit

## Related

- [README.md](README.md) - Pattern overview
- [checklist.md](checklist.md) - Implementation checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Copy-paste templates
