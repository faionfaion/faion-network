# Help Users Recognize, Diagnose, and Recover from Errors

## Summary

Nielsen Heuristic #9: error messages must state what happened, why it happened, and how to fix it — in plain language, without error codes, without blaming the user. Every error must offer a recovery path (button or link), not just a description. Inline placement next to the problematic element is required for form errors; system errors use modal or banner with a retry action.

## Why

Cryptic or vague errors (Error 403, "Something went wrong") leave users stuck and trigger support tickets or abandonment. The three-part structure (what / why / how) directly resolves the failure by giving users the information and action needed to continue. Recovery actions as clickable elements — not instructions — reduce the cognitive load of figuring out what to do next.

## When To Use

- Auditing existing UI error messages for clarity and actionability before a release
- Writing microcopy for form validation, network errors, 404 pages, and payment failures
- Code review: checking that API error strings are user-presentable before surfacing in UI
- When support tickets reveal users confused by a specific error message
- Systematic pre-launch sweep of all error states in a feature

## When NOT To Use

- Preventing errors in the first place — use Heuristic #5 (Error Prevention) instead
- Designing empty states or onboarding flows — different UX domain
- Performance or reliability issues causing errors — fix the root cause, not the message
- Silent background errors that auto-retry without user involvement
- Good error messages cannot fix bad IA — if users reach the wrong place, clarity is irrelevant

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Three-part error message framework, response-time rules, error type handling (validation, system, 404, network) |
| `content/02-examples.xml` | Good/bad examples for error messages; antipatterns (cryptic codes, blame language, dead ends) |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-message-design.md` | Per-error-type design doc: trigger, content (what/why/how), placement, actions |
| `templates/error-audit.md` | Audit table: current message, issues, improved message, placement, recovery path |
| `templates/extract-errors.sh` | Bash script: extract all error string candidates from Python/JS codebase via ripgrep |
