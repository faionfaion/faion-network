<!-- purpose: solution-wide UML use-case diagram (mermaid) -->
<!-- consumes: actor inventory + use_cases[] ids -->
<!-- produces: visual overview; not part of the schema artefact -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~200 tokens -->

# Use Case Diagram: <system_name>

## System Boundary

**System:** [Name of system being analyzed]

## Actors

| Actor | Type | Description |
|-------|------|-------------|
| <actor_1> | Primary | <goal_they_achieve> |
| <actor_2> | Secondary | <role_they_play> |
| <external_system> | System | <system> |

## Use Cases by Actor

### <actor_1>
- UC-001: [Use Case Name]
- UC-002: [Use Case Name]

### [Actor 2]
- UC-003: [Use Case Name]

### Shared
- UC-004: [Use Case Name] — <actor_1> and <actor_2>

## Relationships

| Relationship | Type | Rationale |
|-------------|------|-----------|
| UC-001 includes UC-010 | Include | [UC-010 steps appear in 3+ use cases] |
| UC-002 extends UC-001 | Extend | [Optional behavior at extension point X] |
| UC-005 generalizes UC-006 | Generalize | [UC-005 IS-A specialized version of UC-006] |

## Notes

- Relationships declared only when they de-duplicate 10+ steps
- Each use case owned by exactly one primary actor
