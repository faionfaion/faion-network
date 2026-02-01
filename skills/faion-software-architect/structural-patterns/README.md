# Structural Design Patterns

Patterns for composing objects and classes into larger, flexible structures while maintaining loose coupling and maximizing reuse.

## Overview

Structural patterns focus on **how classes and objects are composed** to form larger structures. They use inheritance and composition to create new functionality from existing components.

| Pattern | Purpose | Key Use Case |
|---------|---------|--------------|
| **Adapter** | Convert interface to another | Legacy/third-party integration |
| **Bridge** | Separate abstraction from implementation | Cross-platform, multi-dimensional variation |
| **Composite** | Tree structures with uniform interface | File systems, UI hierarchies, org charts |
| **Decorator** | Add behavior dynamically | Middleware, logging, caching layers |
| **Facade** | Simplified interface to complex subsystem | Library wrappers, API gateways |
| **Proxy** | Placeholder controlling access | Lazy loading, access control, caching |
| **Flyweight** | Share common state for memory efficiency | Large object pools, game entities |

## Pattern Selection Matrix

| Scenario | Primary Pattern | Alternative |
|----------|-----------------|-------------|
| "Integrate legacy/third-party API" | Adapter | Facade (if simplifying) |
| "Add features without subclassing" | Decorator | Proxy (if controlling access) |
| "Hide complex subsystem" | Facade | Adapter (if single interface) |
| "Tree/hierarchical structures" | Composite | - |
| "Lazy loading, access control" | Proxy | Decorator (if adding behavior) |
| "Multiple dimensions of variation" | Bridge | Adapter (if post-design) |
| "Many similar objects, memory constrained" | Flyweight | Object Pool |

## Wrapping Patterns Comparison

Four patterns involve "wrapping" but serve different purposes:

| Pattern | Timing | What It Does | Example |
|---------|--------|--------------|---------|
| **Adapter** | After design | Converts interface A to interface B | Payment gateway wrapper |
| **Proxy** | Any time | Controls access to object | Lazy image loader |
| **Decorator** | Any time | Adds responsibilities dynamically | Logging middleware |
| **Bridge** | Before design | Separates abstraction from implementation | Cross-platform rendering |

### Quick Decision

```
Need to convert interfaces? → Adapter
Need to control access? → Proxy
Need to add behavior? → Decorator
Need independent hierarchies? → Bridge
```

## Pattern Deep Dives

### 1. Adapter Pattern

**Intent:** Convert the interface of a class into another interface clients expect. Lets classes work together that couldn't otherwise because of incompatible interfaces.

**When to Use:**
- Integrating legacy systems with new code
- Using third-party libraries with incompatible APIs
- Reusing existing class with a different interface
- Creating a unified interface for multiple similar classes

**Key Participants:**
- **Target**: The interface the client expects
- **Adaptee**: The existing class with incompatible interface
- **Adapter**: Converts Adaptee interface to Target interface

**Modern Context (2025):**
- Zero-copy adaptation for performance-critical systems
- Protocol translation between industrial protocols (PROFINET, CAN, Modbus)
- API version adapters for backward compatibility
- Safety boundary demarcation in safety-critical systems

---

### 2. Bridge Pattern

**Intent:** Decouple an abstraction from its implementation so that the two can vary independently.

**When to Use:**
- Designed **up-front** (before implementation)
- Avoiding "class explosion" from multiple dimensions of variation
- Needing runtime implementation switching
- Supporting multiple platforms/backends

**Key Participants:**
- **Abstraction**: High-level interface
- **Implementor**: Low-level implementation interface
- **RefinedAbstraction**: Extended abstraction
- **ConcreteImplementor**: Platform-specific implementation

**Bridge vs Adapter:**

| Aspect | Adapter | Bridge |
|--------|---------|--------|
| **Timing** | Retrofit (after design) | Up-front (before design) |
| **Purpose** | Make incompatible interfaces work | Enable independent variation |
| **Focus** | Interface conversion | Abstraction/implementation separation |

---

### 3. Composite Pattern

**Intent:** Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

**When to Use:**
- Representing hierarchical structures (trees)
- Treating individual and composite objects uniformly
- Building recursive data structures

**Key Participants:**
- **Component**: Common interface for leaves and composites
- **Leaf**: Primitive object with no children
- **Composite**: Contains children, delegates to them

**Common Applications:**
- File systems (files and directories)
- UI component trees (widgets, containers)
- Organization charts
- Document structures (paragraphs, sections, documents)
- Graphics scenes (shapes, groups)

---

### 4. Decorator Pattern

**Intent:** Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality.

**When to Use:**
- Adding responsibilities to objects dynamically
- When extension by subclassing is impractical
- Combining multiple behaviors at runtime
- Middleware and filter chains

**Key Participants:**
- **Component**: Interface for objects that can have responsibilities added
- **ConcreteComponent**: Object being decorated
- **Decorator**: Maintains reference to component, conforms to Component interface
- **ConcreteDecorator**: Adds responsibilities

**Decorator Composition:**
- Multiple decorators can be stacked/chained
- Evaluation order: expressions top-to-bottom, calls bottom-to-top
- Each decorator handles single responsibility (SRP)

**Python vs TypeScript Decorators:**
- Python: Higher-order functions with `@` syntax sugar
- TypeScript: Stage 3 proposal, class/method metadata
- Both differ from the GoF Decorator pattern (which is class-based)

---

### 5. Facade Pattern

**Intent:** Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

**When to Use:**
- Simplifying complex subsystem access
- Layering subsystems
- Reducing coupling between clients and subsystems
- Creating entry points for libraries

**Key Participants:**
- **Facade**: Unified interface to subsystem
- **Subsystem classes**: Complex components hidden behind facade

**API Gateway as Modern Facade:**
- Routes requests to microservices
- Handles authentication, rate limiting
- Transforms/aggregates responses
- Provides versioned APIs

---

### 6. Proxy Pattern

**Intent:** Provide a surrogate or placeholder for another object to control access to it.

**Proxy Types:**

| Type | Purpose | Example |
|------|---------|---------|
| **Virtual Proxy** | Lazy initialization | Load image only when displayed |
| **Protection Proxy** | Access control | Check permissions before operation |
| **Remote Proxy** | Network access | RPC client stub |
| **Cache Proxy** | Result caching | Cache expensive query results |
| **Logging Proxy** | Audit/monitoring | Log all method calls |

**When to Use:**
- Lazy loading of expensive objects
- Access control based on permissions
- Caching expensive operation results
- Logging/auditing access
- Remote object representation

**Virtual Proxy vs Smart Reference:**
- Virtual Proxy: Main purpose is lazy loading
- Smart Reference: May lazy load but also tracks usage, reference counting

---

### 7. Flyweight Pattern

**Intent:** Use sharing to support large numbers of fine-grained objects efficiently.

**Key Concepts:**
- **Intrinsic State**: Shared, immutable data stored in flyweight
- **Extrinsic State**: Context-specific data passed by client

**When to Use:**
- Application uses many similar objects
- Storage costs are high due to object quantity
- Most object state can be made extrinsic
- Objects can be replaced by few shared instances

**Common Applications:**
- Character objects in text editors
- Particle systems in games
- Database connection pools
- String interning
- Icon/image caching

**Memory Optimization (2025):**
- Python: Automatically applies to small integers and some strings
- JavaScript/TypeScript: Particularly useful in large-scale frontend apps
- Go: Combined with sync.Pool for object reuse

**Concurrency Considerations:**
- Make flyweights immutable for thread safety
- Pre-instantiate for known finite values
- Choose between: single-threaded creation vs multiple instances

---

## Design Principles Applied

| Principle | Patterns That Apply It |
|-----------|------------------------|
| **Open/Closed** | Decorator, Composite, Proxy |
| **Single Responsibility** | All (each pattern has focused purpose) |
| **Composition over Inheritance** | Decorator, Bridge, Composite |
| **Program to Interface** | Adapter, Bridge, Proxy |
| **Dependency Inversion** | All (depend on abstractions) |

## Performance Considerations

| Pattern | Performance Impact |
|---------|-------------------|
| **Adapter** | Minimal (thin wrapper) |
| **Bridge** | Minimal (indirection cost) |
| **Composite** | O(n) tree traversal |
| **Decorator** | Stack depth for nested decorators |
| **Facade** | Minimal (delegation) |
| **Proxy** | Depends on proxy type (caching can improve) |
| **Flyweight** | Trades RAM for CPU (extrinsic state computation) |

## LLM-Assisted Pattern Design

### When to Invoke LLM for Structural Patterns

1. **Pattern Selection**: "Which structural pattern fits my scenario?"
2. **Implementation Review**: "Review my Decorator chain for issues"
3. **Refactoring to Patterns**: "Refactor this code to use Adapter"
4. **Pattern Combination**: "How to combine Facade with Proxy?"
5. **Language-Specific Idioms**: "Pythonic way to implement Flyweight"

### Effective LLM Usage Tips

1. **Provide Context**: Include current code structure and interfaces
2. **Specify Language**: Patterns differ by language idioms
3. **State Constraints**: Memory limits, performance requirements
4. **Ask for Trade-offs**: "What are the trade-offs of using Proxy here?"
5. **Request Tests**: "Include unit tests for the Decorator"

### Pattern-Specific LLM Prompts

See [llm-prompts.md](llm-prompts.md) for comprehensive prompts for each pattern.

## Files in This Folder

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Step-by-step pattern selection and implementation checklist |
| [examples.md](examples.md) | Real implementations in Python, TypeScript, Go |
| [templates.md](templates.md) | Copy-paste pattern templates for quick start |
| [llm-prompts.md](llm-prompts.md) | Effective prompts for LLM-assisted pattern design |

## External Resources

### Official Documentation

- [Refactoring.guru - Structural Patterns](https://refactoring.guru/design-patterns/structural-patterns)
- [SourceMaking - Structural Patterns](https://sourcemaking.com/design_patterns/structural_patterns)
- [TypeScript Handbook - Decorators](https://www.typescriptlang.org/docs/handbook/decorators.html)

### Language-Specific Guides

- [Refactoring.guru - Python Patterns](https://refactoring.guru/design-patterns/python)
- [Refactoring.guru - TypeScript Patterns](https://refactoring.guru/design-patterns/typescript)
- [Refactoring.guru - Go Patterns](https://refactoring.guru/design-patterns/go)

### Articles and Tutorials

- [GeeksforGeeks - Structural Design Patterns](https://www.geeksforgeeks.org/system-design/structural-design-patterns/)
- [DigitalOcean - Gang of Four Design Patterns](https://www.digitalocean.com/community/tutorials/gangs-of-four-gof-design-patterns)
- [Baeldung - Proxy, Decorator, Adapter and Bridge](https://www.baeldung.com/java-structural-design-patterns)

### Modern Implementations (2025-2026)

- [Medium - Flyweight Pattern in Modern JavaScript](https://medium.com/@artemkhrenov/the-flyweight-pattern-in-modern-javascript-memory-optimization-for-large-scale-applications-fb651a5511a3)
- [LogRocket - TypeScript Decorators Guide](https://blog.logrocket.com/practical-guide-typescript-decorators/)
- [Technology & Strategy - Design Patterns 2025](https://www.technologyandstrategy.com/news/design-patterns-the-complete-guide-2025)


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Implementation setup | haiku | Applying standard methodology patterns |
| Design decisions | sonnet | Trade-offs analysis |
| Complex scenarios | opus | Novel or complex solutions |
## Related Patterns

| Pattern Category | Link |
|------------------|------|
| Creational Patterns | [creational-patterns/](../creational-patterns/) |
| Behavioral Patterns | [behavioral-patterns/](../behavioral-patterns/) |
| Architectural Patterns | [architectural-patterns/](../architectural-patterns/) |
