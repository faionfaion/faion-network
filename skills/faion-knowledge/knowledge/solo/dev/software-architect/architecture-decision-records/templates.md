# ADR Templates

Copy-paste templates for Architecture Decision Records.

## Template 1: Nygard Format (Minimal)

The original, lightweight ADR format by Michael Nygard.

```markdown
# ADR-NNN: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded by ADR-XXX]
**Date:** YYYY-MM-DD
**Deciders:** [names]

## Context

[What is the issue that we're seeing that is motivating this decision?
Describe the context and problem in 1-2 paragraphs.]

## Decision

[What is the change that we're proposing and/or doing?
State the decision clearly in 1-2 paragraphs.]

## Consequences

[What becomes easier or more difficult to do because of this change?
List both positive and negative consequences.]

### Positive
- [Consequence 1]
- [Consequence 2]

### Negative
- [Consequence 1]
- [Consequence 2]
```

## Template 2: MADR 4.0 (Full)

Markdown Any Decision Records - comprehensive format with options analysis.

```markdown
# ADR-NNN: [Title]

## Metadata

- **Status:** [Proposed | Accepted | Rejected | Deprecated | Superseded]
- **Date:** YYYY-MM-DD
- **Deciders:** [list everyone involved in the decision]
- **Technical Story:** [ticket/issue URL]

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using
two to three sentences or in the form of an illustrative story. You may
want to articulate the problem in form of a question.]

## Decision Drivers

- [Driver 1, e.g., a force, facing concern, ...]
- [Driver 2, e.g., a force, facing concern, ...]
- [Driver 3, ...]

## Considered Options

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome

Chosen option: "[Option X]", because [justification. e.g., only option
which meets k.o. criterion decision driver | which resolves force
force | ... | comes out best (see below)].

### Positive Consequences

- [e.g., improvement of quality attribute satisfaction, follow-up
  decisions required, ...]

### Negative Consequences

- [e.g., compromising quality attribute, follow-up decisions required, ...]

### Neutral Consequences

- [e.g., needs to be monitored, requires follow-up ADR, ...]

## Pros and Cons of Options

### [Option 1]

[example | description | pointer to more information | ...]

- Good, because [argument a]
- Good, because [argument b]
- Neutral, because [argument c]
- Bad, because [argument d]

### [Option 2]

[example | description | pointer to more information | ...]

- Good, because [argument a]
- Good, because [argument b]
- Neutral, because [argument c]
- Bad, because [argument d]

### [Option 3]

[example | description | pointer to more information | ...]

- Good, because [argument a]
- Good, because [argument b]
- Neutral, because [argument c]
- Bad, because [argument d]

## More Information

[You might want to provide additional evidence/confidence for the
decision outcome here and/or document the team agreement on the
decision and/or define when/how this decision should be realized and
if/when it should be re-visited. Links to other decisions and resources
might appear here as well.]

## Links

- [Link to related ADR]
- [Link to external documentation]
- [Link to architectural diagram]
```

## Template 3: MADR Minimal

Stripped-down MADR for simpler decisions.

```markdown
# ADR-NNN: [Title]

**Status:** [Proposed | Accepted | Rejected | Deprecated | Superseded]
**Date:** YYYY-MM-DD

## Context and Problem Statement

[Describe the context and problem statement in 2-3 sentences.]

## Considered Options

1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision Outcome

Chosen option: "[Option X]", because [justification].

### Consequences

- Good, because [positive consequence]
- Bad, because [negative consequence]
```

## Template 4: Y-Statement

Ultra-concise single-sentence format.

```markdown
# ADR-NNN: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Date:** YYYY-MM-DD

## Decision

In the context of **[use case / component]**,
facing **[concern / non-functional requirement]**,
we decided for **[option]**
and neglected **[other options]**,
to achieve **[system qualities / desired consequences]**,
accepting that **[drawbacks / undesired consequences]**.
```

### Y-Statement Expanded Format

For more complex decisions:

```markdown
# ADR-NNN: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Date:** YYYY-MM-DD

## Context

[Functional requirement, use case, or component]

## Facing

[Non-functional requirement, quality attribute, or concern]

## Decision

[The chosen option/approach]

## Neglected Alternatives

- [Alternative 1 and why rejected]
- [Alternative 2 and why rejected]

## Benefits

- [Benefit 1]
- [Benefit 2]

## Drawbacks

- [Drawback 1]
- [Drawback 2]
```

## Template 5: Tyree & Akerman (Enterprise)

Detailed format for formal governance environments.

```markdown
# ADR-NNN: [Title]

## Metadata

| Attribute | Value |
|-----------|-------|
| **Status** | [Proposed / Accepted / Rejected / Deprecated / Superseded] |
| **Date** | YYYY-MM-DD |
| **Decision Maker(s)** | [Names and roles] |
| **Consulted** | [Names and roles] |
| **Informed** | [Names and roles] |
| **Issue** | [Link to issue/ticket] |

## Issue

[Describe the architectural design issue you're addressing. Leave no
questions about why you're addressing this issue now.]

## Decision

[Clearly state the architecture decision in full sentences, with active
voice. "We will ..."]

## Status

[Proposed, Accepted, Rejected, Deprecated, or Superseded. Include date
of each status change.]

## Group

[Classify the decision: infrastructure, technology, cross-cutting,
security, etc.]

## Assumptions

[List underlying assumptions in the environment in which you're making
the decision. Include cost, schedule, technology, and anything that
might affect the decision outcome.]

## Constraints

[List any constraints on the environment that affect the decision.
These may be regulatory, legal, organizational, technical, etc.]

## Positions

[List the positions (viable options or alternatives) considered. These
often require long explanations, sometimes even models and diagrams.]

### Position 1: [Name]
[Description]

### Position 2: [Name]
[Description]

### Position 3: [Name]
[Description]

## Argument

[Outline why the position was selected. This is probably the most
important part of the document. Show evidence supporting the decision.]

## Implications

[What are the implications of this decision? List both positive and
negative implications.]

## Related Decisions

[List the related decisions that may influence, or be influenced by,
this decision.]

## Related Requirements

[List requirements this decision addresses]

## Related Artifacts

[List related architecture and design documents.]

## Related Principles

[List related architecture principles that apply to this decision.]

## Notes

[Any additional notes, meeting minutes, or relevant information.]
```

## Template 6: Log4brains Default

Template used by Log4brains tool (based on MADR).

```markdown
# [Title]

- Status: [proposed | rejected | accepted | deprecated | superseded by [ADR-NNN](NNN-example.md)]
- Deciders: [list everyone involved in the decision]
- Date: YYYY-MM-DD
- Technical Story: [description | ticket/issue URL]

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using
two to three sentences or in the form of an illustrative story.]

## Decision Drivers

- [driver 1, e.g., a force, facing concern, ...]
- [driver 2, e.g., a force, facing concern, ...]
- ...

## Considered Options

- [option 1]
- [option 2]
- [option 3]
- ...

## Decision Outcome

Chosen option: "[option 1]", because [justification. e.g., only option
which meets k.o. criterion decision driver | comes out best (see below)].

### Positive Consequences

- [e.g., improvement of quality attribute satisfaction, ...]
- ...

### Negative Consequences

- [e.g., compromising quality attribute, follow-up decisions required, ...]
- ...

## Pros and Cons of the Options

### [option 1]

[example | description | pointer to more information | ...]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]
- ...

### [option 2]

[example | description | pointer to more information | ...]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]
- ...

### [option 3]

[example | description | pointer to more information | ...]

- Good, because [argument a]
- Good, because [argument b]
- Bad, because [argument c]
- ...

## Links

- [Link type] [Link to ADR]
- ...
```

## Template 7: Superseding ADR

Template for when replacing a previous decision.

```markdown
# ADR-NNN: [New Decision Title]

**Status:** Accepted
**Date:** YYYY-MM-DD
**Deciders:** [names]
**Supersedes:** [ADR-XXX: Previous Decision Title](XXXX-previous-decision.md)

## Context

[ADR-XXX](XXXX-previous-decision.md) was accepted on [date] with the
following decision: [brief summary of original decision].

Since then, the following changes have occurred:
- [Change 1 that invalidates or modifies original decision]
- [Change 2]
- [Lessons learned from implementing original decision]

## Decision

We will now [new decision], replacing the approach defined in ADR-XXX.

## Consequences

### Positive
- [New benefit 1]
- [New benefit 2]

### Negative
- [Migration effort required]
- [New drawback 1]

## Migration Plan

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Links

- **Supersedes:** [ADR-XXX: Previous Decision](XXXX-previous-decision.md)
- Migration tracking: [ticket URL]
```

## Template 8: Rejected ADR

Template for documenting a rejected proposal.

```markdown
# ADR-NNN: [Proposed Decision Title]

**Status:** Rejected
**Date:** YYYY-MM-DD
**Deciders:** [names]

## Context

[Describe the problem that prompted this proposal]

## Proposed Decision

[Describe what was proposed]

## Rationale for Rejection

[Explain why the proposal was rejected]

1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

## Alternative Approach

[If applicable, point to the accepted alternative]

See [ADR-XXX: Alternative Approach](XXXX-alternative.md) for the
accepted solution.

## Conditions for Reconsideration

[Under what circumstances should this proposal be revisited?]

- [Condition 1]
- [Condition 2]
```

## Template 9: ADR Index (README)

Template for the ADR directory index.

```markdown
# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for
[Project Name].

## What is an ADR?

An ADR is a document that captures an important architectural decision
made along with its context and consequences.

## ADR Index

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-001](0001-title.md) | [Title] | Accepted | YYYY-MM-DD |
| [ADR-002](0002-title.md) | [Title] | Accepted | YYYY-MM-DD |
| [ADR-003](0003-title.md) | [Title] | Superseded | YYYY-MM-DD |
| [ADR-004](0004-title.md) | [Title] | Proposed | YYYY-MM-DD |

## By Category

### Infrastructure
- [ADR-001](0001-title.md) - [Title]

### Database
- [ADR-002](0002-title.md) - [Title]

### Security
- [ADR-003](0003-title.md) - [Title]

## Creating a New ADR

1. Copy the appropriate template from `templates/`
2. Create file: `NNNN-title-with-dashes.md`
3. Fill in all sections
4. Submit PR for review
5. Update this index after merge

## Template

Use [ADR template](templates/adr-template.md) for new decisions.
```

## Template 10: Decision Matrix (Supporting Document)

For complex multi-criteria decisions.

```markdown
# Decision Matrix: [Topic]

Supporting document for [ADR-NNN](NNNN-title.md)

## Evaluation Criteria

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Performance | 25% | Response time, throughput |
| Scalability | 20% | Ability to handle growth |
| Cost | 20% | Implementation + operation |
| Team Skills | 15% | Existing expertise |
| Ecosystem | 10% | Community, tooling |
| Security | 10% | Built-in security features |

## Scoring

Scale: 1 (Poor) - 5 (Excellent)

| Option | Perf | Scale | Cost | Skills | Eco | Sec | Weighted |
|--------|------|-------|------|--------|-----|-----|----------|
| Option A | 4 | 5 | 3 | 4 | 5 | 4 | **4.05** |
| Option B | 5 | 3 | 4 | 2 | 3 | 4 | 3.55 |
| Option C | 3 | 4 | 5 | 5 | 2 | 3 | 3.70 |

## Calculation

```
Option A: (4*0.25) + (5*0.20) + (3*0.20) + (4*0.15) + (5*0.10) + (4*0.10)
        = 1.00 + 1.00 + 0.60 + 0.60 + 0.50 + 0.40 = 4.10
```

## Recommendation

Based on the weighted scoring, **Option A** is recommended with a
score of 4.05, primarily due to strong scalability and ecosystem scores.

## Sensitivity Analysis

If Team Skills weight increased to 25% (reducing Performance to 15%):
- Option A: 3.95
- Option C: 4.00 (would become recommended)

This suggests the decision is sensitive to team skill considerations.
```

## Naming Convention Reference

```
docs/adr/
├── 0000-use-markdown-architectural-decision-records.md
├── 0001-use-postgresql-for-database.md
├── 0002-adopt-microservices-architecture.md
├── 0003-implement-jwt-authentication.md
├── 0004-use-kubernetes-for-orchestration.md
├── 0005-migrate-to-graphql.md
├── README.md
└── templates/
    ├── adr-template-nygard.md
    ├── adr-template-madr.md
    └── adr-template-y-statement.md
```

## Quick Reference: Choosing a Template

| Situation | Recommended Template |
|-----------|---------------------|
| Simple technology choice | Nygard (Template 1) |
| Complex decision with many options | MADR Full (Template 2) |
| Quick decision documentation | MADR Minimal (Template 3) |
| Code annotation / inline docs | Y-Statement (Template 4) |
| Enterprise / formal governance | Tyree & Akerman (Template 5) |
| Using Log4brains tool | Log4brains Default (Template 6) |
| Replacing previous decision | Superseding ADR (Template 7) |
| Documenting rejected proposal | Rejected ADR (Template 8) |
