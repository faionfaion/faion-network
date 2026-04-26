# Behavioral Patterns Checklist

Step-by-step guidance for selecting and implementing behavioral design patterns.

## Phase 1: Problem Analysis

### 1.1 Identify the Core Problem

- [ ] What objects need to communicate?
- [ ] Is communication one-to-one, one-to-many, or many-to-many?
- [ ] Does behavior need to change at runtime?
- [ ] Is there a sequence of operations to manage?
- [ ] Do you need undo/redo capabilities?
- [ ] Are there multiple algorithms for the same task?

### 1.2 Document Requirements

- [ ] List all actors (objects) involved
- [ ] Map communication flows between actors
- [ ] Identify state changes and transitions
- [ ] Note any ordering constraints
- [ ] Document extensibility requirements

## Phase 2: Pattern Selection

### 2.1 Strategy Pattern Checklist

**Select if:**
- [ ] Multiple interchangeable algorithms exist
- [ ] Algorithm selection happens at runtime
- [ ] Need to eliminate complex conditionals (switch/if-else)
- [ ] Algorithms should be independently testable

**Pre-implementation:**
- [ ] Define strategy interface with single responsibility
- [ ] List all concrete strategies needed
- [ ] Determine how strategies will be injected (constructor, setter, factory)
- [ ] Plan for strategy validation

**Implementation:**
- [ ] Create abstract strategy interface/protocol
- [ ] Implement each concrete strategy
- [ ] Create context class that uses strategies
- [ ] Add strategy switching mechanism
- [ ] Write unit tests for each strategy

### 2.2 Observer Pattern Checklist

**Select if:**
- [ ] One object's state affects multiple others
- [ ] Number of dependent objects is dynamic
- [ ] Dependencies shouldn't be hardcoded
- [ ] Implementing event-driven behavior

**Pre-implementation:**
- [ ] Define subject interface (attach, detach, notify)
- [ ] Define observer interface (update method)
- [ ] Plan for observer lifecycle management
- [ ] Consider weak references to prevent memory leaks
- [ ] Decide on push vs. pull notification model

**Implementation:**
- [ ] Create subject base class/interface
- [ ] Create observer interface
- [ ] Implement concrete subject with observer list
- [ ] Implement concrete observers
- [ ] Add thread safety if needed
- [ ] Implement cleanup/unsubscribe mechanism
- [ ] Test with multiple observers

### 2.3 Command Pattern Checklist

**Select if:**
- [ ] Need to parameterize objects with operations
- [ ] Need to queue, log, or schedule operations
- [ ] Require undo/redo functionality
- [ ] Want to decouple invoker from executor

**Pre-implementation:**
- [ ] Define command interface (execute, undo)
- [ ] List all commands needed
- [ ] Design command history structure
- [ ] Plan for command composition (macros)
- [ ] Consider command serialization needs

**Implementation:**
- [ ] Create command interface
- [ ] Implement concrete commands with execute/undo
- [ ] Create invoker (command processor)
- [ ] Implement command history stack
- [ ] Add redo capability if needed
- [ ] Create composite command for macros
- [ ] Test undo/redo sequences

### 2.4 State Pattern Checklist

**Select if:**
- [ ] Object behavior depends on its state
- [ ] Many conditionals based on state exist
- [ ] State transitions follow defined rules
- [ ] States are well-defined and finite

**Pre-implementation:**
- [ ] Create state transition diagram
- [ ] List all states and their behaviors
- [ ] Define all valid transitions
- [ ] Identify entry/exit actions for states
- [ ] Plan for invalid transition handling

**Implementation:**
- [ ] Create state interface with all behaviors
- [ ] Implement concrete state classes
- [ ] Create context class holding current state
- [ ] Implement state transition logic
- [ ] Add transition validation
- [ ] Handle invalid transitions gracefully
- [ ] Test all transitions and edge cases

### 2.5 Chain of Responsibility Checklist

**Select if:**
- [ ] Multiple handlers may process a request
- [ ] Handler set should be configurable
- [ ] Processing order matters
- [ ] Need middleware-like pipeline

**Pre-implementation:**
- [ ] List all handlers needed
- [ ] Define handler interface
- [ ] Determine chain ordering
- [ ] Decide if request must be handled or can fall through
- [ ] Plan for handler addition/removal

**Implementation:**
- [ ] Create handler interface with next handler reference
- [ ] Implement setNext method
- [ ] Implement concrete handlers
- [ ] Create chain builder/factory
- [ ] Add chain validation
- [ ] Test various request scenarios
- [ ] Test handler ordering

### 2.6 Template Method Checklist

**Select if:**
- [ ] Algorithm has fixed structure
- [ ] Steps vary but overall flow doesn't
- [ ] Want to enforce algorithm skeleton
- [ ] Need hooks for customization

**Pre-implementation:**
- [ ] Identify invariant algorithm steps
- [ ] Identify steps that vary
- [ ] Define hook points
- [ ] Plan for optional vs. required steps

**Implementation:**
- [ ] Create abstract class with template method
- [ ] Make template method final (prevent override)
- [ ] Define abstract methods for variable steps
- [ ] Add hook methods with default implementations
- [ ] Implement concrete subclasses
- [ ] Test algorithm flow in each subclass

### 2.7 Mediator Pattern Checklist

**Select if:**
- [ ] Many objects communicate in complex ways
- [ ] Want to reduce coupling between components
- [ ] Communication logic should be centralized
- [ ] Components should be reusable independently

**Pre-implementation:**
- [ ] List all colleague objects
- [ ] Map all communication paths
- [ ] Define mediator interface
- [ ] Plan for colleague registration

**Implementation:**
- [ ] Create mediator interface
- [ ] Create colleague base class with mediator reference
- [ ] Implement concrete mediator
- [ ] Implement concrete colleagues
- [ ] Route all inter-colleague communication through mediator
- [ ] Test communication scenarios

### 2.8 Iterator Pattern Checklist

**Select if:**
- [ ] Need to traverse collection without exposing internals
- [ ] Multiple traversal algorithms needed
- [ ] Want uniform traversal interface
- [ ] Collection implementation may change

**Pre-implementation:**
- [ ] Define iterator interface (next, hasNext)
- [ ] Plan for concurrent modification handling
- [ ] Consider bidirectional iteration needs
- [ ] Plan for external vs. internal iteration

**Implementation:**
- [ ] Create iterator interface
- [ ] Implement concrete iterator
- [ ] Add iterable interface to collection
- [ ] Handle end-of-collection
- [ ] Add reverse iterator if needed
- [ ] Test iteration over various collections

### 2.9 Visitor Pattern Checklist

**Select if:**
- [ ] Need to add operations to class hierarchy
- [ ] Don't want to modify existing classes
- [ ] Operations vary more than element types
- [ ] Processing heterogeneous collections

**Pre-implementation:**
- [ ] List all element types
- [ ] List all operations needed
- [ ] Plan for adding new element types (breaks visitor)
- [ ] Design visitor interface with visit method per type

**Implementation:**
- [ ] Create element interface with accept method
- [ ] Create visitor interface with visit methods
- [ ] Implement accept in each element (double dispatch)
- [ ] Implement concrete visitors
- [ ] Test visitors on element collections

## Phase 3: Implementation Quality

### 3.1 Code Quality Checks

- [ ] Single Responsibility: Each class has one reason to change
- [ ] Open/Closed: Extensible without modification
- [ ] Interface Segregation: Interfaces are focused
- [ ] Dependency Inversion: Depend on abstractions
- [ ] DRY: No duplicated logic

### 3.2 Testing Checklist

- [ ] Unit tests for each pattern component
- [ ] Integration tests for component interaction
- [ ] Edge case tests (empty, null, boundary)
- [ ] Performance tests if needed
- [ ] Thread safety tests if concurrent

### 3.3 Documentation Checklist

- [ ] Pattern choice documented (ADR if significant)
- [ ] Class diagram created
- [ ] Usage examples provided
- [ ] Extension points documented
- [ ] Known limitations noted

## Phase 4: Language-Specific Considerations

### Python

- [ ] Use `Protocol` for duck typing (vs ABC)
- [ ] Consider `dataclasses` for immutable objects
- [ ] Use `@abstractmethod` appropriately
- [ ] Leverage `__iter__` for iterators
- [ ] Use type hints throughout

### TypeScript

- [ ] Define proper interfaces
- [ ] Use discriminated unions for state
- [ ] Leverage generics for type safety
- [ ] Consider functional alternatives
- [ ] Use readonly where appropriate

### Go

- [ ] Use interfaces (implicit implementation)
- [ ] Consider channels for observer-like patterns
- [ ] Use function types for strategies
- [ ] Leverage goroutines for async patterns
- [ ] Use context for chain of responsibility

## Phase 5: Review Checklist

### 5.1 Design Review

- [ ] Pattern is appropriate for the problem
- [ ] Not over-engineered
- [ ] Follows language idioms
- [ ] Extensibility considered
- [ ] Error handling is robust

### 5.2 Performance Review

- [ ] No unnecessary object creation
- [ ] Memory management considered
- [ ] No memory leaks (esp. observers)
- [ ] Appropriate data structures used

### 5.3 Maintainability Review

- [ ] Code is readable
- [ ] Naming is clear and consistent
- [ ] Comments explain "why" not "what"
- [ ] Easy to add new variants
