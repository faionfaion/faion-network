<!--
purpose: Full spec.md — problem statement, goals/non-goals, success criteria, functional and non-functional requirements (FR-X/NFR-X), constraints, out-of-scope, dependencies.
consumes: constitution.md, a problem statement and a persona list (see Prerequisites)
produces: specification artefact
depends-on: content/02-output-contract.xml
token-budget-impact: ~560 tokens when filled
-->

# {feature-NNN-name}: Specification

<!-- SUMMARY: {One sentence stating the business problem this feature solves} -->

## Metadata

| Field | Value |
|-------|-------|
| **Feature** | <feature_nnn_name> |
| **Status** | draft / review / approved |
| **Priority** | P0 / P1 / P2 |
| **Complexity** | Low / Medium / High |

## Problem Statement

{2-3 sentences: what pain point does this solve? Who experiences it? What is the cost of not solving it?}

**User:** {who is affected}
**Problem:** <problem>
**Impact:** {measurable consequence of the problem}

## Goals

1. {Specific, measurable outcome — not a feature, an outcome}
2. {Specific, measurable outcome}
3. {Specific, measurable outcome}

## Non-Goals

- {Explicitly out of scope — prevents scope creep}
- {Explicitly out of scope}

## Success Criteria

| Criterion | Metric | Target |
|-----------|--------|--------|
| {e.g. Latency} | p99 response time | < 200ms |
| {e.g. Error rate} | 5xx per 1000 requests | < 1 |
| {e.g. Adoption} | Active users in 30 days | > 500 |

## Functional Requirements

### FR-1: <requirement_title>

{Full description of what the system must do — active voice, present tense}

**Acceptance Criteria:**
- Given: <precondition>
- When: <action>
- Then: <verifiable_result>

### FR-2: <requirement_title>

<full_description>

**Acceptance Criteria:**
- Given: <precondition>
- When: <action>
- Then: <verifiable_result>

**Edge case:**
- Given: <error_precondition>
- When: <action>
- Then: <error_handling_result>

## Non-Functional Requirements

### NFR-1: Performance

- {Specific constraint with measurable target}

### NFR-2: Security

- {Specific constraint — auth, data handling, compliance}

### NFR-3: Scalability

- {Specific load/growth constraint}

## Constraints

- {Technical constraint from constitution.md}
- <business_constraint>
- {Dependency or integration constraint}

## Out of Scope

| Item | Reason |
|------|--------|
| {feature or capability} | <why_excluded> |

## Open Questions

| # | Question | Owner | Status |
|---|----------|-------|--------|
| 1 | {unresolved question blocking design} | <person_role> | open |

## Dependencies

- {External system or API this feature depends on}
- {Other feature that must ship first}
