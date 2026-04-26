# Visibility of System Status

## Summary

Nielsen Heuristic #1: every user action must produce visible feedback within the appropriate time threshold — spinner for 1-3s, progress bar for 3-10s, progress bar with percentage and cancel for >10s. Every interactive element needs three implemented states: loading (disabled + visual indicator), success (confirmation), and error (message with recovery action). Disable the trigger element during async operations to prevent double-submission.

## Why

When users click and nothing visibly happens, they click again (duplicate submissions), wait in uncertainty, or abandon the task. NNG response time thresholds are empirically validated: under 0.1s feels instantaneous; over 1s users feel the system is slow; over 10s users disengage without a progress indicator. Feedback must be immediate even if the operation is not — the loading state is feedback that the click registered.

## When To Use

- Auditing any interactive UI where user actions trigger async operations (form submissions, file uploads, API calls)
- Code review: verifying every button, link, and form has loading, success, and error states
- Before a launch: sweep all user flows for dead-click moments where UI appears unresponsive
- When support tickets or session recordings show users double-clicking or resubmitting forms
- Designing real-time features (chat, live data, collaborative editing) requiring continuous state feedback

## When NOT To Use

- Static informational pages with no interactive elements — nothing to communicate
- Background operations the user does not need to know about (cache refresh completing in &lt;100ms)
- Micro-interactions already covered by platform defaults (OS-level progress bars for file transfers)
- When audit findings for this heuristic are already documented and tracked — fix, don't re-audit

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Response time thresholds, feedback type selection rules, loading/success/error state patterns, state indicator patterns (connection status, document status) |
| `content/02-examples.xml` | Good examples (file upload flow, form submission), bad examples (no feedback, vague status), accessibility requirements (ARIA live regions) |

## Templates

| File | Purpose |
|------|---------|
| `templates/status-audit.md` | Audit table: action, feedback present, feedback type, timing, gaps, severity |
| `templates/loading-state.spec.ts` | Playwright test: verify loading state appears on form submit and file upload |
