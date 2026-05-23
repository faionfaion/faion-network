<!-- purpose: data-dictionary skeleton (entities + fields + owner + DQ + business rules) -->
<!-- consumes: source-system inventory + introspected schemas + DPO classification -->
<!-- produces: spec artefact conforming to 02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400 tokens loaded as template context -->

# Data Dictionary: [System/Domain Name]

**Version:** 1.0
**Author:** [Name]

## Entity: [Entity Name]

**Description:** [What this entity represents in business terms]
**Owner:** [Data owner — team or role]
**Source:** [Where data originates]

### Attributes

| Name | Definition | Type | Format | Required | Valid Values | Rules |
|------|------------|------|--------|----------|--------------|-------|
| [Name] | [Business meaning] | [Type] | [Format spec] | Y/N | [Values or range] | [Rule IDs] |

### Example Records

| [Attr 1] | [Attr 2] | [Attr 3] |
|----------|----------|----------|
| [Value]  | [Value]  | [Value]  |

### Relationships

| Related Entity | Relationship | Cardinality |
|----------------|--------------|-------------|
| [Entity] | [has/belongs to/etc.] | 1:1 / 1:N / N:N |

### Business Rules

| Rule ID | Rule Type | Rule Description |
|---------|-----------|------------------|
| DR-01 | Validation | [Rule] |
| DR-02 | Derivation | [Formula] |
| DR-03 | Default | [Default value and trigger] |
| DR-04 | Constraint | [Cross-field constraint] |
| DR-05 | Uniqueness | [Key definition] |
