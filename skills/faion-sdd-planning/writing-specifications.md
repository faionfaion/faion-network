# Writing Specifications

## Overview

This methodology covers how to write high-quality specification documents that answer **"WHAT are we building and WHY?"**

Specifications are the foundation of SDD workflow - they define requirements, user stories, and acceptance criteria before design and implementation.

---

## Content Organization

This methodology is split into focused files:

| File | Content | Tokens |
|------|---------|--------|
| **[spec-structure.md](spec-structure.md)** | Spec template, structure, quality checklist | ~1800 |
| **[spec-requirements.md](spec-requirements.md)** | SMART requirements, user stories, acceptance criteria | ~1600 |
| **[spec-examples-basic.md](spec-examples-basic.md)** | Basic example (authentication) | ~800 |
| **[spec-example-ecommerce-cart.md](spec-example-ecommerce-cart.md)** | E-commerce cart example (full spec) | ~1100 |
| **[spec-advanced-guidelines.md](spec-advanced-guidelines.md)** | Guidelines for writing advanced specs | ~900 |

---

## Problem

Projects fail when teams build the wrong thing. This happens because:
- Requirements are vague or missing
- Stakeholders have different expectations
- Scope keeps changing during development
- No single source of truth for "what are we building?"
- User needs not properly researched
- Acceptance criteria not testable

**The root cause:** No written specification that everyone agrees on.

---

## Framework

### What is a Specification?

A specification (spec) answers: **"WHAT are we building and WHY?"**

It does NOT answer "how" - that's for the design document.

### Spec vs Design vs Implementation Plan

| Document | Question | Output |
|----------|----------|--------|
| Specification | WHAT and WHY? | Requirements, user stories, acceptance criteria |
| Design | HOW? | Architecture, file structure, API contracts |
| Implementation Plan | IN WHAT ORDER? | Tasks, dependencies, estimates |

---

## Writing Process

### Phase 1: Load Context

Before writing, read and understand:

```
1. .aidocs/constitution.md - project principles, tech stack
2. .aidocs/features/done/ - completed features (patterns)
3. Related specs in features/todo/ or features/in-progress/
```

Extract:
- Tech stack constraints
- Code standards
- Existing patterns
- Related features to reference

### Phase 2: Problem Analysis

Use SMART criteria to define the problem clearly.

See: [spec-requirements.md](spec-requirements.md) - Problem Analysis section

### Phase 3: User Research

Define user personas with roles, goals, pain points, and context.

See: [spec-requirements.md](spec-requirements.md) - User Personas section

### Phase 4: User Story Mapping

Create user story map with backbone, walking skeleton, and releases.

See: [spec-requirements.md](spec-requirements.md) - User Story Mapping section

### Phase 5: Use Cases (For Complex Features)

Write use cases for multi-step workflows, multiple actors, complex validations.

See: [spec-requirements.md](spec-requirements.md) - Use Cases section

### Phase 6: Functional Requirements

Write SMART requirements with MoSCoW prioritization and traceability.

See: [spec-requirements.md](spec-requirements.md) - Functional Requirements section

### Phase 7: Non-Functional Requirements

Define performance, security, scalability, accessibility requirements.

See: [spec-requirements.md](spec-requirements.md) - Non-Functional Requirements section

### Phase 8: Acceptance Criteria

Write Given-When-Then acceptance criteria covering all scenarios.

See: [spec-requirements.md](spec-requirements.md) - Acceptance Criteria section

### Phase 9: Scope Definition

Explicitly define what IS and IS NOT in scope.

See: [spec-requirements.md](spec-requirements.md) - Scope Definition section

---

## Templates

### Full Spec Template

See: [spec-structure.md](spec-structure.md) - Full Spec Template v2.0

Includes:
- Reference documents
- Problem statement
- User personas
- User stories
- Use cases
- Functional requirements
- Non-functional requirements
- Acceptance criteria
- Out of scope
- Assumptions & constraints
- Dependencies
- Related features
- Recommended skills & methodologies

---

## Quality Checklist

See: [spec-structure.md](spec-structure.md) - Quality Checklist section

Covers:
- Completeness (all sections filled)
- Clarity (no ambiguity)
- Consistency (no conflicts)
- Context (references constitution, related features)

---

## Examples

### Authentication Spec (Condensed)

See: [spec-examples-basic.md](spec-examples-basic.md) - Example: Authentication Spec

Shows:
- Problem statement
- User stories
- Functional requirements
- Acceptance criteria
- Out of scope

### E-commerce Cart Spec (Full)

See: [spec-example-ecommerce-cart.md](spec-example-ecommerce-cart.md) - Full e-commerce cart example
See: [spec-advanced-guidelines.md](spec-advanced-guidelines.md) - Guidelines for writing advanced specs

Shows:
- Complete spec structure
- Multiple personas
- Complex user stories
- NFRs
- Detailed acceptance criteria
- Dependencies and constraints

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| "System should be fast" | SMART: "Response time < 500ms p95" |
| No user personas | Define at least 2 personas |
| User stories without benefits | Always include "so that [benefit]" |
| Requirements without IDs | Always use FR-X, NFR-X format |
| No traceability | Every FR must trace to a user story |
| AC not testable | Use Given-When-Then with specific values |
| Missing out-of-scope | Explicitly list what you're NOT building |
| No related features | Check features/done/ for patterns |

---

## Methodology Reference

**Primary:** writing-specifications (Writing Specifications v2.0)

**Integrated:**
| Domain | Methodology | Principle Applied |
|--------|-------------|-------------------|
| BA | smart-requirements | SMART requirements criteria |
| BA | requirements-traceability | Requirements traceability (FR-X → US-X) |
| BA | use-case-modeling | Use Case diagrams and flows |
| BA | user-story-mapping | User Story Mapping |
| BA | acceptance-criteria | Acceptance criteria (Given-When-Then) |
| PdM | mvp-scoping | MVP scoping (MoSCoW prioritization) |
| PdM | user-story-mapping | User Story Mapping |
| PdM | spec-writing | PRD writing best practices |
| PM | scope-management | Scope Management |
| UX | user-research | User Research synthesis |
| UX | persona-development | Persona development |

---

## Sources

- [Requirements Engineering Fundamentals](https://www.ireb.org/en/cpre/fundamentals/) - IREB certification standard
- [User Stories Applied](https://www.mountaingoatsoftware.com/books/user-stories-applied) - Mike Cohn's guide
- [Specification by Example](https://gojko.net/books/specification-by-example/) - Gojko Adzic's methodology
- [Product Requirements Document Guide](https://www.productplan.com/learn/product-requirements-document/) - Modern PRD practices
- [Jobs-to-be-Done Framework](https://jtbd.info/) - JTBD methodology
