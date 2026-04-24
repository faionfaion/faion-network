---
version: "1.0"
status: draft
created: YYYY-MM-DD
updated: YYYY-MM-DD
feature: "feature-NNN-name"
spec: "./spec.md"
design: "./design.md"
---

# Test Plan: [Feature Name]

## Test Strategy

| Aspect | Approach |
|--------|----------|
| Unit tests | [framework, coverage target] |
| Integration tests | [what integrations to test] |
| E2E tests | [critical user flows] |
| Manual testing | [if any, what and why] |

## Test Cases by Acceptance Criteria

### AC-1: [AC title from spec.md]

| ID | Test Case | Type | Preconditions | Input | Expected Result |
|----|-----------|------|---------------|-------|-----------------|
| TC-1.1 | [description] | unit | [setup] | [input] | [expected] |
| TC-1.2 | [description] | integration | [setup] | [input] | [expected] |

**Edge cases:**
- [edge case not obvious from AC]

### AC-2: [AC title from spec.md]

| ID | Test Case | Type | Preconditions | Input | Expected Result |
|----|-----------|------|---------------|-------|-----------------|
| TC-2.1 | [description] | unit | [setup] | [input] | [expected] |

**Edge cases:**
- [edge case]

## Error Scenarios

| ID | Scenario | Expected Behavior | Test Type |
|----|----------|-------------------|-----------|
| ERR-1 | [error condition] | [graceful handling] | unit |

## Test Infrastructure

### Fixtures / Test Data
- [what test data is needed]

### Mocks / Stubs
- [what to mock and why]

### Test Database
- [setup requirements, migrations]

## Coverage Summary

| AC | Unit | Integration | E2E | Total Cases |
|----|------|-------------|-----|-------------|
| AC-1 | N | N | N | N |
| AC-2 | N | N | N | N |
| **Total** | | | | |

---

*test-plan.md template v1.0*
