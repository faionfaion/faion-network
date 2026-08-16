<!--
purpose: Canonical spec.md skeleton this methodology owns — problem statement, personas, user stories, FR/NFR, acceptance criteria, out of scope, assumptions, dependencies.
consumes: spec-structure spec per Prerequisites
produces: artefact conforming to content/02-output-contract.xml (template_path, sections_locked)
depends-on: content/01-core-rules.xml
token-budget-impact: ~800-1300 tokens when loaded as context
-->

# Feature: <feature_name>

**Version:** 1.0
**Status:** Draft | Review | Approved
**Author:** <author_name>
**Date:** YYYY-MM-DD
**Project:** <project_name>

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

**Who:** <user_persona>
**Problem:** {What they cannot do}
**Impact:** <business_user_impact>
**Solution:** {High-level approach — no implementation details}
**Success Metric:** {How we measure success — must be measurable}

---

## User Personas

### Persona 1: <name_archetype>
- **Role:** {What they do}
- **Goal:** <what_they_want>
- **Pain Points:** <current_frustrations>
- **Context:** {When/where they use product}

### Persona 2: <name_archetype>
- **Role:** {What they do}
- **Goal:** <what_they_want>
- **Pain Points:** <current_frustrations>
- **Context:** {When/where they use product}

---

## User Stories

### US-001: <story_title>
**As a** <persona>
**I want to** <action>
**So that** <benefit_required>

**Priority:** Must | Should | Could | Won't
**Acceptance Criteria:** AC-001

### US-002: <story_title>
**As a** <persona>
**I want to** <action>
**So that** <benefit>

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
| NFR-002 | Security | <requirement> | <numeric_target> | Must |

---

## Acceptance Criteria

### AC-001: <scenario_title>

**Scenario:** <brief_description>

**Given:** <precondition>
**And:** <additional_precondition>
**When:** <action>
**Then:** {expected result with specific values}
**And:** <additional_result>

### AC-002: <error_scenario_title>

**Given:** <precondition>
**When:** {action with invalid input}
**Then:** <specific_error_response>

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
- <technical_constraint>
- <business_constraint>

---

## Dependencies

### Internal
- {Other feature this depends on}

### External
- {Third-party service or API}
