<!-- purpose: Error handling audit scoring message components, placement and recovery sufficiency -->
<!-- consumes: error class inventory, tone / voice guide -->
<!-- produces: error handling audit (markdown) -->
<!-- depends-on: content/01-core-rules.xml, content/02-output-contract.xml -->
<!-- token-budget-impact: ~400 tokens filled -->

# Error Handling Audit: <feature>

**Date:** <date>
**Reviewer:** <reviewer_name>
**Scope:** [Features, forms, or screens reviewed]

## Error Messages Reviewed

| Error | Current Message | Issues Found | Improved Message |
|-------|-----------------|--------------|------------------|
| [Error] | "<current_text>" | [Missing component / jargon / blame] | "<better_version>" |

**Issues reference:** Missing "what happened" / Missing "why" / Missing "how to fix" / Technical jargon / Error code only / Blame language / Dead end (no recovery action)

## Error Placement Review

| Context | Current Placement | Appropriate? | Notes |
|---------|-------------------|--------------|-------|
| <form_field_x> | [Top of page / inline / banner] | Y/N | [What to change] |
| <system_error> | <modal_toast_inline> | Y/N | [What to change] |

## Recovery Options

| Error | Current Recovery Path | Sufficient? | Additional Options Needed |
|-------|-----------------------|-------------|--------------------------|
| [Error] | <current_button_link> | Y/N | <suggestions> |

## Accessibility Check

| Error | Color-only? | ARIA alert? | Focus managed? | Pass? |
|-------|-------------|-------------|----------------|-------|
| [Error] | Y/N | Y/N | Y/N | Y/N |

## Priority Fixes

1. **Critical:** [Error that leaves users with no recovery path]
2. **High:** [Error with technical language or blame framing]
3. **Medium:** [Error with missing "how to fix" component]
