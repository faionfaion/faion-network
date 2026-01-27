# Structural Patterns Checklist

Step-by-step checklist for pattern selection and implementation.

## Phase 1: Problem Analysis

### 1.1 Identify the Core Problem

- [ ] What is the primary challenge? (interface mismatch, complexity, memory, access control)
- [ ] Is this a design-time or runtime problem?
- [ ] Are you integrating existing code or designing new code?
- [ ] What are the performance/memory constraints?

### 1.2 Understand Current Structure

- [ ] Document existing interfaces/classes involved
- [ ] Identify dependencies between components
- [ ] Map the data flow through the system
- [ ] Note any constraints (legacy code, third-party libraries)

---

## Phase 2: Pattern Selection

### 2.1 Quick Selection Guide

**Answer these questions to narrow down patterns:**

```
Q1: Are you trying to integrate incompatible interfaces?
    YES → Consider Adapter
    NO → Continue

Q2: Do you need to add behavior dynamically without subclassing?
    YES → Consider Decorator
    NO → Continue

Q3: Do you need to simplify access to a complex subsystem?
    YES → Consider Facade
    NO → Continue

Q4: Are you working with hierarchical/tree structures?
    YES → Consider Composite
    NO → Continue

Q5: Do you need lazy loading, access control, or caching?
    YES → Consider Proxy
    NO → Continue

Q6: Do you have multiple independent dimensions of variation?
    YES → Consider Bridge (if designing up-front)
    NO → Continue

Q7: Do you have many similar objects consuming too much memory?
    YES → Consider Flyweight
    NO → Reconsider requirements
```

### 2.2 Pattern-Specific Selection Criteria

#### Adapter Checklist

- [ ] Need to use existing class with incompatible interface
- [ ] Want to create reusable class that cooperates with unrelated classes
- [ ] Adapting legacy code to new interface
- [ ] Wrapping third-party library
- [ ] Creating unified interface for multiple similar classes

**Proceed with Adapter if 2+ items checked.**

#### Bridge Checklist

- [ ] Designing new system (not retrofitting)
- [ ] Abstraction and implementation should vary independently
- [ ] Multiple platforms/backends to support
- [ ] Want to avoid class explosion from combinations
- [ ] Need runtime switching of implementations

**Proceed with Bridge if 2+ items checked.**

#### Composite Checklist

- [ ] Working with tree/hierarchical structure
- [ ] Part-whole relationships exist
- [ ] Want to treat leaves and composites uniformly
- [ ] Recursive operations needed (e.g., calculate total size)
- [ ] Structure can be represented as tree

**Proceed with Composite if 3+ items checked.**

#### Decorator Checklist

- [ ] Want to add responsibilities dynamically
- [ ] Subclassing is impractical or impossible
- [ ] Need to combine behaviors at runtime
- [ ] Responsibilities can be withdrawn
- [ ] Building middleware/filter chain

**Proceed with Decorator if 2+ items checked.**

#### Facade Checklist

- [ ] Subsystem has many classes with complex interactions
- [ ] Want to provide simple entry point
- [ ] Decoupling subsystem from clients
- [ ] Layering the system
- [ ] Creating library wrapper

**Proceed with Facade if 2+ items checked.**

#### Proxy Checklist

- [ ] Need lazy initialization of expensive objects
- [ ] Access control based on permissions required
- [ ] Caching expensive operation results
- [ ] Logging/auditing access
- [ ] Remote object representation needed

**Proceed with Proxy if 1+ items checked (proxy type determines specifics).**

#### Flyweight Checklist

- [ ] Application creates large number of similar objects
- [ ] Memory usage is a concern
- [ ] Most object state can be made extrinsic
- [ ] Identity of objects is not important
- [ ] Objects are immutable or mostly immutable

**Proceed with Flyweight if 3+ items checked.**

---

## Phase 3: Implementation Checklist by Pattern

### 3.1 Adapter Implementation

- [ ] **Define Target interface** that client expects
- [ ] **Identify Adaptee** (existing class to adapt)
- [ ] **Create Adapter class** implementing Target interface
- [ ] **Store reference** to Adaptee in Adapter
- [ ] **Implement all Target methods** by delegating to Adaptee
- [ ] **Handle interface mismatches** (parameter conversion, return values)
- [ ] **Write tests** for adapted interface
- [ ] **Document** the adaptation mapping

**Validation:**
- [ ] Client code uses only Target interface
- [ ] Adaptee class unchanged
- [ ] All Target methods work correctly

### 3.2 Bridge Implementation

- [ ] **Define Implementor interface** (low-level operations)
- [ ] **Create ConcreteImplementors** for each platform/variant
- [ ] **Define Abstraction class** with reference to Implementor
- [ ] **Implement Abstraction methods** using Implementor interface
- [ ] **Create RefinedAbstractions** if needed
- [ ] **Inject Implementor** into Abstraction (constructor or setter)
- [ ] **Write tests** for all abstraction-implementation combinations
- [ ] **Document** the two hierarchies

**Validation:**
- [ ] Abstraction and Implementor can vary independently
- [ ] Adding new implementation doesn't change abstraction
- [ ] Runtime switching works correctly

### 3.3 Composite Implementation

- [ ] **Define Component interface** with common operations
- [ ] **Create Leaf class** implementing Component
- [ ] **Create Composite class** implementing Component
- [ ] **Add child management** to Composite (add, remove, getChildren)
- [ ] **Implement Component methods** in Leaf (single object)
- [ ] **Implement Component methods** in Composite (delegate to children)
- [ ] **Handle edge cases** (empty composite, null children)
- [ ] **Write tests** for leaf, composite, and nested structures

**Validation:**
- [ ] Leaves and composites treated uniformly
- [ ] Recursive operations work correctly
- [ ] Tree traversal is efficient

### 3.4 Decorator Implementation

- [ ] **Define Component interface**
- [ ] **Create ConcreteComponent** (object being decorated)
- [ ] **Create Decorator base class** implementing Component
- [ ] **Store Component reference** in Decorator
- [ ] **Create ConcreteDecorators** adding specific behavior
- [ ] **Implement forwarding** in base Decorator
- [ ] **Add pre/post behavior** in ConcreteDecorators
- [ ] **Ensure decorators are stackable**
- [ ] **Write tests** for individual and combined decorators

**Validation:**
- [ ] Decorators can be stacked in any order
- [ ] Original component unchanged
- [ ] Each decorator adds single responsibility

### 3.5 Facade Implementation

- [ ] **Identify subsystem classes** to be wrapped
- [ ] **Define simple Facade interface** for clients
- [ ] **Create Facade class** with references to subsystem objects
- [ ] **Implement high-level methods** coordinating subsystem
- [ ] **Hide complexity** from clients
- [ ] **Keep subsystem accessible** if needed (advanced users)
- [ ] **Write tests** for facade operations
- [ ] **Document** what complexity is hidden

**Validation:**
- [ ] Client code simpler than direct subsystem access
- [ ] Subsystem still works independently
- [ ] Facade doesn't add business logic

### 3.6 Proxy Implementation

- [ ] **Define Subject interface** for real and proxy objects
- [ ] **Create RealSubject** implementing Subject
- [ ] **Create Proxy class** implementing Subject
- [ ] **Store reference** to RealSubject (lazy or eager)
- [ ] **Implement access control** (if protection proxy)
- [ ] **Implement lazy loading** (if virtual proxy)
- [ ] **Implement caching** (if cache proxy)
- [ ] **Delegate to RealSubject** after pre-processing
- [ ] **Write tests** for proxy behavior

**Validation:**
- [ ] Proxy and RealSubject interchangeable
- [ ] Access control enforced correctly
- [ ] Lazy loading works as expected

### 3.7 Flyweight Implementation

- [ ] **Identify intrinsic state** (shared, immutable)
- [ ] **Identify extrinsic state** (context-specific)
- [ ] **Create Flyweight class** storing only intrinsic state
- [ ] **Make Flyweight immutable** for thread safety
- [ ] **Create FlyweightFactory** managing flyweight pool
- [ ] **Implement get method** returning existing or new flyweight
- [ ] **Modify client** to pass extrinsic state to flyweight methods
- [ ] **Measure memory savings**
- [ ] **Write tests** including concurrency tests

**Validation:**
- [ ] Flyweights are shared correctly
- [ ] Extrinsic state passed correctly
- [ ] Memory usage reduced significantly

---

## Phase 4: Integration Checklist

### 4.1 Code Integration

- [ ] Pattern integrated with existing codebase
- [ ] Dependencies injected properly
- [ ] No circular dependencies introduced
- [ ] Backward compatibility maintained (if required)

### 4.2 Testing

- [ ] Unit tests for pattern components
- [ ] Integration tests with real dependencies
- [ ] Edge case tests (empty, null, large inputs)
- [ ] Performance tests (if applicable)
- [ ] Concurrency tests (Flyweight, Proxy)

### 4.3 Documentation

- [ ] Pattern usage documented in code comments
- [ ] README updated with pattern description
- [ ] Architecture Decision Record (ADR) created
- [ ] Examples provided for common use cases

---

## Phase 5: Review Checklist

### 5.1 Design Principles

- [ ] **Open/Closed**: Can extend without modifying?
- [ ] **Single Responsibility**: Each class has one reason to change?
- [ ] **Liskov Substitution**: Subtypes substitutable for base types?
- [ ] **Interface Segregation**: No client depends on unused methods?
- [ ] **Dependency Inversion**: Depends on abstractions, not concretions?

### 5.2 Pattern-Specific Review

#### Adapter Review
- [ ] Adapter doesn't leak Adaptee details
- [ ] No business logic in Adapter (just translation)
- [ ] Type conversion handled correctly

#### Bridge Review
- [ ] Two hierarchies truly independent
- [ ] No shortcuts bypassing the bridge
- [ ] Implementation switching tested

#### Composite Review
- [ ] Consistent interface for leaves and composites
- [ ] Deep nesting handled efficiently
- [ ] Clear ownership of children

#### Decorator Review
- [ ] Decorators can be reordered
- [ ] No hidden state coupling between decorators
- [ ] Base component still usable standalone

#### Facade Review
- [ ] Facade is thin (doesn't add logic)
- [ ] Subsystem still testable independently
- [ ] Common operations covered

#### Proxy Review
- [ ] Proxy transparent to client
- [ ] No memory leaks (lazy loading lifecycle)
- [ ] Thread safety considered

#### Flyweight Review
- [ ] Clear separation of intrinsic/extrinsic state
- [ ] Factory manages sharing correctly
- [ ] No mutable intrinsic state

---

## Phase 6: Common Mistakes to Avoid

### 6.1 General Mistakes

- [ ] **Over-engineering**: Using pattern when not needed
- [ ] **Wrong pattern**: Mistaking Adapter for Bridge or Proxy for Decorator
- [ ] **Ignoring performance**: Not measuring impact
- [ ] **Missing tests**: Pattern logic untested

### 6.2 Pattern-Specific Mistakes

| Pattern | Common Mistake | Prevention |
|---------|----------------|------------|
| Adapter | Adding business logic to adapter | Keep adapter as thin translation layer |
| Bridge | Using Bridge when Adapter suffices | Bridge is for up-front design only |
| Composite | Inconsistent interface for leaves/composites | Ensure Component interface covers all cases |
| Decorator | Decorator order matters unexpectedly | Document and test decorator ordering |
| Facade | Facade becomes God class | Keep facade focused, create multiple if needed |
| Proxy | Memory leak with lazy proxy | Implement proper lifecycle management |
| Flyweight | Mutable intrinsic state | Make flyweights immutable |

---

## Quick Reference: Pattern Selection

| Symptom | Pattern | Alternative |
|---------|---------|-------------|
| "Can't use this class - wrong interface" | Adapter | - |
| "Too many subclass combinations" | Bridge | Decorator |
| "Want to treat tree uniformly" | Composite | - |
| "Add features without inheritance" | Decorator | Proxy |
| "Subsystem too complex" | Facade | - |
| "Need lazy/cached/secured access" | Proxy | - |
| "Too many similar objects" | Flyweight | Object Pool |
