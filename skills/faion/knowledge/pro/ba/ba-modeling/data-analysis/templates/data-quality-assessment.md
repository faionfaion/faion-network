<!-- purpose: DQ baseline skeleton scoring six dimensions per entity -->
<!-- consumes: sample data + measurement scripts -->
<!-- produces: dq_baseline section of the dictionary -->
<!-- depends-on: content/01-core-rules.xml r2 -->
<!-- token-budget-impact: ~250 tokens -->

# Data Quality Assessment: [Data Domain]

**Assessor:** [Name]
**Data Source:** [Source system]
**Sample Size:** [N records — minimum 100 or 10% of volume]
**Assessment Date:** [Date]

## Quality Dimensions

### Accuracy
- **Metric:** Error rate vs. authoritative source
- **Finding:** [X%] of records have incorrect values
- **Examples:** [Specific examples of errors found]

### Completeness
- **Metric:** Missing value percentage
- **Finding:** [Field X] has [Y%] null values
- **Impact:** [Downstream impact of missing data]

### Consistency
- **Metric:** Cross-system conflict count
- **Finding:** [X%] of records have conflicting values across systems
- **Discrepancies:** [Types of inconsistencies found]

### Timeliness
- **Metric:** Average data age
- **Finding:** Average data age is [X hours/days]
- **Impact:** [Impact of stale data on operations]

### Validity
- **Metric:** Business rule violation rate
- **Finding:** [X%] of records violate defined rules
- **Violations:** [Types and examples of violations]

### Uniqueness
- **Metric:** Duplicate rate
- **Finding:** [X%] duplicate records
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
| [Issue] | [Action] | H/M/L | H/M/L |
