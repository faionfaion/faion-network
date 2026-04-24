# Specification Structure

## What is a Specification?

A specification (spec) answers: **"WHAT are we building and WHY?"**

It does NOT answer "how" - that's for the design document.

### Spec vs Design vs Implementation Plan

| Document | Question | Output |
|----------|----------|--------|
| Specification | WHAT and WHY? | Requirements, user stories, acceptance criteria |
| Design | HOW? | Architecture, file structure, API contracts |
| Implementation Plan | IN WHAT ORDER? | Tasks, dependencies, estimates |

---

## Spec Structure v2.0

```markdown
# Feature: [Name]

## Reference Documents
[Links to constitution, related specs]

## Overview
[1-2 paragraphs explaining what this feature does]

## Problem Statement
[Who, what problem, why it matters, business value]

## User Personas
[Who are the users]

## User Stories (User Story Mapping)
[Backbone → Walking Skeleton → Full Product]

## Use Cases (if complex)
[Actor, preconditions, flow, alternatives]

## Functional Requirements
[FR-X with SMART criteria, MoSCoW priority]

## Non-Functional Requirements
[NFR-X: performance, security, scalability]

## Acceptance Criteria (BDD)
[Given-When-Then format]

## Out of Scope
[Explicit exclusions]

## Assumptions & Constraints
[What we assume, limitations]


## Agent Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Planning task breakdown | haiku | Task decomposition from checklist |
| Estimating task complexity | sonnet | Comparative complexity assessment |
| Creating strategic roadmaps | opus | Long-term planning, dependency chains |
## Related Features
[Feature dependencies, related specs]

## Recommended Skills & Methodologies
[For implementation phase]
```

---

## Full Spec Template v2.0

```markdown
# Feature: [Feature Name]

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** [Name]
**Date:** YYYY-MM-DD
**Project:** [project-name]

---

## Reference Documents

| Document | Path | Sections |
|----------|------|----------|
| Constitution | `.aidocs/constitution.md` | Tech stack, standards |
| Related Feature | `features/done/{NN}-{feature}/spec.md` | Patterns to follow |

---

## Overview

[2-3 sentences describing the feature and its purpose]

---

## Problem Statement

**Who:** [User persona]
**Problem:** [What they cannot do]
**Impact:** [Business/user impact]
**Solution:** [High-level approach]
**Success Metric:** [How we measure success]

---

## User Personas

### Persona 1: [Name/Archetype]
- **Role:** [What they do]
- **Goal:** [What they want]
- **Pain Points:** [Current frustrations]
- **Context:** [When/where they use product]

---

## User Stories

### US-001: [Story Title]
**As a** [persona]
**I want to** [action]
**So that** [benefit]

**Priority:** Must | Should | Could
**Estimate:** [story points or T-shirt size]
**Acceptance Criteria:** AC-001

### US-002: [Story Title]
...

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL [requirement] | US-001 | Must |
| FR-002 | System SHALL [requirement] | US-001 | Must |
| FR-003 | System SHOULD [requirement] | US-002 | Should |

### FR-001: [Requirement Title]

**Requirement:** System SHALL [specific, testable requirement].

**Rationale:** [Why this is needed]

**Traces to:** US-001

**Validation Rules:**
- [Rule 1]
- [Rule 2]

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |
| NFR-002 | Security | Password storage | bcrypt 12 rounds | Must |
| NFR-003 | Scalability | Concurrent users | 10,000 | Should |

---

## Acceptance Criteria

### AC-001: [Scenario Title - Happy Path]

**Scenario:** [Brief description]

**Given:** [precondition]
**And:** [additional precondition]
**When:** [action]
**Then:** [expected result]
**And:** [additional result]

### AC-002: [Scenario Title - Error Case]
...

### AC-003: [Scenario Title - Edge Case]
...

**Coverage:**
- [x] Happy path
- [x] Error handling
- [ ] Boundary conditions
- [ ] Security scenarios
- [ ] Performance scenarios

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| [Feature] | [Why excluded] | [Future phase or Never] |

---

## Assumptions & Constraints

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Constraints
- [Technical constraint]
- [Business constraint]

---

## Dependencies

### Internal
- [Other feature this depends on]

### External
- [Third-party service]
- [Library requirement]

---

## Related Features

| Feature | Relationship | Status |
|---------|-------------|--------|
| [NN-feature] | Depends on | Done |
| [NN-feature] | Blocks | Todo |

---

## Recommended Skills & Methodologies

### Skills
| Skill | Purpose |
|-------|---------|
| faion-software-developer | Implementation |
| faion-ux-ui-designer | UI components |

### Methodologies
| ID | Name | Purpose |
|----|------|---------|
| M-DEV-XXX | [Name] | [How it helps] |

---

## Open Questions

- [ ] [Question to resolve before design]

---

## Appendix

### Wireframes
[Link or embed]

### Data Models (if known)
[Preliminary models]

### API Contracts (if known)
[Preliminary contracts]
```

---

## Quality Checklist

### Spec Quality Gate (Before Design Phase)

**Completeness:**
- [ ] Problem statement is clear (SMART)
- [ ] All user personas defined
- [ ] All user stories have INVEST criteria
- [ ] All FR-X have SMART criteria
- [ ] All FR-X trace to user stories
- [ ] NFRs cover performance, security, scalability
- [ ] All acceptance criteria in Given-When-Then

**Clarity:**
- [ ] Each requirement has ONE interpretation
- [ ] No ambiguous words (good, fast, easy, etc.)
- [ ] Technical terms defined or linked
- [ ] All acceptance criteria are testable

**Consistency:**
- [ ] Requirement IDs are unique
- [ ] No conflicting requirements
- [ ] MoSCoW priorities assigned
- [ ] Traceability matrix complete

**Context:**
- [ ] Constitution referenced
- [ ] Related features identified
- [ ] Skills/methodologies recommended
- [ ] Out of scope explicitly defined

---

## Sources

- [ISO/IEC/IEEE 29148](https://www.iso.org/standard/72089.html) - Requirements engineering standard
- [Agile Requirements](https://www.scaledagileframework.com/features-and-capabilities/) - SAFe framework
- [Product Requirements Document Template](https://www.productplan.com/glossary/product-requirements-document/) - PRD guide
- [Gherkin Reference](https://cucumber.io/docs/gherkin/reference/) - BDD scenario language
- [Requirements Traceability](https://www.reqview.com/doc/traceability-matrix.html) - Traceability matrix practices
