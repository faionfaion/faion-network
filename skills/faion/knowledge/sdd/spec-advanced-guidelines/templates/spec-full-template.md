<!--
purpose: Full 14-section spec skeleton — metadata, personas, user stories, FR/NFR, acceptance criteria, out of scope, dependencies, open questions.
consumes: Base spec draft, NFR catalogue, AC quality rubric per Prerequisites
produces: artefact conforming to content/02-output-contract.xml (spec, advanced blocks)
depends-on: content/01-core-rules.xml
token-budget-impact: ~900-1500 tokens when loaded as context
-->

# Spec: <feature_name>

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

- **Who:** <target_user_group>
- **Problem:** [what problem they face]
- **Impact:** <impact>
- **Solution:** <high_level_approach>
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
| US-001 | As <persona_1>, I want to [...] so that [...] | Must | AC-001, AC-002 |
| US-002 | As <persona_2>, I want to [...] so that [...] | Should | AC-003 |

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

### NFR-001: <nfr_name>
- **Requirement:** <feature> SHALL <behavior> <quantifiable_target>.
- **Measurement:** [how to measure]
- **Priority:** Must / Should / Could
- **Validation:** <test_method>

---

## 7. Acceptance Criteria

### AC-001: <happy_path>
Traces to: FR-001

**Given** [...],
**When** [...],
**Then** [...].

### AC-002: <error_case>
Traces to: FR-001

**Given** [...],
**When** [...],
**Then** [...].

### AC-003: <edge_case>
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
