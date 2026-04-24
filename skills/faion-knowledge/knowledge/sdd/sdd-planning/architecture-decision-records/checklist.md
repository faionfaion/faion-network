# Architecture Decision Records (ADR) Checklist

## Phase 1: Identify Decision

- [ ] Recognize architectural decision point
- [ ] Determine decision impacts (scope, teams affected)
- [ ] Check if decision is significant enough for ADR
- [ ] Identify decision makers (cross-functional team)
- [ ] Assign ADR owner/author

## Phase 2: Gather Context

- [ ] Document current situation and problem
- [ ] List technical constraints
- [ ] List business/organizational constraints
- [ ] Identify timeline pressures
- [ ] Note team capabilities
- [ ] Document dependencies on other decisions
- [ ] Research similar decisions in industry

## Phase 3: Generate Alternatives

- [ ] Brainstorm at least 2-3 alternatives
- [ ] For each alternative, list pros and cons
- [ ] Estimate effort/cost for each option
- [ ] Identify risks per alternative
- [ ] Consider long-term maintenance implications
- [ ] Evaluate learning curve for team

## Phase 4: Write ADR Document

- [ ] Create file in `docs/adr/NNN-title.md` (sequential numbering)
- [ ] Set status to "Proposed"
- [ ] Fill Context section (situation, forces, constraints)
- [ ] Write Decision section (clear action statement)
- [ ] Document Alternatives Considered with pros/cons
- [ ] Describe Consequences (positive, negative, neutral)
- [ ] Link Related Decisions
- [ ] Include date and deciders
- [ ] Keep document concise and focused

## Phase 5: Review Process

- [ ] Share draft with affected teams
- [ ] Use Amazon-style silent reading (10 min read, then discuss)
- [ ] Gather feedback and iterate
- [ ] Address concerns and questions
- [ ] Ensure broad agreement (not unanimous, but consensus)
- [ ] Get approval from decision makers

## Phase 6: Status Update & Archival

- [ ] Change status from "Proposed" to "Accepted"
- [ ] Document approval date and approvers
- [ ] Commit to version control with code
- [ ] Update related ADRs (link new ADR)
- [ ] If superseding older ADR, mark old one as "Superseded"
- [ ] Add new ADR to decision registry/index

## Phase 7: Maintenance

- [ ] Review ADR periodically (every 6-12 months)
- [ ] Update status if decision becomes deprecated
- [ ] Link to new ADR if superseded
- [ ] Keep historical records for team onboarding
