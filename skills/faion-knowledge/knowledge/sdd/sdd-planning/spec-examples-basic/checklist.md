# Spec Examples Basic Checklist

## Phase 1: Recognize When to Use Condensed Specs

- [ ] MVP features with clear, well-understood requirements
- [ ] Simple CRUD operations (create, read, update, delete)
- [ ] Well-known patterns (auth, registration, forms)
- [ ] Small team, fast iteration environment
- [ ] Proof of concept or rapid prototyping
- [ ] NOT for complex multi-step workflows or enterprise features

## Phase 2: Include Minimum Viable Sections

- [ ] Problem Statement (WHO, PROBLEM, IMPACT, SOLUTION, METRIC)
- [ ] User Stories (1-3 stories, not extensive personas)
- [ ] Functional Requirements (3-5 requirements, not exhaustive)
- [ ] Acceptance Criteria (happy path + 1 error case, not comprehensive)
- [ ] Out of Scope (what's NOT included, when it will be)

## Phase 3: Decide What to Skip

- [ ] NO detailed persona profiles (use simple "As a [role]")
- [ ] NO extensive wireframes or designs
- [ ] NO multiple NFR categories (skip unless critical)
- [ ] NO deep technical appendices
- [ ] NO open questions section (resolve questions first)

## Phase 4: Write Problem Statement

- [ ] WHO: simple user type ("New users", "Freelance developers")
- [ ] PROBLEM: what they cannot do ("Cannot register", "Cannot access premium")
- [ ] IMPACT: business consequence ("Blocks signup flow", "Prevents monetization")
- [ ] SOLUTION: high-level approach ("Email-based registration")
- [ ] SUCCESS METRIC: quantified outcome ("1000 registrations in month 1")

## Phase 5: Write User Stories

- [ ] 1-3 stories maximum for condensed spec
- [ ] Format: "As a [role], I want [action], so that [benefit]"
- [ ] Assign priority: Must (MVP), Should (nice to have)
- [ ] Link to acceptance criteria
- [ ] Keep descriptions brief and focused

## Phase 6: Write Functional Requirements

- [ ] 3-5 requirements maximum
- [ ] Focus on MUST requirements for MVP
- [ ] Format: "System SHALL [specific requirement]"
- [ ] No ambiguous words ("support", "handle", "validate")
- [ ] Specify validation rules if critical

## Phase 7: Write Acceptance Criteria

- [ ] Create 2-3 scenarios only
- [ ] AC-1: Happy path (successful scenario)
- [ ] AC-2: Error case (validation failure)
- [ ] Use Given-When-Then format
- [ ] Use specific values ("test@example.com", not "valid email")
- [ ] Keep scenarios concise

## Phase 8: Define Out of Scope

- [ ] Explicitly list Phase 2 features
- [ ] Explicitly list features marked "Later"
- [ ] For each: state reason and timeline
- [ ] Prevents debate during implementation

## Phase 9: Keep It Concise

- [ ] NO long prose paragraphs
- [ ] NO implementation details
- [ ] NO code examples
- [ ] NO extensive background information
- [ ] Total spec: 1100-1650 tokens typical

## Phase 10: Focus on MVP Only

- [ ] Include MUST requirements for MVP
- [ ] Exclude SHOULD/COULD features
- [ ] Keep it launchable and minimal
- [ ] Plan Phase 2 for additional features

## Phase 11: Use Traceability

- [ ] Map FR-001 to User Story
- [ ] Map AC-001 to Functional Requirement
- [ ] Ensure nothing is orphaned
- [ ] Simple traceability in tables

## Phase 12: Quality Gate for Condensed Specs

- [ ] Problem is clear and SMART
- [ ] User stories are specific with clear benefits
- [ ] Requirements are testable
- [ ] Acceptance criteria use Given-When-Then
- [ ] Out of scope is explicit
- [ ] No implementation details mixed in
- [ ] Scope is focused (MVP only)
- [ ] Ready for rapid design and execution