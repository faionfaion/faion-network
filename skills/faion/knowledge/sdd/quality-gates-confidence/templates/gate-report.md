# Gate Report: {feature-NNN-name}

**Feature:** {feature-NNN-name}
**Task:** TASK_XXX — {title}
**Date:** {YYYY-MM-DD}
**Phase:** pre-{design|implementation|merge}

## Results

| Gate | Name | Checks | Score | Status |
|------|------|--------|-------|--------|
| L1 | Syntax & Format | {passed}/{total} | {X}% | PASS / FAIL / SKIP |
| L2 | Unit Tests | {passed}/{total} | {X}% | PASS / FAIL / SKIP |
| L3 | Integration Tests | {passed}/{total} | {X}% | PASS / FAIL / SKIP |
| L4 | Spec Compliance | {passed}/{total} | {X}% | PASS / FAIL / SKIP |
| L5 | Non-Functional | {passed}/{total} | {X}% | PASS / FAIL / SKIP |
| L6 | Human Review | {passed}/{total} | {X}% | PASS / FAIL / SKIP |

**Confidence score:** {X}% (threshold: 90%)

**Decision:** PROCEED / BLOCK

## Failures

<!-- List any failed checks with details -->

### L{X}: {check name}

**Command:** `{command that was run}`
**Output:**
```
{error output — truncated if long}
```
**Fix required:** {what needs to be done}

## Notes

<!-- Any context about skipped gates, manual review findings, etc. -->
