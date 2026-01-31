# Writing Specifications Checklist

## Phase 1: Load Context

- [ ] Read `.aidocs/constitution.md` - project principles and tech stack
- [ ] Review `features/done/` for completed feature patterns
- [ ] Identify related specs in `features/todo/` or `features/in-progress/`
- [ ] Extract tech stack constraints and code standards
- [ ] Note existing patterns and architecture decisions

## Phase 2: Problem Analysis (SMART)

- [ ] Define problem with WHO/WHAT/WHY/IMPACT clearly
- [ ] Apply SMART criteria: Specific, Measurable, Achievable, Relevant, Time-bound
- [ ] Create business value statement linking user need to impact
- [ ] Define success metric that measures outcome

## Phase 3: User Research

- [ ] Define minimum 2 user personas with role, goal, pain points, context
- [ ] Map user activities and create story mapping backbone
- [ ] Identify walking skeleton (MVP) vs phase 2 stories
- [ ] Validate personas with stakeholders

## Phase 4: Requirements Definition

- [ ] Write user stories in "As a...I want...so that" format
- [ ] Ensure each story follows INVEST principle (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- [ ] Create functional requirements (FR-X) with MoSCoW prioritization
- [ ] Define non-functional requirements (NFR-X) for performance, security, scalability
- [ ] Ensure all requirements are SMART and testable

## Phase 5: Acceptance Criteria

- [ ] Write Given-When-Then scenarios covering happy path
- [ ] Write error handling scenarios
- [ ] Write boundary condition scenarios
- [ ] Use specific values (not "valid" or "fast")
- [ ] Ensure criteria are testable with pass/fail verification

## Phase 6: Scope Definition

- [ ] Explicitly list what IS in scope
- [ ] Explicitly list what is NOT in scope with reason and timeline
- [ ] Define assumptions about user behavior and system constraints
- [ ] Identify dependencies on other features or systems

## Phase 7: Quality Gates

- [ ] Verify all sections are complete (problem, personas, stories, FR, NFR, AC, scope)
- [ ] Check for ambiguous language (good, fast, easy, etc.)
- [ ] Validate traceability: each FR traces to a user story
- [ ] Confirm requirements are SMART and not solution-focused
- [ ] Ensure out-of-scope section is explicit

## Phase 8: Review & Approval

- [ ] Present specification to stakeholders for feedback
- [ ] Resolve open questions and gaps
- [ ] Update spec based on feedback
- [ ] Obtain formal approval before moving to design phase