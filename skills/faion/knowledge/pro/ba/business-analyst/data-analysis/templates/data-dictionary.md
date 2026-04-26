# Data Dictionary: [System or Domain Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]
**Snapshot:** [ISO date — when this dictionary reflects the actual system state]

## Entity: [Entity Name]

**Description:** [What this entity represents in business terms]
**Owner:** [Team responsible for data quality]
**Source:** [Where data originates]

### Attributes

| Name | Definition | Type | Format | Required | Valid Values | Rules |
|------|------------|------|--------|----------|--------------|-------|
| [Name] | [Business meaning] | [Type] | [Format] | Y/N | [Values or range] | [Rule IDs] |

### Example Records

| [Attr 1] | [Attr 2] | [Attr 3] |
|----------|----------|----------|
| [Value] | [Value] | [Value] |

### Relationships

| Related Entity | Relationship | Cardinality |
|----------------|--------------|-------------|
| [Entity] | [has many | belongs to | references] | [1:1 | 1:N | N:N] |

### Business Rules

| Rule ID | Rule Description |
|---------|------------------|
| DR-01 | [Rule in plain language] |
