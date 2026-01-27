# ADR Templates

Copy-paste templates for Architecture Decision Records. Choose the format that best fits your needs.

## Quick Selection Guide

| Format | Best For | Sections | Effort |
|--------|----------|----------|--------|
| [Nygard (Minimal)](#nygard-format-minimal) | Quick decisions, small teams | 5 | Low |
| [Nygard (Extended)](#nygard-format-extended) | Standard decisions | 7 | Low-Medium |
| [MADR (Minimal)](#madr-format-minimal) | Focused decisions with alternatives | 6 | Medium |
| [MADR (Full)](#madr-format-full) | Comprehensive decisions | 10+ | Medium-High |
| [Y-Statement](#y-statement-format) | One-liner summary | 1 | Very Low |
| [Y-Statement (Extended)](#y-statement-extended) | Summary + context | 4 | Low |
| [Enterprise](#enterprise-format) | Compliance, governance | 12+ | High |

---

## Nygard Format (Minimal)

The original ADR format by [Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions). Simple and effective.

```markdown
# ADR-NNNN: [Short Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date:** YYYY-MM-DD

## Context

[Describe the forces at play: technical, business, political, social.
Use value-neutral language. State facts, not opinions.]

## Decision

[State the decision in full sentences with active voice.
"We will..." or "We have decided to..."]

## Consequences

[Describe the resulting context after applying the decision.
Include both positive and negative consequences.]
```

---

## Nygard Format (Extended)

Enhanced version with alternatives and structured consequences.

```markdown
# ADR-NNNN: [Short Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date:** YYYY-MM-DD
**Deciders:** [List of people involved in the decision]

## Context

[What is the issue? What forces are at play?
Include technical, business, and team constraints.
Be objective - state facts, not opinions.]

## Decision

[What is the change being proposed/made?
State in full sentences with active voice: "We will..."]

## Alternatives Considered

### Alternative 1: [Name]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why rejected:** [reason]

### Alternative 2: [Name]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why rejected:** [reason]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Risk to mitigate]

### Neutral
- [Implication neither good nor bad]

## Related Decisions

- ADR-XXXX: [Related decision]
- ADR-YYYY: [Supersedes this if applicable]

## Notes

[Any additional context, meeting notes, or future considerations]
```

---

## MADR Format (Minimal)

[Markdown Any Decision Records](https://adr.github.io/madr/) - streamlined for decisions with clear alternatives.

```markdown
# [Short Title]

* Status: proposed | accepted | deprecated | superseded by [ADR-XXXX]
* Deciders: [list of people involved]
* Date: YYYY-MM-DD

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two
to three sentences or in the form of an illustrative story. You may want
to articulate the problem in form of a question.]

## Considered Options

* [Option 1]
* [Option 2]
* [Option 3]

## Decision Outcome

Chosen option: "[Option X]", because [justification].

### Consequences

* Good, because [positive consequence]
* Bad, because [negative consequence]
```

---

## MADR Format (Full)

Complete MADR 4.0 template with all optional sections.

```markdown
# [Short Title]

* Status: proposed | accepted | deprecated | superseded by [ADR-XXXX]
* Deciders: [list everyone involved in the decision]
* Date: YYYY-MM-DD
* Technical Story: [ticket/issue number if applicable]

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two
to three sentences or in the form of an illustrative story. You may want
to articulate the problem in form of a question.]

## Decision Drivers

* [Driver 1, e.g., a force, facing concern, ...]
* [Driver 2, e.g., a force, facing concern, ...]
* ...

## Considered Options

* [Option 1]
* [Option 2]
* [Option 3]
* ...

## Decision Outcome

Chosen option: "[Option X]", because [justification. e.g., only option
which meets k.o. criterion decision driver | which resolves force force |
... | comes out best (see below)].

### Consequences

* Good, because [positive consequence, e.g., improvement of one or more
  desired qualities, ...]
* Bad, because [negative consequence, e.g., compromising one or more
  desired qualities, ...]
* ...

### Confirmation

[Describe how the implementation of/compliance with the ADR is confirmed.
E.g., by a review or an ArchUnit test. Although we classify this as
optional, it is recommended to include this section.]

## Pros and Cons of the Options

### [Option 1]

[Example | description | pointer to more information | ...]

* Good, because [argument a]
* Good, because [argument b]
* Neutral, because [argument c]
* Bad, because [argument d]
* ...

### [Option 2]

[Example | description | pointer to more information | ...]

* Good, because [argument a]
* Good, because [argument b]
* Neutral, because [argument c]
* Bad, because [argument d]
* ...

### [Option 3]

[Example | description | pointer to more information | ...]

* Good, because [argument a]
* Good, because [argument b]
* Neutral, because [argument c]
* Bad, because [argument d]
* ...

## More Information

[You might want to provide additional evidence/confidence for the decision
outcome here and/or document the team agreement on the decision and/or
define when this decision should be revisited and/or how the decision is
validated. Links to other decisions and resources might appear here as well.]
```

---

## Y-Statement Format

Ultra-compact format by [Olaf Zimmermann](https://medium.com/olzzio/y-statements-10eb07b5a177). Captures everything in one structured sentence.

```markdown
# ADR-NNNN: [Short Title]

**Status:** Accepted
**Date:** YYYY-MM-DD

## Decision

In the context of [functional requirement or architecture component],
facing [non-functional requirement or quality attribute],
we decided for [option chosen]
and against [options rejected],
to achieve [quality attribute or benefit],
accepting that [tradeoff or downside].
```

### Y-Statement Examples

**Database Selection:**
```
In the context of the e-commerce platform's data layer,
facing the need for ACID-compliant transactions and complex queries,
we decided for PostgreSQL
and against MongoDB and MySQL,
to achieve data integrity for financial transactions and advanced JSON support,
accepting that horizontal scaling will require additional tooling (Citus/read replicas).
```

**API Design:**
```
In the context of the public developer API,
facing the need for broad ecosystem adoption and HTTP caching,
we decided for REST with OpenAPI specification
and against GraphQL and gRPC,
to achieve maximum third-party developer accessibility and CDN cacheability,
accepting that some clients will experience over-fetching for complex data needs.
```

**Frontend Framework:**
```
In the context of the customer dashboard frontend,
facing the need for SEO optimization and fast initial page loads,
we decided for Next.js with React Server Components
and against Vite SPA and Create React App,
to achieve better Core Web Vitals scores and search engine indexing,
accepting that the team needs to learn Server Components patterns.
```

---

## Y-Statement Extended

Y-statement with supporting context and consequences.

```markdown
# ADR-NNNN: [Short Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date:** YYYY-MM-DD
**Deciders:** [Names]

## Y-Statement

In the context of [functional requirement or architecture component],
facing [non-functional requirement or quality attribute],
we decided for [option chosen]
and against [options rejected],
to achieve [quality attribute or benefit],
accepting that [tradeoff or downside].

## Extended Context

[Additional background, constraints, and forces not captured in Y-statement]

## Alternatives Summary

| Option | Why Rejected |
|--------|--------------|
| [Option A] | [Brief reason] |
| [Option B] | [Brief reason] |

## Detailed Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Tradeoff 1]
- [Risk 1]

## Related ADRs

- [ADR-XXXX: Related decision]
```

---

## Enterprise Format

Comprehensive template for compliance-heavy environments, governance requirements, or large organizations.

```markdown
# ADR-NNNN: [Full Descriptive Title]

## Metadata

| Field | Value |
|-------|-------|
| **Status** | Draft | Proposed | Accepted | Rejected | Deprecated | Superseded |
| **Date Created** | YYYY-MM-DD |
| **Date Decided** | YYYY-MM-DD |
| **Date Last Updated** | YYYY-MM-DD |
| **Deciders** | [Names and roles] |
| **Consulted** | [Stakeholders consulted] |
| **Informed** | [Stakeholders to be informed] |
| **Technical Story** | [Ticket/Epic reference] |
| **Supersedes** | ADR-XXXX (if applicable) |
| **Superseded by** | ADR-XXXX (if applicable) |

## Executive Summary

[2-3 sentence summary for executives who won't read the full ADR]

## Context

### Background
[Historical context and how we got here]

### Current State
[Description of the current situation]

### Problem Statement
[Clear articulation of the problem to be solved]

### Scope
[What is in scope and out of scope for this decision]

## Requirements

### Functional Requirements
- [FR-1: Description]
- [FR-2: Description]

### Non-Functional Requirements
- [NFR-1: Description (e.g., performance, security, scalability)]
- [NFR-2: Description]

### Constraints
- [Technical constraints]
- [Business constraints]
- [Regulatory constraints]
- [Timeline constraints]
- [Budget constraints]

## Decision Drivers

[Prioritized list of factors influencing the decision]

1. [Driver 1 - e.g., Security compliance] - Priority: High
2. [Driver 2 - e.g., Time to market] - Priority: High
3. [Driver 3 - e.g., Cost] - Priority: Medium
4. [Driver 4 - e.g., Team expertise] - Priority: Low

## Options Analysis

### Option 1: [Name]

**Description:** [Detailed description]

**Architecture Diagram:** [Link or embed diagram]

| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Security | X | [explanation] |
| Performance | X | [explanation] |
| Cost | X | [explanation] |
| Maintainability | X | [explanation] |
| Team Expertise | X | [explanation] |
| **Total Score** | XX | |

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Risks:**
- [Risk 1 with mitigation]
- [Risk 2 with mitigation]

**Estimated Cost:** [Initial + ongoing]

### Option 2: [Name]

[Same structure as Option 1]

### Option 3: [Name]

[Same structure as Option 1]

## Decision Matrix

| Criterion | Weight | Option 1 | Option 2 | Option 3 |
|-----------|--------|----------|----------|----------|
| Security | 5 | X | X | X |
| Performance | 4 | X | X | X |
| Cost | 3 | X | X | X |
| Maintainability | 3 | X | X | X |
| Time to Implement | 2 | X | X | X |
| **Weighted Score** | | XX | XX | XX |

## Decision

### Chosen Option
[Option X]

### Rationale
[Detailed justification for the decision]

### Decision Statement
We will [clear statement of what will be done].

## Consequences

### Positive Consequences
- [Positive 1]
- [Positive 2]

### Negative Consequences
- [Negative 1]
- [Negative 2]

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation strategy] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation strategy] |

## Implementation

### Implementation Plan
[High-level implementation approach]

### Migration Strategy
[If replacing existing solution]

### Rollback Plan
[How to revert if implementation fails]

### Success Metrics
- [Metric 1: Target value]
- [Metric 2: Target value]

### Validation Approach
[How we will confirm the decision was correct]

## Compliance and Security

### Regulatory Considerations
- [GDPR, SOC 2, HIPAA, etc.]

### Security Review
- [Security team sign-off]

### Data Classification Impact
- [Any changes to data handling]

## Related Decisions

| ADR | Relationship |
|-----|--------------|
| ADR-XXXX | [Relates to / Supersedes / Superseded by] |
| ADR-YYYY | [Relates to / Supersedes / Superseded by] |

## References

- [Link 1: Description]
- [Link 2: Description]
- [Meeting notes: Date]

## Approval

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Technical Lead | | | |
| Architect | | | |
| Product Owner | | | |
| Security | | | |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | [Name] | Initial version |
| 1.1 | YYYY-MM-DD | [Name] | [Changes made] |
```

---

## Specialized Templates

### Technology Selection ADR

```markdown
# ADR-NNNN: [Technology] Selection for [Purpose]

**Status:** Accepted
**Date:** YYYY-MM-DD
**Deciders:** [Names]

## Context

We need to select a [technology type] for [purpose].

### Requirements
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

### Evaluation Criteria
| Criterion | Weight | Description |
|-----------|--------|-------------|
| [Criterion 1] | High | [Why important] |
| [Criterion 2] | Medium | [Why important] |
| [Criterion 3] | Low | [Why important] |

## Options Evaluated

| Technology | [Criterion 1] | [Criterion 2] | [Criterion 3] | Score |
|------------|---------------|---------------|---------------|-------|
| [Option A] | [Rating] | [Rating] | [Rating] | X |
| [Option B] | [Rating] | [Rating] | [Rating] | X |
| [Option C] | [Rating] | [Rating] | [Rating] | X |

## Decision

We will use [Technology] because [primary reasons].

## Consequences

### Positive
- [Benefit 1]

### Negative
- [Tradeoff 1]

### Migration Path
[If replacing existing technology]
```

### API Change ADR

```markdown
# ADR-NNNN: [API Change Description]

**Status:** Accepted
**Date:** YYYY-MM-DD
**Deciders:** API Team
**Breaking Change:** Yes | No

## Context

[Why this API change is needed]

## Current API

```json
// Current request/response
```

## Proposed API

```json
// New request/response
```

## Decision

We will [change description].

## Migration Plan

### Deprecation Timeline
- [Date]: Deprecation notice
- [Date]: Migration guide published
- [Date]: Old API sunset

### Consumer Impact
| Consumer | Impact | Action Required |
|----------|--------|-----------------|
| [App A] | [Impact] | [Action] |
| [App B] | [Impact] | [Action] |

## Consequences

### For Consumers
- [Impact 1]

### For API Team
- [Impact 1]
```

---

## File Naming Conventions

```
docs/adr/
├── 0001-record-architecture-decisions.md
├── 0002-use-postgresql.md
├── 0003-rest-api-design.md
├── 0004-jwt-authentication.md
└── 0005-kubernetes-deployment.md
```

**Rules:**
- 4-digit sequential numbers (0001, 0002...)
- Lowercase with hyphens
- Short descriptive title
- Numbers never reused (even for rejected/superseded)

---

## Template Customization Tips

1. **Start minimal**: Begin with Nygard or MADR minimal
2. **Add sections as needed**: Don't force enterprise format on small teams
3. **Be consistent**: Pick one format and stick with it
4. **Document your template**: First ADR should be "Use ADRs with [format]"
5. **Adapt to context**: Compliance-heavy environments need more sections

## Related Files

- [README.md](README.md) - Overview and when to use ADRs
- [checklist.md](checklist.md) - Step-by-step writing guide
- [examples.md](examples.md) - Real-world ADR examples
- [llm-prompts.md](llm-prompts.md) - LLM prompts for ADR writing
