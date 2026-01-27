# LLM Prompts for Modular Monolith Design

Effective prompts for LLM-assisted modular monolith architecture and implementation.

## Domain Analysis Prompts

### Identify Bounded Contexts

```
I'm building a [type of application] with the following capabilities:
[List of features/functionality]

Help me identify bounded contexts for a modular monolith architecture:

1. Group related capabilities into distinct domains
2. For each domain, identify:
   - Core responsibilities
   - Data it owns
   - Key operations
   - Dependencies on other domains
3. Suggest module names that reflect business terminology
4. Identify potential shared kernel (truly common code)

Tech stack: [Python/Django, Go, Java/Spring, etc.]
Team size: [number]
Expected scale: [users, transactions, data volume]
```

### Analyze Existing Codebase

```
I have an existing [framework] monolith that I want to modularize.

Current structure:
[Paste directory structure or description]

Key models/entities:
[List main models]

Please analyze and suggest:
1. Natural module boundaries based on domain cohesion
2. Current coupling issues to address
3. Recommended extraction order (which module first)
4. Dependencies that need to be inverted
5. Shared code that should remain in a common package
```

### Define Module Boundaries

```
I'm designing a modular monolith for [domain/industry].

Business context:
[Describe the business domain]

Key stakeholders:
[List stakeholders and their concerns]

Help me define clear module boundaries:
1. What data does each module own exclusively?
2. What operations belong to each module?
3. Where are the interaction points between modules?
4. What events should modules publish?
5. What queries will cross module boundaries?

I want to ensure modules align with team structure and can be independently developed.
```

## Architecture Design Prompts

### Module API Design

```
Design a public API for the [ModuleName] module in a modular monolith.

Module responsibilities:
[List what this module does]

Consumers of this module:
[List other modules that will use this API]

Required operations:
[List operations needed]

Please provide:
1. Service interface with method signatures
2. DTOs for input/output (immutable, typed)
3. Custom exceptions for error cases
4. Events this module should publish
5. Events this module should handle

Use [Python/Go/Java] conventions.
Include docstrings/comments explaining each element.
```

### Event Schema Design

```
Design domain events for the [ModuleName] module.

Module operations:
[List key operations]

Other modules that need to react:
[List consumers and what they need]

For each event, provide:
1. Event name (past tense, describing what happened)
2. Event schema with all necessary fields
3. Versioning strategy
4. Example payload
5. Which modules should handle it and what they should do

Consider:
- Events should be self-contained (no need to call back)
- Include enough context for consumers
- Plan for schema evolution
```

### Database Schema Design

```
Design the database schema for the [ModuleName] module.

Module responsibilities:
[What this module does]

Data owned by this module:
[List entities/tables]

References to other modules:
[List IDs from other modules that this one needs]

Requirements:
1. Use separate schema per module
2. No foreign keys to other module schemas
3. Store only IDs for cross-module references
4. Denormalize data needed for display (if applicable)

Provide:
1. CREATE TABLE statements
2. Indexes for common queries
3. Explanation of denormalization decisions
4. Migration strategy from current schema (if applicable)
```

### Communication Pattern Selection

```
Help me choose communication patterns for my modular monolith.

Module interactions:
[List module A -> module B interactions]

Requirements:
- [Consistency requirements: strong vs eventual]
- [Performance requirements]
- [Reliability requirements]

For each interaction, recommend:
1. Sync (direct call) or async (event)?
2. Rationale for the choice
3. Error handling strategy
4. Retry/circuit breaker needs
5. Code example in [language]

Consider that this is a modular monolith (in-process), but I want to prepare for potential microservices extraction.
```

## Implementation Prompts

### Module Structure Generation

```
Generate the file structure and boilerplate for a [ModuleName] module in [framework].

Module purpose:
[Description]

Public API operations:
[List of operations]

Internal components needed:
- Domain models: [list]
- Database tables: [list]
- External integrations: [list]

Please provide:
1. Directory structure
2. __init__.py / package exports (what's public)
3. Service interface
4. DTOs
5. Domain model stubs
6. Repository interface
7. Event definitions
8. Test structure

Follow [Clean Architecture / Hexagonal / Vertical Slice] patterns.
```

### Boundary Enforcement Configuration

```
Help me configure boundary enforcement for my modular monolith.

Tech stack: [Python with import-linter / Java with ArchUnit / etc.]

Modules:
[List modules]

Allowed dependencies:
- All modules can use: shared
- [ModuleA] can call: [ModuleB], [ModuleC]
- ...

Rules to enforce:
1. Modules cannot access internal packages of other modules
2. No circular dependencies
3. Domain layer cannot depend on infrastructure
4. Only public API can be imported

Provide:
1. Configuration file content
2. Architecture test code
3. CI integration snippet
4. Common violations to watch for
```

### Migration Planning

```
Help me plan migration from traditional monolith to modular monolith.

Current state:
[Describe current architecture/structure]

Pain points:
[List current issues]

Goals:
[What we want to achieve]

Please provide:
1. Prioritized list of modules to extract
2. For each module:
   - Prerequisites
   - Steps to extract
   - Risks and mitigations
   - Validation criteria
3. Estimated complexity for each step
4. Recommended team organization during migration
5. Rollback strategy

We want to maintain continuous delivery throughout the migration.
```

### Microservices Extraction Planning

```
I have a modular monolith and want to extract [ModuleName] as a microservice.

Current module status:
- Has separate schema: [yes/no]
- Uses events for communication: [yes/no]
- Has clear API boundary: [yes/no]
- Dependencies: [list]

Target architecture:
[Describe target deployment]

Help me plan the extraction:
1. Pre-extraction checklist
2. Strangler fig implementation steps
3. API gateway/facade design
4. Database extraction strategy
5. Event migration (in-memory to message queue)
6. Rollback plan
7. Performance testing approach
8. Monitoring requirements

Timeline preference: [gradual vs rapid]
```

## Code Review Prompts

### Module Design Review

```
Review this module design for a modular monolith:

[Paste code or design document]

Check for:
1. Clear module boundaries
2. Proper use of DTOs vs domain models
3. Event design quality
4. API completeness and usability
5. Error handling
6. Testability
7. Potential coupling issues
8. Missing edge cases

Provide specific, actionable feedback with code examples for improvements.
```

### Boundary Violation Detection

```
Analyze this code for modular monolith boundary violations:

[Paste code]

Module structure:
[Describe expected module boundaries]

Check for:
1. Direct imports of internal packages
2. Shared mutable state
3. Cross-module database queries
4. Missing DTOs (using domain models directly)
5. Circular dependencies
6. God modules (doing too much)
7. Anemic modules (doing too little)

For each issue found:
1. Explain why it's a problem
2. Show how to fix it
3. Rate severity (high/medium/low)
```

### Event Contract Review

```
Review these event definitions for a modular monolith:

[Paste event schemas]

Publishing module: [name]
Consuming modules: [list]

Evaluate:
1. Event naming (past tense, descriptive)
2. Payload completeness (self-contained?)
3. Schema evolution readiness
4. Versioning strategy
5. Missing events for important state changes
6. Events that should be split or combined
7. Potential ordering issues

Provide improved versions where needed.
```

## Troubleshooting Prompts

### Circular Dependency Resolution

```
I have a circular dependency in my modular monolith:

[Module A] -> [Module B] -> [Module A]

Context:
[Explain why each module needs the other]

Current code:
[Paste relevant imports/calls]

Help me break this cycle:
1. Analyze the nature of the dependency
2. Suggest patterns to resolve it:
   - Dependency inversion
   - Events
   - Mediator
   - Extracting shared module
3. Show code examples for the recommended solution
4. Explain trade-offs of each approach
```

### Performance Optimization

```
I'm experiencing performance issues in my modular monolith:

Symptom:
[Describe the issue]

Current architecture:
[Describe relevant modules and their interactions]

Metrics:
[Response times, throughput, resource usage]

Suspected causes:
[List suspicions]

Help me diagnose and fix:
1. Likely root causes
2. How to confirm each hypothesis
3. Optimization strategies:
   - Caching within modules
   - Denormalization for queries
   - Event-based updates
   - Query optimization
4. Trade-offs of each approach
5. Implementation priority
```

### Data Consistency Issues

```
I'm having data consistency issues between modules:

Scenario:
[Describe the flow that causes issues]

Modules involved:
[List modules and their role]

Current implementation:
[Paste relevant code]

Expected behavior:
[What should happen]

Actual behavior:
[What's happening]

Help me fix this:
1. Root cause analysis
2. Is eventual consistency acceptable here?
3. Solutions:
   - Saga pattern
   - Outbox pattern
   - Compensating transactions
   - Two-phase commit (if appropriate)
4. Implementation in [language]
5. How to test the fix
```

## Meta Prompts

### Generate Custom Prompts

```
I need help generating prompts for LLM-assisted modular monolith work.

My specific context:
- Industry: [industry]
- Tech stack: [stack]
- Team experience level: [junior/mid/senior]
- Current architecture: [description]
- Main challenges: [list]

Generate 5-10 specific prompts I can use to:
1. [Specific goal 1]
2. [Specific goal 2]
3. [Specific goal 3]

Make the prompts specific enough to get actionable responses but general enough to reuse.
```

### Explain Architecture Decision

```
Explain the following modular monolith architecture decision to [audience]:

Decision:
[Describe the decision]

Context:
[Why this came up]

Options considered:
[List alternatives]

Chosen approach:
[What was decided]

Please explain:
1. For [technical/non-technical] audience
2. Why this is the right choice
3. Trade-offs accepted
4. What would change this decision
5. How to evaluate success

Use [analogies/diagrams/examples] to clarify.
```

## Best Practices for LLM Interaction

### Effective Prompting Tips

| Do | Don't |
|----|-------|
| Provide specific context | Be vague about requirements |
| Include tech stack details | Assume LLM knows your setup |
| Specify desired output format | Leave format ambiguous |
| Ask for trade-offs | Request "the best" solution |
| Request code examples | Accept abstract explanations |
| Iterate and refine | Accept first response blindly |

### Context to Always Include

1. **Tech stack** - Language, framework, database
2. **Scale** - Team size, expected load, data volume
3. **Constraints** - Budget, timeline, existing code
4. **Goals** - What success looks like
5. **Current state** - Where you are now

### Iteration Pattern

```
Initial prompt → Response → Refinement questions →
Clarified response → Implementation request →
Code review → Final adjustments
```

### Validation Checklist

Before implementing LLM suggestions:

- [ ] Does it match our coding standards?
- [ ] Are there obvious bugs or issues?
- [ ] Does it handle edge cases?
- [ ] Is error handling complete?
- [ ] Are there security concerns?
- [ ] Does it fit our existing patterns?
- [ ] Can we test it properly?
