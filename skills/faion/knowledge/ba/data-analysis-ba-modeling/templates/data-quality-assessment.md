<!-- purpose: DQ baseline skeleton scoring six dimensions per entity -->
<!-- consumes: sample data + measurement scripts -->
<!-- produces: dq_baseline section of the dictionary -->
<!-- depends-on: content/01-core-rules.xml r2 -->
<!-- token-budget-impact: ~250 tokens -->

# Data Quality Assessment: <data_domain>

**Assessor:** <name>
**Data Source:** <source_system>
**Sample Size:** <sample_size>
**Assessment Date:** <date>

## Quality Dimensions

### Accuracy
- **Metric:** Error rate vs. authoritative source
- **Finding:** <x> of records have incorrect values
- **Examples:** [Specific examples of errors found]

### Completeness
- **Metric:** Missing value percentage
- **Finding:** <field_x> has <y> null values
- **Impact:** [Downstream impact of missing data]

### Consistency
- **Metric:** Cross-system conflict count
- **Finding:** <x> of records have conflicting values across systems
- **Discrepancies:** [Types of inconsistencies found]

### Timeliness
- **Metric:** Average data age
- **Finding:** Average data age is <x_hours_days>
- **Impact:** [Impact of stale data on operations]

### Validity
- **Metric:** Business rule violation rate
- **Finding:** <x> of records violate defined rules
- **Violations:** [Types and examples of violations]

### Uniqueness
- **Metric:** Duplicate rate
- **Finding:** <x> duplicate records
- **Impact:** [Downstream impact of duplicates]

## Summary

| Dimension    | Score (1-5) | Status | Priority |
|--------------|-------------|--------|----------|
| Accuracy     | [X] | Green/Yellow/Red | H/M/L |
| Completeness | [X] | Green/Yellow/Red | H/M/L |
| Consistency  | [X] | Green/Yellow/Red | H/M/L |
| Timeliness   | [X] | Green/Yellow/Red | H/M/L |
| Validity     | [X] | Green/Yellow/Red | H/M/L |
| Uniqueness   | [X] | Green/Yellow/Red | H/M/L |

## Recommendations

| Issue | Recommendation | Priority | Effort |
|-------|----------------|----------|--------|
| <issue> | <action> | H/M/L | H/M/L |
