<!-- purpose: Error prevention audit scoring constraints, confirmation quality and error points -->
<!-- consumes: error class inventory, form / control inventory -->
<!-- produces: error prevention audit (markdown) -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400 tokens filled -->

# Error Prevention Audit: <feature>

**Date:** <date>
**Reviewer:** <reviewer_name>
**Scope:** [Forms, flows, or screens reviewed]

## Form Fields Analysis

| Field | Input Type | Constraints Applied | Validation Timing | Default Value | Issues | Recommendation |
|-------|------------|---------------------|-------------------|---------------|--------|----------------|
| <field> | text/select/date | <what_constraints> | blur/keypress/submit | <default> | <issues> | <fix> |

## Destructive Actions

| Action | Has Confirmation? | Confirmation Quality | Undo Available? | Risk Level | Recommendation |
|--------|-------------------|----------------------|-----------------|------------|----------------|
| <action> | Y/N | <good_weak_none> | Y/N | H/M/L | <recommendation> |

**Confirmation quality criteria:**
- Good: describes consequence + count + irreversibility, button label repeats the action
- Weak: generic "Are you sure?" without specifics
- None: action fires immediately without warning

## Common Error Points (from analytics or support data)

| Error Type | Frequency | Root Cause | Prevention Strategy |
|------------|-----------|------------|---------------------|
| <error> | <count_rate> | [Why it occurs] | <constraint_validation_default> |

## Priority Recommendations

1. **High:** [Prevention that eliminates a frequent or high-impact error]
2. **Medium:** [Prevention that reduces friction for a moderate error]
3. **Low:** [Nice-to-have improvement]
