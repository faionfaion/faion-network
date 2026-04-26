# User Control and Freedom

## Summary

Nielsen's Usability Heuristic #3: every interface must provide clearly marked "emergency exits" — undo, cancel, back, close, and reset — so users can recover from mistakes without going through extended processes. Prefer undo over confirmation dialogs for reversible actions; reserve confirmation only for irreversible, high-stakes operations.

## Why

Users make errors. Interfaces that trap users or impose permanent consequences destroy trust and cause abandonment. Forgiving design lowers the cognitive cost of exploration and reduces fear of mistakes, which directly increases engagement and task completion rates.

## When To Use

- Heuristic audit of a feature spec or UI for missing undo/cancel/exit mechanisms
- Generating a User Control Audit report (action table with undo/cancel/recovery columns)
- Code review: checking that destructive backend actions have soft-delete or undo hooks
- Accessibility review: verifying keyboard escape paths and focus management in modal flows
- Design review of multi-step wizards or onboarding flows for trapped-user patterns

## When NOT To Use

- As a substitute for actual usability testing — structural absence of controls is detectable, but whether users *feel* trapped requires behavioral data
- Complex undo architecture in database-backed systems — engineering judgment on consistency and rollback scope is required
- When the system genuinely cannot support undo (sent emails, executed financial transactions) — the design solution (clear warnings) needs human decision

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Control mechanisms, undo vs. confirmation decision rule, implementation patterns |
| `content/02-rules.xml` | Concrete rules, common mistakes, accessibility requirements, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/control-audit.md` | User Control Audit: actions × undo/cancel/exit/recovery columns + gap severity |
| `templates/verify-escape-exits.spec.js` | Playwright test to verify Escape key closes all modals |
