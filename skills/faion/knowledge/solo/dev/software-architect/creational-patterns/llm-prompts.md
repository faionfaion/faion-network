# LLM Prompts for Creational Patterns

> Effective prompts for LLM-assisted creational pattern design and implementation.

## Table of Contents

- [Pattern Selection](#pattern-selection)
- [Factory Method](#factory-method)
- [Abstract Factory](#abstract-factory)
- [Builder](#builder)
- [Singleton and Alternatives](#singleton-and-alternatives)
- [Prototype](#prototype)
- [Dependency Injection](#dependency-injection)
- [Object Pool](#object-pool)
- [Code Review](#code-review)
- [Refactoring](#refactoring)

---

## Pattern Selection

### Analyze Requirements and Suggest Pattern

```
Analyze the following requirements and recommend the most appropriate creational design pattern(s):

**Context:**
- Language: [Python/TypeScript/Go]
- Framework: [Django/FastAPI/NestJS/Gin/etc.]
- Domain: [e-commerce/fintech/healthcare/etc.]

**Requirements:**
[Describe object creation requirements, e.g.:
- Need to create different types of payment processors
- Payment type determined at runtime based on user selection
- Each processor has different configuration requirements
- Need to add new payment types without modifying existing code]

**Constraints:**
- Testing: [Unit tests required / Integration tests / Both]
- Performance: [Latency requirements, throughput]
- Team: [Team size, expertise level]

Please provide:
1. Recommended pattern(s) with rationale
2. Alternative patterns considered and why rejected
3. Key implementation considerations
4. Potential pitfalls to avoid
```

### Compare Multiple Patterns

```
Compare [Pattern A] vs [Pattern B] for the following use case:

**Use Case:**
[Describe the specific scenario]

**Criteria:**
- Testability
- Extensibility
- Code complexity
- Performance
- Team learning curve

Provide:
1. Side-by-side comparison table
2. Recommendation with justification
3. Code skeleton for the recommended approach
```

---

## Factory Method

### Design Factory Method Pattern

```
Design a Factory Method pattern for [use case] in [language].

**Context:**
- Creating [type of objects, e.g., notification handlers, payment processors, document parsers]
- Types include: [list specific types]
- New types may be added: [frequently/occasionally/rarely]

**Requirements:**
- Return interface/protocol, not concrete type
- Support configuration per type
- Include error handling for unknown types

Please provide:
1. Product interface definition
2. Concrete product implementations
3. Factory implementation (prefer registry pattern)
4. Usage example
5. Unit test example

**Code style:**
- Use type hints/generics
- Follow [language] idioms
- Include docstrings/comments
```

### Refactor Switch Statement to Factory

```
Refactor the following switch/if-else statement to use Factory Method pattern:

```[language]
[paste code with switch statement for object creation]
```

Requirements:
1. Extract product interface
2. Create concrete implementations
3. Replace switch with factory registry
4. Ensure Open/Closed Principle compliance
5. Maintain backward compatibility

Provide the refactored code with explanation of changes.
```

---

## Abstract Factory

### Design Abstract Factory Pattern

```
Design an Abstract Factory pattern for [product families] in [language].

**Context:**
- Product families: [e.g., Material Design, iOS, Bootstrap]
- Products in each family: [e.g., Button, Input, Modal, Card]
- Selection criteria: [e.g., user preference, platform detection, configuration]

**Requirements:**
- All products in a family must be compatible
- Easy to add new families
- Client code should use only abstract interfaces

Please provide:
1. Abstract product interfaces
2. At least 2 complete product families
3. Abstract factory interface
4. Concrete factory implementations
5. Factory selector function
6. Usage example showing family consistency
```

### Extend Existing Abstract Factory

```
I have an existing Abstract Factory for [domain]. I need to add:
- New product type: [describe new product]
- OR New family: [describe new family]

Current code:
```[language]
[paste existing factory code]
```

Please:
1. Analyze impact of the change
2. Provide updated interfaces
3. Implement the extension
4. Ensure backward compatibility
5. Note any breaking changes
```

---

## Builder

### Design Builder Pattern

```
Design a Builder pattern for [complex object] in [language].

**Object has:**
- Required fields: [list required fields with types]
- Optional fields: [list optional fields with types and defaults]
- Validation rules: [list any validation requirements]

**Requirements:**
- Fluent interface (method chaining)
- Immutable final object
- Validation on build()
- Clear error messages for invalid state

Please provide:
1. Final product class/struct (immutable)
2. Builder class with fluent methods
3. Validation logic
4. Usage examples showing various configurations
5. Example of invalid configuration handling
```

### Go Functional Options Pattern

```
Implement the Functional Options pattern for [type] in Go.

**Type has:**
- Required fields: [list]
- Optional fields: [list with defaults]

**Requirements:**
- Validate on construction
- Support chaining options
- Clear option naming (With* prefix)
- Handle errors in options

Provide:
1. Struct definition
2. Option type and functions
3. Constructor with variadic options
4. Usage examples
5. Testing approach
```

### Convert Constructor to Builder

```
Convert the following constructor with many parameters to Builder pattern:

```[language]
[paste constructor with many parameters]
```

Requirements:
1. Identify required vs optional parameters
2. Create fluent builder
3. Add validation
4. Make result immutable (if applicable)
5. Provide migration guide for existing callers
```

---

## Singleton and Alternatives

### Evaluate Singleton Usage

```
I'm considering using Singleton for [use case]. Please evaluate:

**Current approach:**
```[language]
[paste code or describe current implementation]
```

**Why Singleton seems appropriate:**
[list reasons]

Please provide:
1. Analysis of whether Singleton is appropriate
2. Testing implications
3. Concurrency considerations
4. Recommended alternatives (if any)
5. If Singleton is appropriate, best implementation for [language]
6. If not, alternative implementation with better testability
```

### Replace Singleton with DI

```
Refactor the following Singleton to use Dependency Injection:

```[language]
[paste Singleton code]
```

**Target DI framework:** [dependency-injector/TSyringe/Wire/manual]

Please provide:
1. Interface extraction
2. Service implementation (non-singleton)
3. DI container configuration
4. Lifetime/scope configuration
5. Updated client code
6. Test setup with mock injection
```

### Thread-Safe Singleton Implementation

```
Implement a thread-safe Singleton for [use case] in [language].

**Requirements:**
- Lazy initialization
- Thread-safe without excessive locking
- Testable (reset capability for tests)
- [Additional requirements]

Provide:
1. Implementation with thread safety explanation
2. Test helper for resetting instance
3. Usage example
4. Known limitations
```

---

## Prototype

### Design Prototype Pattern

```
Design a Prototype pattern for [use case] in [language].

**Object characteristics:**
- Fields: [list fields with types]
- Nested objects: [list nested objects]
- External resources: [file handles, connections, etc.]

**Clone requirements:**
- Deep clone needed for: [list fields]
- Shallow clone acceptable for: [list fields]
- Handle circular references: [yes/no]

Please provide:
1. Prototype interface
2. Clone implementation (deep copy)
3. Shallow clone option (if applicable)
4. Prototype registry for templates
5. Usage example with modifications after clone
6. Unit test verifying clone independence
```

### Implement Clone with Modern Methods

```
Implement deep cloning for [object type] in [language] using modern approaches.

Object structure:
```[language]
[paste object definition]
```

Consider:
- Python: copy.deepcopy, dataclasses.replace
- TypeScript: structuredClone (Node 17+), spread operators
- Go: encoding/gob, manual copy

Provide:
1. Best approach for this object
2. Implementation
3. Performance considerations
4. Edge cases (dates, functions, circular refs)
```

---

## Dependency Injection

### Design DI Architecture

```
Design a Dependency Injection architecture for [application type] in [language].

**Components:**
- Services: [list services]
- Repositories: [list data access components]
- External integrations: [list external services]

**Requirements:**
- Framework: [dependency-injector/TSyringe/Wire/manual]
- Scopes needed: [singleton/transient/scoped]
- Configuration: [environment variables, config files]

Please provide:
1. Interface definitions for all components
2. Concrete implementations
3. Container/composition root setup
4. Scope/lifetime configuration
5. Example of swapping implementations
6. Test setup with mocks
```

### Setup DI for Testing

```
Create a test setup for DI container with mock injections:

Production container:
```[language]
[paste production DI configuration]
```

**Components to mock:**
- [List components that need mocking]

**Test scenarios:**
- [List test scenarios]

Provide:
1. Test container factory function
2. Mock implementations
3. Per-test override capability
4. Example test using mocks
5. Cleanup/reset between tests
```

### Migrate from Singleton to DI

```
I have multiple Singletons that need to be migrated to DI:

```[language]
[paste code with multiple Singletons]
```

**Target framework:** [specify DI framework]

Please provide:
1. Step-by-step migration plan
2. Interface extraction for each Singleton
3. DI configuration
4. Updated client code
5. Backward compatibility layer (if needed)
6. Testing strategy
```

---

## Object Pool

### Design Object Pool

```
Design an Object Pool for [resource type] in [language].

**Resource characteristics:**
- Creation cost: [high/medium, describe]
- Usage pattern: [frequent short-lived / occasional long-lived]
- Cleanup requirements: [what needs reset between uses]
- Validation: [how to check if resource is still valid]

**Pool requirements:**
- Initial size: [number]
- Max size: [number]
- Acquisition timeout: [duration]
- Idle policy: [keep all / evict after timeout / shrink to min]

Please provide:
1. Pool implementation with all features
2. Resource wrapper (if needed)
3. Context manager / RAII pattern for auto-release
4. Metrics/stats exposure
5. Graceful shutdown
6. Usage example
7. Test for pool exhaustion handling
```

### Add Pooling to Existing Resource

```
Add object pooling to the following resource that's currently created on-demand:

```[language]
[paste current resource creation code]
```

**Observed issues:**
- [e.g., High GC pressure, slow response times, connection limits]

Please provide:
1. Pool wrapper for the resource
2. Reset function for reuse
3. Validation function
4. Migration path from current code
5. Metrics to track improvement
```

---

## Code Review

### Review Creational Pattern Implementation

```
Review the following [pattern name] implementation:

```[language]
[paste implementation]
```

Please evaluate:
1. **Correctness:** Does it follow the pattern correctly?
2. **SOLID compliance:** Any violations?
3. **Thread safety:** Any concurrency issues?
4. **Testability:** Can this be easily unit tested?
5. **Error handling:** Are edge cases covered?
6. **Performance:** Any concerns?
7. **Idiomatic:** Does it follow [language] conventions?

Provide specific improvement suggestions with code.
```

### Review Pattern Selection

```
Review whether the chosen pattern is appropriate:

**Problem:** [describe the problem being solved]

**Chosen pattern:** [pattern name]

**Implementation:**
```[language]
[paste code]
```

Please evaluate:
1. Is this the right pattern for the problem?
2. Is it over-engineered?
3. Would a simpler solution work?
4. What are the trade-offs?
5. Recommendations
```

---

## Refactoring

### Extract Factory from Mixed Code

```
Extract creational logic into appropriate pattern:

```[language]
[paste code with mixed concerns]
```

The code currently:
- [describe current behavior]
- [note issues]

Please:
1. Identify the creational pattern needed
2. Extract product interface
3. Create factory/builder/etc.
4. Refactor client code
5. Ensure no behavior changes
6. Add tests for the extraction
```

### Modernize Legacy Pattern

```
Modernize this legacy [pattern name] implementation:

```[language]
[paste old-style implementation]
```

**Target:**
- Language version: [e.g., Python 3.12, TypeScript 5, Go 1.22]
- Use modern features: [list specific features to use]

Please provide:
1. Updated implementation using modern idioms
2. Explanation of improvements
3. Backward compatibility notes
4. Migration guide
```

---

## Prompt Templates Summary

| Task | Key Elements to Include |
|------|------------------------|
| Pattern Selection | Context, requirements, constraints, criteria |
| Pattern Design | Use case, types/fields, validation rules, language idioms |
| Code Review | Full code, evaluation criteria, specific concerns |
| Refactoring | Current code, issues, target state, constraints |
| Testing | Components to test, scenarios, mock requirements |

## Tips for Better Results

1. **Be specific about language and version** - Modern features vary significantly
2. **Include constraints** - Testing requirements, performance needs, team expertise
3. **Show existing code** - Context helps with consistent style
4. **Ask for trade-offs** - Understand alternatives considered
5. **Request tests** - Ensures implementation is testable
6. **Specify error handling** - Include edge cases and failure modes

---

## Related Files

| File | Description |
|------|-------------|
| [README.md](README.md) | Pattern overview |
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Full examples |
| [templates.md](templates.md) | Copy-paste templates |
