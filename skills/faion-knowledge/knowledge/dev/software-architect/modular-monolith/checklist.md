# Modular Monolith Checklist

Step-by-step guide for building and migrating to modular monolith architecture.

## Phase 1: Domain Analysis

### 1.1 Identify Bounded Contexts

- [ ] List all business capabilities
- [ ] Group related capabilities into domains
- [ ] Identify domain experts for each area
- [ ] Map existing code to potential modules
- [ ] Document domain vocabulary (ubiquitous language)

### 1.2 Define Module Boundaries

- [ ] Each module represents ONE bounded context
- [ ] Module name reflects business domain (not technical layer)
- [ ] No overlapping responsibilities between modules
- [ ] Clear ownership for each piece of data
- [ ] Document module responsibilities

### 1.3 Map Dependencies

- [ ] Draw module dependency diagram
- [ ] Identify circular dependencies (must eliminate)
- [ ] Mark which modules are "upstream" vs "downstream"
- [ ] Identify shared kernel (truly common code)
- [ ] Plan dependency direction (acyclic graph)

## Phase 2: Project Structure

### 2.1 Directory Organization

- [ ] Create top-level directory per module
- [ ] Each module has standard internal structure
- [ ] Shared/common code in dedicated package
- [ ] Clear separation of public API vs internal code
- [ ] Tests co-located with modules or in parallel structure

**Standard module structure:**
```
module_name/
├── __init__.py          # Public API exports
├── api.py               # Public interface (functions, DTOs)
├── models.py            # Domain models (internal)
├── services.py          # Business logic (internal)
├── repository.py        # Data access (internal)
├── events.py            # Domain events (if using)
└── tests/               # Module tests
```

### 2.2 Package Visibility

- [ ] Mark internal packages/modules as private
- [ ] Export only public API from `__init__.py`
- [ ] Use language-specific visibility (internal in Go, package-private in Java)
- [ ] Document what is public vs internal

### 2.3 Shared Code

- [ ] Create `shared/` or `common/` package
- [ ] Include only truly cross-cutting concerns:
  - [ ] Base exceptions
  - [ ] Utility functions
  - [ ] Common interfaces
  - [ ] Infrastructure abstractions
- [ ] Avoid business logic in shared code
- [ ] Keep shared package minimal

## Phase 3: Module APIs

### 3.1 Define Public Interfaces

- [ ] Each module exposes a service interface
- [ ] Use DTOs for data transfer (not domain models)
- [ ] Define clear method signatures
- [ ] Document expected behavior
- [ ] Version APIs if needed

### 3.2 Data Transfer Objects

- [ ] Create DTOs for each public operation
- [ ] DTOs are immutable (frozen dataclasses, records)
- [ ] No business logic in DTOs
- [ ] Map between domain models and DTOs internally
- [ ] Use typed DTOs (not dicts/maps)

### 3.3 Error Handling

- [ ] Define module-specific exceptions
- [ ] Translate internal errors to public exceptions
- [ ] Don't leak internal state in errors
- [ ] Document error conditions

## Phase 4: Data Isolation

### 4.1 Database Schema Separation

- [ ] Create schema/database per module
- [ ] Each module owns its tables exclusively
- [ ] No foreign keys across module boundaries
- [ ] Use IDs for cross-module references
- [ ] Document schema ownership

### 4.2 Data Access Rules

- [ ] Modules only access own schema
- [ ] No cross-schema JOINs
- [ ] Query other modules via API
- [ ] Denormalize data when needed for performance
- [ ] Document data dependencies

### 4.3 Migrations

- [ ] Module owns its migrations
- [ ] Migrations run per-module or with clear ordering
- [ ] No migration dependencies across modules
- [ ] Test migrations independently

## Phase 5: Communication

### 5.1 Synchronous Communication

- [ ] Define service interfaces
- [ ] Inject dependencies (not hardcoded imports)
- [ ] Handle timeouts/errors gracefully
- [ ] Log cross-module calls for debugging
- [ ] Consider circuit breakers for critical paths

### 5.2 Asynchronous Communication (Events)

- [ ] Define event contracts (schemas)
- [ ] Use in-memory event bus initially
- [ ] Events are immutable facts
- [ ] Include event version for evolution
- [ ] Handle duplicate events (idempotency)

### 5.3 Event Design

- [ ] Event names describe what happened (past tense)
- [ ] Include all necessary data in event payload
- [ ] Don't include internal implementation details
- [ ] Document event consumers
- [ ] Plan for event schema evolution

## Phase 6: Boundary Enforcement

### 6.1 Static Analysis

- [ ] Configure import linter (Python: import-linter)
- [ ] Configure architecture tests (Java: ArchUnit)
- [ ] Run checks in CI pipeline
- [ ] Block PRs that violate boundaries
- [ ] Document allowed dependencies

### 6.2 Architecture Tests

- [ ] Test module independence
- [ ] Test layer dependencies (if using layered arch)
- [ ] Test no circular dependencies
- [ ] Test internal packages are not accessed
- [ ] Test public API surface

### 6.3 Code Review Guidelines

- [ ] Review cross-module changes carefully
- [ ] Check for boundary violations
- [ ] Verify DTOs are used (not domain models)
- [ ] Ensure events are well-designed
- [ ] Validate new dependencies

## Phase 7: Testing Strategy

### 7.1 Unit Tests

- [ ] Test business logic in isolation
- [ ] Mock cross-module dependencies
- [ ] Focus on domain model behavior
- [ ] High coverage for complex logic

### 7.2 Integration Tests

- [ ] Test module API contracts
- [ ] Test database interactions
- [ ] Test event publishing/handling
- [ ] Use test database per module

### 7.3 End-to-End Tests

- [ ] Test critical user journeys
- [ ] Test cross-module workflows
- [ ] Keep E2E tests minimal
- [ ] Run in CI before deploy

### 7.4 Contract Tests

- [ ] Define API contracts
- [ ] Test producer fulfills contract
- [ ] Test consumer expects correct contract
- [ ] Version contracts appropriately

## Phase 8: Deployment & Operations

### 8.1 Single Deployment

- [ ] Single deployable artifact
- [ ] All modules deploy together
- [ ] Feature flags for gradual rollout
- [ ] Blue-green or canary deployment

### 8.2 Observability

- [ ] Structured logging with module context
- [ ] Metrics per module (latency, errors)
- [ ] Tracing across module calls
- [ ] Dashboards for module health

### 8.3 Configuration

- [ ] Module-specific configuration sections
- [ ] Environment-based configuration
- [ ] Secrets management
- [ ] Feature flags per module

## Phase 9: Migration from Monolith

### 9.1 Preparation

- [ ] Identify highest-value module to extract first
- [ ] Map current dependencies
- [ ] Document current architecture
- [ ] Get team buy-in

### 9.2 Incremental Extraction

- [ ] Extract one module at a time
- [ ] Create module boundary first
- [ ] Move code into module structure
- [ ] Add public API
- [ ] Update callers to use API
- [ ] Separate database schema
- [ ] Add boundary enforcement
- [ ] Repeat for next module

### 9.3 Validation

- [ ] No regression in functionality
- [ ] Performance acceptable
- [ ] Tests passing
- [ ] Boundary tests passing
- [ ] Team understands new structure

## Phase 10: Migration to Microservices

### 10.1 Pre-Extraction Checklist

- [ ] Module has clear API boundary
- [ ] Module owns its database schema
- [ ] Communication is via events (preferred) or API
- [ ] No shared state with other modules
- [ ] Module is independently testable

### 10.2 Strangler Fig Extraction

- [ ] Create new service repository
- [ ] Copy module code to service
- [ ] Set up independent deployment
- [ ] Create API gateway/facade
- [ ] Route traffic to new service
- [ ] Replace in-process calls with HTTP/gRPC
- [ ] Replace in-memory events with message queue
- [ ] Extract database schema
- [ ] Decommission module in monolith

### 10.3 Post-Extraction Validation

- [ ] Latency acceptable with network calls
- [ ] Error handling for network failures
- [ ] Circuit breakers in place
- [ ] Monitoring for new service
- [ ] Rollback plan ready

## Quality Gates

### Before Module Extraction

| Check | Status |
|-------|--------|
| Domain boundaries clear | [ ] |
| No circular dependencies | [ ] |
| Database schema identified | [ ] |
| API designed | [ ] |
| Tests exist | [ ] |

### Before Microservice Extraction

| Check | Status |
|-------|--------|
| Module fully isolated | [ ] |
| Event-based communication | [ ] |
| Independent database | [ ] |
| Boundary tests pass | [ ] |
| Performance benchmarks | [ ] |
| Ops team ready | [ ] |

## Common Pitfalls

### Avoid These Mistakes

- [ ] Extracting services before modularizing
- [ ] Cross-module database joins
- [ ] Sharing domain models between modules
- [ ] Circular dependencies between modules
- [ ] Too many small modules (over-modularization)
- [ ] Too few modules (under-modularization)
- [ ] Ignoring data ownership
- [ ] Distributed monolith (network calls without boundaries)

### Warning Signs

| Sign | Action |
|------|--------|
| Module imports internal from another | Fix boundary violation |
| Cross-schema JOIN in SQL | Refactor to use API |
| Shared mutable state | Extract to owner module |
| Circular dependency | Break cycle, introduce events |
| Module > 50 files | Consider splitting |
| Module < 5 files | Consider merging |
