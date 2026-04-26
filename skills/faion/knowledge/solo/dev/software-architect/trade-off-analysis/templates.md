# Trade-off Analysis Templates

Copy-paste templates for documenting trade-off analyses, decision matrices, and ADRs.

## Quick Decision Template

For Type 2 (reversible) decisions needing fast documentation.

```markdown
# Decision: [Title]

**Date:** YYYY-MM-DD
**Decision Owner:** [Name]
**Status:** Proposed | Accepted | Superseded

## Context

[1-2 sentences on what prompted this decision]

## Options

1. **[Option A]**: [Brief description]
2. **[Option B]**: [Brief description]
3. **[Option C]**: [Brief description]

## Decision

We will [chosen option] because [key reason].

## Trade-offs

| What We Get | What We Lose |
|-------------|--------------|
| [Benefit 1] | [Sacrifice 1] |
| [Benefit 2] | [Sacrifice 2] |

## Review Date

[Date to revisit this decision, if applicable]
```

---

## Decision Matrix Template

For structured comparison of multiple options.

```markdown
# Decision Matrix: [Decision Title]

## Context

[Problem description and decision scope]

## Options Evaluated

| Option | Description |
|--------|-------------|
| A: [Name] | [Description] |
| B: [Name] | [Description] |
| C: [Name] | [Description] |

## Evaluation Criteria

| Criterion | Weight (1-5) | Rationale |
|-----------|--------------|-----------|
| [Criterion 1] | [Weight] | [Why this weight] |
| [Criterion 2] | [Weight] | [Why this weight] |
| [Criterion 3] | [Weight] | [Why this weight] |
| [Criterion 4] | [Weight] | [Why this weight] |
| [Criterion 5] | [Weight] | [Why this weight] |

## Scoring

**Scale:** 1 = Poor, 2 = Below Average, 3 = Average, 4 = Good, 5 = Excellent

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| [Criterion 1] | [W] | [Score] ([W*S]) | [Score] ([W*S]) | [Score] ([W*S]) |
| [Criterion 2] | [W] | [Score] ([W*S]) | [Score] ([W*S]) | [Score] ([W*S]) |
| [Criterion 3] | [W] | [Score] ([W*S]) | [Score] ([W*S]) | [Score] ([W*S]) |
| [Criterion 4] | [W] | [Score] ([W*S]) | [Score] ([W*S]) | [Score] ([W*S]) |
| [Criterion 5] | [W] | [Score] ([W*S]) | [Score] ([W*S]) | [Score] ([W*S]) |
| **Total** | | **[Sum]** | **[Sum]** | **[Sum]** |

## Scoring Rationale

### Option A: [Name]
- [Criterion 1]: [Score] - [Justification]
- [Criterion 2]: [Score] - [Justification]

### Option B: [Name]
- [Criterion 1]: [Score] - [Justification]
- [Criterion 2]: [Score] - [Justification]

### Option C: [Name]
- [Criterion 1]: [Score] - [Justification]
- [Criterion 2]: [Score] - [Justification]

## Sensitivity Analysis

- If [Criterion X] weight increased to [N], [Option Y] would win
- [Criterion Z] has highest impact on outcome

## Recommendation

[Recommended option] with score [X] is recommended because [key reasons].
```

---

## Trade-off Analysis ADR Template

Architecture Decision Record with explicit trade-off documentation.

```markdown
# ADR-[NNN]: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Decision Makers:** [Names]
**Consulted:** [Stakeholders consulted]
**Informed:** [Stakeholders to inform]

## Context

### Problem Statement

[What is the problem or decision we need to make?]

### Business Drivers

- [Driver 1]
- [Driver 2]
- [Driver 3]

### Constraints

| Constraint | Description |
|------------|-------------|
| Budget | [Budget constraint] |
| Timeline | [Timeline constraint] |
| Technical | [Technical constraint] |
| Team | [Team capability constraint] |
| Regulatory | [Compliance constraint] |

### Quality Attribute Priorities

| Attribute | Priority (H/M/L) | Target |
|-----------|------------------|--------|
| Performance | [Priority] | [e.g., p95 < 200ms] |
| Scalability | [Priority] | [e.g., 10K concurrent] |
| Availability | [Priority] | [e.g., 99.9%] |
| Security | [Priority] | [e.g., SOC2 compliant] |
| Maintainability | [Priority] | [e.g., deploy daily] |

## Options Considered

### Option 1: [Name]

**Description:** [What is this option?]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option 2: [Name]

**Description:** [What is this option?]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

### Option 3: [Name]

**Description:** [What is this option?]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

## Decision

We have decided to implement **[chosen option]**.

### Rationale

[Explain why this option was chosen over others. Reference the key factors that made this the best choice given the constraints and priorities.]

## Trade-offs

### What We Gain

| Benefit | Impact |
|---------|--------|
| [Benefit 1] | [How it helps] |
| [Benefit 2] | [How it helps] |
| [Benefit 3] | [How it helps] |

### What We Sacrifice

| Sacrifice | Mitigation |
|-----------|------------|
| [Sacrifice 1] | [How we mitigate] |
| [Sacrifice 2] | [How we mitigate] |
| [Sacrifice 3] | [How we mitigate] |

### Trade-off Points

| Improving | Degrades | Acceptable? |
|-----------|----------|-------------|
| [Quality A] | [Quality B] | [Yes/No - Why] |
| [Quality C] | [Quality D] | [Yes/No - Why] |

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | H/M/L | H/M/L | [Mitigation strategy] |
| [Risk 2] | H/M/L | H/M/L | [Mitigation strategy] |
| [Risk 3] | H/M/L | H/M/L | [Mitigation strategy] |

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1]
- [Negative consequence 2]

### Neutral

- [Neutral consequence 1]

## Implementation Notes

- [Implementation note 1]
- [Implementation note 2]

## Review Schedule

- **First review:** [Date] - Validate initial assumptions
- **Regular review:** [Frequency] or [Trigger condition]

## Related Decisions

- [ADR-XXX](./ADR-XXX.md): [Related decision]
- [ADR-YYY](./ADR-YYY.md): [Related decision]
```

---

## ATAM Utility Tree Template

For quality attribute scenario development.

```markdown
# Utility Tree: [System Name]

## Overview

| Attribute | Description |
|-----------|-------------|
| System | [System name and version] |
| Date | YYYY-MM-DD |
| Participants | [List] |

## Quality Attribute Tree

**Priority Format:** (Business Importance, Technical Difficulty) using H/M/L

```
Utility
├── Performance
│   ├── Latency
│   │   ├── API response < 200ms for 95th percentile (H, M)
│   │   └── Search results < 500ms (M, H)
│   └── Throughput
│       ├── Support 10K requests/second (H, H)
│       └── Batch process 1M records/hour (M, M)
│
├── Availability
│   ├── Uptime
│   │   ├── 99.9% availability (H, M)
│   │   └── Zero downtime deployments (M, H)
│   └── Recovery
│       ├── RTO < 15 minutes (H, M)
│       └── RPO < 1 minute (H, H)
│
├── Security
│   ├── Authentication
│   │   ├── MFA for all admin access (H, L)
│   │   └── SSO integration (M, M)
│   └── Data Protection
│       ├── Encryption at rest and in transit (H, L)
│       └── PII anonymization in non-prod (H, M)
│
├── Modifiability
│   ├── Feature Velocity
│   │   ├── Deploy new features daily (H, M)
│   │   └── A/B test any feature (M, H)
│   └── Technology
│       ├── Replace database without code changes (L, H)
│       └── Add new payment provider in 1 week (M, M)
│
└── Scalability
    ├── Horizontal
    │   ├── Auto-scale to 10x traffic (H, M)
    │   └── Multi-region deployment (M, H)
    └── Data
        ├── Support 100M users (H, H)
        └── 5-year data retention (M, M)
```

## High Priority Scenarios (H, H)

### Scenario 1: [Name]

| Element | Description |
|---------|-------------|
| Source | [Who/what triggers] |
| Stimulus | [The event] |
| Artifact | [What is affected] |
| Environment | [System state] |
| Response | [What should happen] |
| Response Measure | [How to measure success] |

### Scenario 2: [Name]

[Same format as above]

## Architectural Approaches Mapped to Scenarios

| Scenario | Architectural Approach | Trade-offs |
|----------|------------------------|------------|
| [Scenario 1] | [Approach] | [Trade-offs] |
| [Scenario 2] | [Approach] | [Trade-offs] |
```

---

## Build vs Buy Analysis Template

```markdown
# Build vs Buy Analysis: [Capability Name]

**Date:** YYYY-MM-DD
**Decision Owner:** [Name]
**Analysis Period:** [Duration]

## Capability Definition

### What We Need

[Description of the capability required]

### Requirements

| Requirement | Priority | Notes |
|-------------|----------|-------|
| [Req 1] | Must | [Notes] |
| [Req 2] | Must | [Notes] |
| [Req 3] | Should | [Notes] |
| [Req 4] | Could | [Notes] |

### Strategic Importance

| Question | Answer |
|----------|--------|
| Is this core to competitive advantage? | [Yes/No - Explanation] |
| Does this create IP value? | [Yes/No - Explanation] |
| Is this a differentiating capability? | [Yes/No - Explanation] |

## Build Analysis

### Capability Assessment

| Factor | Rating (1-5) | Notes |
|--------|--------------|-------|
| Team expertise | [Rating] | [Notes] |
| Available capacity | [Rating] | [Notes] |
| Technology familiarity | [Rating] | [Notes] |

### Cost Estimate

| Cost Type | Year 1 | Year 2 | Year 3 | Total |
|-----------|--------|--------|--------|-------|
| Development | $[X] | $0 | $0 | $[X] |
| Maintenance (15-20%/yr) | $0 | $[X] | $[X] | $[X] |
| Infrastructure | $[X] | $[X] | $[X] | $[X] |
| Opportunity cost | $[X] | $[X] | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

### Timeline

| Milestone | Duration |
|-----------|----------|
| MVP | [X weeks/months] |
| Feature parity with buy | [X weeks/months] |
| Production ready | [X weeks/months] |

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Schedule overrun | [H/M/L] | [H/M/L] | [Mitigation] |
| Technical complexity | [H/M/L] | [H/M/L] | [Mitigation] |
| Maintenance burden | [H/M/L] | [H/M/L] | [Mitigation] |

## Buy Analysis

### Vendor Evaluation

| Vendor | Product | Market Position | Stability |
|--------|---------|-----------------|-----------|
| [Vendor 1] | [Product] | [Position] | [Rating] |
| [Vendor 2] | [Product] | [Position] | [Rating] |
| [Vendor 3] | [Product] | [Position] | [Rating] |

### Feature Fit Analysis

| Requirement | Vendor 1 | Vendor 2 | Vendor 3 |
|-------------|----------|----------|----------|
| [Req 1] | [Yes/No/Partial] | [Yes/No/Partial] | [Yes/No/Partial] |
| [Req 2] | [Yes/No/Partial] | [Yes/No/Partial] | [Yes/No/Partial] |
| **Fit %** | **[X]%** | **[X]%** | **[X]%** |

### Cost Estimate (Best Vendor)

| Cost Type | Year 1 | Year 2 | Year 3 | Total |
|-----------|--------|--------|--------|-------|
| License/Subscription | $[X] | $[X] | $[X] | $[X] |
| Implementation | $[X] | $0 | $0 | $[X] |
| Integration | $[X] | $0 | $0 | $[X] |
| Training | $[X] | $0 | $0 | $[X] |
| Customization | $[X] | $[X] | $[X] | $[X] |
| **Total** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Vendor lock-in | [H/M/L] | [H/M/L] | [Mitigation] |
| Price increases | [H/M/L] | [H/M/L] | [Mitigation] |
| Feature gaps | [H/M/L] | [H/M/L] | [Mitigation] |
| Vendor stability | [H/M/L] | [H/M/L] | [Mitigation] |

## Comparison Summary

| Factor | Build | Buy | Winner |
|--------|-------|-----|--------|
| 3-Year TCO | $[X] | $[X] | [Build/Buy] |
| Time to value | [X months] | [X months] | [Build/Buy] |
| Strategic fit | [Score] | [Score] | [Build/Buy] |
| Risk level | [H/M/L] | [H/M/L] | [Build/Buy] |
| Flexibility | [Score] | [Score] | [Build/Buy] |
| Team impact | [Score] | [Score] | [Build/Buy] |

## Recommendation

**Recommended:** [Build / Buy / Hybrid]

### Rationale

[Explanation of recommendation]

### Trade-offs Accepted

| What We Get | What We Lose |
|-------------|--------------|
| [Benefit 1] | [Sacrifice 1] |
| [Benefit 2] | [Sacrifice 2] |

### Exit Strategy

[How we maintain optionality / what happens if this doesn't work]

### Contract Requirements (if Buy)

- [ ] Price cap clause
- [ ] Data portability clause
- [ ] Exit/termination terms
- [ ] SLA guarantees
- [ ] Security/compliance attestations
```

---

## Technical Debt Documentation Template

```markdown
# Technical Debt Registry Entry

## Debt ID: DEBT-[NNN]

**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD
**Owner:** [Name]
**Status:** Active | Paying Off | Paid | Accepted

## Classification

| Dimension | Value |
|-----------|-------|
| Deliberate/Inadvertent | [Deliberate / Inadvertent] |
| Prudent/Reckless | [Prudent / Reckless] |
| Debt Type | [Code / Architectural / Test / Doc / Infrastructure] |
| Severity | [Critical / High / Medium / Low] |

## Description

### What Is the Debt?

[Description of the technical shortcut or quality issue]

### Why Was It Created?

[Business/technical context for creating this debt]

### Where Is It Located?

| Location | Impact |
|----------|--------|
| [File/Service 1] | [Impact description] |
| [File/Service 2] | [Impact description] |

## Impact Assessment

### Current Impact

| Metric | Value |
|--------|-------|
| Developer time per week | [X hours] |
| Bug frequency (related) | [X per month] |
| Deployment friction | [H/M/L] |
| Customer impact | [H/M/L] |

### Future Impact (if not addressed)

[What happens if we don't pay this off?]

## Remediation

### Remediation Plan

1. [Step 1]
2. [Step 2]
3. [Step 3]

### Effort Estimate

| Task | Estimate |
|------|----------|
| [Task 1] | [X days] |
| [Task 2] | [X days] |
| **Total** | **[X days]** |

### Trigger for Remediation

Pay off this debt when ANY of:
- [ ] [Trigger 1, e.g., "Next feature in this area"]
- [ ] [Trigger 2, e.g., "Third bug related to this"]
- [ ] [Trigger 3, e.g., "Q2 2025"]

## Trade-off Documentation

### Original Decision

**Date:** YYYY-MM-DD

We chose to [shortcut taken] because [reason], accepting that [consequence].

### Current Assessment

| Factor | Then | Now |
|--------|------|-----|
| Team capacity | [Description] | [Description] |
| Business priority | [Description] | [Description] |
| Debt tolerance | [Description] | [Description] |

## History

| Date | Action | Notes |
|------|--------|-------|
| YYYY-MM-DD | Created | [Context] |
| YYYY-MM-DD | [Action] | [Notes] |
```

---

## Stakeholder Communication Template

For presenting trade-off decisions to non-technical stakeholders.

```markdown
# [Decision Title] - Executive Summary

**Decision Required By:** YYYY-MM-DD
**Presented By:** [Name]
**Audience:** [Executive Team / Product / etc.]

## The Question

[One sentence: What decision do we need to make?]

## Why Now?

[Brief context on urgency/importance]

## Options

### Option A: [Name]

**One-liner:** [Simple description]

| Aspect | Details |
|--------|---------|
| Cost | $[X] over [Y] years |
| Timeline | [X] months to implement |
| Risk Level | [Low / Medium / High] |

**Best if:** [When this is the right choice]

### Option B: [Name]

**One-liner:** [Simple description]

| Aspect | Details |
|--------|---------|
| Cost | $[X] over [Y] years |
| Timeline | [X] months to implement |
| Risk Level | [Low / Medium / High] |

**Best if:** [When this is the right choice]

### Option C: [Name]

[Same format]

## Recommendation

We recommend **[Option X]** because:

1. [Business reason 1]
2. [Business reason 2]
3. [Business reason 3]

## Trade-offs Summary

| With [Option X] we get... | But we accept... |
|---------------------------|------------------|
| [Benefit in business terms] | [Downside in business terms] |
| [Benefit in business terms] | [Downside in business terms] |

## Key Risks

| Risk | Likelihood | Our Plan |
|------|------------|----------|
| [Risk 1] | [%] | [Mitigation] |
| [Risk 2] | [%] | [Mitigation] |

## Decision Needed

[Specific ask: What do you need stakeholders to approve?]

## Questions?

[Contact information]
```

---

## ATAM Results Summary Template

```markdown
# ATAM Evaluation Results: [System Name]

**Evaluation Date:** YYYY-MM-DD
**Evaluation Team:** [Names]
**Participants:** [Count] stakeholders from [Teams]

## Executive Summary

[2-3 paragraph summary of key findings]

## Business Drivers

1. [Driver 1]
2. [Driver 2]
3. [Driver 3]

## Architecture Overview

[Brief description of evaluated architecture]

## Quality Attribute Scenarios Analyzed

| Priority | Scenario | Satisfied? |
|----------|----------|------------|
| H,H | [Scenario 1] | [Yes/Partial/No] |
| H,H | [Scenario 2] | [Yes/Partial/No] |
| H,M | [Scenario 3] | [Yes/Partial/No] |

## Sensitivity Points

| ID | Architectural Element | Quality Affected |
|----|----------------------|------------------|
| S1 | [Element] | [Quality attribute] |
| S2 | [Element] | [Quality attribute] |

## Trade-off Points

| ID | Architectural Element | Qualities Affected | Trade-off |
|----|----------------------|-------------------|-----------|
| T1 | [Element] | [QA1] vs [QA2] | [Description] |
| T2 | [Element] | [QA1] vs [QA2] | [Description] |

## Risks

| ID | Risk | Scenario | Severity |
|----|------|----------|----------|
| R1 | [Risk description] | [Related scenario] | [H/M/L] |
| R2 | [Risk description] | [Related scenario] | [H/M/L] |

## Risk Themes

| Theme | Related Risks | Business Impact |
|-------|---------------|-----------------|
| [Theme 1] | R1, R3, R5 | [Impact] |
| [Theme 2] | R2, R4 | [Impact] |

## Non-Risks

| ID | Architectural Decision | Why It's Safe |
|----|----------------------|---------------|
| N1 | [Decision] | [Explanation] |
| N2 | [Decision] | [Explanation] |

## Recommendations

### Immediate Actions (0-30 days)

1. [Action 1]
2. [Action 2]

### Short-term Actions (1-3 months)

1. [Action 1]
2. [Action 2]

### Long-term Considerations

1. [Consideration 1]
2. [Consideration 2]

## Appendix

### A: Full Utility Tree

[Link or embed]

### B: Scenario Details

[Link or embed]

### C: Participant List

[Full list with roles]
```
