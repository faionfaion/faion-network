# Architecture Decision Records (ADR)

Research compilation on capturing and documenting architectural decisions using ADR format.

**Research Date:** 2026-01-19
**Sources:** AWS, Google Cloud, Microsoft Azure, ADR GitHub, UK GOV

---

## Metadata

| Field | Value |
|-------|-------|
| **ID** | architecture-decision-records |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #architecture, #adr, #decisions |
| **Domain Skill** | faion-sdd |
| **Year** | 2025-2026 |

---

## Problem

Architecture decisions are lost over time:
- New team members don't understand "why" of existing design
- Same discussions repeated without historical context
- Production incidents lack design context
- Decisions seem "puzzling" without knowing when/why they were made

---

## Framework

### What is an ADR?

A document capturing an important architectural decision along with its context and consequences.

### ADR Structure (Nygard Format)

```
+-------------------------------------+
| TITLE: Short decision description   |
+-------------------------------------+
| STATUS: Proposed|Accepted|Deprecated|
+-------------------------------------+
| CONTEXT: What is the situation?     |
+-------------------------------------+
| DECISION: What did we decide?       |
+-------------------------------------+
| CONSEQUENCES: What results from it? |
+-------------------------------------+
```

### ADR Lifecycle

```
PROPOSED -> ACCEPTED -> [DEPRECATED | SUPERSEDED]
    |          |              |
  Review    Active        Link to new ADR
  period    decision
```

### Status Types

| Status | Meaning |
|--------|---------|
| **Proposed** | Under discussion, gathering feedback |
| **Accepted** | Approved, active decision |
| **Deprecated** | No longer relevant, kept for history |
| **Superseded** | Replaced by newer ADR (link required) |

---

## Templates

### ADR Template (docs/adr/NNN-title.md)

```markdown
# ADR-NNN: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXX
**Date:** YYYY-MM-DD
**Deciders:** [List of people involved]

## Context

[What is the issue? What forces are at play?
Include technical, business, and team constraints.]

## Decision

[What is the change being proposed/made?
State in full sentences with active voice: "We will..."]

## Alternatives Considered

### Alternative 1: [Name]
- **Pros:** [benefits]
- **Cons:** [drawbacks]
- **Why rejected:** [reason]

### Alternative 2: [Name]
...

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

- ADR-NNN: [Related decision]
- ADR-NNN: [Supersedes this if applicable]

## Notes

[Any additional context, meeting notes, or future considerations]
```

### ADR Review Meeting Template

```markdown
# ADR Review: ADR-NNN

**Date:** YYYY-MM-DD
**Duration:** 30 min (10 min silent read, 20 min discussion)
**Attendees:** [Keep under 10 people]

## Reading Period (10 min)
- Read the ADR silently
- Add inline comments to specific sections

## Discussion Points
1. [Comment/question from review]
2. [Comment/question from review]

## Decision
- [ ] Approved as-is
- [ ] Approved with changes: [list changes]
- [ ] Needs revision: [list concerns]
- [ ] Rejected: [reason]

## Action Items
- [ ] [Action] - @owner - due date
```

---

## Best Practices

| Practice | Description |
|----------|-------------|
| **Co-locate with code** | Store in `docs/adr/` in same repo |
| **Sequential numbering** | Use NNN format (001, 002...) |
| **Immutable by default** | Prefer new ADR over editing existing |
| **Timestamp everything** | Include date and system version |
| **Keep pithy** | Focus on decision, not design guide |
| **Single decision focus** | One ADR = one decision |
| **Cross-functional review** | Involve affected teams (under 10 people) |
| **Silent reading** | Amazon-style: 10 min read, then discuss |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| ADR as design guide | Keep focused on decision, not implementation details |
| Not updating status | Mark superseded ADRs, link to replacement |
| Missing alternatives | Always document what you considered and rejected |
| No timestamps | Include date for historical context |
| Hidden in wiki | Store in version control with code |

---

## Sources

- [AWS Architecture Blog: ADR Best Practices](https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/)
- [Google Cloud: ADR Overview](https://cloud.google.com/architecture/architecture-decision-records)
- [Microsoft: Azure ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [ADR GitHub](https://adr.github.io/)
- [UK GOV: ADR Framework](https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework)

---

*Reference Document | Architecture Decision Records (ADR) | Version 1.0*
