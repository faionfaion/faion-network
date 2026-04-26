# Error Prevention

## Summary

Nielsen's Usability Heuristic #5: design to eliminate error-prone conditions before they occur.
Apply six strategies in order of preference — constraints, suggestions, defaults, confirmation,
real-time validation, and affordances. Use confirmation dialogs only for irreversible or
high-consequence actions; avoid them for routine or easily reversible ones.

## Why

Error recovery is always more expensive than prevention: the user wastes effort, support costs
rise, and data quality degrades. Prevention strategies — particularly input constraints and
inline validation — interrupt errors at the point of entry rather than after form submission,
reducing abandonment and the cognitive load of parsing a list of errors at the end of a long
form.

## When To Use

- Designing or auditing any form with consequential data (payments, account changes, orders).
- When form abandonment or submission error rates are high in analytics.
- When reviewing any destructive action (delete, cancel subscription, bulk operation) for
  whether it needs a confirmation step.
- When validating that input fields constrain or guide input to valid values only.

## When NOT To Use

- Do not add confirmation dialogs to routine or easily reversible actions — over-confirming
  trains users to dismiss dialogs without reading, defeating the purpose.
- Do not apply real-time validation to every field indiscriminately — aggressive inline errors
  before the user has finished typing increase frustration; validate on blur for most fields,
  on keypress only for password strength indicators.

## Content

| File | What's inside |
|------|---------------|
| `content/01-strategies.xml` | Six prevention strategies with concrete patterns per input type (text, numeric, date, select) |
| `content/02-examples.xml` | Good examples (Gmail, Google Forms, Amazon), bad examples (submit-only validation) |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-prevention-audit.md` | Audit table: field, input type, constraints, validation timing, defaults, recommendations |
