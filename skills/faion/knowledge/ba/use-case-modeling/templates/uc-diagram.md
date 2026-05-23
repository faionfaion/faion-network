# Use Case Diagram: [System Name]

## System Boundary

[One paragraph defining exactly what is inside and outside the system boundary. Sign off before diagramming.]

## Actors

| Actor | Type | Description |
|-------|------|-------------|
| [Actor 1] | human | [Goal-bearing role description] |
| [Actor 2] | system | [External system description] |
| [Actor 3] | time | [Scheduled trigger description] |

## Use Cases by Actor

### [Actor 1]
- UC-001: [Verb + Noun]
- UC-002: [Verb + Noun]

### [Actor 2]
- UC-003: [Verb + Noun]

### Shared
- UC-004: [Verb + Noun] — [Actor 1] and [Actor 2]

## Relationships

| Source | Relationship | Target | Rationale |
|--------|-------------|--------|-----------|
| UC-001 | includes | UC-010 | [Why UC-010 always executes] |
| UC-002 | extends | UC-001 | [Extension point in UC-001 that triggers UC-002] |
| UC-003 | generalization of | UC-004 | [How UC-003 specializes UC-004] |

## UC Index (for index script)

```json
[
  {"id": "UC-001", "name": "[Verb Noun]", "actor": "[Actor 1]", "status": "Draft"},
  {"id": "UC-002", "name": "[Verb Noun]", "actor": "[Actor 1]", "status": "Draft"}
]
```
