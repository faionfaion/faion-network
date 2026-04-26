# Interface Catalog: [System Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Interface Summary

| IF-ID | Name | Type | Direction | External System | Criticality | Sensitivity | Status |
|-------|------|------|-----------|-----------------|-------------|-------------|--------|
| IF-001 | [Name] | System/API | Out | [System] | 1-4 | internal/confidential/restricted | active |
| IF-002 | [Name] | System/File | In | [System] | 1-4 | internal | design |
| IF-003 | [Name] | User | Bi | User | — | — | active |

Criticality tiers: 1 = business-critical (24/7 monitoring, contract tests, breaking-change review) → 4 = informational (register row only).

## Context Diagram

```
[External System A] --IF-001--> [Our System] --IF-003--> [User]
                                    |
                               <--IF-002--
                               [External System B]
```

## Active Traffic Reality Check

Last verified: [Date]
- Interfaces with no gateway traffic in 90 days (retirement candidates): [IF-IDs or "none"]
- Gateway traffic without register entry (governance violations): [IF-IDs or "none"]

## Detailed Specifications

| IF-ID | Specification | Owner | Last Reviewed |
|-------|---------------|-------|---------------|
| IF-001 | [link to spec] | [Team] | [Date] |
| IF-002 | [link to spec] | [Team] | [Date] |
