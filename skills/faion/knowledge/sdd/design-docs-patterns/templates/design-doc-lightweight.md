# Design Doc: [Feature Name]

**Author:** [Name]
**Reviewers:** [Names] — deadline: [YYYY-MM-DD]
**Status:** Draft | In Review | Approved | Implemented
**Last Updated:** YYYY-MM-DD
**Spec Reference:** [Link to spec.md or ticket]

---

## Overview

[1-2 paragraphs describing what this doc covers and why it exists. Must be readable by someone unfamiliar with the project. State the problem clearly before the solution.]

---

## Context and Background

[What led to this design being needed? What is the current state of the system? What constraints exist (technical, timeline, budget, org)?]

---

## Goals

- [Goal 1 — specific and measurable]
- [Goal 2 — specific and measurable]
- [Goal 3 — specific and measurable]

## Non-Goals

- [Explicit scope boundary 1 — must be something readers might assume is in scope]
- [Explicit scope boundary 2]
- [Note: "do not rewrite everything" is not a non-goal — be specific]

---

## Design

[Key technical decisions, component interactions, data flow. Include a simple diagram if it clarifies the design. For lightweight docs, 1-2 paragraphs per major component is sufficient.]

```
[Optional: simple ASCII or text diagram showing component relationships]
ComponentA → ComponentB → Database
                ↓
          ExternalService
```

### Data Model

[Key entities and their relationships. Schema details if relevant.]

### API Contracts

[New or changed endpoints. Request/response shape if this is an API-facing change.]

---

## Alternatives Considered

| Option | Pros | Cons | Chosen? |
|--------|------|------|---------|
| [Proposed approach] | [Honest pros] | [Honest cons] | Yes |
| [Alternative 1] | [Pros] | [Cons — why not chosen] | No |
| [Alternative 2 / do nothing] | [Pros] | [Cons — why status quo fails] | No |

[Add 1-2 sentences per alternative explaining the "why not chosen" rationale for future reference.]

---

## Cross-Cutting Concerns

### Security
[Authentication, authorization, input validation, encryption. Be specific to this feature.]

### Scalability
[Expected load, scaling approach, known bottlenecks.]

### Reliability
[Failure modes, graceful degradation, recovery. What happens when a dependency is down?]

### Observability
[Key metrics to add, logging strategy, alerting thresholds.]

---

## Open Questions

- [ ] [Unresolved question 1] — Owner: [Name]
- [ ] [Unresolved question 2] — Owner: [Name]

---

## References

- [Link to spec.md]
- [Related design docs or ADRs]
- [Relevant external documentation]
