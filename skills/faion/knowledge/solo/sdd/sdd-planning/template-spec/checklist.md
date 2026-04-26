# Template Spec Checklist

## Phase 1: Prepare Specification Document

- [ ] Create file at `.aidocs/features/{backlog|todo}/{NN}-{name}/spec.md`
- [ ] Fill metadata: Version, Status, Author, Date, Project
- [ ] Add reference documents section linking to constitution
- [ ] Copy reference document table template

## Phase 2: Write Overview Section

- [ ] Write 2-3 sentences explaining feature purpose
- [ ] Describe what users can do with this feature
- [ ] Link to related features if applicable

## Phase 3: Complete Problem Statement

- [ ] Define WHO - which persona(s) affected
- [ ] State PROBLEM - what they cannot do currently
- [ ] Explain IMPACT - business or user consequences
- [ ] Outline SOLUTION - high-level approach (not implementation details)
- [ ] Define SUCCESS METRIC - measurable outcome

## Phase 4: Define User Personas

- [ ] Create minimum 2 distinct personas
- [ ] For each persona: Role, Goal, Pain Points, Context
- [ ] Use specific archetype names
- [ ] Include when/where they use product

## Phase 5: Write User Stories

- [ ] Create US-001, US-002, etc. with meaningful titles
- [ ] Use format: "As a [persona], I want [action], so that [benefit]"
- [ ] Assign priority (Must/Should/Could)
- [ ] Link acceptance criteria (AC-001, etc.)
- [ ] Add story point estimate if using estimation

## Phase 6: Create Functional Requirements

- [ ] Create FR-001, FR-002, etc. table with ID, Requirement, Traces To, Priority
- [ ] Write each requirement with "System SHALL [specific action]"
- [ ] Ensure one interpretation only - no ambiguous language
- [ ] Link each FR to user story it traces to
- [ ] Assign MoSCoW priority
- [ ] Add validation rules if complex

## Phase 7: Add Non-Functional Requirements

- [ ] Create NFR-001, NFR-002, etc. table with ID, Category, Requirement, Target, Priority
- [ ] Cover: Performance, Security, Scalability, Availability (if applicable)
- [ ] Use specific metrics (not "fast" but "< 500ms p95")
- [ ] Define how to measure each NFR

## Phase 8: Write Acceptance Criteria

- [ ] Create AC-001, AC-002, etc. with scenario titles
- [ ] Use Given-When-Then format
- [ ] Cover happy path (successful scenario)
- [ ] Cover error cases (validation failures)
- [ ] Cover boundary conditions (limits, edge cases)
- [ ] Use specific values (not generic)
- [ ] Verify criteria are testable with pass/fail

## Phase 9: Define Out of Scope

- [ ] Create explicit list of what is NOT included
- [ ] For each out-of-scope item: state reason and timeline
- [ ] Separate "Phase 2", "Never", "To be decided" items
- [ ] Use table format for clarity

## Phase 10: Document Assumptions & Constraints

- [ ] List all assumptions about user behavior
- [ ] List all assumptions about system state
- [ ] List technical constraints (limits, integrations)
- [ ] List business constraints (budget, timeline)

## Phase 11: Add Related Information

- [ ] Identify internal dependencies (other features needed first)
- [ ] Identify external dependencies (APIs, services)
- [ ] List related features with relationship type (depends on, blocks, related)
- [ ] Add recommended skills and methodologies
- [ ] Document open questions needing resolution

## Phase 12: Quality Gate Review

- [ ] Problem statement is SMART and clear
- [ ] All personas defined with specific details
- [ ] All user stories have "so that" benefits
- [ ] All FR have traceability to US
- [ ] All NFRs have specific targets (no vague words)
- [ ] All AC use Given-When-Then format
- [ ] Requirement IDs unique (no duplicates)
- [ ] Out of scope explicitly defined
- [ ] No implementation details in spec
- [ ] Spec follows template structure