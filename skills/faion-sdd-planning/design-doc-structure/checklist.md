# Design Document Structure Checklist

## Phase 1: Design Document Preparation

- [ ] Read specification (spec.md) completely
- [ ] Review constitution.md for tech stack
- [ ] Identify reference documents to include
- [ ] Confirm document status (Draft, Review, Approved)
- [ ] Set document version number

## Phase 2: Overview & Coverage

- [ ] Write 2-3 sentence technical approach summary
- [ ] Create Spec Coverage matrix (FR-X → AD-X)
- [ ] Map all functional requirements
- [ ] Map all non-functional requirements
- [ ] Verify 100% coverage of spec requirements

## Phase 3: Architectural Decisions

- [ ] Create at least 3-5 architectural decisions
- [ ] Document Context for each decision
- [ ] State Decision clearly
- [ ] Provide Rationale (2-3 reasons minimum)
- [ ] List Alternatives Considered (2+ per decision)
- [ ] Document Consequences (positive, negative)
- [ ] Trace each AD to FR-X/NFR-X

## Phase 4: File Structure & Changes

- [ ] List all CREATE actions with files
- [ ] List all MODIFY actions with files
- [ ] Create directory tree visualization
- [ ] Map file changes to FR-X and AD-X
- [ ] Include test file structure

## Phase 5: Data Models & API

- [ ] Define TypeScript types/interfaces
- [ ] Write database schema (SQL)
- [ ] Document all table relationships
- [ ] Create indexes for performance
- [ ] Document API endpoints (OpenAPI style)
- [ ] Define request/response JSON with examples
- [ ] Document error responses

## Phase 6: Dependencies & Security

- [ ] List all new packages with versions
- [ ] List external service dependencies
- [ ] Add security considerations table
- [ ] Document authentication approach
- [ ] Include input validation rules
- [ ] Plan encryption if needed

## Phase 7: Testing & Migration

- [ ] Design test pyramid strategy
- [ ] Define unit test targets
- [ ] Plan integration tests
- [ ] Plan E2E tests for critical paths
- [ ] Document migration strategy if needed
- [ ] Create rollback plan

## Phase 8: Quality Gate

- [ ] Verify all FR-X have AD-X
- [ ] Verify all NFR-X are addressed
- [ ] Check all files listed with actions
- [ ] Confirm API endpoints documented
- [ ] Verify data models complete
- [ ] Validate dependencies listed
- [ ] Check traceability matrix complete