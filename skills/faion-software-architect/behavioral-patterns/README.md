# Behavioral Design Patterns

Behavioral patterns define how objects interact, communicate, and distribute responsibilities. They focus on algorithms, assignment of responsibilities, and communication between objects.

## Overview

| Pattern | Purpose | Common Use Cases |
|---------|---------|------------------|
| **Strategy** | Interchangeable algorithms at runtime | Payment processing, sorting, validation |
| **Observer** | One-to-many dependency notification | Event systems, reactive programming, pub/sub |
| **Command** | Encapsulate request as object | Undo/redo, queuing, macro recording |
| **State** | Object behavior changes with internal state | Workflows, FSMs, document lifecycle |
| **Chain of Responsibility** | Pass request along handler chain | Middleware, validation, logging |
| **Template Method** | Define algorithm skeleton, defer steps | Data processing, lifecycle hooks |
| **Mediator** | Centralize complex communication | Chat rooms, air traffic control, UI components |
| **Iterator** | Sequential access without exposing internals | Collections, streams, generators |
| **Visitor** | Add operations without modifying classes | AST traversal, serialization, reporting |

## When to Use Each Pattern

### Strategy Pattern

**Use when:**
- Multiple algorithms for the same task (e.g., payment methods, compression)
- Need to swap behavior at runtime without conditionals
- Want to isolate algorithm implementation from consuming code

**Avoid when:**
- Only 2-3 simple algorithms that rarely change
- Clients don't need to know about different strategies

**Modern trends (2025-2026):**
- Functional implementations using higher-order functions
- Strategy as dependency injection in frameworks
- TypeScript discriminated unions for type-safe strategies

### Observer Pattern

**Use when:**
- Objects need to be notified of state changes
- Implementing event-driven architectures
- Building reactive systems (RxJS, signals)

**Avoid when:**
- Simple one-to-one relationships
- Notification order matters critically

**Modern trends:**
- Reactive streams (RxJS, RxPy, channels in Go)
- Signals in frontend frameworks (Solid, Angular, Vue)
- Event sourcing integration

### Command Pattern

**Use when:**
- Need undo/redo functionality
- Queuing operations for later execution
- Logging or auditing all actions
- Implementing transactions or sagas

**Avoid when:**
- Simple operations without undo requirements
- No need for operation history

**Modern trends:**
- CQRS (Command Query Responsibility Segregation)
- Event sourcing with commands
- Saga orchestration in microservices

### State Pattern

**Use when:**
- Object behavior varies significantly by state
- Complex conditional logic based on state
- Implementing finite state machines

**Avoid when:**
- Only 2-3 simple states with minimal logic
- States rarely change

**Modern trends:**
- XState for TypeScript state machines
- Type-safe FSMs with discriminated unions
- Functional state machines with pure transitions

### Chain of Responsibility

**Use when:**
- Multiple handlers may process a request
- Handler set should be dynamic
- Implementing middleware pipelines

**Avoid when:**
- Only one handler needed
- Request must always be handled

**Modern trends:**
- Express/Koa/Hono middleware patterns
- Pipeline operators
- Functional composition chains

### Template Method

**Use when:**
- Algorithm structure is fixed, steps vary
- Multiple classes share workflow structure
- Framework extension points needed

**Avoid when:**
- Algorithm needs complete flexibility
- Only one implementation exists

**Modern trends:**
- Hooks and lifecycle methods in React
- Abstract base classes with default implementations
- Protocol/trait-based approaches

### Mediator Pattern

**Use when:**
- Many objects communicate in complex ways
- Reducing coupling between components
- Centralized control point needed

**Avoid when:**
- Simple direct communication suffices
- Mediator would become a god object

**Modern trends:**
- Message brokers (RabbitMQ, Kafka)
- Redux/Vuex as UI mediators
- Event bus implementations

### Iterator Pattern

**Use when:**
- Need uniform traversal of collections
- Hiding collection implementation details
- Multiple traversal algorithms needed

**Modern trends:**
- Built-in iterators in all modern languages
- Generators and async iterators
- Stream processing (lazy evaluation)

### Visitor Pattern

**Use when:**
- Adding operations to class hierarchy without modification
- Operations on heterogeneous collections
- AST processing, serialization

**Avoid when:**
- Class hierarchy changes frequently
- Operations are simple or few

**Modern trends:**
- Pattern matching as alternative
- Double dispatch implementations
- AST traversal in compilers/transpilers

## Pattern Relationships

```
Strategy <-> State: Both change behavior, but State transitions automatically

Observer <-> Mediator: Observer is distributed, Mediator is centralized

Command <-> Memento: Command stores operations, Memento stores state

Chain of Responsibility <-> Composite: Often used together for tree traversal

Visitor <-> Iterator: Visitor processes elements, Iterator provides access
```

## Pattern Selection Matrix

| Situation | Primary Pattern | Alternative |
|-----------|-----------------|-------------|
| "Multiple algorithms, choose at runtime" | Strategy | Command |
| "Notify many objects of changes" | Observer | Mediator |
| "Undo/redo support needed" | Command | Memento |
| "Object behaves differently per state" | State | Strategy |
| "Pipeline of handlers" | Chain of Responsibility | Decorator |
| "Same algorithm structure, different steps" | Template Method | Strategy |
| "Reduce many-to-many dependencies" | Mediator | Observer |
| "Traverse collection uniformly" | Iterator | Visitor |
| "Add operations without changing classes" | Visitor | Strategy |

## LLM Usage Tips

### When Designing with LLMs

1. **Describe the problem, not the solution**: "Users can pay with credit card, PayPal, or crypto. How should I structure payment processing?" rather than "Implement Strategy pattern"

2. **Ask for trade-offs**: "What are the drawbacks of using Observer here vs. direct callbacks?"

3. **Request alternatives**: "Show me both OOP and functional implementations of this pattern"

4. **Validate complexity**: "Is this pattern overkill for my 3-state workflow?"

### Common LLM Mistakes to Avoid

- Over-engineering simple scenarios with complex patterns
- Ignoring language-specific idioms (e.g., Go channels vs. Observer)
- Not considering testing implications
- Missing type safety opportunities in TypeScript

### Effective Prompts

```
"I need to implement [feature] in [language]. The requirements are:
- [Requirement 1]
- [Requirement 2]
Which behavioral pattern fits best and why?"
```

```
"Review this [pattern] implementation. Does it follow modern best practices?
What would you change for [Python/TypeScript/Go]?"
```

## External Resources

### Official References
- [Refactoring.guru - Behavioral Patterns](https://refactoring.guru/design-patterns/behavioral-patterns)
- [SourceMaking - Behavioral Patterns](https://sourcemaking.com/design_patterns/behavioral_patterns)

### Books
- "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF)
- "Head First Design Patterns" (Freeman & Robson)
- "Patterns of Enterprise Application Architecture" (Fowler)

### Modern Resources
- [XState Documentation](https://statemachine.io/) - State machines in TypeScript
- [RxJS Documentation](https://rxjs.dev/) - Reactive extensions for JavaScript
- [Python Design Patterns](https://python-patterns.guide/)

### GitHub Repositories
- [design-patterns-typescript](https://github.com/DiegoRomario/design-patterns-typescript) - GoF patterns in TypeScript
- [faif/python-patterns](https://github.com/faif/python-patterns) - Patterns in Python
- [tmrts/go-patterns](https://github.com/tmrts/go-patterns) - Patterns in Go

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step pattern selection checklist |
| [examples.md](examples.md) | Real-world implementations by pattern |
| [templates.md](templates.md) | Copy-paste templates for each pattern |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted design |


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related

- [creational-patterns/](../creational-patterns/) - Object creation patterns
- [structural-patterns/](../structural-patterns/) - Object composition patterns
- [distributed-patterns/](../distributed-patterns/) - Distributed system patterns
