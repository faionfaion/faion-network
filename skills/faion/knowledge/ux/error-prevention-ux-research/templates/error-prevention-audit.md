# Error Prevention Audit: [Feature]

**Date:** [Date]
**Reviewer:** [Name]
**Scope:** [Forms, flows, or screens reviewed]

## Form Fields Analysis

| Field | Input Type | Constraints Applied | Validation Timing | Default Value | Issues | Recommendation |
|-------|------------|---------------------|-------------------|---------------|--------|----------------|
| [Field] | text/select/date | [What constraints] | blur/keypress/submit | [Default] | [Issues] | [Fix] |

## Destructive Actions

| Action | Has Confirmation? | Confirmation Quality | Undo Available? | Risk Level | Recommendation |
|--------|-------------------|----------------------|-----------------|------------|----------------|
| [Action] | Y/N | [Good/Weak/None] | Y/N | H/M/L | [Recommendation] |

**Confirmation quality criteria:**
- Good: describes consequence + count + irreversibility, button label repeats the action
- Weak: generic "Are you sure?" without specifics
- None: action fires immediately without warning

## Common Error Points (from analytics or support data)

| Error Type | Frequency | Root Cause | Prevention Strategy |
|------------|-----------|------------|---------------------|
| [Error] | [Count/rate] | [Why it occurs] | [Constraint/validation/default] |

## Priority Recommendations

1. **High:** [Prevention that eliminates a frequent or high-impact error]
2. **Medium:** [Prevention that reduces friction for a moderate error]
3. **Low:** [Nice-to-have improvement]
