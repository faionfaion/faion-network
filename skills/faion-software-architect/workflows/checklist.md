# Architecture Workflow Checklists

Step-by-step checklists for executing architecture workflows systematically.

## Table of Contents

1. [System Design Workflow](#1-system-design-workflow)
2. [Architecture Review Workflow](#2-architecture-review-workflow)
3. [ADR Creation Workflow](#3-adr-creation-workflow)
4. [Technology Evaluation Workflow](#4-technology-evaluation-workflow)
5. [Architecture Assessment (ATAM)](#5-architecture-assessment-atam)
6. [Migration Planning Workflow](#6-migration-planning-workflow)
7. [Design Document Review](#7-design-document-review)

---

## 1. System Design Workflow

### Phase 1: Requirements Clarification (10-15 min in interviews)

**Functional Requirements**
- [ ] Identify core features and user workflows
- [ ] Define inputs and outputs
- [ ] List key use cases (happy path + edge cases)
- [ ] Clarify user types and roles
- [ ] Determine read/write patterns

**Non-Functional Requirements**
- [ ] Performance: latency requirements (p50, p95, p99)
- [ ] Availability: uptime requirements (99.9%, 99.99%)
- [ ] Scalability: expected load and growth rate
- [ ] Security: authentication, authorization, encryption
- [ ] Consistency: strong vs eventual consistency
- [ ] Durability: data loss tolerance

**Constraints**
- [ ] Budget limitations
- [ ] Team skills and experience
- [ ] Timeline constraints
- [ ] Compliance requirements (GDPR, HIPAA, SOC2)
- [ ] Technology mandates or restrictions

### Phase 2: Scale Estimation (5-10 min)

- [ ] Estimate DAU/MAU
- [ ] Calculate requests per second (RPS)
  - Average RPS = DAU * actions/day / 86400
  - Peak RPS = Average * peak multiplier (typically 2-5x)
- [ ] Estimate data storage needs
  - Per-record size * records/day * retention days
- [ ] Calculate bandwidth requirements
  - Request size * RPS * 8 bits
- [ ] Project growth (1 year, 5 years)

### Phase 3: High-Level Design (15-20 min)

- [ ] Draw C4 Context diagram (system + external systems)
- [ ] Draw C4 Container diagram (major components)
- [ ] Define API contracts (REST/GraphQL/gRPC)
- [ ] Show data flow (request path from user to DB)
- [ ] Identify communication patterns (sync/async)
- [ ] Plan database architecture (SQL/NoSQL, single/distributed)

### Phase 4: Component Deep Dive (15-20 min)

**Database Design**
- [ ] Select database type(s)
- [ ] Design schema/data model
- [ ] Plan indexing strategy
- [ ] Consider partitioning/sharding
- [ ] Plan replication and failover

**Caching Strategy**
- [ ] Identify cacheable data
- [ ] Choose cache type (CDN, application, database)
- [ ] Define cache invalidation strategy
- [ ] Estimate cache hit ratio

**Message Queues (if needed)**
- [ ] Identify async operations
- [ ] Choose message broker
- [ ] Design queue topology
- [ ] Plan dead letter handling

### Phase 5: Quality Attributes (10-15 min)

**Scalability**
- [ ] Horizontal scaling strategy
- [ ] Load balancing approach
- [ ] Auto-scaling triggers

**Reliability**
- [ ] Redundancy plan
- [ ] Failover mechanisms
- [ ] Circuit breaker patterns
- [ ] Retry strategies

**Security**
- [ ] Authentication method
- [ ] Authorization model
- [ ] Data encryption (at rest, in transit)
- [ ] Rate limiting
- [ ] Input validation

### Phase 6: Documentation (5-10 min)

- [ ] List key architectural decisions
- [ ] Document trade-offs made
- [ ] Note open questions
- [ ] Identify follow-up items

---

## 2. Architecture Review Workflow

### Pre-Review Preparation

- [ ] Gather existing documentation
  - [ ] Architecture diagrams
  - [ ] ADRs
  - [ ] Design documents
  - [ ] API specifications
- [ ] Review codebase structure
- [ ] Collect metrics (if available)
  - [ ] Performance data
  - [ ] Error rates
  - [ ] Usage patterns
- [ ] Identify stakeholders
- [ ] Schedule review meeting(s)

### Roadmap Review (Should we build this?)

- [ ] Understand business objectives
- [ ] Assess strategic alignment
- [ ] Evaluate resource requirements
- [ ] Identify dependencies
- [ ] Assess risks and unknowns
- [ ] Make go/no-go recommendation

### Design Review (Is this design good?)

**Architecture Analysis**
- [ ] Verify requirements coverage
- [ ] Check component responsibilities
- [ ] Validate data flow
- [ ] Review API design
- [ ] Assess scalability approach

**Quality Attribute Check**
- [ ] Performance: meets latency requirements?
- [ ] Scalability: handles expected load?
- [ ] Availability: meets uptime requirements?
- [ ] Security: threat model addressed?
- [ ] Maintainability: easy to modify?

**Risk Assessment**
- [ ] Identify single points of failure
- [ ] Find potential bottlenecks
- [ ] Check for anti-patterns
- [ ] Assess technical debt
- [ ] Review security vulnerabilities

### Post-Review Actions

- [ ] Document findings
- [ ] Prioritize issues (critical/high/medium/low)
- [ ] Create action items
- [ ] Assign owners
- [ ] Schedule follow-up (if needed)

---

## 3. ADR Creation Workflow

### Phase 1: Identification

- [ ] Confirm decision is architecturally significant
  - [ ] Affects structure?
  - [ ] Has non-functional implications?
  - [ ] Hard to reverse?
  - [ ] Affects multiple teams?
- [ ] Check if similar ADR exists
- [ ] Assign ADR number and title

### Phase 2: Context Gathering

- [ ] Document current situation
- [ ] Describe problem to solve
- [ ] List constraints
- [ ] Identify stakeholders
- [ ] Note drivers (business, technical)

### Phase 3: Research Alternatives

- [ ] Identify 2-4 viable options
- [ ] For each option:
  - [ ] Document pros
  - [ ] Document cons
  - [ ] Estimate effort
  - [ ] Assess risks
- [ ] Create comparison matrix

### Phase 4: Decision Making

- [ ] Prepare ADR draft
- [ ] Schedule readout meeting (30-45 min)
- [ ] During meeting:
  - [ ] 10-15 min silent reading
  - [ ] 15-25 min discussion
  - [ ] 5 min decision
- [ ] If no consensus, schedule one more readout (max 3 total)

### Phase 5: Finalization

- [ ] Document final decision
- [ ] Record rationale
- [ ] Note consequences (positive and negative)
- [ ] Get required approvals
- [ ] Merge ADR to repository
- [ ] Communicate decision

### Phase 6: Maintenance

- [ ] Schedule 30-day review
- [ ] Compare ADR with actual implementation
- [ ] Update status if needed
- [ ] Link to related ADRs
- [ ] Archive if superseded

---

## 4. Technology Evaluation Workflow

### Phase 1: Define Criteria

**Must-Haves (Non-negotiable)**
- [ ] Technical requirements
- [ ] Security requirements
- [ ] Compliance requirements
- [ ] Integration requirements

**Nice-to-Haves (Preferred)**
- [ ] Developer experience
- [ ] Community size
- [ ] Documentation quality
- [ ] Vendor support

**Constraints**
- [ ] Budget limits
- [ ] Team skills
- [ ] Timeline
- [ ] Licensing restrictions

### Phase 2: Research Options

- [ ] Identify candidate technologies (3-5)
- [ ] For each candidate:
  - [ ] Review documentation
  - [ ] Check community activity
  - [ ] Find case studies
  - [ ] Read reviews/comparisons
  - [ ] Check security history
- [ ] Use AI to accelerate research (optional)

### Phase 3: Evaluate

**Scoring Matrix**
- [ ] Create weighted scoring matrix
- [ ] Score each option against criteria
- [ ] Calculate weighted totals

**Proof of Concept (if needed)**
- [ ] Define POC scope
- [ ] Set success criteria
- [ ] Time-box effort (1-2 weeks)
- [ ] Evaluate results

**Additional Analysis**
- [ ] SWOT analysis
- [ ] Total cost of ownership (TCO)
- [ ] Risk assessment

### Phase 4: Decide

- [ ] Present findings to stakeholders
- [ ] Get buy-in from affected teams
- [ ] Make selection
- [ ] Document in ADR

### Phase 5: Post-Selection

- [ ] Create adoption plan
- [ ] Plan training (if needed)
- [ ] Set up initial infrastructure
- [ ] Define success metrics
- [ ] Schedule review (30/60/90 days)

---

## 5. Architecture Assessment (ATAM)

### Phase 1: Partnership and Preparation

- [ ] Identify evaluation team
- [ ] Identify stakeholders
- [ ] Collect architecture documentation
- [ ] Schedule evaluation sessions
- [ ] Prepare presentation materials

### Phase 2: Evaluation (Day 1)

**Step 1: Present ATAM**
- [ ] Explain ATAM process to participants
- [ ] Set expectations

**Step 2: Present Business Drivers**
- [ ] Business context
- [ ] Key business goals
- [ ] Constraints
- [ ] Quality attribute requirements

**Step 3: Present Architecture**
- [ ] System overview
- [ ] Key architectural decisions
- [ ] Component interactions
- [ ] Data flow

**Step 4: Identify Architectural Approaches**
- [ ] List patterns used
- [ ] Document design decisions
- [ ] Note key technologies

**Step 5: Generate Quality Attribute Utility Tree**
- [ ] Elicit quality attributes
- [ ] Create scenarios for each
- [ ] Prioritize scenarios (High/Medium/Low)

### Phase 3: Evaluation (Day 2)

**Step 6: Analyze Architectural Approaches**
- [ ] Map scenarios to architecture
- [ ] Identify sensitivity points
- [ ] Identify trade-off points
- [ ] Document risks

**Step 7: Brainstorm and Prioritize Scenarios**
- [ ] Stakeholder scenario brainstorming
- [ ] Consolidate with utility tree
- [ ] Reprioritize if needed

**Step 8: Analyze (Refined)**
- [ ] Analyze additional scenarios
- [ ] Update risk list
- [ ] Finalize findings

### Phase 4: Reporting

- [ ] Compile findings
- [ ] Document:
  - [ ] Business drivers
  - [ ] Architectural approaches
  - [ ] Quality attribute utility tree
  - [ ] Sensitivity points
  - [ ] Trade-off points
  - [ ] Risks and non-risks
  - [ ] Recommendations
- [ ] Present to stakeholders
- [ ] Create action plan

---

## 6. Migration Planning Workflow

### Phase 1: Current State Assessment

- [ ] Document existing architecture
- [ ] Identify technical debt
- [ ] Map dependencies
- [ ] Assess pain points
- [ ] Collect metrics
- [ ] Interview stakeholders

### Phase 2: Target State Definition

- [ ] Define target architecture
- [ ] Identify quality attribute goals
- [ ] Create architecture diagrams
- [ ] Document assumptions
- [ ] Get stakeholder approval

### Phase 3: Migration Strategy

**Component Selection**
- [ ] List all components
- [ ] Prioritize by:
  - [ ] Business value
  - [ ] Technical risk
  - [ ] Dependencies
  - [ ] Effort
- [ ] Select first migration candidate

**Pattern Selection**
- [ ] Choose migration pattern:
  - [ ] Strangler Fig (incremental)
  - [ ] Blue-Green (parallel)
  - [ ] Canary (gradual traffic shift)
  - [ ] Big Bang (complete switchover)

**Planning**
- [ ] Create detailed migration plan
- [ ] Define milestones
- [ ] Estimate resources
- [ ] Plan rollback strategy
- [ ] Set up monitoring

### Phase 4: Execution (per component)

**Implement**
- [ ] Build new implementation
- [ ] Set up routing/proxy layer
- [ ] Configure feature flags

**Test**
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Security tests

**Deploy**
- [ ] Deploy to staging
- [ ] Run smoke tests
- [ ] Deploy to production (canary)
- [ ] Monitor metrics

**Validate**
- [ ] Verify functionality
- [ ] Compare performance
- [ ] Check error rates
- [ ] Get user feedback

**Complete**
- [ ] Gradually shift traffic (10% → 50% → 100%)
- [ ] Decommission legacy component
- [ ] Update documentation
- [ ] Archive old code

### Phase 5: Post-Migration

- [ ] Verify all components migrated
- [ ] Update architecture documentation
- [ ] Conduct retrospective
- [ ] Document lessons learned
- [ ] Plan optimization phase

---

## 7. Design Document Review

### Pre-Review

- [ ] Author submits design document
- [ ] Reviewer confirms scope
- [ ] Set review deadline
- [ ] Identify required reviewers

### Review Checklist

**Completeness**
- [ ] Problem statement clear?
- [ ] Requirements documented?
- [ ] Non-functional requirements addressed?
- [ ] Alternatives considered?
- [ ] Trade-offs explained?

**Technical Correctness**
- [ ] Architecture appropriate for requirements?
- [ ] Components well-defined?
- [ ] Interfaces clear?
- [ ] Data model sound?
- [ ] Error handling addressed?

**Quality Attributes**
- [ ] Performance considered?
- [ ] Scalability addressed?
- [ ] Security covered?
- [ ] Reliability planned?
- [ ] Maintainability considered?

**Implementation**
- [ ] Clear enough to implement?
- [ ] Phasing plan sensible?
- [ ] Dependencies identified?
- [ ] Risks documented?
- [ ] Testing strategy defined?

### Feedback Process

- [ ] Write feedback (comments, suggestions)
- [ ] Categorize issues:
  - [ ] Blocking (must fix)
  - [ ] Non-blocking (should fix)
  - [ ] Minor (nice to fix)
  - [ ] Question (need clarification)
- [ ] Submit review
- [ ] Author addresses feedback
- [ ] Follow-up review if needed
- [ ] Approve document

### Post-Review

- [ ] Document approved
- [ ] Stakeholders notified
- [ ] ADRs created for key decisions
- [ ] Implementation can begin

---

## Quick Reference: Workflow Selection

| Situation | Use Workflow |
|-----------|--------------|
| Designing new system | System Design |
| Evaluating existing architecture | Architecture Review |
| Making technology choice | Technology Evaluation |
| Documenting decision | ADR Creation |
| Formal quality assessment | ATAM |
| Modernizing legacy system | Migration Planning |
| Reviewing design document | Design Document Review |

---

*Part of faion-software-architect skill*
