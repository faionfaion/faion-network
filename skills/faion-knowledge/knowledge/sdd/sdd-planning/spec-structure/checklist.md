# Spec Structure Checklist

## Phase 1: Understand Spec Purpose

- [ ] Specification answers "WHAT and WHY", not "HOW"
- [ ] Spec differs from Design (HOW) and Implementation Plan (WHEN/ORDER)
- [ ] Spec is foundation for design and execution phases
- [ ] Spec is communication tool between business and engineering

## Phase 2: Complete Spec Structure v2.0

- [ ] **Overview:** 2-3 sentences describing feature purpose
- [ ] **Problem Statement:** WHO, PROBLEM, IMPACT, SOLUTION, SUCCESS METRIC
- [ ] **User Personas:** Minimum 2 with role, goal, pain points, context
- [ ] **User Stories:** With "As a...I want...so that" format
- [ ] **Use Cases:** (if complex) with actor, preconditions, main flow, alternatives
- [ ] **Functional Requirements:** FR-X with SMART criteria and MoSCoW priority
- [ ] **Non-Functional Requirements:** NFR-X for performance, security, scalability
- [ ] **Acceptance Criteria:** Given-When-Then format, Given-When-Then coverage
- [ ] **Out of Scope:** Explicit exclusions with reasons and timeline
- [ ] **Assumptions & Constraints:** What we assume, what limits us
- [ ] **Related Features:** Dependencies and blocking relationships
- [ ] **Recommended Skills:** Methodologies for implementation

## Phase 3: Problem Statement Quality

- [ ] WHO is specific (persona or user type)
- [ ] PROBLEM is clearly stated (what they cannot do)
- [ ] IMPACT is quantified (business/user consequences)
- [ ] SOLUTION is high-level (not implementation details)
- [ ] SUCCESS METRIC is measurable (not "users like it")

## Phase 4: User Personas Quality

- [ ] Minimum 2 distinct personas
- [ ] Each has NAME/ARCHETYPE, ROLE, GOAL, PAIN POINTS
- [ ] CONTEXT describes when/where they use product
- [ ] Personas are different enough (not duplicates)
- [ ] Personas reflect actual user research or domain knowledge

## Phase 5: User Stories Quality

- [ ] Format: "As a [PERSONA], I want [ACTION], so that [BENEFIT]"
- [ ] Each story has clear benefit ("so that" clause)
- [ ] Stories follow INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable
- [ ] Stories are not implementation details
- [ ] Stories map to personas and acceptance criteria
- [ ] Priority is assigned (Must/Should/Could)
- [ ] No conflicting stories

## Phase 6: Functional Requirements Quality

- [ ] Each has ID (FR-001, FR-002, etc.)
- [ ] Each has "System SHALL [specific, testable action]"
- [ ] Each requirement has ONE interpretation only
- [ ] No ambiguous words ("good", "fast", "easy", "support")
- [ ] Each traces to at least one user story
- [ ] Each has MoSCoW priority (Must/Should/Could/Won't)
- [ ] Each has validation rules if complex

## Phase 7: Non-Functional Requirements Quality

- [ ] Categories covered: Performance, Security, Scalability, Availability, Accessibility, Usability
- [ ] Each has specific metric (not "fast", but "<500ms p95")
- [ ] Each has priority
- [ ] Each is measurable and testable
- [ ] Each specifies how measurement will be done

## Phase 8: Acceptance Criteria Quality

- [ ] Each scenario has title describing what is being tested
- [ ] Format: Given → When → Then (Gherkin/BDD format)
- [ ] Given: preconditions before action
- [ ] When: the action being tested
- [ ] Then: expected result after action
- [ ] Uses specific values (not "valid email", but "test@example.com")
- [ ] Covers: happy path, error cases, boundary conditions, security, performance
- [ ] Each AC is testable with pass/fail result

## Phase 9: Out of Scope Quality

- [ ] Explicitly lists features NOT included
- [ ] For each: states reason and when it will be done
- [ ] Separates "Phase 2", "Never", "Future" items
- [ ] Prevents scope creep during implementation

## Phase 10: Assumptions & Constraints Quality

- [ ] Lists all assumptions about user behavior
- [ ] Lists all assumptions about system state
- [ ] Lists technical constraints (limits, integrations)
- [ ] Lists business constraints (budget, timeline)
- [ ] Assumptions are documented and validated

## Phase 11: Traceability Quality

- [ ] Every FR traces to a user story
- [ ] Every AC validates an FR
- [ ] No orphaned requirements
- [ ] No orphaned acceptance criteria
- [ ] Traceability matrix can be created from spec

## Phase 12: Final Quality Gate

- [ ] Completeness: all required sections present
- [ ] Clarity: no ambiguous language, technical terms defined
- [ ] Consistency: no conflicting requirements
- [ ] Context: constitution referenced, related features identified
- [ ] Coverage: all user needs addressed
- [ ] Readability: organized, well-formatted, easy to follow
- [ ] Approval: ready for stakeholder and agent review