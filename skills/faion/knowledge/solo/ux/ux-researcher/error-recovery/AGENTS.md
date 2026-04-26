# Error Recovery (Help Users Recognize, Diagnose, and Recover)

## Summary

Nielsen's Usability Heuristic #9: error messages must be expressed in plain language, precisely
indicate the problem, and constructively suggest a solution. Every error message needs three
components: what happened, why it happened, and how to fix it. Placement must be inline and
proximate to the problem; recovery actions must be explicit buttons or links — never dead ends.

## Why

Cryptic or generic error messages (Error 403, "Something went wrong") abandon users at the
moment they most need guidance. Users who cannot diagnose or fix an error abandon the task,
generate support tickets, or lose trust in the product. Well-formed error messages with
concrete recovery paths eliminate the support escalation path for the most common failure
modes and keep users moving forward without external help.

## When To Use

- Auditing any form, API response surface, or system state where errors can occur.
- Writing microcopy for validation errors, system failures, 404 pages, network errors.
- During a design review for any new feature that has failure states.
- When support ticket analysis reveals recurring user confusion about a specific error.

## When NOT To Use

- Do not conflate error recovery with error prevention — prevention (Heuristic #5) eliminates
  errors before they occur; this methodology handles errors that do occur. Apply both, not
  one instead of the other.
- Do not use for success or informational states — the three-component structure (what/why/fix)
  is specific to failure states.

## Content

| File | What's inside |
|------|---------------|
| `content/01-principles.xml` | Three-component message structure, five message principles, placement rules per error type |
| `content/02-examples.xml` | Good (Stripe, GitHub 404, form validation) and bad (cryptic, vague, blame, dead-end) examples |

## Templates

| File | Purpose |
|------|---------|
| `templates/error-message.md` | Per-error design doc: trigger, technical cause, user impact, message content, visual design, actions |
| `templates/error-audit.md` | Audit table: error, current message, issues, improved message, placement, recovery options |
