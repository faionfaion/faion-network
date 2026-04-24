# LLM Prompts for Structural Patterns

Effective prompts for LLM-assisted structural pattern design, implementation, and review.

---

## Pattern Selection Prompts

### General Pattern Selection

```
I need to choose a structural design pattern for the following scenario:

**Context:**
- [Describe the problem domain]
- [Current architecture/codebase state]
- [Key constraints (performance, memory, legacy integration)]

**Requirements:**
- [List specific requirements]
- [Expected behavior]

**Questions:**
1. Which structural pattern(s) would be most appropriate?
2. What are the trade-offs of each option?
3. Are there any patterns I should avoid for this scenario?

Please provide reasoning and a recommendation.
```

### Wrapping Pattern Decision

```
Help me choose between Adapter, Proxy, Decorator, and Bridge patterns.

**My Situation:**
- [Describe what you're trying to wrap/modify]
- [Is this design-time or retrofit?]
- [What behavior needs to change?]

**Specific Questions:**
1. Which "wrapping" pattern fits best?
2. How do I distinguish between these patterns for my case?
3. What are the implementation differences?

Language: [Python/TypeScript/Go]
```

---

## Adapter Pattern Prompts

### Design an Adapter

```
Design an Adapter pattern implementation for the following:

**Target Interface (what I need):**
```[language]
[Paste the interface/protocol you want to use]
```

**Adaptee (what I have):**
```[language]
[Paste the existing class/API to adapt]
```

**Requirements:**
- Language: [Python/TypeScript/Go]
- [Any specific conversion logic needed]
- [Error handling requirements]
- [Performance considerations]

Please provide:
1. Complete Adapter implementation
2. Usage example
3. Unit tests
4. Any potential issues or edge cases
```

### Review Adapter Implementation

```
Review this Adapter pattern implementation:

```[language]
[Paste your adapter code]
```

**Check for:**
1. Does the adapter correctly translate between interfaces?
2. Is there any business logic that shouldn't be in the adapter?
3. Are there type conversion issues?
4. Is the adapter testable and maintainable?
5. Performance concerns?

Provide specific improvements if needed.
```

### Adapter for Multiple Adaptees

```
I need to create adapters for multiple similar services to a unified interface.

**Target Interface:**
```[language]
[Unified interface definition]
```

**Adaptees:**
1. [First service/API description]
2. [Second service/API description]
3. [Third service/API description]

**Requirements:**
- Factory pattern to select adapter
- Consistent error handling
- Easy to add new adaptees

Language: [Python/TypeScript/Go]
Provide complete implementation with factory.
```

---

## Bridge Pattern Prompts

### Design a Bridge

```
Design a Bridge pattern to separate abstraction from implementation.

**Abstraction Dimension:**
- [Describe the high-level concepts that vary]
- [List concrete abstractions needed]

**Implementation Dimension:**
- [Describe the low-level implementations that vary]
- [List concrete implementations needed]

**Why Bridge:**
- [Why these dimensions should vary independently]
- [Expected future extensions]

Language: [Python/TypeScript/Go]

Provide:
1. Implementor interface
2. Concrete Implementors
3. Abstraction with Implementor reference
4. Refined Abstractions
5. Usage examples showing independence
```

### Bridge vs Adapter Decision

```
I'm unsure whether to use Bridge or Adapter for this scenario:

**Current Situation:**
- [Describe what you're building]
- [Is this new design or retrofitting existing code?]
- [What kind of variations do you expect?]

**Questions:**
1. Should I use Bridge (design up-front) or Adapter (retrofit)?
2. What are the long-term implications of each choice?
3. Can I combine both patterns?

Please explain with examples relevant to my scenario.
```

---

## Composite Pattern Prompts

### Design a Composite Structure

```
Design a Composite pattern for a hierarchical structure.

**Domain:**
- [Describe the tree structure (e.g., file system, org chart, UI)]
- [What are the leaf elements?]
- [What are the composite elements?]

**Operations:**
- [List operations that should work uniformly on leaves and composites]
- [Any composite-specific operations?]

**Requirements:**
- Language: [Python/TypeScript/Go]
- [Iteration/traversal requirements]
- [Performance considerations for large trees]

Provide:
1. Component interface
2. Leaf implementation
3. Composite implementation with add/remove
4. Recursive operation examples
5. Tree traversal (depth-first, breadth-first)
```

### Composite with Type Safety

```
I need a type-safe Composite pattern where:

- Only certain composites can contain certain leaves
- Some operations only apply to leaves
- Some operations only apply to composites

**Structure:**
- [Describe the hierarchy with constraints]

Language: [TypeScript preferred for type safety]

How can I implement this while maintaining the uniform interface principle?
Provide implementation with compile-time safety.
```

---

## Decorator Pattern Prompts

### Design Decorator Chain

```
Design a Decorator pattern for adding behaviors dynamically.

**Base Component:**
```[language]
[The component interface and concrete component]
```

**Decorators Needed:**
1. [First decorator: what it adds]
2. [Second decorator: what it adds]
3. [Third decorator: what it adds]

**Requirements:**
- Decorators must be stackable in any order
- Each decorator should be independent
- [Any ordering constraints?]

Language: [Python/TypeScript/Go]

Provide:
1. Base decorator class
2. Each concrete decorator
3. Examples of different stacking orders
4. Tests for decorator combinations
```

### Function Decorator (Python)

```
Create a Python function decorator for:

**Purpose:**
- [What the decorator should do]

**Parameters:**
- [List decorator parameters if any]

**Requirements:**
- Preserve function metadata (use @functools.wraps)
- Type hints with TypeVar and ParamSpec
- Handle both sync and async functions (if needed)
- [Error handling requirements]

Provide:
1. Decorator implementation
2. Usage examples
3. Tests
```

### Decorator Order Analysis

```
I have these decorators applied to a function/class:

```[language]
@decorator_a
@decorator_b
@decorator_c
def my_function():
    ...
```

**Questions:**
1. What is the execution order?
2. How does data flow through the decorators?
3. Are there any potential issues with this order?
4. How would I change the order to achieve [specific goal]?

Please trace through the execution with a concrete example.
```

---

## Facade Pattern Prompts

### Design a Facade

```
Design a Facade to simplify this complex subsystem:

**Subsystem Components:**
1. [Component A: what it does]
2. [Component B: what it does]
3. [Component C: what it does]
4. [Dependencies between components]

**Client Needs:**
- [List high-level operations clients need]
- [What complexity should be hidden?]

**Requirements:**
- Should subsystem still be accessible directly? [yes/no]
- Language: [Python/TypeScript/Go]
- [Error handling across subsystem]

Provide:
1. Facade class with simplified interface
2. Subsystem coordination logic
3. Error aggregation/handling
4. Usage examples
5. When to bypass facade for advanced use
```

### API Gateway as Facade

```
Design an API Gateway acting as a Facade for microservices.

**Services:**
1. [Service A: endpoints, responsibilities]
2. [Service B: endpoints, responsibilities]
3. [Service C: endpoints, responsibilities]

**Gateway Requirements:**
- Request routing
- Authentication/authorization
- Response aggregation
- Error handling
- Rate limiting

Language: [Python/TypeScript/Go]
Framework: [FastAPI/Express/Gin]

Provide:
1. Gateway facade implementation
2. Routing configuration
3. Middleware integration
4. Example aggregated endpoint
```

---

## Proxy Pattern Prompts

### Design a Proxy

```
Design a Proxy pattern for: [Virtual/Protection/Cache/Logging/Remote]

**Subject Interface:**
```[language]
[The interface to proxy]
```

**Real Subject:**
```[language]
[The real implementation]
```

**Proxy Requirements:**
- Type: [Virtual Proxy | Protection Proxy | Cache Proxy | Logging Proxy]
- [Specific behavior to add]
- [Lazy loading requirements if virtual]
- [Access rules if protection]
- [Cache invalidation if caching]

Language: [Python/TypeScript/Go]

Provide:
1. Proxy implementation
2. Integration with real subject
3. Tests for proxy behavior
4. Memory/performance considerations
```

### Combine Multiple Proxy Types

```
I need a proxy that combines multiple concerns:

**Concerns:**
- [ ] Lazy loading (virtual proxy)
- [ ] Access control (protection proxy)
- [ ] Caching (cache proxy)
- [ ] Logging (logging proxy)

**Subject:**
```[language]
[The subject interface and implementation]
```

**Questions:**
1. Should I use multiple nested proxies or one combined proxy?
2. What's the recommended order if nesting?
3. How do I handle the complexity?

Language: [Python/TypeScript/Go]
Provide implementation with recommended approach.
```

### Lazy Loading Proxy with Cache

```
Design a proxy that:
1. Lazily loads the real subject on first access
2. Caches results with TTL
3. Handles cache invalidation

**Subject:**
```[language]
[Interface definition]
```

**Cache Requirements:**
- TTL: [duration]
- Invalidation strategy: [time-based/event-based/manual]
- Thread safety: [required/not required]

Language: [Python/TypeScript/Go]
```

---

## Flyweight Pattern Prompts

### Design a Flyweight System

```
Design a Flyweight pattern for memory optimization.

**Object Type:**
- [What objects are consuming too much memory?]
- [How many instances exist?]
- [Current memory per instance?]

**State Analysis:**
- Intrinsic (shared) state: [list properties that can be shared]
- Extrinsic (context) state: [list properties that vary per instance]

**Requirements:**
- Language: [Python/TypeScript/Go]
- Thread safety: [required/not required]
- Pre-population: [known values upfront?]

Provide:
1. Flyweight class (immutable)
2. Flyweight Factory with caching
3. Context class with extrinsic state
4. Memory usage comparison
5. Thread-safety implementation if needed
```

### Flyweight with Object Pool

```
I need to combine Flyweight with Object Pool pattern.

**Scenario:**
- [Describe the objects and their lifecycle]
- [Why flyweight alone isn't enough]
- [Pooling requirements]

**Questions:**
1. How do Flyweight and Object Pool complement each other?
2. What should be in the flyweight vs the pool?
3. How to manage object lifecycle?

Language: [Python/TypeScript/Go]
Provide combined implementation.
```

---

## Pattern Combination Prompts

### Combining Structural Patterns

```
Help me combine multiple structural patterns effectively.

**Patterns to Combine:**
1. [Pattern A: why it's needed]
2. [Pattern B: why it's needed]
3. [Pattern C: why it's needed]

**Architecture:**
- [Describe the overall system]
- [How patterns should interact]

**Concerns:**
- Will this add too much complexity?
- Are there simpler alternatives?
- How to maintain this code?

Language: [Python/TypeScript/Go]
Provide architecture with pattern interactions.
```

### Structural + Other Pattern Categories

```
I'm using [structural pattern] and need to integrate with:

**Creational Pattern:** [e.g., Factory to create decorated objects]
**Behavioral Pattern:** [e.g., Strategy within Bridge implementations]

**Questions:**
1. How do these patterns work together?
2. Where should each pattern be applied?
3. What are common integration points?

Provide example showing pattern integration.
```

---

## Refactoring Prompts

### Refactor to Structural Pattern

```
Refactor this code to use [structural pattern]:

```[language]
[Paste existing code that needs refactoring]
```

**Why Refactoring:**
- [Current problems with the code]
- [Benefits expected from pattern]

**Constraints:**
- [Backward compatibility requirements]
- [Performance constraints]
- [Testing requirements]

Provide:
1. Step-by-step refactoring plan
2. Refactored code
3. Before/after comparison
4. Migration guide for existing code
```

### Pattern Migration

```
I need to migrate from [current approach] to [structural pattern].

**Current Implementation:**
```[language]
[Current code]
```

**Target Pattern:** [Adapter/Bridge/Composite/Decorator/Facade/Proxy/Flyweight]

**Migration Requirements:**
- Zero downtime
- Gradual rollout possible
- Rollback strategy

Provide:
1. Migration strategy
2. Intermediate steps
3. Feature flags if needed
4. Testing strategy during migration
```

---

## Code Review Prompts

### Pattern Implementation Review

```
Review this [structural pattern] implementation:

```[language]
[Paste implementation]
```

**Review Criteria:**
1. Does it follow the pattern correctly?
2. SOLID principles adherence?
3. Testability?
4. Performance implications?
5. Thread safety (if applicable)?
6. Error handling?
7. Documentation quality?

Provide:
- Issues found
- Severity (critical/major/minor)
- Suggested fixes
- Best practices recommendations
```

### Pattern Usage Review

```
Review how this [structural pattern] is being used in context:

**Pattern Implementation:**
```[language]
[Pattern code]
```

**Usage in Application:**
```[language]
[How pattern is used]
```

**Questions:**
1. Is this the right pattern for the use case?
2. Is the pattern being used correctly?
3. Are there simpler alternatives?
4. Anti-patterns present?

Provide recommendations.
```

---

## Language-Specific Prompts

### Pythonic Implementation

```
Provide a Pythonic implementation of [structural pattern].

**Requirements:**
- Use Python 3.10+ features (match statements, union types)
- Type hints with Protocol for interfaces
- Dataclasses where appropriate
- @functools.wraps for decorators
- Context managers if applicable
- async/await support if needed

Pattern: [Adapter/Bridge/Composite/Decorator/Facade/Proxy/Flyweight]
Use Case: [Describe specific use case]

Include:
1. Implementation following Python conventions
2. Type stubs if complex
3. pytest tests
4. Documentation with doctests
```

### TypeScript Implementation

```
Provide a TypeScript implementation of [structural pattern].

**Requirements:**
- Strict TypeScript (strict: true)
- Generics where applicable
- Utility types (Partial, Pick, etc.)
- Discriminated unions if helpful
- Class decorators if using Decorator pattern
- Type guards for runtime checks

Pattern: [Adapter/Bridge/Composite/Decorator/Facade/Proxy/Flyweight]
Use Case: [Describe specific use case]

Include:
1. Implementation with full type safety
2. Generic version if applicable
3. Jest/Vitest tests
4. JSDoc comments
```

### Go Implementation

```
Provide an idiomatic Go implementation of [structural pattern].

**Requirements:**
- Effective Go style
- Interface-based design
- Error handling with errors package
- Context for cancellation if async
- sync primitives for thread safety
- Embed for composition

Pattern: [Adapter/Bridge/Composite/Decorator/Facade/Proxy/Flyweight]
Use Case: [Describe specific use case]

Include:
1. Implementation following Go conventions
2. Concurrency-safe if needed
3. Table-driven tests
4. Benchmarks for performance-critical code
5. GoDoc comments
```

---

## Troubleshooting Prompts

### Pattern Not Working

```
My [structural pattern] implementation isn't working as expected.

**Implementation:**
```[language]
[Paste code]
```

**Expected Behavior:**
[What it should do]

**Actual Behavior:**
[What it's doing]

**Error Messages (if any):**
```
[Error output]
```

Help me:
1. Identify the problem
2. Understand why it's happening
3. Fix the issue
4. Prevent similar issues
```

### Performance Issues

```
My [structural pattern] is causing performance issues.

**Implementation:**
```[language]
[Code]
```

**Performance Problem:**
- [Slow operations]
- [High memory usage]
- [Throughput issues]

**Profiling Data (if available):**
```
[Profiler output]
```

**Questions:**
1. Where is the bottleneck?
2. Is this pattern appropriate for high-performance scenarios?
3. How can I optimize without breaking the pattern?
4. Should I consider a different pattern?
```

---

## Quick Reference

| Task | Prompt Focus |
|------|-------------|
| Pattern selection | Context, requirements, constraints |
| Design | Interface definitions, responsibilities |
| Implementation | Language-specific, tests, edge cases |
| Review | Correctness, SOLID, performance |
| Refactoring | Current code, migration strategy |
| Troubleshooting | Behavior, errors, profiling data |
