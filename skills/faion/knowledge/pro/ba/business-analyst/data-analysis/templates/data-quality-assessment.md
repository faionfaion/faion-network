# Data Quality Assessment: [Data Domain]

**Date:** [Date]
**Assessor:** [Name]
**Data Source:** [Source system and table/view]
**Sample Size:** [N records — state if this is full population or sample]
**Snapshot at:** [ISO timestamp]

## Quality Dimensions

### Accuracy
- **Metric:** Error rate (incorrect values / total values)
- **Finding:** [X%] of records have errors
- **Examples:** [Specific error types observed]
- **Root cause:** [Why errors exist]

### Completeness
- **Metric:** Missing value percentage per required field
- **Finding:** [Field X] has [Y%] null or empty values
- **Impact:** [What breaks when data is missing]

### Consistency
- **Metric:** Match rate across systems
- **Finding:** [X%] of records match between [System A] and [System B]
- **Discrepancies:** [Types of inconsistencies observed]

### Timeliness
- **Metric:** Age of data vs. business SLA
- **Finding:** Average data age is [X hours/days]
- **Impact:** [What decisions are affected by stale data]

### Validity
- **Metric:** Rule violation rate
- **Finding:** [X%] of records violate business rules
- **Violations:** [Specific rule violations observed]

### Uniqueness
- **Metric:** Duplicate rate
- **Finding:** [X%] duplicate records
- **Impact:** [What double-counting or conflicts result]

## Summary Scorecard

| Dimension | Score (1-5) | Status | Priority |
|-----------|-------------|--------|----------|
| Accuracy | [X] | Green/Yellow/Red | H/M/L |
| Completeness | [X] | Green/Yellow/Red | H/M/L |
| Consistency | [X] | Green/Yellow/Red | H/M/L |
| Timeliness | [X] | Green/Yellow/Red | H/M/L |
| Validity | [X] | Green/Yellow/Red | H/M/L |
| Uniqueness | [X] | Green/Yellow/Red | H/M/L |

## Recommendations

| Issue | Recommendation | Priority | Effort |
|-------|----------------|----------|--------|
| [Issue] | [Specific action] | H/M/L | H/M/L |
