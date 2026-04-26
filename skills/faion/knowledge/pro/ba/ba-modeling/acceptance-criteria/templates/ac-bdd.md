# Acceptance Criteria: [Story/Requirement ID]

**Requirement:** [Brief description]
**Author:** [Name]
**Date:** [Date]

## Scenarios

### AC-FEATURE-01: [Happy Path Name]
**Given** [precondition/context]
**And** [additional precondition — max 2 And items]
**When** [action taken]
**Then** [expected outcome]
**And** [additional outcome if truly inseparable]

### AC-FEATURE-02: [Error Handling Name]
**Given** [precondition/context]
**When** [action that causes error]
**Then** [error handling behaviour — observable to user]

### AC-FEATURE-03: [Boundary Name]
**Given** [at the limit — e.g., maximum items reached]
**When** [action that hits the boundary]
**Then** [boundary behaviour]

## Non-Functional Criteria

### AC-FEATURE-04: Performance
[Action] must complete within [Xms] at p95.
Verifiable via: [k6 / Artillery / Lighthouse CI — specify tool]

### AC-FEATURE-05: Security
Only [role] can [action].
Verifiable via: [auth test / Playwright / contract test]

## Out of Scope
- [What is NOT covered — be explicit to prevent scope creep]
