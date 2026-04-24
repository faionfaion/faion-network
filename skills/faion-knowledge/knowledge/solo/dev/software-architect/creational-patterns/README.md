# Creational Design Patterns

> Object creation mechanisms that increase flexibility and reuse of existing code.

## Overview

Creational patterns abstract the instantiation process, making systems independent of how objects are created, composed, and represented. They encapsulate knowledge about which concrete classes the system uses and hide how instances of these classes are created and combined.

## Pattern Catalog

| Pattern | Purpose | Complexity | Use When |
|---------|---------|------------|----------|
| [Factory Method](#factory-method) | Create objects without specifying exact class | Low | Multiple related classes, extensibility needed |
| [Abstract Factory](#abstract-factory) | Create families of related objects | Medium | Platform-specific UIs, themed components |
| [Builder](#builder) | Construct complex objects step by step | Medium | Many optional parameters, immutable objects |
| [Singleton](#singleton) | Ensure single instance globally | Low | Logging, config, connection pools |
| [Prototype](#prototype) | Clone existing objects | Low | Expensive initialization, runtime configuration |
| [Dependency Injection](#dependency-injection) | Decouple object creation from usage | Medium | Testability, loose coupling, modularity |
| [Object Pool](#object-pool) | Reuse expensive objects | Medium | Database connections, thread pools, buffers |

## Quick Selection Guide

```
Need to create objects without specifying class?
├─ One product type → Factory Method
└─ Family of products → Abstract Factory

Object has many optional parameters?
└─ Builder

Need exactly one instance?
├─ Testing important → Dependency Injection (singleton scope)
└─ Cross-cutting concern (logging) → Singleton (carefully)

Object expensive to create?
├─ Need copies → Prototype
└─ Need reuse → Object Pool

Need loose coupling and testability?
└─ Dependency Injection
```

---

## Factory Method

**Intent:** Define an interface for creating objects, letting subclasses decide which class to instantiate.

### When to Use

- Object type determined at runtime
- Class cannot anticipate the type of objects it must create
- Subclasses should specify the objects they create

### Structure

```
Creator (abstract)
├── factoryMethod(): Product  ← abstract
└── someOperation()           ← uses factoryMethod()

ConcreteCreatorA
└── factoryMethod(): ConcreteProductA

ConcreteCreatorB
└── factoryMethod(): ConcreteProductB
```

### Key Considerations

- **Pros:** Single Responsibility, Open/Closed Principle, loose coupling
- **Cons:** Can lead to many subclasses
- **Evolution:** Often starts as Factory Method, evolves to Abstract Factory or Builder

---

## Abstract Factory

**Intent:** Create families of related objects without specifying concrete classes.

### When to Use

- System should be independent of how products are created
- System should be configured with one of multiple families of products
- Family of related products designed to be used together
- Provide a library of products, revealing only interfaces

### Structure

```
AbstractFactory
├── createProductA(): AbstractProductA
└── createProductB(): AbstractProductB

ConcreteFactory1
├── createProductA(): ProductA1
└── createProductB(): ProductB1

ConcreteFactory2
├── createProductA(): ProductA2
└── createProductB(): ProductB2
```

### Key Considerations

- **Pros:** Ensures product compatibility, isolates concrete classes
- **Cons:** Difficult to add new product types
- **Pattern Combinations:** Often implemented with Factory Methods, can use Prototype

---

## Builder

**Intent:** Construct complex objects step by step, allowing different representations.

### When to Use

- Object has many optional parameters
- Need to create immutable objects
- Object requires multiple steps to create
- Same construction process should create different representations

### Structure

```
Builder (interface)
├── buildPartA()
├── buildPartB()
└── getResult(): Product

ConcreteBuilder
├── buildPartA()
├── buildPartB()
└── getResult(): Product

Director (optional)
└── construct(builder)
```

### Key Considerations

- **Pros:** Construct step by step, reuse code, Single Responsibility Principle
- **Cons:** Code complexity increases with many builder classes
- **Modern Usage:** Fluent interfaces, method chaining common in modern implementations

---

## Singleton

**Intent:** Ensure a class has only one instance and provide global access point.

### When to Use

- Exactly one instance needed (logging, config, connection pool)
- Instance must be accessible from well-known access point
- Sole instance should be extensible by subclassing

### Modern Perspective (2025)

> **Warning:** Singleton is considered an anti-pattern in many contexts. The Gang of Four themselves noted it would likely not be included in a modern reprint of Design Patterns.

**Problems with Singleton:**
- Makes testing difficult (40% increase in test complexity per JetBrains surveys)
- Hidden dependencies
- Violates Single Responsibility Principle
- Global state issues in concurrent systems

**Alternatives:**
1. **Dependency Injection** (preferred) - frameworks manage lifecycle
2. **Module-level instance** - Python/JS modules are singletons by nature
3. **Monostate Pattern** - multiple instances share state
4. **Service Locator** - centralized registry

### When Singleton Still Makes Sense

- **Ambient dependencies:** Logging, metrics (cross-cutting concerns)
- **Hardware resources:** Printer spooler, device drivers
- **Truly global configuration:** Read-only, immutable config

---

## Prototype

**Intent:** Create new objects by copying existing instances.

### When to Use

- Object creation is expensive (database fetch, network call, complex computation)
- System should be independent of how products are created and represented
- Classes to instantiate specified at runtime
- Avoid building class hierarchies of factories

### Cloning Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Shallow Copy** | Copies object, references shared | Immutable nested objects |
| **Deep Copy** | Copies entire object graph | Mutable nested objects |

### Implementation Approaches

1. **Clone Method:** Override clone() in each class
2. **Copy Constructor:** Constructor taking same type as parameter
3. **Serialization:** Serialize and deserialize (resource-intensive)

### Key Considerations

- **Pros:** Clone without coupling to concrete classes, avoid repeated initialization
- **Cons:** Complex for objects with circular references, deep copy overhead
- **Caution:** Objects with external resources (file handles, connections) may not clone properly

---

## Dependency Injection

**Intent:** Separate object creation from object usage to promote loose coupling.

### Types of Injection

| Type | Description | Use Case |
|------|-------------|----------|
| **Constructor Injection** | Dependencies via constructor | Required dependencies |
| **Setter Injection** | Dependencies via setters | Optional dependencies |
| **Interface Injection** | Dependency provides injector method | Less common |

### Why DI Over Singleton

According to 2024 Stack Overflow Developer Survey, applications using DI reduce maintenance bugs by 27%:

- **Testability:** Inject mocks easily (70% of high-performing teams use mocking frameworks)
- **Modularity:** Swap implementations without code changes
- **Lifecycle Management:** Framework manages object lifecycles
- **Refactor Speed:** 20-30% faster refactoring per release cycle

### Popular DI Frameworks

| Language | Frameworks |
|----------|------------|
| **Python** | dependency-injector, injector, FastAPI DI |
| **TypeScript** | InversifyJS, TSyringe, NestJS DI |
| **Go** | Wire (compile-time), Uber Dig/Fx (runtime), do |
| **Java** | Spring, Guice, Dagger |
| **C#** | .NET Core DI, Autofac, Ninject |

---

## Object Pool

**Intent:** Manage a pool of reusable objects to avoid expensive allocation/deallocation.

### When to Use

- Object creation is expensive (database connections, threads, network sockets)
- Objects needed frequently but used briefly
- Limited number of a resource type available
- Need to control resource usage

### Key Design Decisions

| Aspect | Options |
|--------|---------|
| **Size** | Fixed, Dynamic (min/max), Unlimited |
| **Acquisition** | Blocking, Non-blocking, Timeout |
| **Idle Policy** | Keep all, Shrink over time, Evict oldest |
| **Validation** | On borrow, On return, Background check |

### Best Practices

1. **Reset State:** Pool MUST reset objects before reuse (never trust consumers)
2. **Timeouts:** Prevent clients from waiting forever
3. **Health Checks:** Validate objects before returning to clients
4. **Thread Safety:** Use proper synchronization (consider per-CPU pools for high concurrency)
5. **Metrics:** Track pool utilization, wait times, object creation rate

### Common Implementations

- **Go:** `sync.Pool` (GC-aware), custom implementations
- **Python:** Database connection pools (SQLAlchemy, psycopg2)
- **TypeScript/Node:** generic-pool, database drivers
- **Java:** Apache Commons Pool, HikariCP

---

## Pattern Relationships

```
Factory Method ──evolves to──→ Abstract Factory
                              ↓
                          Builder (for complex products)
                              ↓
                          Prototype (for cloning)

Singleton ──replaced by──→ Dependency Injection
                              ↓
Object Pool ──uses──→ Factory Method (to create objects)
                              ↓
                          Singleton (pool itself often singleton)
```

## LLM Usage Tips

When using LLMs for creational pattern design:

1. **Provide Context:** Include domain, language, existing architecture
2. **Specify Constraints:** Testing requirements, performance needs, team size
3. **Ask for Trade-offs:** Request pros/cons for each approach
4. **Request Examples:** Ask for language-specific implementations
5. **Iterate:** Refine based on specific use case requirements

### Example Prompt Structure

```
I need to implement [PATTERN] for [USE CASE].

Context:
- Language: [Python/TypeScript/Go]
- Framework: [Django/FastAPI/NestJS/etc.]
- Existing patterns: [what's already used]
- Constraints: [testing, performance, team expertise]

Please provide:
1. Implementation with type hints
2. Usage example
3. Test example
4. Trade-offs vs alternatives
```

## External Resources

### Official Documentation

- [Refactoring.guru - Creational Patterns](https://refactoring.guru/design-patterns/creational-patterns)
- [SourceMaking - Creational Patterns](https://sourcemaking.com/design_patterns/creational_patterns)

### Language-Specific

- [Python Design Patterns](https://python-patterns.guide/)
- [TypeScript Design Patterns](https://refactoring.guru/design-patterns/typescript)
- [Go Design Patterns](https://refactoring.guru/design-patterns/go)

### Books

- "Design Patterns: Elements of Reusable Object-Oriented Software" (GoF, 1994)
- "Head First Design Patterns" (Freeman & Robson)
- "Patterns of Enterprise Application Architecture" (Fowler)

### Modern Perspectives

- [Design Patterns Revisited: Are Singleton and Factory Still Relevant?](https://www.javacodegeeks.com/2025/09/design-patterns-revisited-are-singleton-and-factory-still-relevant.html)
- [The Singleton Pattern Is a Refactoring Nightmare](https://thenewstack.io/unmasking-the-singleton-anti-pattern/)
- [Dependency Injection in Go: Patterns & Best Practices](https://www.glukhov.org/post/2025/12/dependency-injection-in-go/)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related

- [checklist.md](checklist.md) - Step-by-step pattern selection
- [examples.md](examples.md) - Real implementations
- [templates.md](templates.md) - Copy-paste templates
- [llm-prompts.md](llm-prompts.md) - Effective prompts for LLM assistance
