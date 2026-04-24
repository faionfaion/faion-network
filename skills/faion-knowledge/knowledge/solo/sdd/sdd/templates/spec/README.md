# Specification Template

Feature specification defines WHAT to build. Copy and customize for each feature.

---

```markdown
---
version: "1.0"
status: draft | review | approved
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: {name}
feature: {feature-NNN-slug}
project: {project-name}
---

# Feature: {Feature Name}

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |
| Related Feature | `.aidocs/done/{NN}-{feature}/spec.md` |

---

## Overview

{2-3 sentences describing the feature and its purpose. What is being built and why.}

---

## Problem Statement

| Aspect | Description |
|--------|-------------|
| **Who** | {User persona or segment} |
| **Problem** | {What they cannot do or struggle with} |
| **Impact** | {Business or user impact of not solving} |
| **Solution** | {High-level approach} |
| **Success Metric** | {How we measure success} |

---

## User Personas

### Persona 1: {Name/Archetype}

| Attribute | Description |
|-----------|-------------|
| Role | {What they do} |
| Goal | {What they want to achieve} |
| Pain Points | {Current frustrations} |
| Context | {When/where they use the product} |
| Tech Savviness | {Low / Medium / High} |

### Persona 2: {Name/Archetype}

{If multiple personas, repeat the table}

---

## User Stories

### US-001: {Story Title}

**As a** {persona}
**I want to** {action}
**So that** {benefit}

| Attribute | Value |
|-----------|-------|
| Priority | Must / Should / Could |
| Acceptance Criteria | AC-001 |
| Complexity | Low / Medium / High |

### US-002: {Story Title}

**As a** {persona}
**I want to** {action}
**So that** {benefit}

| Attribute | Value |
|-----------|-------|
| Priority | Must / Should / Could |
| Acceptance Criteria | AC-002, AC-003 |
| Complexity | Low / Medium / High |

---

## Functional Requirements

| ID | Requirement | Traces To | Priority | Notes |
|----|-------------|-----------|----------|-------|
| FR-001 | System SHALL {requirement} | US-001 | Must | |
| FR-002 | System SHALL {requirement} | US-001 | Must | |
| FR-003 | System SHOULD {requirement} | US-002 | Should | |
| FR-004 | System MAY {requirement} | US-003 | Could | Future |

**RFC 2119 Keywords:**
- **SHALL/MUST**: Required functionality
- **SHOULD**: Recommended, can be omitted with justification
- **MAY/COULD**: Optional, nice-to-have

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |
| NFR-002 | Performance | Concurrent users | 1000+ | Should |
| NFR-003 | Security | Password storage | bcrypt 12+ rounds | Must |
| NFR-004 | Security | Data encryption | TLS 1.3 in transit | Must |
| NFR-005 | Availability | Uptime | 99.9% | Should |
| NFR-006 | Scalability | Horizontal scaling | Stateless design | Should |
| NFR-007 | Accessibility | WCAG compliance | Level AA | Should |

---

## Acceptance Criteria

### AC-001: {Scenario Title}

**Scenario:** {Brief description}

```gherkin
Given {precondition}
  And {additional precondition}
When {action}
Then {expected result}
  And {additional result}
```

### AC-002: {Scenario Title}

**Scenario:** {Brief description}

```gherkin
Given {precondition}
When {action}
Then {expected result}
```

### AC-003: {Error Scenario}

**Scenario:** {Error condition}

```gherkin
Given {precondition}
When {invalid action}
Then {error handling}
  And {user feedback}
```

---

## UI/UX Requirements

### Wireframes

{Link to Figma/sketch or ASCII representation}

### User Flow

```
[Entry Point] -> [Step 1] -> [Step 2] -> [Success State]
                    |
                    v
              [Error State]
```

### Key Interactions

| Interaction | Expected Behavior |
|-------------|-------------------|
| {action} | {what happens} |

---

## Data Requirements

### Inputs

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| {field} | {type} | Yes/No | {rules} |

### Outputs

| Field | Type | Description |
|-------|------|-------------|
| {field} | {type} | {what it represents} |

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| {Feature 1} | {Why excluded} | Phase 2 |
| {Feature 2} | {Why excluded} | Never |
| {Feature 3} | {Why excluded} | If requested |

---

## Assumptions

- {Assumption 1}
- {Assumption 2}
- {Assumption 3}

---

## Constraints

### Technical

- {Technical constraint 1}
- {Technical constraint 2}

### Business

- {Business constraint 1}
- {Business constraint 2}

### Regulatory

- {Compliance requirement, if any}

---

## Dependencies

### Internal

| Dependency | Type | Status |
|------------|------|--------|
| {Feature/Component} | Requires | {status} |
| {Feature/Component} | Requires | {status} |

### External

| Dependency | Type | Notes |
|------------|------|-------|
| {Third-party API} | Integration | {notes} |
| {External service} | Data source | {notes} |

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {Risk 1} | High/Med/Low | High/Med/Low | {mitigation} |
| {Risk 2} | High/Med/Low | High/Med/Low | {mitigation} |

---

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| {metric} | {baseline} | {goal} | {how measured} |

---

## Open Questions

| # | Question | Owner | Status | Answer |
|---|----------|-------|--------|--------|
| 1 | {question} | {who} | Open/Resolved | {answer if resolved} |
| 2 | {question} | {who} | Open/Resolved | {answer if resolved} |

---

## Appendix

### Glossary

| Term | Definition |
|------|------------|
| {term} | {definition} |

### References

- {Reference 1}
- {Reference 2}

---

*Specification v1.0*
*Feature: {feature-NNN-slug}*
```

---

## Usage Notes

### INVEST Criteria

Good user stories are:
- **I**ndependent - Can be developed separately
- **N**egotiable - Details can be discussed
- **V**aluable - Delivers value to user
- **E**stimable - Can estimate complexity
- **S**mall - Fits in one iteration
- **T**estable - Has clear acceptance criteria

### SMART Requirements

Good requirements are:
- **S**pecific - Clear and unambiguous
- **M**easurable - Can verify completion
- **A**chievable - Technically feasible
- **R**elevant - Aligned with goals
- **T**ime-bound - Has priority/timeline

### Traceability

Every requirement should trace back to a user story, and every acceptance criterion should trace to requirements. This enables:
- Impact analysis when requirements change
- Verification that all requirements are tested
- Documentation of "why" for future reference
