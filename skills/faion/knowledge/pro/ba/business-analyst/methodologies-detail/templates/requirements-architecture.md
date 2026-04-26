# Requirements Architecture: [Feature or System]

**Date:** [Date]
**Analyst:** [Name]

## Viewpoints

| Viewpoint | Stakeholders | Key Concerns |
|-----------|--------------|--------------|
| Business | Sponsor, Executives | ROI, Strategy alignment |
| User | End users | Usability, Features |
| Technical | Developers, Architects | Feasibility, Architecture |
| Operational | Operations, Support | Maintainability, SLAs |

## Requirement Hierarchy

```
BR-001: [Business Requirement]
  SR-001: [Stakeholder Requirement]
    FR-001: [Functional Requirement]
    FR-002: [Functional Requirement]
  SR-002: [Stakeholder Requirement]
    FR-003: [Functional Requirement]
```

## Dependencies

| Requirement | Depends On | Enables | Conflicts With |
|-------------|------------|---------|----------------|
| FR-001 | — | FR-003, FR-004 | — |
| FR-002 | FR-001 | FR-005 | — |

## Completeness Check

| Layer | Total | Covered | Gaps |
|-------|-------|---------|------|
| Business requirements | [N] | [N] | [List gap IDs] |
| Stakeholder requirements | [N] | [N] | [List gap IDs] |
| Functional requirements | [N] | [N] | [List gap IDs] |
