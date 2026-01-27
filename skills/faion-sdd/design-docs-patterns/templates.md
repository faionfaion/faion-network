# Design Doc Templates

Copy-paste templates for different design document styles. Choose based on your context and adapt as needed.

## Table of Contents

1. [Google-Style Design Doc](#google-style-design-doc)
2. [Amazon 6-Pager](#amazon-6-pager)
3. [Amazon PR-FAQ](#amazon-pr-faq)
4. [Uber RFC](#uber-rfc)
5. [Spotify DIBB](#spotify-dibb)
6. [Rust-Style RFC](#rust-style-rfc)
7. [Lightweight Design Doc](#lightweight-design-doc)
8. [Architecture Decision Record (ADR)](#architecture-decision-record-adr)
9. [API Design Doc](#api-design-doc)
10. [Service Design Doc](#service-design-doc)

---

## Google-Style Design Doc

Best for: General feature design, cross-team projects, internal tooling.

```markdown
# Design Doc: [Project Name]

**Author:** [Your Name]
**Reviewers:** [Names]
**Status:** Draft | In Review | Approved | Implemented
**Last Updated:** YYYY-MM-DD

---

## Overview

[1-2 paragraphs describing what this doc covers and why it exists. Should be understandable by someone unfamiliar with the project.]

## Context and Scope

### Background

[What led to this design being needed? What's the current state?]

### Goals

- [Goal 1 - specific, measurable]
- [Goal 2 - specific, measurable]
- [Goal 3 - specific, measurable]

### Non-Goals

- [Explicitly what this design does NOT address]
- [Common misconceptions to clarify]

## Design

### System Overview

[High-level architecture diagram]

```
[ASCII diagram or link to image]
```

[Description of the major components and how they interact]

### Detailed Design

#### Component A

[Details about component A: responsibilities, interfaces, key decisions]

#### Component B

[Details about component B]

#### Component C

[Details about component C]

### Data Model

[Database schema, data structures, key entities]

```sql
-- Example schema
CREATE TABLE example (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    created_at TIMESTAMP
);
```

### API

[API endpoints, request/response formats, contracts]

```
POST /api/v1/resource
Request:
{
    "field": "value"
}
Response:
{
    "id": "uuid",
    "status": "created"
}
```

## Alternatives Considered

### Alternative 1: [Name]

[Description of the alternative approach]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Why not chosen:** [Clear rationale]

### Alternative 2: [Name]

[Description]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Why not chosen:** [Clear rationale]

### Alternative 3: Do Nothing

- **Pros:** No implementation cost
- **Cons:** [Problems that remain unsolved]
- **Why not chosen:** [Why status quo is unacceptable]

## Cross-cutting Concerns

### Security

[Security implications and mitigations]
- Authentication approach
- Authorization model
- Data encryption
- Input validation
- Threat considerations

### Privacy

[Data privacy considerations]
- PII handling
- Data retention
- User consent

### Scalability

[How the design handles growth]
- Expected load
- Scaling strategy
- Bottleneck analysis

### Reliability

[Failure modes and mitigation]
- Redundancy
- Graceful degradation
- Recovery procedures

### Monitoring

[Observability approach]
- Key metrics
- Alerting strategy
- Dashboards

## Implementation Plan

### Milestones

| Milestone | Description | Status |
|-----------|-------------|--------|
| M1 | [Description] | [ ] |
| M2 | [Description] | [ ] |
| M3 | [Description] | [ ] |

### Rollout Strategy

[How the feature will be rolled out]
- Feature flags
- Percentage rollout
- Rollback plan

## Open Questions

1. [Unresolved question 1] - Owner: [Name]
2. [Unresolved question 2] - Owner: [Name]
3. [Unresolved question 3] - Owner: [Name]

## References

- [Link to related design docs]
- [Link to ADRs]
- [Link to external documentation]
- [Link to tickets/epics]
```

---

## Amazon 6-Pager

Best for: Strategic initiatives, executive reviews, complex proposals requiring deep thinking.

**Note:** Amazon 6-pagers use narrative prose, NOT bullet points. Write in complete sentences and paragraphs.

```markdown
# [Project Title]

**Author:** [Name]
**Date:** YYYY-MM-DD
**Status:** Draft | Final

---

## Introduction

[Hook the reader with the problem or opportunity. State clearly what this document proposes. Establish why this matters now. This section should make the reader want to continue. Approximately 1/2 page.]

The [team/organization] faces [specific problem]. This document proposes [solution summary] which will [key benefit].

## Goals

[State specific, measurable, achievable, relevant, and time-bound (SMART) goals. Each goal should have a clear success metric. Approximately 1/2 page.]

Our primary goal is [main objective with metric]. We will measure success by [specific KPI]. Secondary goals include [additional objectives].

The success criteria for this initiative are:
1. [Metric 1]: Achieve [X] by [date]
2. [Metric 2]: Improve [Y] by [percentage]
3. [Metric 3]: Reduce [Z] to below [threshold]

## Tenets

[Guiding principles that will govern decision-making throughout this project. List in priority order so when tenets conflict, the higher one wins. Approximately 1/2 page.]

We will be guided by the following tenets, in order of priority:

1. **Customer experience first:** We will not sacrifice user experience for internal convenience.
2. **Simplicity over features:** We prefer fewer, well-executed features over breadth.
3. **Data-driven decisions:** We will validate assumptions with data before scaling.

## State of the Business

[Current situation analysis. Include relevant data, metrics, customer insights. Be factual and specific. This is the longest section at 1-2 pages.]

Currently, our [process/system/product] handles [X] per [time period]. Analysis of [data source] reveals that [key insight with numbers].

Customer feedback from [source] indicates [specific finding]. For example, [representative quote or data point]. This aligns with industry trends showing [relevant context].

The competitive landscape shows [competitor analysis]. Specifically, [Competitor A] has [relevant capability], while [Competitor B] approaches this by [alternative approach].

Our current approach has these limitations:
- [Limitation 1 with quantified impact]
- [Limitation 2 with quantified impact]
- [Limitation 3 with quantified impact]

## Lessons Learned

[What has been tried before? What worked and what didn't? What can we learn from others? Approximately 1/2 page.]

Previous attempts to address this challenge have taught us valuable lessons. In [timeframe], we tried [approach], which resulted in [outcome with data]. The key learnings were [specific insights].

External examples provide additional guidance. [Company/Project] addressed a similar problem by [approach], achieving [results]. However, their context differs from ours in [specific ways], suggesting we should [adaptation].

## Strategic Priorities

[The proposed solution. How it will be implemented. Resources required. This section is 1-2 pages and represents the "ask".]

We propose [solution description]. This approach was chosen because [rationale connecting to goals and tenets].

The implementation will proceed in [N] phases:

**Phase 1: [Name] ([timeframe])**
[Description of first phase, resources needed, expected outcomes]

**Phase 2: [Name] ([timeframe])**
[Description of second phase]

**Phase 3: [Name] ([timeframe])**
[Description of final phase]

Resources required include [specific resource needs]. The total investment is estimated at [amount/effort], with expected return of [benefit quantification].

Risks to this plan include [risk 1], which we will mitigate by [mitigation]. Additionally, [risk 2] could impact [aspect], and our contingency is [contingency plan].

---

## Appendix

[Supporting data, detailed analysis, charts, graphs - no page limit]

### A. Detailed Data Analysis

[Tables, charts, supporting calculations]

### B. Customer Research Details

[Survey results, interview summaries]

### C. Technical Specifications

[Architecture diagrams, system requirements]
```

---

## Amazon PR-FAQ

Best for: New product ideas, customer-facing features, working backwards from launch.

```markdown
# [Product Name] - Press Release / FAQ

**Author:** [Name]
**Date:** YYYY-MM-DD
**Status:** Draft | Approved

---

# PRESS RELEASE

## [Product Name] Enables [Customer Benefit]

**[City, Date]** - [Company] today announced [Product Name], a [brief description] that enables [target customer] to [key benefit].

[Second paragraph expanding on what the product does and why it matters to customers.]

"[Quote from leader explaining the vision and customer obsession behind this product]," said [Name, Title]. "[Additional context about why this matters now.]"

[Paragraph describing how it works from the customer's perspective. Focus on the experience, not the technology.]

[Customer quote - either real or representative]: "[How this product solved their problem]," said [Customer Name, Title/Company]. "[Specific benefit they experienced.]"

[Product Name] is available starting [date] at [price/availability]. To learn more, visit [URL].

---

# FREQUENTLY ASKED QUESTIONS

## Customer FAQ (External)

### What is [Product Name]?

[Clear, simple explanation a customer would understand]

### Who is this for?

[Target customer description]

### How much does it cost?

[Pricing model explanation]

### How do I get started?

[Simple onboarding steps]

### What makes this different from [competitor/alternative]?

[Differentiation without bashing competitors]

### What if I have problems?

[Support approach]

---

## Internal FAQ (Stakeholders)

### Why are we building this?

[Business justification, market opportunity, strategic fit]

### What is the market size?

[TAM/SAM/SOM analysis]

### How does this fit with our strategy?

[Strategic alignment]

### What are the key risks?

[Risk assessment with mitigations]

### What is the timeline?

[High-level milestones]

### What resources do we need?

[Team size, budget, dependencies]

### How will we measure success?

[KPIs and success metrics]

### What are the dependencies?

[Internal and external dependencies]

### Who are the competitors?

[Competitive landscape analysis]

### What's the go-to-market strategy?

[Launch and distribution approach]

### What happens if this fails?

[Exit criteria and pivot options]
```

---

## Uber RFC

Best for: Technical proposals requiring formal approval, service changes, platform modifications.

```markdown
# RFC: [Title]

| Field | Value |
|-------|-------|
| RFC Number | RFC-NNN |
| Author | [Name] |
| Status | Draft / Review / Approved / Rejected / Superseded |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |

## Approvers

| Approver | Team | Status | Date |
|----------|------|--------|------|
| [Name] | [Team] | Pending / Approved / Rejected | |
| [Name] | [Team] | Pending / Approved / Rejected | |
| [Name] | [Team] | Pending / Approved / Rejected | |

---

## Summary

[One paragraph summary of the proposal. What are we proposing and why?]

## Motivation

[Why are we doing this? What problem does it solve? What's the business impact?]

### Problem Statement

[Clear articulation of the problem]

### Business Impact

[Quantified impact if possible]

### User Impact

[How users are affected by the current state]

## Proposal

### Overview

[High-level description of the proposed solution]

### Detailed Design

[Technical details of the implementation]

#### Architecture

[System architecture, components, interactions]

```
[Architecture diagram]
```

#### Data Model

[Schema changes, data structures]

#### API Changes

[New or modified APIs]

```
[API specification]
```

### Service SLAs

| Metric | Current | Target |
|--------|---------|--------|
| Availability | [X]% | [Y]% |
| P50 Latency | [X]ms | [Y]ms |
| P99 Latency | [X]ms | [Y]ms |
| Throughput | [X] RPS | [Y] RPS |
| Error Rate | [X]% | [Y]% |

### Dependencies

| Dependency | Type | Owner | Status |
|------------|------|-------|--------|
| [Service A] | Hard | [Team] | [Status] |
| [Library B] | Soft | [Team] | [Status] |

### Rollout Plan

| Phase | Description | Criteria | Rollback |
|-------|-------------|----------|----------|
| 1 | [Description] | [Success criteria] | [Rollback steps] |
| 2 | [Description] | [Success criteria] | [Rollback steps] |
| 3 | [Description] | [Success criteria] | [Rollback steps] |

## Alternatives

### Alternative 1: [Name]

[Description]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Rejection reason:** [Why not chosen]

### Alternative 2: [Name]

[Description]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Rejection reason:** [Why not chosen]

## Security Considerations

[Security analysis]

- [ ] Authentication requirements
- [ ] Authorization model
- [ ] Data encryption approach
- [ ] Input validation
- [ ] Audit logging

## Operational Considerations

### Deployment

[Deployment approach, feature flags, canary]

### Monitoring

[Metrics, dashboards, alerts]

### On-Call Impact

[Changes to on-call procedures, runbooks]

### Rollback Procedure

[Step-by-step rollback instructions]

## Timeline

| Phase | Description | Target |
|-------|-------------|--------|
| Design Review | RFC approval | [Date] |
| Implementation | Core functionality | [Date] |
| Testing | Integration tests | [Date] |
| Rollout | Production deployment | [Date] |
| Completion | Full rollout | [Date] |

## Open Questions

1. [Question] - Owner: [Name] - Due: [Date]
2. [Question] - Owner: [Name] - Due: [Date]

## References

- [Link to related RFCs]
- [Link to documentation]
- [Link to tickets]
```

---

## Spotify DIBB

Best for: Strategic decisions, product bets, data-driven initiatives.

```markdown
# DIBB: [Initiative Name]

**Author:** [Name]
**Date:** YYYY-MM-DD
**Status:** Draft | In Discussion | Approved
**Bet Level:** Company Bet | Functional Bet | Team Bet

---

## Data

[Objective facts that describe the customer, product, or market. These should be inarguable truths.]

| Data Point | Source | Date |
|------------|--------|------|
| [Metric/Fact 1] | [Source] | [Date] |
| [Metric/Fact 2] | [Source] | [Date] |
| [Metric/Fact 3] | [Source] | [Date] |

Key data points:
- [Data 1]: [Specific number/fact from reliable source]
- [Data 2]: [Specific number/fact from reliable source]
- [Data 3]: [Specific number/fact from reliable source]

---

## Insight

[Learning, theory, or conclusion drawn from the data. The "so what" of the data.]

Based on the data above, we observe that:

1. [Insight 1]: [What the data tells us]
2. [Insight 2]: [Pattern or trend we've identified]
3. [Insight 3]: [Customer behavior or market signal]

The key insight is: [One sentence synthesis of what we've learned]

---

## Belief

[Hypothesis formed from insights. A belief about what will be true if we act.]

We believe that:

**If** [we take this action],
**Then** [this outcome will occur],
**Because** [reasoning based on insights].

Supporting beliefs:
- [Belief 1]: [Hypothesis]
- [Belief 2]: [Hypothesis]

Assumptions we're making:
- [Assumption 1]
- [Assumption 2]

---

## Bet

[Specific initiative to test the belief. What we're going to do.]

### Bet Description

[Clear description of what we're proposing to do]

### Success Metrics

| Metric | Current | Target | Timeframe |
|--------|---------|--------|-----------|
| [Metric 1] | [X] | [Y] | [Period] |
| [Metric 2] | [X] | [Y] | [Period] |

### Scope

**In scope:**
- [Item 1]
- [Item 2]

**Out of scope:**
- [Item 1]
- [Item 2]

### Resources Required

| Resource | Amount | Duration |
|----------|--------|----------|
| Engineering | [X FTE] | [Y weeks] |
| Design | [X FTE] | [Y weeks] |
| Other | [X] | [Y] |

### Timeline

| Phase | Description | Duration |
|-------|-------------|----------|
| Discovery | [Description] | [X weeks] |
| Build | [Description] | [X weeks] |
| Launch | [Description] | [X weeks] |
| Measure | [Description] | [X weeks] |

### Kill Criteria

We will stop this bet if:
- [Condition 1]
- [Condition 2]

### Related Bets

| Bet | Relationship |
|-----|--------------|
| [Bet Name] | [How it relates] |

---

## Discussion Log

| Date | Participant | Feedback | Resolution |
|------|-------------|----------|------------|
| | | | |
```

---

## Rust-Style RFC

Best for: Language/framework changes, open source projects, community-driven decisions.

```markdown
- Feature Name: [feature_name]
- Start Date: YYYY-MM-DD
- RFC PR: [rust-lang/rfcs#0000](link)
- Tracking Issue: [rust-lang/rust#0000](link)

# Summary

[One paragraph explanation of the feature.]

# Motivation

[Why are we doing this? What use cases does it support? What is the expected outcome?]

# Guide-level explanation

[Explain the proposal as if it was already implemented and you were teaching it to another user. This generally means:

- Introducing new named concepts.
- Explaining the feature largely in terms of examples.
- Explaining how users should *think* about the feature.
- If applicable, provide sample error messages, deprecation warnings, or migration guidance.]

# Reference-level explanation

[This is the technical portion of the RFC. Explain the design in sufficient detail that:

- Its interaction with other features is clear.
- It is reasonably clear how the feature would be implemented.
- Corner cases are dissected by example.

The section should return to the examples given in the previous section, and explain more fully how the detailed proposal makes those examples work.]

# Drawbacks

[Why should we *not* do this?]

# Rationale and alternatives

[Why is this design the best in the space of possible designs?]

[What other designs have been considered and what is the rationale for not choosing them?]

[What is the impact of not doing this?]

# Prior art

[Discuss prior art, both the good and the bad, in relation to this proposal. A few examples of what this can include are:

- For language, library, and compiler proposals: Does this feature exist in other programming languages and what experience have their community had?
- For community proposals: Is this done by some other community and what were their experiences with it?
- Papers: Are there any published papers or great posts that discuss this? If you have some relevant papers to refer to, this can serve as a more detailed theoretical background.]

# Unresolved questions

[What parts of the design do you expect to resolve through the RFC process before this gets merged?]

[What parts of the design do you expect to resolve through the implementation of this feature before stabilization?]

[What related issues do you consider out of scope for this RFC that could be addressed in the future independently of the solution that comes out of this RFC?]

# Future possibilities

[Think about what the natural extension and evolution of your proposal would be and how it would affect the language and project as a whole. Try to use this section as a tool to more fully consider all possible interactions with the project in your proposal.]
```

---

## Lightweight Design Doc

Best for: Small features, team-scoped changes, rapid iteration.

```markdown
# [Feature Name]

**Author:** [Name] | **Date:** YYYY-MM-DD | **Status:** Draft/Approved

## Problem

[2-3 sentences describing the problem]

## Solution

[2-3 sentences describing the solution]

## Design

[Key technical decisions, can include simple diagram]

```
[Simple diagram if helpful]
```

## Alternatives

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| [Option A] | [Pros] | [Cons] | Yes |
| [Option B] | [Pros] | [Cons] | No |

## Risks

- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

## Open Questions

- [ ] [Question 1]
- [ ] [Question 2]

## Approvals

- [ ] [Reviewer 1]
- [ ] [Reviewer 2]
```

---

## Architecture Decision Record (ADR)

Best for: Recording individual architectural decisions, building decision logs.

```markdown
# ADR-NNN: [Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-XXX]
**Deciders:** [Names]

## Context

[What is the issue that we're seeing that is motivating this decision or change?]

## Decision

[What is the change that we're proposing and/or doing?]

We will [decision].

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]

### Negative

- [Negative consequence 1]
- [Negative consequence 2]

### Neutral

- [Neutral consequence 1]

## Alternatives Considered

### [Alternative 1]

[Description]

Rejected because: [Reason]

### [Alternative 2]

[Description]

Rejected because: [Reason]

## References

- [Link to design doc]
- [Link to related ADRs]
- [Link to external resources]
```

---

## API Design Doc

Best for: New APIs, significant API changes, external-facing interfaces.

```markdown
# API Design: [API Name]

**Author:** [Name]
**Version:** v1.0
**Status:** Draft | Review | Approved
**Date:** YYYY-MM-DD

## Overview

[Brief description of the API and its purpose]

## Use Cases

| # | Actor | Goal | Priority |
|---|-------|------|----------|
| 1 | [Who] | [What they want to do] | Must Have |
| 2 | [Who] | [What they want to do] | Should Have |

## Endpoints

### [Resource Name]

#### Create [Resource]

```
POST /api/v1/[resources]
```

**Request:**
```json
{
    "field1": "string",
    "field2": 123,
    "field3": true
}
```

**Response (201 Created):**
```json
{
    "id": "uuid",
    "field1": "string",
    "field2": 123,
    "field3": true,
    "created_at": "2024-01-01T00:00:00Z"
}
```

**Errors:**
| Code | Condition |
|------|-----------|
| 400 | Invalid request body |
| 401 | Unauthorized |
| 409 | Resource already exists |

#### Get [Resource]

```
GET /api/v1/[resources]/{id}
```

[Continue for all endpoints...]

## Data Models

### [Model Name]

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | Yes | Unique identifier |
| name | String | Yes | Display name |
| status | Enum | Yes | active, inactive |

## Authentication

[Authentication mechanism: API key, OAuth, JWT, etc.]

## Rate Limiting

| Tier | Requests/minute | Burst |
|------|-----------------|-------|
| Free | 60 | 10 |
| Pro | 1000 | 100 |

## Versioning

[Versioning strategy: URL path, header, query parameter]

## Pagination

[Pagination approach: cursor, offset, page-based]

## Error Format

```json
{
    "error": {
        "code": "INVALID_REQUEST",
        "message": "Human readable message",
        "details": []
    }
}
```

## Migration Guide

[For breaking changes: how to migrate from previous version]

## References

- [OpenAPI Spec link]
- [Related design docs]
```

---

## Service Design Doc

Best for: New microservices, service decomposition, backend systems.

```markdown
# Service Design: [Service Name]

**Author:** [Name]
**Status:** Draft | Approved
**Date:** YYYY-MM-DD

## Overview

[What this service does and why it exists]

**Service Type:** [API Service | Worker | Gateway | etc.]
**Team:** [Owning team]

## Responsibilities

### In Scope

- [Responsibility 1]
- [Responsibility 2]

### Out of Scope

- [Not responsibility 1]
- [Not responsibility 2]

## Architecture

```
[Architecture diagram]
```

### Dependencies

| Service | Type | Purpose |
|---------|------|---------|
| [Service A] | Sync | [Purpose] |
| [Service B] | Async | [Purpose] |

### Dependents

| Service | Purpose |
|---------|---------|
| [Service C] | [Purpose] |

## API

[Reference to API design doc or inline specification]

## Data

### Database

| Table | Purpose | Estimated Size |
|-------|---------|----------------|
| [Table A] | [Purpose] | [Size] |

### Events Published

| Event | Schema | Consumers |
|-------|--------|-----------|
| [Event A] | [Link] | [Services] |

### Events Consumed

| Event | Source | Purpose |
|-------|--------|---------|
| [Event A] | [Service] | [Purpose] |

## SLAs

| Metric | Target |
|--------|--------|
| Availability | 99.9% |
| P50 Latency | 50ms |
| P99 Latency | 200ms |
| Error Rate | < 0.1% |

## Capacity Planning

| Resource | Initial | Growth Rate |
|----------|---------|-------------|
| Instances | [N] | [X/month] |
| Storage | [N GB] | [X GB/month] |
| Throughput | [N RPS] | [X RPS/month] |

## Security

- [ ] Authentication: [Mechanism]
- [ ] Authorization: [Model]
- [ ] Encryption: [At rest/in transit]
- [ ] Secrets management: [Approach]

## Operational

### Deployment

[Deployment strategy, environments]

### Monitoring

[Key metrics, dashboards, alerts]

### Runbooks

| Scenario | Runbook |
|----------|---------|
| [Scenario 1] | [Link] |

## References

- [Related design docs]
- [ADRs]
- [External docs]
```

---

*For real examples using these templates, see [examples.md](examples.md). For a step-by-step guide, see [checklist.md](checklist.md).*
