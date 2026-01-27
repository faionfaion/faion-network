# Pattern Selection Checklist

Step-by-step checklist for selecting and implementing design patterns.

## Phase 1: Problem Analysis

### 1.1 Identify the Problem

- [ ] Document the specific problem to solve
- [ ] Identify pain points in current implementation
- [ ] List symptoms (code duplication, tight coupling, etc.)
- [ ] Determine if problem is recurring or one-time

### 1.2 Understand Context

- [ ] What is the expected system scale?
- [ ] What are the performance requirements?
- [ ] What languages/frameworks are in use?
- [ ] What is the team's experience level?
- [ ] What are the maintenance expectations?

### 1.3 Constraint Assessment

| Constraint | Impact | Notes |
|------------|--------|-------|
| Performance | Low/Medium/High | |
| Memory | Low/Medium/High | |
| Testability | Required/Nice-to-have | |
| Extensibility | Required/Nice-to-have | |
| Team familiarity | Low/Medium/High | |

## Phase 2: Pattern Category Selection

### 2.1 Creational Pattern Indicators

Use when the problem involves:
- [ ] Complex object construction
- [ ] Object creation flexibility needed
- [ ] Hide concrete classes from client
- [ ] Control over instantiation process

**Decision tree:**
```
Complex object with many parameters? → Builder
Object family that varies together? → Abstract Factory
Single creation point, type varies? → Factory Method
Expensive object, need to reuse? → Prototype
Only one instance needed? → Singleton (use sparingly)
Need runtime configuration? → Dependency Injection
```

### 2.2 Structural Pattern Indicators

Use when the problem involves:
- [ ] Incompatible interfaces
- [ ] Complex object hierarchies
- [ ] Adding features without modification
- [ ] Controlling object access

**Decision tree:**
```
Incompatible interface to adapt? → Adapter
Multiple dimensions of variation? → Bridge
Tree structure with uniform treatment? → Composite
Add behavior without subclassing? → Decorator
Complex subsystem to simplify? → Facade
Many similar objects sharing state? → Flyweight
Control access or add behavior transparently? → Proxy
```

### 2.3 Behavioral Pattern Indicators

Use when the problem involves:
- [ ] Algorithm variation
- [ ] Object communication
- [ ] State management
- [ ] Request handling

**Decision tree:**
```
Vary algorithm at runtime? → Strategy
Notify multiple objects of changes? → Observer
Encapsulate request as object? → Command
Behavior changes with state? → State
Pass request along chain? → Chain of Responsibility
Define algorithm skeleton? → Template Method
Traverse collection? → Iterator
Reduce many-to-many dependencies? → Mediator
Add operations without modifying classes? → Visitor
Save and restore state? → Memento
```

## Phase 3: Pattern Validation

### 3.1 Fit Assessment

| Criterion | Pattern fits? | Notes |
|-----------|--------------|-------|
| Solves the core problem | Yes/No/Partial | |
| Appropriate complexity | Yes/No | |
| Team can implement | Yes/No | |
| Maintainable long-term | Yes/No | |
| Testable | Yes/No | |

### 3.2 Trade-off Analysis

For the selected pattern, evaluate:

- [ ] **Benefits confirmed:** List expected improvements
- [ ] **Costs identified:** Additional complexity, classes, etc.
- [ ] **Alternatives considered:** Other patterns or simpler solutions
- [ ] **Over-engineering check:** Is pattern necessary, or is simpler solution better?

### 3.3 Anti-Pattern Check

Verify you are NOT falling into:

| Anti-Pattern | Check | Status |
|--------------|-------|--------|
| Pattern-itis | Using pattern for its own sake | |
| Golden Hammer | Forcing same pattern everywhere | |
| Premature optimization | Pattern adds unnecessary complexity | |
| God Object | Pattern creates oversized class | |
| Speculative Generality | Pattern for hypothetical future needs | |

## Phase 4: Implementation Planning

### 4.1 Design

- [ ] Draw class/component diagram
- [ ] Identify interfaces and abstract classes
- [ ] Define method signatures
- [ ] Plan for extensibility points
- [ ] Document pattern intent in code comments

### 4.2 Integration Points

- [ ] Identify where pattern connects to existing code
- [ ] Plan refactoring steps if needed
- [ ] Define API contracts
- [ ] Consider backward compatibility

### 4.3 Testing Strategy

| Test Type | Coverage Target |
|-----------|-----------------|
| Unit tests | Pattern components in isolation |
| Integration tests | Pattern with dependent code |
| Behavior tests | End-to-end scenarios |

## Phase 5: Implementation

### 5.1 Step-by-Step Implementation

- [ ] Create interfaces/protocols first
- [ ] Implement concrete classes
- [ ] Wire up dependencies
- [ ] Add factory/builder if needed
- [ ] Write unit tests alongside implementation

### 5.2 Code Quality Gates

- [ ] Single Responsibility: Each class has one reason to change
- [ ] Open/Closed: Open for extension, closed for modification
- [ ] Liskov Substitution: Subtypes are substitutable
- [ ] Interface Segregation: No client depends on unused methods
- [ ] Dependency Inversion: Depend on abstractions

### 5.3 Documentation

- [ ] Document pattern usage in README or ADR
- [ ] Add code comments explaining pattern choice
- [ ] Create usage examples
- [ ] Update architecture diagrams

## Phase 6: Validation

### 6.1 Code Review Checklist

- [ ] Pattern correctly implements its intent
- [ ] No unnecessary complexity added
- [ ] Code is readable and maintainable
- [ ] Tests cover pattern behavior
- [ ] Documentation is complete

### 6.2 Pattern Smell Detection

Watch for these implementation smells:

| Smell | Indicates | Action |
|-------|-----------|--------|
| Too many classes | Over-engineering | Simplify or reconsider pattern |
| Complex inheritance | Wrong pattern | Consider composition-based pattern |
| Tight coupling | Implementation leak | Review interface design |
| Duplicate code | Incomplete pattern | Extract common behavior |
| Hard to test | Poor separation | Improve dependency injection |

## Quick Reference: Common Combinations

| Scenario | Pattern Combination |
|----------|---------------------|
| Plugin system | Factory + Strategy |
| Undo/redo | Command + Memento |
| Event handling | Observer + Mediator |
| Document processing | Composite + Visitor |
| Caching proxy | Proxy + Flyweight |
| Request pipeline | Chain of Responsibility + Command |
| State machine | State + Observer |
| Builder validation | Builder + Strategy |

## Quick Reference: Pattern Selection Matrix

| Need | Primary Pattern | Alternatives |
|------|-----------------|--------------|
| Create complex objects | Builder | Factory, Prototype |
| Plug-in different algorithms | Strategy | Template Method |
| Handle events/notifications | Observer | Mediator, Pub/Sub |
| Add features dynamically | Decorator | Proxy, Composite |
| Simplify complex API | Facade | Adapter |
| Manage object state | State | Strategy |
| Queue operations | Command | Observer |
| Access control | Proxy | Decorator |

---

*Pattern Selection Checklist v1.0*
