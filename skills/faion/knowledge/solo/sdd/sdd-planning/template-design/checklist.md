# Template Design Checklist

## Phase 1: Prepare Design Document

- [ ] Create file at `.aidocs/features/{status}/{feature}/design.md`
- [ ] Fill metadata: Version, Status, Author, Date
- [ ] Link to spec.md and constitution.md
- [ ] Write 2-3 sentence technical overview

## Phase 2: Document Architecture Decisions (AD-X)

- [ ] For each major decision: create AD-001, AD-002, etc.
- [ ] Include Context section: what problem is this solving
- [ ] List Options (minimum 2 alternatives) with Pros/Cons for each
- [ ] State Decision: which option chosen and why
- [ ] Write Rationale: reasoning behind choice, influencing factors
- [ ] Reference related FRs this decision implements

## Phase 3: Define Components

- [ ] Identify all new and modified components
- [ ] For each component: name, purpose, location, dependencies
- [ ] Create component diagram if complex
- [ ] Show interactions between components
- [ ] Reference similar patterns in existing codebase

## Phase 4: Document Data Flow

- [ ] Create data flow diagram: Component A → B → C
- [ ] Show validation points, transformations, persistence
- [ ] Document error handling at each step
- [ ] Include both success and failure paths
- [ ] Reference data models for shape of data

## Phase 5: Define Data Models

- [ ] Create table for each data entity: fields, types, constraints
- [ ] Show relationships between models
- [ ] Document validation rules for each field
- [ ] Include sample data or example values
- [ ] Link to database design if applicable

## Phase 6: Specify API Endpoints

- [ ] Reference contracts.md for API definitions (do NOT redefine)
- [ ] Create table: Method, Path, Description, FR
- [ ] For each endpoint: parameters, request/response schema
- [ ] Document error responses and status codes
- [ ] Link to related data models

## Phase 7: List Files to Change

- [ ] Create action table: File, Action (CREATE/MODIFY), Scope
- [ ] For CREATE files: what to create and why
- [ ] For MODIFY files: what changes and extent (lines, sections)
- [ ] Organize by layer: models, services, views, tests
- [ ] Show file structure for new packages

## Phase 8: Define Testing Strategy

### Unit Tests

- [ ] List components/functions to test in isolation
- [ ] Define test file locations
- [ ] Specify coverage targets
- [ ] List critical code paths to cover

### Integration Tests

- [ ] Define end-to-end flows to test
- [ ] Specify test data and fixtures needed
- [ ] Document flow from user action to database
- [ ] Include error scenarios

## Phase 9: Identify Risks

- [ ] Technical risks: API limits, schema complexity, performance
- [ ] Dependency risks: external services, blocking dependencies
- [ ] Complexity risks: unclear requirements, architectural unknowns
- [ ] For each risk: impact (High/Med/Low), mitigation strategy
- [ ] Document contingency plan

## Phase 10: FR/AD Coverage Mapping

- [ ] Create table: FR | AD | Files | Status
- [ ] Verify every FR is addressed by at least one AD
- [ ] Verify every AD is implemented by specific files
- [ ] Ensure no FR is missed
- [ ] Check each file contributes to at least one FR

## Phase 11: Quality Gate Review

- [ ] All AD decisions have context, options, rationale
- [ ] All FR requirements mapped to AD decisions
- [ ] All components documented with purpose and location
- [ ] Data models match requirements
- [ ] API endpoints reference contracts.md (not redefined)
- [ ] Files list is complete (CREATE/MODIFY)
- [ ] Testing strategy covers happy path and errors
- [ ] Risks identified and mitigated
- [ ] No implementation details (code snippets)
- [ ] Design follows template structure

## Phase 12: Review & Approval

- [ ] Present architecture decisions to stakeholders
- [ ] Confirm all FR requirements can be implemented
- [ ] Verify design aligns with constitution standards
- [ ] Get approval from architect/tech lead
- [ ] Update design based on feedback