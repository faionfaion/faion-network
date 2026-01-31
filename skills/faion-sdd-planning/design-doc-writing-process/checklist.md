# Design Document Writing Process Checklist

## Phase 1: Load SDD Context (Critical)

- [ ] Read .aidocs/constitution.md
- [ ] Extract tech stack from constitution
- [ ] Review API naming conventions
- [ ] Understand project patterns
- [ ] Identify coding standards
- [ ] Review existing architectural patterns

## Phase 2: Codebase Research (Token Intensive)

- [ ] Search for similar features in codebase
- [ ] Find existing service patterns
- [ ] Locate controller/handler patterns
- [ ] Review existing router implementations
- [ ] Study existing database schemas
- [ ] Examine existing component hierarchies
- [ ] Read existing test patterns

## Phase 3: Create Traceability Matrix

- [ ] List all FR-X from specification
- [ ] List all NFR-X from specification
- [ ] Plan AD (architectural decisions) needed
- [ ] Map FR-X to AD-X (each FR → at least 1 AD)
- [ ] Map NFR-X to AD-X
- [ ] Document in Spec Coverage table

## Phase 4: Write Architectural Decisions

- [ ] Define decision categories (Data, API, Architecture, Libraries, Security, Performance)
- [ ] Write each AD with Context section
- [ ] State Decision with active voice
- [ ] Provide 2-3 rationale reasons
- [ ] List 2+ alternatives for each decision
- [ ] Explain why alternatives rejected
- [ ] Document positive consequences
- [ ] Document negative consequences/tradeoffs
- [ ] Document risks
- [ ] Trace each AD to FR/NFR

## Phase 5: File Structure Planning

- [ ] List all files to CREATE
- [ ] List all files to MODIFY
- [ ] Create directory tree
- [ ] Assign FR and AD to each file
- [ ] Define file relationships
- [ ] Plan import/dependency structure

## Phase 6: Data Models Definition

- [ ] Define TypeScript interfaces
- [ ] Add field descriptions
- [ ] Plan database schema
- [ ] Define table relationships
- [ ] Plan indexes
- [ ] Document naming conventions

## Phase 7: API Contract Definition

- [ ] Document each endpoint with method and path
- [ ] Add summary for each endpoint
- [ ] Define authentication requirements
- [ ] Write request body examples
- [ ] Define response examples (success cases)
- [ ] List error responses with status codes
- [ ] Add validation rules

## Phase 8: Complete Design Components

- [ ] Add dependencies section (packages, services)
- [ ] Add security considerations
- [ ] Add performance considerations
- [ ] Add testing strategy
- [ ] Add migration strategy (if applicable)
- [ ] Add related designs reference

## Phase 9: Quality Review

- [ ] Verify every FR-X has corresponding AD-X
- [ ] Check every file listed with action
- [ ] Confirm traceability is complete
- [ ] Verify API contracts are detailed
- [ ] Check data models are complete
- [ ] Review alternatives are documented
- [ ] Ensure consequences are clear