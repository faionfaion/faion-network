<!--
purpose: status audit report skeleton (Nielsen H#1)
consumes: action inventory + Playwright traces / session recordings
produces: a visibility-of-system-status artefact validating against scripts/validate-visibility-of-system-status.py
depends-on: content/01-core-rules.xml, content/02-output-contract.xml
token-budget-impact: ~600-1500 tokens once filled
-->
# System Status Audit: [Feature / Page]

**Date:** [Date]
**Reviewer:** [Name]
**Scope:** [Which screens / user flows]

## Actions Reviewed

| Action | Feedback Present | Feedback Type | Timing | ARIA | Notes |
|--------|-----------------|---------------|--------|------|-------|
| [Button click] | Y/N | [spinner / toast / banner] | [<100ms / <1s / <3s] | Present/Missing | |
| [Form submit] | Y/N | [disabled + spinner] | [immediate] | aria-busy? | |
| [File upload] | Y/N | [progress bar] | [% shown?] | role="progressbar"? | |

## State Coverage

| Interactive Element | Loading State | Success State | Error State |
|--------------------|--------------|--------------|-------------|
| [Submit button] | Present/Missing | Present/Missing | Present/Missing |
| [Upload trigger] | Present/Missing | Present/Missing | Present/Missing |

## Gaps Identified

| Issue | Severity | Recommendation |
|-------|----------|----------------|
| [No loading state on checkout submit] | 3 (Major) | [Disable button + show spinner on click] |
| [Success toast auto-dismisses error] | 3 (Major) | [Remove auto-dismiss from error states] |
| [No progress on file upload > 3s] | 2 (Minor) | [Add progress bar with percentage] |

## Accessibility

| Element | ARIA Required | ARIA Present | Fix |
|---------|--------------|--------------|-----|
| [Loading region] | aria-busy="true" | Missing | Add to button during async |
| [Status updates] | aria-live="polite" | Missing | Add role="status" to toast container |
| [Error messages] | aria-live="assertive" | Present | OK |

## Priority Recommendations

1. [Severity 4/3: most critical missing state]
2. [Severity 3: second priority]
3. [Severity 2: minor gap]
