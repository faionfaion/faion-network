# Architecture Workflow Templates

Copy-paste templates for architecture workflows.

## Table of Contents

1. [System Design Template](#1-system-design-template)
2. [Architecture Review Report](#2-architecture-review-report)
3. [ADR Templates](#3-adr-templates)
4. [Technology Evaluation Matrix](#4-technology-evaluation-matrix)
5. [ATAM Templates](#5-atam-templates)
6. [Migration Planning Templates](#6-migration-planning-templates)
7. [Design Document Review](#7-design-document-review)

---

## 1. System Design Template

### System Design Document

```markdown
# System Design: [System Name]

## 1. Overview

**Purpose:** [One-line description of the system]
**Author:** [Name]
**Date:** [YYYY-MM-DD]
**Status:** Draft | In Review | Approved

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-1 | [Description] | Must-have |
| FR-2 | [Description] | Should-have |
| FR-3 | [Description] | Nice-to-have |

### 2.2 Non-Functional Requirements

| Attribute | Requirement | Target |
|-----------|-------------|--------|
| Performance | Latency p95 | < 200ms |
| Availability | Uptime | 99.9% |
| Scalability | Peak traffic | 10K RPS |
| Security | [Requirement] | [Target] |

### 2.3 Constraints

- Budget: [Amount]
- Timeline: [Duration]
- Team: [Size and skills]
- Technology: [Any mandates or restrictions]

## 3. Scale Estimation

| Metric | Value | Calculation |
|--------|-------|-------------|
| DAU | [X] M | |
| RPS (average) | [X] | DAU * actions / 86400 |
| RPS (peak) | [X] | Average * 5 |
| Storage (year) | [X] TB | Records * size * 365 |
| Bandwidth | [X] MB/s | RPS * request_size |

## 4. High-Level Design

### 4.1 Architecture Diagram

```
[Insert C4 Container diagram or system diagram]
```

### 4.2 Component Overview

| Component | Responsibility | Technology |
|-----------|---------------|------------|
| API Gateway | Routing, auth, rate limiting | Kong |
| [Service 1] | [Description] | [Stack] |
| [Service 2] | [Description] | [Stack] |
| Database | [Description] | PostgreSQL |
| Cache | [Description] | Redis |

### 4.3 Data Flow

```
1. User sends request to API Gateway
2. Gateway authenticates and routes to [Service]
3. [Service] queries [Database/Cache]
4. Response returned to user
```

## 5. Component Deep Dive

### 5.1 Database Design

**Schema:**
```sql
CREATE TABLE [table_name] (
    id UUID PRIMARY KEY,
    -- fields
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_[field] ON [table_name]([field]);
```

### 5.2 API Design

**Endpoints:**
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/v1/[resource] | List resources |
| POST | /api/v1/[resource] | Create resource |
| GET | /api/v1/[resource]/{id} | Get resource |
| PUT | /api/v1/[resource]/{id} | Update resource |
| DELETE | /api/v1/[resource]/{id} | Delete resource |

### 5.3 Caching Strategy

| Data | Cache Type | TTL | Invalidation |
|------|------------|-----|--------------|
| [Data 1] | Redis | 5 min | On update |
| [Data 2] | CDN | 1 hour | Manual |

## 6. Quality Attributes

### 6.1 Scalability

- Horizontal scaling: [Strategy]
- Load balancing: [Approach]
- Auto-scaling: [Triggers]

### 6.2 Reliability

- Redundancy: [N+1, active-passive, etc.]
- Failover: [Strategy]
- Circuit breaker: [Implementation]

### 6.3 Security

- Authentication: [Method]
- Authorization: [Model]
- Encryption: [At rest, in transit]

## 7. Trade-offs

| Decision | Option Chosen | Alternative | Rationale |
|----------|---------------|-------------|-----------|
| Database | PostgreSQL | MongoDB | [Why] |
| [Decision] | [Choice] | [Alternative] | [Why] |

## 8. Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

## 9. References

- Related ADRs: ADR-XXX, ADR-YYY
- Diagrams: [Link]
- API Spec: [Link]
```

---

## 2. Architecture Review Report

```markdown
# Architecture Review Report

## Overview

| Field | Value |
|-------|-------|
| System | [System Name] |
| Review Date | [YYYY-MM-DD] |
| Reviewers | [Names] |
| Review Type | Roadmap / Design / Ad-hoc |

## Executive Summary

[2-3 sentence summary of findings and overall assessment]

**Overall Assessment:** APPROVED / APPROVED WITH CONDITIONS / NEEDS WORK / REJECTED

## System Context

[Brief description of the system being reviewed]

## Review Scope

- [ ] Architecture design
- [ ] Quality attributes
- [ ] Security
- [ ] Scalability
- [ ] Performance
- [ ] Reliability

## Findings

### Critical Issues (Must Fix)

| ID | Issue | Impact | Recommendation |
|----|-------|--------|----------------|
| C1 | [Issue] | [Impact] | [Recommendation] |

### High Priority Issues

| ID | Issue | Impact | Recommendation |
|----|-------|--------|----------------|
| H1 | [Issue] | [Impact] | [Recommendation] |

### Medium Priority Issues

| ID | Issue | Impact | Recommendation |
|----|-------|--------|----------------|
| M1 | [Issue] | [Impact] | [Recommendation] |

### Observations (Non-blocking)

| ID | Observation | Suggestion |
|----|-------------|------------|
| O1 | [Observation] | [Suggestion] |

## Quality Attribute Assessment

| Attribute | Status | Notes |
|-----------|--------|-------|
| Performance | Pass/Fail/Partial | [Notes] |
| Scalability | Pass/Fail/Partial | [Notes] |
| Availability | Pass/Fail/Partial | [Notes] |
| Security | Pass/Fail/Partial | [Notes] |
| Maintainability | Pass/Fail/Partial | [Notes] |

## Risk Assessment

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation] |

## Recommendations Summary

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

## Action Items

| Item | Owner | Due Date | Status |
|------|-------|----------|--------|
| [Action] | [Owner] | [Date] | Open |

## Follow-up

- Next review: [Date or trigger]
- Dependencies: [Any dependencies]

## Appendix

### A. Reviewed Documents
- [Document 1]
- [Document 2]

### B. Participants
- [Name, Role]
```

---

## 3. ADR Templates

### 3.1 Standard ADR (Nygard Format)

```markdown
# ADR-[NUMBER]: [TITLE]

## Status

Proposed | Accepted | Deprecated | Superseded by ADR-XXX

## Date

[YYYY-MM-DD]

## Context

[Describe the issue motivating this decision. What is the problem we're trying to solve? What are the forces at play (technical, political, social, project)?]

## Decision

[Describe the decision we've made. Use full sentences, with active voice: "We will..."]

## Consequences

[Describe the resulting context, after applying the decision. All consequences should be listed here, not just the positive ones.]

### Positive

- [Consequence 1]
- [Consequence 2]

### Negative

- [Consequence 1]
- [Consequence 2]

### Neutral

- [Consequence 1]
```

### 3.2 MADR (Markdown ADR) Format

```markdown
# [ADR-NUMBER] [TITLE]

## Status

[Proposed | Accepted | Deprecated | Superseded]

**Deciders:** [List everyone involved in the decision]
**Date:** [YYYY-MM-DD]

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences or in the form of an illustrative story. You may want to articulate the problem in form of a question.]

## Decision Drivers

* [Driver 1, e.g., a force, facing concern, ...]
* [Driver 2, e.g., a force, facing concern, ...]
* ...

## Considered Options

* [Option 1]
* [Option 2]
* [Option 3]

## Decision Outcome

**Chosen option:** "[Option X]", because [justification. e.g., only option which meets k.o. criterion decision driver | which resolves force force | ... | comes out best (see below)].

### Consequences

* Good, because [positive consequence, e.g., improvement of one or more desired qualities, ...]
* Bad, because [negative consequence, e.g., compromising one or more desired qualities, ...]

## Pros and Cons of the Options

### [Option 1]

[Example | description | pointer to more information | ...]

* Good, because [argument a]
* Good, because [argument b]
* Bad, because [argument c]
* ...

### [Option 2]

* Good, because [argument a]
* Bad, because [argument b]
* ...

### [Option 3]

* Good, because [argument a]
* Bad, because [argument b]
* ...

## More Information

[Links to related ADRs, design documents, meeting notes, etc.]
```

### 3.3 Y-Statement Format

```markdown
# ADR-[NUMBER]: [TITLE]

## Status

[Proposed | Accepted | Deprecated | Superseded]

## Decision

In the context of [use case/story],
facing [concern],
we decided for [option],
and against [other options],
to achieve [quality/goal],
accepting [downside/tradeoff].

## Full Context

[Detailed context if needed]

## Consequences

[Positive and negative consequences]
```

---

## 4. Technology Evaluation Matrix

### 4.1 Weighted Scoring Matrix

```markdown
# Technology Evaluation: [Category]

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| [Criterion 1] | 25% | [Description] |
| [Criterion 2] | 20% | [Description] |
| [Criterion 3] | 20% | [Description] |
| [Criterion 4] | 20% | [Description] |
| [Criterion 5] | 15% | [Description] |
| **Total** | 100% | |

## Scoring Scale

| Score | Description |
|-------|-------------|
| 5 | Excellent - Exceeds requirements |
| 4 | Good - Meets requirements well |
| 3 | Acceptable - Meets minimum requirements |
| 2 | Poor - Does not fully meet requirements |
| 1 | Unacceptable - Does not meet requirements |

## Evaluation Results

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| [Criterion 1] | 25% | [1-5] | [1-5] | [1-5] |
| [Criterion 2] | 20% | [1-5] | [1-5] | [1-5] |
| [Criterion 3] | 20% | [1-5] | [1-5] | [1-5] |
| [Criterion 4] | 20% | [1-5] | [1-5] | [1-5] |
| [Criterion 5] | 15% | [1-5] | [1-5] | [1-5] |
| **Weighted Total** | 100% | [X.XX] | [X.XX] | [X.XX] |

## Detailed Analysis

### Option A: [Name]

**Overview:** [Brief description]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Notes:** [Additional observations]

### Option B: [Name]

[Same structure as Option A]

### Option C: [Name]

[Same structure as Option A]

## Recommendation

**Selected:** [Option X]

**Rationale:** [Justification for selection]

**Next Steps:**
1. [Action 1]
2. [Action 2]
```

### 4.2 SWOT Analysis Template

```markdown
# SWOT Analysis: [Technology/Option]

## Strengths (Internal, Positive)

- [Strength 1]
- [Strength 2]
- [Strength 3]

## Weaknesses (Internal, Negative)

- [Weakness 1]
- [Weakness 2]
- [Weakness 3]

## Opportunities (External, Positive)

- [Opportunity 1]
- [Opportunity 2]
- [Opportunity 3]

## Threats (External, Negative)

- [Threat 1]
- [Threat 2]
- [Threat 3]

## Summary

| Factor | Impact | Notes |
|--------|--------|-------|
| Key Strength | High/Med/Low | [Notes] |
| Key Weakness | High/Med/Low | [Notes] |
| Key Opportunity | High/Med/Low | [Notes] |
| Key Threat | High/Med/Low | [Notes] |
```

---

## 5. ATAM Templates

### 5.1 Quality Attribute Utility Tree

```markdown
# Quality Attribute Utility Tree

## [System Name]

```
Quality Attributes
├── Performance
│   ├── [Scenario 1] (H, H)
│   │   └── Stimulus: [X], Response: [Y], Measure: [Z]
│   └── [Scenario 2] (M, L)
│       └── Stimulus: [X], Response: [Y], Measure: [Z]
│
├── Availability
│   ├── [Scenario 1] (H, M)
│   │   └── Stimulus: [X], Response: [Y], Measure: [Z]
│   └── [Scenario 2] (L, L)
│       └── Stimulus: [X], Response: [Y], Measure: [Z]
│
├── Security
│   ├── [Scenario 1] (H, H)
│   └── [Scenario 2] (M, M)
│
├── Modifiability
│   ├── [Scenario 1] (H, M)
│   └── [Scenario 2] (M, H)
│
└── Usability
    ├── [Scenario 1] (L, L)
    └── [Scenario 2] (M, L)

Legend: (Importance, Difficulty)
H = High, M = Medium, L = Low
```

### 5.2 Quality Attribute Scenario

```markdown
# Quality Attribute Scenario

## Scenario ID: [QA-XXX]

| Field | Value |
|-------|-------|
| Quality Attribute | [Performance/Availability/Security/etc.] |
| Source | [Who/what generates the stimulus] |
| Stimulus | [What condition arrives at the system] |
| Artifact | [What part of the system is stimulated] |
| Environment | [Conditions when stimulus occurs] |
| Response | [How the system should respond] |
| Response Measure | [How response is measured] |

## Priority

- Business Importance: High / Medium / Low
- Technical Difficulty: High / Medium / Low

## Notes

[Additional context or considerations]
```

### 5.3 ATAM Results Summary

```markdown
# ATAM Results Summary

## System: [Name]
## Date: [YYYY-MM-DD]

## Sensitivity Points

| ID | Point | Quality Attribute | Impact |
|----|-------|-------------------|--------|
| S1 | [Decision/mechanism] | [QA] | [Impact description] |
| S2 | [Decision/mechanism] | [QA] | [Impact description] |

## Trade-off Points

| ID | Point | Attributes Affected | Trade-off |
|----|-------|---------------------|-----------|
| T1 | [Decision] | [QA1] vs [QA2] | [Description] |
| T2 | [Decision] | [QA1] vs [QA2] | [Description] |

## Risks

| ID | Risk | Severity | Mitigation |
|----|------|----------|------------|
| R1 | [Risk description] | High/Med/Low | [Mitigation strategy] |
| R2 | [Risk description] | High/Med/Low | [Mitigation strategy] |

## Non-Risks

| ID | Decision | Why It's Not a Risk |
|----|----------|---------------------|
| NR1 | [Decision] | [Explanation] |
| NR2 | [Decision] | [Explanation] |

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]
```

---

## 6. Migration Planning Templates

### 6.1 Migration Plan

```markdown
# Migration Plan: [System Name]

## Overview

| Field | Value |
|-------|-------|
| Current State | [Description] |
| Target State | [Description] |
| Migration Pattern | Strangler Fig / Blue-Green / Big Bang |
| Duration | [Estimated timeline] |

## Current Architecture

[Diagram or description of current state]

## Target Architecture

[Diagram or description of target state]

## Migration Phases

### Phase 1: [Name]

**Duration:** [X weeks]
**Components:** [List of components]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Rollback Plan:**
[Rollback steps]

### Phase 2: [Name]

[Same structure as Phase 1]

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation] |

## Resource Requirements

| Resource | Phase 1 | Phase 2 | Phase 3 |
|----------|---------|---------|---------|
| Engineers | X | X | X |
| Infrastructure | [Details] | [Details] | [Details] |

## Timeline

```
Phase 1     Phase 2     Phase 3     Cleanup
   |-----------|-----------|-----------|
Week 1-4    Week 5-8    Week 9-12   Week 13-14
```

## Communication Plan

| Milestone | Audience | Channel |
|-----------|----------|---------|
| [Milestone] | [Audience] | [Channel] |
```

### 6.2 Component Migration Checklist

```markdown
# Component Migration Checklist: [Component Name]

## Pre-Migration

- [ ] Document current component behavior
- [ ] Identify all dependencies
- [ ] Create API contract for new component
- [ ] Set up new component infrastructure
- [ ] Create monitoring and alerting
- [ ] Write migration test suite
- [ ] Create rollback procedure

## Implementation

- [ ] Implement new component
- [ ] Write unit tests (>80% coverage)
- [ ] Write integration tests
- [ ] Set up CI/CD pipeline
- [ ] Security review completed
- [ ] Load testing completed

## Routing Setup

- [ ] Configure proxy/gateway
- [ ] Set up feature flags
- [ ] Configure canary deployment
- [ ] Test routing logic

## Validation

- [ ] Comparison testing (old vs new)
- [ ] Smoke tests passing
- [ ] Performance benchmarks met
- [ ] Error rates acceptable

## Traffic Migration

- [ ] Route 1% traffic to new component
- [ ] Monitor for 24 hours
- [ ] Route 10% traffic
- [ ] Monitor for 48 hours
- [ ] Route 50% traffic
- [ ] Monitor for 1 week
- [ ] Route 100% traffic

## Post-Migration

- [ ] Decommission old component
- [ ] Update documentation
- [ ] Archive old code
- [ ] Post-mortem/retrospective

## Sign-offs

| Role | Name | Date |
|------|------|------|
| Tech Lead | | |
| QA Lead | | |
| Operations | | |
```

---

## 7. Design Document Review

### 7.1 Design Review Feedback Template

```markdown
# Design Review Feedback

## Document: [Document Name]
## Reviewer: [Name]
## Date: [YYYY-MM-DD]

## Overall Assessment

[Approved / Approved with Changes / Needs Revision / Rejected]

## Summary

[2-3 sentence summary of feedback]

## Blocking Issues

| ID | Section | Issue | Suggestion |
|----|---------|-------|------------|
| B1 | [Section] | [Issue] | [Suggestion] |

## Non-Blocking Issues

| ID | Section | Issue | Suggestion |
|----|---------|-------|------------|
| NB1 | [Section] | [Issue] | [Suggestion] |

## Questions

| ID | Section | Question |
|----|---------|----------|
| Q1 | [Section] | [Question] |

## Positive Feedback

- [Positive point 1]
- [Positive point 2]

## Next Steps

1. [Action 1]
2. [Action 2]
```

### 7.2 Design Review Checklist

```markdown
# Design Review Checklist

## Document: [Name]
## Reviewer: [Name]
## Date: [YYYY-MM-DD]

### Completeness

- [ ] Problem statement is clear
- [ ] Requirements are documented
- [ ] All stakeholders identified
- [ ] Scope is well-defined
- [ ] Out of scope items listed

### Technical Design

- [ ] High-level architecture is clear
- [ ] Component responsibilities defined
- [ ] Data model is appropriate
- [ ] API contracts are specified
- [ ] Error handling is addressed

### Quality Attributes

- [ ] Performance requirements addressed
- [ ] Scalability approach defined
- [ ] Availability/reliability covered
- [ ] Security considerations included
- [ ] Maintainability considered

### Trade-offs

- [ ] Alternatives were considered
- [ ] Trade-offs are documented
- [ ] Rationale for decisions is clear

### Implementation

- [ ] Design is implementable
- [ ] Dependencies identified
- [ ] Risks documented
- [ ] Testing strategy included
- [ ] Phasing plan is sensible

### Documentation

- [ ] Diagrams are clear
- [ ] Terminology is consistent
- [ ] References are provided
- [ ] No ambiguous statements

## Verdict

- [ ] Approved
- [ ] Approved with minor changes
- [ ] Needs revision
- [ ] Rejected

## Comments

[Additional comments]
```

---

## Quick Reference: Choosing a Template

| Situation | Template |
|-----------|----------|
| Designing new system | System Design Template |
| Reviewing architecture | Architecture Review Report |
| Recording decision | ADR (Nygard/MADR/Y-Statement) |
| Comparing technologies | Evaluation Matrix + SWOT |
| Formal assessment | ATAM Templates |
| Planning migration | Migration Plan + Checklist |
| Reviewing design doc | Review Feedback + Checklist |

---

*Part of faion-software-architect skill*
