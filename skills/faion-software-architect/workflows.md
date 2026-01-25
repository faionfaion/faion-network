# Architecture Workflows

## System Design Workflow

```
1. CLARIFY Requirements
   - Functional requirements (what it does)
   - Non-functional requirements (quality attributes)
   - Constraints (budget, team, timeline)
   ↓
2. ESTIMATE Scale
   - Users (DAU, MAU, peak)
   - Data (storage, growth rate)
   - Traffic (RPS, bandwidth)
   ↓
3. DESIGN High-Level
   - C4 Context and Container diagrams
   - Major components and data flow
   - API contracts (REST/GraphQL/gRPC)
   ↓
4. DEEP DIVE Components
   - Database schema
   - Caching strategy
   - Message queues
   ↓
5. ADDRESS Quality Attributes
   - Scalability: horizontal/vertical
   - Reliability: redundancy, failover
   - Security: auth, encryption, rate limiting
   ↓
6. DOCUMENT Decisions
   - ADRs for key choices
   - Diagrams in repo
```

## Technology Selection Workflow

```
1. DEFINE Criteria
   - Must-haves (non-negotiable)
   - Nice-to-haves (preferred)
   - Constraints (team skills, cost)
   ↓
2. RESEARCH Options
   - Industry standards
   - Team familiarity
   - Community/support
   ↓
3. EVALUATE
   - Proof of concept if needed
   - Score against criteria
   ↓
4. DECIDE
   - Document in ADR
   - Get stakeholder buy-in
```

## ADR Creation Workflow

```
1. IDENTIFY Decision
   - What needs to be decided?
   - Why now?
   ↓
2. GATHER Context
   - Current situation
   - Problem to solve
   - Constraints
   ↓
3. RESEARCH Alternatives
   - 2-4 viable options
   - Pros/cons for each
   ↓
4. EVALUATE
   - Score against criteria
   - Consider trade-offs
   ↓
5. DECIDE
   - Select best option
   - Document rationale
   ↓
6. REVIEW
   - Stakeholder feedback
   - Finalize ADR
```

## Architecture Review Workflow

```
1. PREPARE
   - Gather diagrams
   - Review ADRs
   - List quality attributes
   ↓
2. ANALYZE
   - Check against quality attributes
   - Identify risks
   - Review patterns used
   ↓
3. EVALUATE
   - Scalability analysis
   - Security assessment
   - Performance review
   ↓
4. REPORT
   - Findings
   - Recommendations
   - Action items
```

## C4 Model Creation Workflow

```
1. CONTEXT DIAGRAM (C1)
   - System in scope
   - External systems
   - Users/actors
   ↓
2. CONTAINER DIAGRAM (C2)
   - Applications
   - Databases
   - Services
   - Communication protocols
   ↓
3. COMPONENT DIAGRAM (C3)
   - Internal components
   - Responsibilities
   - Dependencies
   ↓
4. CODE DIAGRAM (C4) [Optional]
   - Key classes
   - Interfaces
   - Relationships
```

## Database Design Workflow

```
1. IDENTIFY Entities
   - Core business objects
   - Relationships
   ↓
2. DESIGN Schema
   - Tables/collections
   - Fields/attributes
   - Indexes
   ↓
3. NORMALIZE (SQL)
   - 1NF, 2NF, 3NF
   - De-normalize for performance if needed
   ↓
4. DEFINE Constraints
   - Primary keys
   - Foreign keys
   - Unique constraints
   ↓
5. PLAN Migrations
   - Version control
   - Rollback strategy
```

## API Design Workflow

```
1. DEFINE Resources
   - Entities to expose
   - Operations (CRUD)
   ↓
2. CHOOSE Style
   - REST (resource-based)
   - GraphQL (flexible queries)
   - gRPC (high performance)
   ↓
3. DESIGN Endpoints
   - URL structure (REST)
   - Schemas (GraphQL)
   - Proto files (gRPC)
   ↓
4. SPECIFY Contracts
   - Request/response formats
   - Error handling
   - Authentication
   ↓
5. VERSION
   - Versioning strategy
   - Backward compatibility
   ↓
6. DOCUMENT
   - OpenAPI/Swagger (REST)
   - Schema introspection (GraphQL)
```

## Microservices Decomposition Workflow

```
1. IDENTIFY Bounded Contexts
   - Domain-driven design
   - Business capabilities
   ↓
2. DEFINE Service Boundaries
   - Single responsibility
   - Loose coupling
   ↓
3. DESIGN APIs
   - Synchronous (REST, gRPC)
   - Asynchronous (events)
   ↓
4. PLAN Data Management
   - Database per service
   - Data consistency strategy
   ↓
5. ADDRESS Cross-Cutting
   - Authentication
   - Logging
   - Monitoring
```

## Migration Strategy Workflow

```
1. ASSESS Current State
   - Architecture analysis
   - Technical debt
   - Pain points
   ↓
2. DEFINE Target State
   - Desired architecture
   - Quality attributes
   ↓
3. PLAN Migration
   - Phased approach
   - Strangler fig pattern
   - Feature flags
   ↓
4. EXECUTE Incrementally
   - Small, safe changes
   - Rollback plan
   ↓
5. VALIDATE
   - Testing at each step
   - Monitor metrics
```

---

*Part of faion-software-architect skill*
