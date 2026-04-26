# Error Prevention

## Summary

Nielsen Heuristic #5: design out error-prone conditions before they occur rather than
relying on error messages to recover from them. Apply constraints, smart defaults, inline
validation, and targeted confirmation dialogs. Audit forms, destructive actions, and API
input boundaries for missing prevention mechanisms.

## Why

Prevention costs less than recovery. A constraint on a date field eliminates an entire
class of invalid-input errors at zero user effort. Inline validation surfaces problems
while context is fresh, not after a multi-field form is submitted. Confirmation dialogs
protect against irreversible actions — but overuse causes dialog fatigue that defeats the
purpose.

## When To Use

- Auditing form specs for missing input constraints, absent real-time validation, or unguarded destructive actions
- Reviewing API endpoint contracts for inputs accepted without server-side constraints
- Drafting confirmation dialog copy for delete, cancel-subscription, or bulk operations
- Reviewing code PRs for validation gaps: fields that accept any string where a constrained type is appropriate

## When NOT To Use

- Replacing QA — error prevention is a design heuristic, not a test suite
- Adding confirmations to routine, easily reversible actions — dialog fatigue reduces effectiveness for genuinely dangerous actions
- Very early concept stage where form fields are not yet defined

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategies.xml` | Six prevention strategies: constraints, suggestions, defaults, confirmation, validation, affordances |
| `content/02-patterns.xml` | Field-type patterns: date picker, inline validation timing, confirmation dialog rules, format guidance |
| `content/03-examples.xml` | Good examples (Gmail, Google Forms, Amazon); bad examples (submit-only validation, accepted invalid data) |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-prevention-audit.md` | Audit table: fields, constraints, validation timing, defaults, destructive actions |
| `templates/zod-schema-generator.py` | Python stub: generate Zod validation schema from a field spec list |
| `templates/prompt-audit.txt` | LLM prompt for auditing a form spec against Heuristic #5 |
