# LLM Prompts for Architecture Discussions

Prompts for productive conversations with LLM assistants about architectural patterns.

## Pattern Selection Prompts

### Initial Architecture Discovery

```
I'm starting a new project with the following characteristics:
- Domain: {describe domain}
- Team size: {number}
- Expected scale: {users/requests}
- Input channels: {REST, CLI, GraphQL, etc.}
- External dependencies: {databases, services, etc.}

Based on these characteristics, recommend an architectural pattern (Clean Architecture, Hexagonal, Onion, or DDD). Explain your reasoning and show the recommended folder structure.
```

### Pattern Comparison

```
Compare Clean Architecture, Hexagonal Architecture, and DDD for a {type} application with {characteristics}.

For each pattern, provide:
1. Suitability score (1-10)
2. Main advantages for this use case
3. Potential challenges
4. When to choose this pattern

Recommend one pattern and explain why.
```

### Migration Assessment

```
We have an existing {framework} application with {description of current architecture}.

Assess the feasibility of migrating to {Clean/Hexagonal/DDD} architecture:
1. What would need to change?
2. What can stay the same?
3. Suggested migration strategy (big bang vs incremental)
4. Estimated effort (high/medium/low)
5. Risks and mitigations
```

---

## Design Review Prompts

### Architecture Review

```
Review this folder structure for {Clean/Hexagonal/DDD} architecture compliance:

{paste folder structure}

Check for:
1. Correct dependency direction
2. Layer responsibilities
3. Missing components
4. Potential violations
5. Naming consistency

Provide specific fixes for any issues found.
```

### Dependency Rule Verification

```
Analyze these imports for Clean Architecture dependency violations:

File: src/domain/entities/Order.ts
{paste imports}

File: src/application/use-cases/PlaceOrder.ts
{paste imports}

File: src/infrastructure/persistence/OrderRepository.ts
{paste imports}

Identify any violations of the dependency rule (dependencies should point inward toward the domain).
```

### Code Review for Pattern Compliance

```
Review this {entity/use-case/repository} implementation for {Clean/Hexagonal/DDD} compliance:

```{language}
{paste code}
```

Check for:
1. Single responsibility
2. Proper abstraction level
3. Domain logic placement
4. Infrastructure leakage
5. Testability

Provide corrected version if needed.
```

---

## Implementation Prompts

### Entity Implementation

```
Create a domain entity for {entity name} following Clean Architecture principles.

Requirements:
- Properties: {list properties}
- Behaviors: {list behaviors/methods}
- Invariants: {list business rules}
- Events: {list domain events to raise}

Include:
1. Private constructor
2. Factory methods (create, reconstitute)
3. Domain behavior methods
4. Event collection

Use TypeScript. Make the entity rich, not anemic.
```

### Use Case Implementation

```
Implement a use case for {use case name} following Clean Architecture.

Input: {describe input}
Output: {describe output}
Steps:
1. {step 1}
2. {step 2}
3. ...

Dependencies needed:
- {repository interfaces}
- {service interfaces}

Include error handling and validation. Use TypeScript.
```

### Repository Implementation

```
Implement a repository for {entity name} following Clean Architecture.

Target database: {PostgreSQL/MongoDB/etc.}
ORM/Driver: {Prisma/TypeORM/pg/etc.}

The repository should:
1. Implement I{EntityName}Repository interface
2. Map between domain entity and persistence model
3. Handle transactions if needed
4. Support: save, findById, findAll, delete
5. Add these custom queries: {list queries}

Show both the interface and implementation.
```

### Port and Adapter Implementation

```
Implement a Hexagonal port and adapter for {external service}.

Port (interface):
- Define operations the core needs
- Use domain types, not infrastructure types

Adapter (implementation):
- Implement the port interface
- Handle {service} specific details
- Include error mapping
- Include retry logic if appropriate

Use TypeScript. Show both port and adapter.
```

---

## DDD-Specific Prompts

### Aggregate Design

```
Design an aggregate for {aggregate name} in a {domain} system.

Business rules:
1. {rule 1}
2. {rule 2}
3. ...

The aggregate should include:
- Aggregate root entity
- Child entities (if any)
- Value objects
- Domain events

Show the aggregate with proper invariant enforcement. Explain why you chose this aggregate boundary.
```

### Bounded Context Identification

```
Help me identify bounded contexts for a {domain} system.

System capabilities:
1. {capability 1}
2. {capability 2}
3. ...

User types: {list user types}
Key business processes: {list processes}

Identify:
1. Bounded contexts (2-5)
2. Core/supporting/generic classification
3. Context relationships (partnership, customer-supplier, etc.)
4. Shared kernel candidates

Provide a context map diagram (text-based).
```

### Domain Event Design

```
Design domain events for the {aggregate name} aggregate.

State transitions:
- {state A} -> {state B}: when {condition}
- {state B} -> {state C}: when {condition}
...

For each event, provide:
1. Event name (past tense)
2. Event properties
3. When it's raised
4. Potential consumers

Show TypeScript implementations.
```

---

## Testing Prompts

### Test Strategy

```
Create a testing strategy for a {Clean/Hexagonal/DDD} architecture project.

Stack: {language/framework}

Define tests for each layer:
1. Domain layer: what to test, how to test
2. Application layer: what to mock
3. Infrastructure layer: integration approach
4. E2E: key scenarios

Include example test code for each layer.
```

### Unit Test Generation

```
Generate unit tests for this {entity/use-case/service}:

```{language}
{paste code}
```

Cover:
1. Happy path
2. Edge cases
3. Error conditions
4. Invariant violations

Use {Jest/Vitest/pytest/etc.}. Follow AAA (Arrange-Act-Assert) pattern.
```

### Integration Test Design

```
Design integration tests for this repository:

Interface:
{paste repository interface}

Implementation uses: {database/ORM}

Tests should verify:
1. CRUD operations work correctly
2. Custom queries return expected results
3. Transaction rollback works
4. Concurrent access handling (if applicable)

Use testcontainers or in-memory database approach.
```

---

## Refactoring Prompts

### Extract Domain Logic

```
This controller has domain logic that should be moved to the domain layer:

```{language}
{paste controller code}
```

Refactor to:
1. Extract domain logic to entity/service
2. Create use case for orchestration
3. Leave controller thin (HTTP concerns only)

Show the refactored code for all files.
```

### Introduce Repository Pattern

```
This code directly accesses the database from the use case:

```{language}
{paste code}
```

Refactor to:
1. Create repository interface in domain layer
2. Move query logic to repository implementation
3. Inject repository into use case

Show the repository interface, implementation, and updated use case.
```

### Convert to Hexagonal

```
Convert this layered architecture code to Hexagonal:

Current structure:
{paste folder structure}

Example file:
```{language}
{paste code}
```

Create:
1. Port interfaces (inbound and outbound)
2. Core service implementing inbound port
3. Adapters for external dependencies

Show the new folder structure and converted code.
```

---

## Documentation Prompts

### ADR Generation

```
Create an Architecture Decision Record (ADR) for choosing {pattern} architecture.

Context:
- Project: {description}
- Team: {size and experience}
- Constraints: {list constraints}

Include:
1. Title
2. Status
3. Context
4. Decision
5. Consequences (positive and negative)
6. Alternatives considered

Use standard ADR format.
```

### Architecture Documentation

```
Generate architecture documentation for this project:

Pattern: {Clean/Hexagonal/DDD}
Structure:
{paste folder structure}

Create:
1. Architecture overview (1 paragraph)
2. Layer responsibilities (table)
3. Dependency rules (diagram - text-based)
4. File naming conventions
5. Example request flow (step by step)

Format for CLAUDE.md or README.md.
```

---

## Problem-Solving Prompts

### Circular Dependency Resolution

```
I have a circular dependency between:
- {module A}: depends on {module B}
- {module B}: depends on {module A}

Both are in the {layer} layer.

Help me resolve this by:
1. Identifying the root cause
2. Suggesting interface extraction
3. Proposing dependency inversion
4. Showing the refactored code
```

### Transaction Boundary Design

```
I need to implement a use case that:
1. Creates {entity A}
2. Updates {entity B}
3. Calls {external service}
4. Sends {notification}

Design the transaction boundaries following {Clean/Hexagonal/DDD} principles:
1. What should be in the same transaction?
2. How to handle external service failures?
3. Where does event publishing happen?
4. Show the implementation.
```

### Cross-Cutting Concerns

```
How should I implement {logging/caching/validation/authorization} in a {Clean/Hexagonal/DDD} architecture?

Current structure:
{paste folder structure}

Provide:
1. Where the implementation goes
2. How to inject into layers that need it
3. Example code
4. Any pattern recommendations (decorator, middleware, etc.)
```

---

## Best Practices for Prompting

### Do

- Provide context about your project
- Specify the architectural pattern
- Include code samples when asking for reviews
- Ask for explanations, not just code
- Request alternatives and trade-offs

### Don't

- Ask vague questions ("How do I do Clean Architecture?")
- Skip providing current state when asking for migration
- Request entire project generation in one prompt
- Ignore the pattern's principles in follow-up requests

### Iterative Refinement

```
[After receiving initial response]

This is good. Now let's refine:
1. Add error handling for {specific case}
2. Make {component} more testable by {approach}
3. Show how this would change if we need to support {new requirement}
```
