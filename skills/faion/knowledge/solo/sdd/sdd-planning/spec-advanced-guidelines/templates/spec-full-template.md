# Spec: [Feature Name]

<!-- Full spec: use for complex features with multiple user types or significant NFRs -->
<!-- Minimal spec: skip to just Overview + 1-2 stories + basic AC for simple CRUD -->

## Metadata

- **id:** FEAT-NNN
- **status:** draft
- **priority:** P1
- **version:** "1.0.0"
- **created:** YYYY-MM-DD
- **updated:** YYYY-MM-DD

---

## 1. Overview

_2-3 sentence summary of what this feature does and why it matters._

---

## 2. Problem Statement

- **Who:** [target user group]
- **Problem:** [what problem they face]
- **Impact:** [business or user cost if unsolved]
- **Solution:** [high-level approach]
- **Success Metric:** [how to measure the feature succeeded]

---

## 3. User Personas

### Persona 1: [Name]
- **Role:** ...
- **Goals:** ...
- **Pain points:** ...
- **Usage context:** (mobile / desktop / API / ...)

### Persona 2: [Name]
- **Role:** ...
- **Goals:** ...
- **Pain points:** ...

---

## 4. User Stories

| ID | Story | Priority | AC |
|----|-------|----------|----|
| US-001 | As [Persona 1], I want to [...] so that [...] | Must | AC-001, AC-002 |
| US-002 | As [Persona 2], I want to [...] so that [...] | Should | AC-003 |

---

## 5. Functional Requirements

### FR-001: [Requirement name]
Traces to: US-001

**SHALL** [specific observable behavior].

### FR-002: [Requirement name]
Traces to: US-001

**SHALL** [specific observable behavior].

---

## 6. Non-Functional Requirements

### NFR-001: [NFR name]
- **Requirement:** [Feature] SHALL [behavior] [quantifiable target].
- **Measurement:** [how to measure]
- **Priority:** Must / Should / Could
- **Validation:** [test method]

---

## 7. Acceptance Criteria

### AC-001: [Happy path]
Traces to: FR-001

**Given** [...],
**When** [...],
**Then** [...].

### AC-002: [Error case]
Traces to: FR-001

**Given** [...],
**When** [...],
**Then** [...].

### AC-003: [Edge case]
Traces to: FR-002

**Given** [...],
**When** [...],
**Then** [...].

---

## 8. Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| ... | Not MVP | Phase 2 |

---

## 9. Assumptions and Constraints

- **Assumption:** [...]. If wrong: [...].
- **Constraint:** [...].

---

## 10. Dependencies

| Feature / System | Relationship | Status |
|-----------------|--------------|--------|
| ... | Depends on | Done / Todo |

---

## 11. Related Features

- Blocks: FEAT-NNN
- Blocked by: (none)

---

## 12. Recommended Skills

- ...

---

## 13. Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | ... | ... | Open |

---

## 14. Appendix

_Wireframes, data models, mockups, or external references._
