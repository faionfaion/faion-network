# Design Doc Templates

Copy-paste templates for design documents, RFCs, and architecture decision records. Based on practices from Google, Amazon, Uber, Spotify, HashiCorp, and other leading companies.

---

## Template Index

| Template | Best For | Length |
|----------|----------|--------|
| [Google-Style Design Doc](#google-style-design-doc) | General engineering projects | 2-5 pages |
| [Uber RFC](#uber-rfc-template) | Cross-team technical changes | 3-6 pages |
| [Amazon 6-Pager](#amazon-6-pager-template) | Strategy and major initiatives | 6 pages |
| [Amazon PR-FAQ](#amazon-pr-faq-template) | New products/features | 2-4 pages |
| [Spotify ADR](#spotify-adr-template) | Recording architectural decisions | 1-2 pages |
| [Mini RFC](#mini-rfc-template) | Team-scope quick decisions | 1 page |
| [HashiCorp RFC](#hashicorp-rfc-template) | Open source projects | 3-5 pages |
| [Lightweight Design Doc](#lightweight-design-doc-template) | Small features | 1-2 pages |

---

## Google-Style Design Doc

```markdown
# Design Doc: [Project Name]

**Author:** [Your Name]
**Reviewers:** [Names of reviewers]
**Status:** Draft | In Review | Approved | Implemented | Deprecated
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

---

## Overview

[1-2 paragraphs describing what this doc covers, what you're proposing, and why it matters. A reader should understand the purpose from this section alone.]

## Context and Scope

### Background

[What led to this design being needed? Describe the current state, pain points, and any relevant history. 1-2 paragraphs.]

### Goals

- [Goal 1: Specific, measurable outcome]
- [Goal 2: Specific, measurable outcome]
- [Goal 3: Specific, measurable outcome]

### Non-Goals

- [Explicitly what this design does NOT address]
- [Why certain things are intentionally out of scope]

## Design

### System Overview

[High-level architecture. Include a diagram if helpful.]

```
[ASCII diagram or description of component relationships]
```

### Detailed Design

#### [Component A]

[Description of component A, its responsibilities, and how it works.]

#### [Component B]

[Description of component B, its responsibilities, and how it works.]

### Data Model

[Database schema, data structures, or state that will be stored.]

```sql
-- Example schema
CREATE TABLE example (
    id UUID PRIMARY KEY,
    field_1 TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### API

[API endpoints, request/response formats, or interface contracts.]

```
POST /api/v1/resource
Request: { "field": "value" }
Response: { "id": "123", "status": "created" }
```

## Alternatives Considered

### Alternative 1: [Name]

[Description of the alternative approach.]

- **Pros:** [Benefits of this approach]
- **Cons:** [Drawbacks of this approach]
- **Why not chosen:** [Clear reasoning]

### Alternative 2: [Name]

[Description of the alternative approach.]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Why not chosen:** [Reasoning]

### Alternative 3: Do Nothing

[What happens if we don't build this?]

- **Pros:** No development effort
- **Cons:** [Consequences of inaction]
- **Why not chosen:** [Why action is needed]

## Cross-cutting Concerns

### Security

[Authentication, authorization, data protection, threat considerations.]

### Privacy

[PII handling, data retention, compliance requirements.]

### Scalability

[How the design handles growth. Expected load, bottlenecks, scaling strategy.]

### Reliability

[Failure modes, recovery strategies, SLAs.]

### Monitoring and Observability

[Metrics, logging, alerting, dashboards.]

## Implementation Plan

### Rollout Strategy

1. [Phase 1: Description and scope]
2. [Phase 2: Description and scope]
3. [Phase 3: Full rollout]

### Milestones

| Milestone | Description | Target |
|-----------|-------------|--------|
| Design approval | This document approved | [Date] |
| Implementation complete | Code merged | [Date] |
| Rollout complete | Live in production | [Date] |

### Rollback Plan

[How to revert if something goes wrong.]

## Open Questions

1. [Question that needs resolution before/during implementation]
2. [Another open question]
3. [Question with owner and deadline if assigned]

## References

- [Link to related design doc]
- [Link to ADR or spec]
- [External resource]

---

*Design Doc Template | Google Style*
```

---

## Uber RFC Template

```markdown
# RFC: [Title]

**RFC Number:** RFC-YYYY-NNN
**Author:** [Name] (@handle)
**Status:** Draft | Review | Approved | Rejected | Superseded
**Created:** YYYY-MM-DD
**Last Updated:** YYYY-MM-DD

---

## Approvers

| Approver | Team | Status | Date |
|----------|------|--------|------|
| [Name] | [Team] | Pending | |
| [Name] | [Team] | Pending | |
| [Name] | [Team] | Pending | |

---

## Summary

[One paragraph summary of the proposal. What are you proposing and why?]

## Motivation

[Why are we doing this? What problem does it solve? What's the current pain point?]

### Current State

[Describe how things work today and why that's insufficient.]

### Desired State

[Describe the end state after this RFC is implemented.]

## Proposal

### Overview

[High-level description of the proposed solution. Include architecture diagram if helpful.]

### Detailed Design

[Technical details of the implementation. Be specific enough that another engineer could implement this.]

#### [Subsection 1]

[Details...]

#### [Subsection 2]

[Details...]

### Service SLAs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.9% | [How measured] |
| P99 Latency | <100ms | [How measured] |
| Throughput | N RPS | [How measured] |
| Error Rate | <0.1% | [How measured] |

### Dependencies

| Dependency | Type | Status |
|------------|------|--------|
| [Service/Library] | Required | [Available/Planned] |
| [Service/Library] | Required | [Available/Planned] |

### API Changes

[New or modified APIs. Include request/response schemas.]

```yaml
# OpenAPI-style definition
POST /v1/endpoint:
  request:
    field: string
  response:
    id: string
    status: string
```

### Data Model Changes

[New or modified data models. Include migration strategy if applicable.]

### Configuration Changes

[New configuration options, feature flags, environment variables.]

## Rollout Plan

### Phases

| Phase | Scope | Duration | Success Criteria |
|-------|-------|----------|------------------|
| 1 | [Scope] | [Duration] | [Criteria] |
| 2 | [Scope] | [Duration] | [Criteria] |
| 3 | Full | [Duration] | [Criteria] |

### Rollback Plan

[How to revert changes at each phase. What triggers a rollback?]

### Migration Strategy

[If applicable: how existing data/systems are migrated.]

## Alternatives

### Alternative 1: [Name]

[Description]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Why rejected:** [Reasoning]

### Alternative 2: [Name]

[Description]

- **Pros:** [Benefits]
- **Cons:** [Drawbacks]
- **Why rejected:** [Reasoning]

## Security Considerations

[Security implications, threat model, mitigations.]

- Authentication: [How handled]
- Authorization: [How handled]
- Data protection: [Encryption, etc.]
- Audit: [Logging, compliance]

## Operational Considerations

### Deployment

[How will this be deployed? CI/CD changes needed?]

### Monitoring

[New metrics, dashboards, alerts needed.]

### On-call

[Impact on on-call. New runbooks needed?]

### Cost

[Infrastructure cost implications. New resources needed?]

## Timeline

| Milestone | Target Date |
|-----------|-------------|
| RFC Approval | YYYY-MM-DD |
| Phase 1 Complete | YYYY-MM-DD |
| Phase 2 Complete | YYYY-MM-DD |
| Full Rollout | YYYY-MM-DD |

## Open Questions

1. [Question 1] - Owner: @person, Due: YYYY-MM-DD
2. [Question 2] - Owner: @person, Due: YYYY-MM-DD

## References

- [Related RFC]
- [External documentation]
- [ADR]

---

*RFC Template | Uber Style*
```

---

## Amazon 6-Pager Template

```markdown
# [Title]

**Author:** [Team/Name]
**Date:** [Month Year]
**Audience:** [Leadership/Team/Stakeholders]

---

## Introduction

[2-3 paragraphs introducing the topic. What is this document about? Why should the reader care? Set the stage for the narrative that follows. Write in complete sentences, not bullet points.]

## Goals

[Describe the specific, measurable goals in narrative form. What does success look like? How will we know when we've achieved it? Goals should be ambitious but achievable, and directly tied to customer or business outcomes.]

[Second paragraph elaborating on how these goals align with broader company strategy or customer needs.]

## Tenets

[List 3-5 guiding principles that will inform decision-making throughout this initiative. These are the non-negotiable beliefs that will guide the team when facing difficult trade-offs.]

[First tenet: Explanation of why this principle matters and how it will guide decisions.]

[Second tenet: Explanation of its importance and application.]

[Third tenet: Explanation and examples of application.]

## State of the Business

[Comprehensive analysis of the current state. Use data to paint a picture of where things stand today. What are the key metrics? What trends are we seeing? Where are the pain points?]

[Second paragraph diving deeper into specific areas of concern or opportunity. Include relevant data points, but put detailed charts and graphs in the appendix.]

[Third paragraph on competitive landscape or industry context if relevant.]

[Fourth paragraph on customer feedback or research that informs this analysis.]

## Lessons Learned

[What have we tried before? What did we learn from those attempts? This section demonstrates that the proposal isn't naive but builds on past experience.]

[Specific example of a past initiative, what happened, and what we learned.]

[Another example with concrete outcomes and takeaways.]

[Synthesis of lessons into principles that inform the current proposal.]

## Strategic Priorities

[Outline the key initiatives or priorities that will achieve the goals. Write in order of priority, with the most important first.]

[Priority 1: Detailed description of the first strategic priority. What will we do? Why is this the right approach? What are the expected outcomes? What resources are needed?]

[Priority 2: Second strategic initiative with similar level of detail. Include how this builds on or complements Priority 1.]

[Priority 3: Third initiative. Continue the narrative flow, showing how all priorities work together as a coherent strategy.]

[Priority 4 (if applicable): Additional initiatives with proportionally less detail for lower priorities.]

[Closing paragraph on how these priorities work together and what success looks like when fully implemented.]

---

## Appendix A: Supporting Data

[Charts, graphs, detailed metrics that support the narrative above.]

## Appendix B: Financial Analysis

[Cost-benefit analysis, projections, resource requirements.]

## Appendix C: Risk Analysis

[Identified risks and mitigation strategies.]

## Appendix D: Timeline

[Detailed timeline and milestones.]

---

*6-Pager Template | Amazon Style*

**Formatting Rules:**
- Maximum 6 pages of narrative (appendices unlimited)
- No bullet points in main document
- Full sentences and paragraphs only
- Every word must add value
- Write for a reader unfamiliar with the topic
```

---

## Amazon PR-FAQ Template

```markdown
# [Product Name]

## Press Release

**[CITY, DATE]** - [Company] today announced [Product Name], a [brief description] that enables [target customers] to [key benefit]. [Product Name] is available starting [date/now] at [price/website].

[Customer pain point paragraph]: "[Quote from a customer persona about the problem they face]," said [fictional customer name, title at fictional company]. "[Describe the struggle and frustration in customer's voice]."

[Solution paragraph]: [Product Name] solves this by [description of how it works]. Key features include [feature 1], [feature 2], and [feature 3]. Customers can [primary action] in [time/ease metric], compared to [previous solution].

"[Quote from company executive about why this matters]," said [Exec Name, Title]. "[Vision statement about how this helps customers and fits company strategy]."

[Differentiator paragraph]: Unlike [existing solutions], [Product Name] [unique value proposition]. [Specific example of the difference in practice].

[Availability paragraph]: [Product Name] is available [now/date] in [regions/platforms]. Pricing starts at [price] for [tier]. Customers can get started at [website].

---

## Frequently Asked Questions

### Customer FAQ

**Q: What is [Product Name]?**
A: [Clear, simple explanation of the product in 2-3 sentences.]

**Q: Who is [Product Name] for?**
A: [Product Name] is designed for [target customer segments]. It's especially useful for [specific use cases].

**Q: How much does it cost?**
A: [Pricing tiers and what's included in each.]

**Q: How do I get started?**
A: [Step-by-step getting started process.]

**Q: How is this different from [competitor/existing solution]?**
A: [Honest comparison highlighting genuine differentiators.]

**Q: What if I need help?**
A: [Support options and resources available.]

### Internal FAQ

**Q: Why are we building this?**
A: [Strategic rationale. What customer need does this address? How does it fit our strategy?]

**Q: Why now?**
A: [Market timing, competitive pressure, capability readiness.]

**Q: What's the business model?**
A: [Revenue model, unit economics, growth expectations.]

**Q: What are the key risks?**
A: [Top 3-5 risks and how we're mitigating them.]

**Q: What does success look like?**
A: [Success metrics with specific targets and timeframes.]

**Q: What's the timeline?**
A: [Key milestones and launch date.]

**Q: What resources do we need?**
A: [Team size, budget, dependencies.]

**Q: What are we NOT doing?**
A: [Explicit non-goals and why they're out of scope.]

---

*PR-FAQ Template | Amazon Working Backwards*
```

---

## Spotify ADR Template

```markdown
# ADR-[YYYY]-[NNN]: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Deciders:** [List of people who made or need to make this decision]
**Consulted:** [People whose opinions were sought]
**Informed:** [People who need to know about this decision]

---

## Context

[Describe the context and problem statement. What forces are at play? What constraints exist? Why is a decision needed now?]

[Include relevant technical context, business drivers, and any time pressure.]

## Decision

[Clearly state the decision. What did we decide to do?]

**We will [action].**

[Additional details about what this decision means in practice.]

## Consequences

### Positive

- [Positive consequence 1]
- [Positive consequence 2]
- [Positive consequence 3]

### Negative

- [Negative consequence 1 and any mitigation]
- [Negative consequence 2 and any mitigation]

### Neutral

- [Consequence that is neither clearly positive nor negative]

## Alternatives Considered

### [Alternative 1]

[Brief description]

- Rejected because: [Reason]

### [Alternative 2]

[Brief description]

- Rejected because: [Reason]

## Related Decisions

- [ADR-XXX: Related decision]
- [RFC-XXX: Related RFC that led to this ADR]

## Notes

[Any additional context, links to discussions, or implementation notes.]

---

*ADR Template | Spotify Style*
```

---

## Mini RFC Template

```markdown
# Mini RFC: [Title]

**Author:** @[handle]
**Status:** Open | Accepted | Rejected
**Deadline:** YYYY-MM-DD
**Scope:** Team-only | Cross-team

---

## Problem Statement

[2-3 sentences describing the problem. What's broken? What's the pain?]

## Proposed Solution

[Brief description of your proposed solution. 1 paragraph.]

## Implementation Details

[Key technical details. What will you actually build/change?]

- [Detail 1]
- [Detail 2]
- [Detail 3]

## Success Metrics

[How will you know this worked?]

- [Metric 1]
- [Metric 2]

## Questions/Concerns

[Open questions for reviewers]

1. [Question 1]
2. [Question 2]

---

**Review Process:**
- Open for comments until deadline
- If no veto by deadline, author proceeds
- Major concerns require author response before proceeding

---

*Mini RFC Template | Lightweight Decisions*
```

---

## HashiCorp RFC Template

```markdown
# RFC: [Title]

**Status:** EARLY IDEA | OPEN FOR DETAILED REVIEW | BEING IMPLEMENTED | COMPLETED | ON HOLD | SUPERSEDED
**Author:** [Name]
**Created:** YYYY-MM-DD
**Last Edited:** YYYY-MM-DD

---

## Overview

[One or two paragraphs explaining the goal of this RFC. Anyone opening this document should understand the RFC's intent from reading this section alone. Don't dive into "why", "why now", or "how" yet - just clearly state what you're proposing.]

## Background

[At least two paragraphs, up to one page. The guiding goal: as a newcomer to this project, can I read this section and follow any links to get the full context of why this change is necessary?]

[Include relevant history, current state, and what's driving this change.]

[Link to related documents, previous attempts, or external resources.]

## Proposal

### High-Level Design

[Overview of the proposed solution. Architecture diagrams welcome.]

### Detailed Design

[Implementation specifics. Enough detail that someone could implement this.]

#### [Subsection as needed]

[Details...]

### Backwards Compatibility

[How are existing users or systems affected? Migration path?]

## Alternatives

### Alternative 1: [Name]

[Description, why it was considered, why it was rejected]

### Alternative 2: [Name]

[Description, why it was considered, why it was rejected]

## Trade-offs

[What are the disadvantages of your design? What trade-offs are you making because you think the downsides are worth the benefits?]

[Be honest. This section builds trust with reviewers by showing you've thought critically about your own proposal.]

## Security Considerations

[Security implications of this change. What new attack surfaces? What mitigations?]

## Open Questions

1. [Question needing resolution]
2. [Question needing resolution]

## References

- [Related doc]
- [External resource]

---

*RFC Template | HashiCorp Style*
```

---

## Lightweight Design Doc Template

```markdown
# Design: [Feature Name]

**Author:** [Name]
**Date:** YYYY-MM-DD
**Status:** Draft | Approved | Implemented

---

## Summary

[One paragraph: What are we building and why?]

## Design

[Description of the solution. Include diagram if helpful.]

### Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision 1] | [Choice] | [Why] |
| [Decision 2] | [Choice] | [Why] |

### API/Interface

[Key interfaces or APIs being created/modified]

## Risks

| Risk | Mitigation |
|------|------------|
| [Risk 1] | [Mitigation] |
| [Risk 2] | [Mitigation] |

## Open Questions

- [Question 1]
- [Question 2]

---

*Lightweight Design Doc | For small features*
```

---

## Template Selection Guide

| Situation | Recommended Template |
|-----------|---------------------|
| New microservice | Uber RFC |
| Architecture change | Uber RFC + Spotify ADR |
| New product initiative | Amazon 6-Pager |
| New product feature | Amazon PR-FAQ |
| Internal tool/library | Google Design Doc |
| Quick team decision | Mini RFC |
| Open source contribution | HashiCorp RFC |
| Small feature (<1 week) | Lightweight Design Doc |
| Recording a past decision | Spotify ADR |

---

*Templates | Design Docs at Big Tech | v2.0*
