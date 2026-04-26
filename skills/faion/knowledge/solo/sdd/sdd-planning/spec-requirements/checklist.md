# Spec Requirements Checklist

## Phase 1: Apply SMART Problem Analysis

- [ ] **Specific:** Exactly who (which persona) and what (which problem)?
- [ ] **Measurable:** How will success be measured? (metric, not "feels good")
- [ ] **Achievable:** Technically feasible with current technology?
- [ ] **Relevant:** Ties to actual business goal (not "nice to have")?
- [ ] **Time-bound:** When is this needed? (timeframe or priority)
- [ ] Create Business Value Statement: [WHO] cannot [WHAT], impacts [IMPACT], solve with [SOLUTION]

## Phase 2: Define User Personas

- [ ] Create minimum 2 distinct personas
- [ ] For each persona: Name/Archetype, Role, Goal, Pain Points, Context
- [ ] Personas must be different (not duplicates)
- [ ] Based on research or domain knowledge
- [ ] Include where/when they use product
- [ ] Specific enough to guide design decisions

## Phase 3: Create User Story Mapping

- [ ] Identify high-level USER ACTIVITIES (e.g., "Manage Account")
- [ ] Create BACKBONE - main actions under each activity
- [ ] Map WALKING SKELETON - MVP stories under each backbone
- [ ] Map v1.1 stories - Phase 2 features
- [ ] Show story priorities with swimlanes
- [ ] Ensure MVP is launchable independently

## Phase 4: Write User Stories (INVEST)

- [ ] Format: "As a [PERSONA], I want [ACTION], so that [BENEFIT]"
- [ ] **Independent:** Can be delivered separately?
- [ ] **Negotiable:** Details can be refined?
- [ ] **Valuable:** User or business value?
- [ ] **Estimable:** Can estimate effort?
- [ ] **Small:** Fits in one iteration?
- [ ] **Testable:** Acceptance criteria possible?
- [ ] Assign priority: Must (MVP), Should, Could

## Phase 5: Create Use Cases (if Complex)

- [ ] For multi-step workflows or multiple actors
- [ ] Primary Actor, Preconditions, Main Flow, Alternative Flows, Postconditions
- [ ] Main Flow: numbered steps of success scenario
- [ ] Alternative Flows: numbered steps for variations (3a, 4a, etc.)
- [ ] Include error handling and edge cases

## Phase 6: Write Functional Requirements (SMART)

- [ ] Create FR-001, FR-002, etc.
- [ ] Format: "System SHALL [specific, testable requirement]"
- [ ] **Specific:** One interpretation only
- [ ] **Measurable:** Testable with pass/fail
- [ ] **Achievable:** Technically possible
- [ ] **Relevant:** Traces to user story
- [ ] **Time-bound:** Priority assigned (MoSCoW)
- [ ] NO ambiguous words (good, fast, easy, support)
- [ ] Include validation rules if complex

## Phase 7: Apply MoSCoW Prioritization

- [ ] **Must:** Critical for launch, cannot skip (MVP requirements)
- [ ] **Should:** Important but not critical (Phase 2 nice-to-haves)
- [ ] **Could:** Nice to have if time allows (future enhancements)
- [ ] **Won't:** Explicitly not in this release (future or never)
- [ ] Assign each FR to Must, Should, Could, or Won't

## Phase 8: Create Non-Functional Requirements

- [ ] **Performance:** Response times, throughput (e.g., <500ms p95)
- [ ] **Scalability:** Load capacity (e.g., 10k concurrent users)
- [ ] **Security:** Auth, encryption, compliance (bcrypt 12 rounds)
- [ ] **Availability:** Uptime, recovery (99.9% uptime)
- [ ] **Accessibility:** WCAG level (WCAG 2.1 AA)
- [ ] **Usability:** UX metrics (e.g., <3 clicks)
- [ ] Each NFR has specific target and measurement method

## Phase 9: Write Acceptance Criteria (Given-When-Then)

- [ ] Format: Given [precondition] → When [action] → Then [result]
- [ ] Use specific values (not "valid", but "test@example.com")
- [ ] AC-001: Happy path (successful scenario)
- [ ] AC-002: Error case (validation failure)
- [ ] AC-003: Boundary condition (limits, edge cases)
- [ ] AC-004: Security scenario (unauthorized access)
- [ ] AC-005: Performance scenario (if NFR applies)
- [ ] Each scenario is testable with pass/fail

## Phase 10: Define Scope Boundaries

- [ ] **In Scope:** Explicit list of what IS included
- [ ] **Out of Scope:** Explicit list of what is NOT included
- [ ] For each Out of Scope: reason and timeline (Phase 2, Never, v2.0)
- [ ] Prevents scope creep during implementation
- [ ] Clear boundaries for all stakeholders

## Phase 11: Document Assumptions

- [ ] Assumptions about user behavior ("users understand cart shows current prices")
- [ ] Assumptions about system state ("product prices can change")
- [ ] Assumptions about external services ("API available 99%")
- [ ] Validate assumptions with stakeholders

## Phase 12: Document Constraints

- [ ] Technical constraints (max 50 items/cart, 5MB storage limit)
- [ ] Business constraints (budget, timeline)
- [ ] Integration constraints (third-party API limits)
- [ ] Performance constraints (browser capabilities)