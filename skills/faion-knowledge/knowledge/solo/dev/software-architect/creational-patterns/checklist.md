# Creational Design Patterns Checklist

> Comprehensive step-by-step guidance for selecting and implementing creational patterns (Factory, Builder, Singleton, Prototype, DI, Object Pool).

## Phase 1: Requirements Analysis

### 1.1 Object Creation Needs

- [ ] **Identify creation scenarios**
  - How many types of objects need to be created?
  - Are objects created frequently or rarely?
  - Is object creation triggered by user actions, system events, or scheduled tasks?

- [ ] **Analyze object lifecycle**
  - What is the expected lifetime of objects?
  - Are objects created once and reused, or created/destroyed frequently?
  - Do objects need to be pooled or cached?

- [ ] **Determine creation complexity**
  - Does object creation require multiple steps?
  - Are there optional parameters?
  - Is initialization order important?

### 1.2 Dependency Analysis

- [ ] **Map dependencies**
  - What other objects does the new object depend on?
  - Are dependencies required or optional?
  - Can dependencies be injected?

- [ ] **Identify coupling concerns**
  - Is the client code tightly coupled to concrete classes?
  - Would changing implementation require client code changes?
  - Are there testability concerns?

---

## Phase 2: Pattern Selection

### 2.1 Decision Matrix

Use this matrix to guide pattern selection:

| Question | Yes | No |
|----------|-----|-----|
| Multiple related product types? | Abstract Factory | Continue |
| Single product with variants? | Factory Method | Continue |
| Complex object with many params? | Builder | Continue |
| Need to copy existing objects? | Prototype | Continue |
| Expensive object creation/reuse? | Object Pool | Continue |
| Need loose coupling/testability? | Dependency Injection | Continue |
| Exactly one global instance? | Singleton (if DI not possible) | Continue |

### 2.2 Factory Method Checklist

Use when:
- [ ] Class cannot anticipate the class of objects it must create
- [ ] Class wants subclasses to specify the objects it creates
- [ ] Classes delegate responsibility to one of several helper subclasses

Do NOT use when:
- [ ] There's only one product type with no variants
- [ ] Object creation is trivial
- [ ] Adding a new factory requires modifying existing code

### 2.3 Abstract Factory Checklist

Use when:
- [ ] System should be independent of how products are created
- [ ] System should be configured with one of multiple product families
- [ ] Family of related products must be used together
- [ ] You want to provide a library of products, revealing only interfaces

Do NOT use when:
- [ ] Only one family of products exists
- [ ] Products are unrelated
- [ ] Adding new product types is more common than adding new families

### 2.4 Builder Checklist

Use when:
- [ ] Object has 4+ constructor parameters
- [ ] Many parameters are optional
- [ ] Need to create immutable objects
- [ ] Same construction process should create different representations
- [ ] Object creation requires multiple steps in specific order

Do NOT use when:
- [ ] Object has simple construction (1-3 required params)
- [ ] No optional parameters exist
- [ ] Object mutability is acceptable

### 2.5 Prototype Checklist

Use when:
- [ ] Object creation is expensive (network, database, complex computation)
- [ ] Classes to instantiate are specified at runtime
- [ ] Need to avoid building class hierarchies of factories
- [ ] Instances of a class can have one of only a few combinations of state

Do NOT use when:
- [ ] Objects contain circular references (complicates cloning)
- [ ] Objects contain external resources (file handles, connections)
- [ ] Object creation is cheap
- [ ] Objects require unique initialization each time

### 2.6 Singleton Checklist

**Use with extreme caution** when:
- [ ] Exactly one instance of a class is required
- [ ] Instance must be accessible from well-known access point
- [ ] The sole instance should be extensible by subclassing
- [ ] Cross-cutting concern (logging, metrics) where DI is impractical

**Red flags - Consider alternatives:**
- [ ] Unit testing is important for your application
- [ ] Multiple threads will access the singleton
- [ ] You need to mock/stub the singleton in tests
- [ ] The singleton manages state that changes
- [ ] You're using it as a "convenient global variable"

### 2.7 Dependency Injection Checklist

Use when:
- [ ] Testability is a priority
- [ ] Need to swap implementations at runtime or for testing
- [ ] Building a large application with many components
- [ ] Using a framework that supports DI (Spring, NestJS, FastAPI)
- [ ] Want to follow SOLID principles

Framework selection:
- [ ] **Python:** dependency-injector, FastAPI built-in, injector
- [ ] **TypeScript:** InversifyJS, TSyringe, NestJS built-in
- [ ] **Go:** Wire (compile-time), Dig/Fx (runtime)
- [ ] **Java:** Spring, Guice, Dagger
- [ ] **C#:** .NET Core DI, Autofac

### 2.8 Object Pool Checklist

Use when:
- [ ] Object creation is expensive (>1ms for creation)
- [ ] Objects are used frequently but for short periods
- [ ] There's a limit on the number of objects that can exist
- [ ] Memory allocation/deallocation causes GC pressure

Configuration considerations:
- [ ] Initial pool size determined
- [ ] Maximum pool size defined
- [ ] Idle object eviction policy set
- [ ] Object validation strategy chosen
- [ ] Timeout for acquiring objects defined

---

## Phase 3: Implementation

### 3.1 Pre-Implementation

- [ ] **Document decision**
  - Create ADR (Architecture Decision Record) if significant
  - Note alternatives considered and why rejected
  - Document expected benefits and trade-offs

- [ ] **Design interface**
  - Define abstract interfaces/protocols first
  - Ensure interface segregation (no unused methods)
  - Consider future extensibility

- [ ] **Plan for testing**
  - How will this be unit tested?
  - What mocks/stubs are needed?
  - Are integration tests required?

### 3.2 Implementation Checklist by Pattern

#### Factory Method

- [ ] Define product interface with all required methods
- [ ] Create concrete product implementations
- [ ] Define creator class with factory method (abstract or default)
- [ ] Create concrete creators returning specific products
- [ ] Ensure factory method is only creation point for products

#### Abstract Factory

- [ ] Define abstract factory interface with create methods for each product
- [ ] Define abstract product interfaces for each product type
- [ ] Create concrete factories implementing the abstract factory
- [ ] Create concrete products for each factory
- [ ] Ensure client uses only abstract interfaces

#### Builder

- [ ] Define product class with all attributes
- [ ] Create builder class with fluent methods for each attribute
- [ ] Add reset() method to builder if reusable
- [ ] Add validation in build() method
- [ ] Consider Director class for common configurations
- [ ] Ensure product is immutable after build (if required)

#### Prototype

- [ ] Implement Cloneable/Prototype interface
- [ ] Decide shallow vs deep copy for each field
- [ ] Handle circular references if present
- [ ] Consider prototype registry for common prototypes
- [ ] Document which fields are cloned vs shared

#### Singleton

- [ ] Make constructor private
- [ ] Create static instance holder
- [ ] Implement thread-safe lazy initialization
- [ ] Consider double-checked locking or initialization-on-demand holder
- [ ] Document thread-safety guarantees
- [ ] **ADD WARNING COMMENT** about testing difficulties

#### Dependency Injection

- [ ] Define interfaces for all dependencies
- [ ] Use constructor injection for required dependencies
- [ ] Use setter injection for optional dependencies
- [ ] Configure container bindings
- [ ] Define scopes (singleton, transient, scoped)
- [ ] Set up test container with mocks

#### Object Pool

- [ ] Implement pool with thread-safe acquisition/release
- [ ] Add object validation before return to pool
- [ ] Implement object reset/cleanup
- [ ] Add metrics for pool utilization
- [ ] Configure timeouts for acquisition
- [ ] Handle pool exhaustion gracefully

### 3.3 Post-Implementation

- [ ] **Write tests**
  - Unit tests for each component
  - Integration tests for pattern usage
  - Edge cases (null inputs, concurrent access, etc.)

- [ ] **Document usage**
  - Add code comments explaining pattern usage
  - Update README/docs with examples
  - Add to architecture documentation

- [ ] **Review**
  - Code review with focus on pattern implementation
  - Verify pattern solves the original problem
  - Check for over-engineering

---

## Phase 4: Validation

### 4.1 Quality Checklist

- [ ] **Single Responsibility:** Each class has one reason to change
- [ ] **Open/Closed:** New types can be added without modifying existing code
- [ ] **Liskov Substitution:** Derived classes work through base class interface
- [ ] **Interface Segregation:** Clients don't depend on unused interfaces
- [ ] **Dependency Inversion:** High-level modules don't depend on low-level modules

### 4.2 Testing Checklist

- [ ] Can create objects through the pattern successfully
- [ ] Pattern handles edge cases gracefully
- [ ] Concurrent access works correctly (if applicable)
- [ ] Pattern can be mocked/stubbed in tests
- [ ] Performance meets requirements
- [ ] Memory usage is acceptable

### 4.3 Maintainability Checklist

- [ ] Adding new product/factory types is straightforward
- [ ] Pattern doesn't introduce unnecessary complexity
- [ ] Team understands the pattern and its purpose
- [ ] Pattern is used consistently across codebase
- [ ] Documentation is up to date

---

## Anti-Pattern Detection

### Red Flags

| Anti-Pattern | Description | Fix |
|--------------|-------------|-----|
| **Factory for one type** | Factory that only creates one concrete type | Use simple constructor |
| **Builder for simple object** | Builder for object with 1-2 params | Use constructor |
| **Singleton abuse** | Using singleton as "global variable" | Use Dependency Injection |
| **Over-pooling** | Pooling cheap-to-create objects | Remove pool, create directly |
| **Prototype for unique objects** | Cloning objects that need unique initialization | Use Factory |
| **DI for simple scripts** | Full DI container for 100-line script | Use manual injection |

### Code Smells

- [ ] Factory with switch statement on type string
- [ ] Builder with no optional parameters
- [ ] Singleton accessed directly instead of through DI
- [ ] Pool that never returns objects
- [ ] Prototype with no clone implementation

---

## Quick Reference Card

```
FACTORY METHOD
├─ When: Multiple product types, subclass decides
├─ Structure: Creator → ConcreteCreator → Product
└─ Test: Mock Creator, verify Product type

ABSTRACT FACTORY
├─ When: Families of related products
├─ Structure: Factory → ConcreteFactory → ProductA, ProductB
└─ Test: Inject different factory, verify family consistency

BUILDER
├─ When: Many optional params, step-by-step construction
├─ Structure: Builder → ConcreteBuilder → Product
└─ Test: Build with various param combinations

SINGLETON
├─ When: Exactly one instance (use DI instead if possible)
├─ Structure: Class with private constructor, static instance
└─ Test: Reset instance between tests, or use DI

PROTOTYPE
├─ When: Expensive creation, need copies
├─ Structure: Prototype interface with clone()
└─ Test: Verify clone independence, deep vs shallow

DEPENDENCY INJECTION
├─ When: Testability, loose coupling
├─ Structure: Interface → Implementation, Container wires
└─ Test: Inject mocks via container

OBJECT POOL
├─ When: Expensive objects, frequent reuse
├─ Structure: Pool manages acquire/release
└─ Test: Verify object reset, pool exhaustion handling
```
