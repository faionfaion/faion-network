# Feature: {Feature Name}

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** {Name}
**Date:** YYYY-MM-DD
**Project:** {project-name}

---

## Reference Documents

| Document | Path |
|----------|------|
| Constitution | `.aidocs/constitution.md` |
| Related Feature | `features/done/{NN}-{feature}/spec.md` |

---

## Overview

{2-3 sentences describing the feature and its purpose}

---

## Problem Statement

**Who:** {User persona}
**Problem:** {What they cannot do}
**Impact:** {Business/user impact}
**Solution:** {High-level approach — no implementation details}
**Success Metric:** {How we measure success — must be measurable}

---

## User Personas

### Persona 1: {Name/Archetype}
- **Role:** {What they do}
- **Goal:** {What they want}
- **Pain Points:** {Current frustrations}
- **Context:** {When/where they use product}

### Persona 2: {Name/Archetype}
- **Role:** {What they do}
- **Goal:** {What they want}
- **Pain Points:** {Current frustrations}
- **Context:** {When/where they use product}

---

## User Stories

### US-001: {Story Title}
**As a** {persona}
**I want to** {action}
**So that** {benefit — required}

**Priority:** Must | Should | Could | Won't
**Acceptance Criteria:** AC-001

### US-002: {Story Title}
**As a** {persona}
**I want to** {action}
**So that** {benefit}

**Priority:** Must | Should | Could | Won't

---

## Functional Requirements

| ID | Requirement | Traces To | Priority |
|----|-------------|-----------|----------|
| FR-001 | System SHALL {specific action} | US-001 | Must |
| FR-002 | System SHALL {specific action} | US-001 | Must |
| FR-003 | System SHOULD {specific action} | US-002 | Should |

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Priority |
|----|----------|-------------|--------|----------|
| NFR-001 | Performance | Response time | < 500ms p95 | Must |
| NFR-002 | Security | {requirement} | {numeric target} | Must |

---

## Acceptance Criteria

### AC-001: {Scenario Title}

**Scenario:** {Brief description}

**Given:** {precondition}
**And:** {additional precondition}
**When:** {action}
**Then:** {expected result with specific values}
**And:** {additional result}

### AC-002: {Error Scenario Title}

**Given:** {precondition}
**When:** {action with invalid input}
**Then:** {specific error response}

---

## Out of Scope

| Feature | Reason | When |
|---------|--------|------|
| {Feature explicitly discussed and rejected} | {Why excluded} | {Phase 2 / Never / deferred} |
| {Feature explicitly discussed and rejected} | {Why excluded} | {Phase 2 / Never / deferred} |
| {Feature explicitly discussed and rejected} | {Why excluded} | {Phase 2 / Never / deferred} |

---

## Assumptions & Constraints

### Assumptions
- {Assumption about user behavior}
- {Assumption about system state}

### Constraints
- {Technical constraint}
- {Business constraint}

---

## Dependencies

### Internal
- {Other feature this depends on}

### External
- {Third-party service or API}
