# Use Case Diagram: [System Name]

## System Boundary

**System:** [Name of system being analyzed]

## Actors

| Actor | Type | Description |
|-------|------|-------------|
| [Actor 1] | Primary | [Goal they achieve] |
| [Actor 2] | Secondary | [Role they play] |
| [External System] | System | [Data or service provided] |

## Use Cases by Actor

### [Actor 1]
- UC-001: [Use Case Name]
- UC-002: [Use Case Name]

### [Actor 2]
- UC-003: [Use Case Name]

### Shared
- UC-004: [Use Case Name] — [Actor 1] and [Actor 2]

## Relationships

| Relationship | Type | Rationale |
|-------------|------|-----------|
| UC-001 includes UC-010 | Include | [UC-010 steps appear in 3+ use cases] |
| UC-002 extends UC-001 | Extend | [Optional behavior at extension point X] |
| UC-005 generalizes UC-006 | Generalize | [UC-005 IS-A specialized version of UC-006] |

## Notes

- Relationships declared only when they de-duplicate 10+ steps
- Each use case owned by exactly one primary actor
