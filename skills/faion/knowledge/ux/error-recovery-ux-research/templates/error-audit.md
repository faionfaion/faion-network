# Error Handling Audit: [Feature]

**Date:** [Date]
**Reviewer:** [Name]
**Scope:** [Features, forms, or screens reviewed]

## Error Messages Reviewed

| Error | Current Message | Issues Found | Improved Message |
|-------|-----------------|--------------|------------------|
| [Error] | "[Current text]" | [Missing component / jargon / blame] | "[Better version]" |

**Issues reference:** Missing "what happened" / Missing "why" / Missing "how to fix" / Technical jargon / Error code only / Blame language / Dead end (no recovery action)

## Error Placement Review

| Context | Current Placement | Appropriate? | Notes |
|---------|-------------------|--------------|-------|
| [Form field X] | [Top of page / inline / banner] | Y/N | [What to change] |
| [System error] | [Modal / toast / inline] | Y/N | [What to change] |

## Recovery Options

| Error | Current Recovery Path | Sufficient? | Additional Options Needed |
|-------|-----------------------|-------------|--------------------------|
| [Error] | [Current button/link] | Y/N | [Suggestions] |

## Accessibility Check

| Error | Color-only? | ARIA alert? | Focus managed? | Pass? |
|-------|-------------|-------------|----------------|-------|
| [Error] | Y/N | Y/N | Y/N | Y/N |

## Priority Fixes

1. **Critical:** [Error that leaves users with no recovery path]
2. **High:** [Error with technical language or blame framing]
3. **Medium:** [Error with missing "how to fix" component]
