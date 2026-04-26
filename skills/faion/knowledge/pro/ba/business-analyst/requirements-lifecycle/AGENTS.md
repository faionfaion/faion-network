# Requirements Lifecycle Management

## Summary

A governance framework for managing requirements from initial capture through implementation and verification. Defines eight requirement states (Draft → Proposed → Approved → Implemented → Verified, plus Rejected/Deferred/Deleted), enforces change control via a formal change request process, and maintains version history for every requirement. Prevents uncontrolled scope changes and preserves the audit trail needed for compliance and retrospectives.

## Why

Requirements exist in multiple versions with no clarity on which is current; approved requirements change without process; implementation diverges from documentation; nobody can reconstruct the evolution at project end. A lifecycle model with explicit states and a change request gate eliminates version confusion and creates an audit trail that satisfies both governance and postmortem needs.

## When To Use

- Projects with formal change control requirements (regulated industries, government, enterprise IT)
- Long-running projects where requirements evolve over months and version drift is a real risk
- Teams where stakeholders or developers frequently bypass the BA to change requirements informally
- Compliance context (SOX, ISO, HIPAA) requiring a documented requirements audit trail
- Post-implementation review revealed implementation mismatches — lifecycle management prevents recurrence
- Integrating multiple delivery streams that each own a subset of requirements

## When NOT To Use

- Early-stage discovery / hypothesis testing where requirements legitimately change every sprint — add lifecycle overhead only after problem-solution fit
- Tiny internal tools with a single stakeholder and a one-week delivery — a shared doc suffices
- Pure agile backlogs managed in Jira/Linear where the tool already enforces state — duplicate governance adds friction without value
- Throwaway prototypes — formal lifecycle governance is wasted on artifacts designed to be discarded

## Content

| File | What's inside |
|------|---------------|
| `content/01-lifecycle-stages.xml` | Six lifecycle stages, eight requirement states, state-transition rules, validation vs. verification distinction |
| `content/02-change-control.xml` | Change request process, impact analysis categories, approval roles, common mistakes |
| `content/03-examples.xml` | Password Reset requirement state history, CR-012 login timeout change request walkthrough |

## Templates

| File | Purpose |
|------|---------|
| `templates/requirements-status-log.md` | Status summary table and per-requirement detail with current state tracking |
| `templates/change-request.md` | Change request form: current/proposed text, reason, impact analysis by area, approval table |
| `templates/version-history.md` | Per-requirement version log with change descriptions and current vs. previous content |
