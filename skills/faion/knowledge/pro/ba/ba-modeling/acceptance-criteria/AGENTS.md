# Acceptance Criteria

## Summary

Acceptance criteria (AC) define the exact conditions a requirement must satisfy to be accepted as complete. Each criterion is testable, behaviour-level, and carries a stable ID (AC-FEATURE-NN) that cross-references spec.md, test-plan.md, PR description, CI report, and changelog. Two formats: Given/When/Then (Gherkin/BDD) for user-facing behaviour, and rule-based checklists for system constraints.

## Why

Without AC, "done" means different things to developers, testers, and stakeholders; acceptance meetings become scope debates rather than verification checkpoints. Stable IDs create traceability from requirement to test to release. The Gherkin format produces living documentation executable in CI, closing the loop between spec and running behaviour.

## When To Use

- Authoring AC for SDD `spec.md` files before a coding subagent picks up the task.
- Translating a freeform user story or stakeholder note into testable criteria.
- Generating regression scenarios from a bug report so the fix has a definition-of-done gate before merge.
- Splitting an oversized story: when AC count exceeds 7 per story, that is the slicing signal.
- Wiring AC to executable specs (Gherkin to Cucumber / Behave / Playwright) so BA review and CI share one artifact.

## When NOT To Use

- Pure spike / research tasks where the outcome is a learning, not a behaviour.
- Throwaway prototypes or demos with a lifespan under one sprint.
- UX-only changes where verification is subjective (visual polish, brand tone).
- Operational runbook changes (server tweaks, cron edits) — use smoke checks instead.
- Negotiation-heavy external contracts where AC ossify before scope is stable.

## Content

| File | What's inside |
|------|---------------|
| `content/01-formats-and-rules.xml` | GWT format, rule-based format, coverage categories (happy / alternative / boundary / error / security / performance), INVEST rules, stable-ID convention. |
| `content/02-examples.xml` | Login feature (GWT scenarios), shopping cart (rule-based checklist), bug-fix AC pattern. |
| `content/03-agentic-workflow.xml` | 3-stage chain: research → authoring → verification. Subagent recommendations, XML prompt pattern, ac-coverage.sh gating script. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-bdd.md` | Given/When/Then AC template with scenario headers and non-functional sections. |
| `templates/ac-rule-based.md` | Rule-based checklist AC template covering functional, validation, error, performance, security criteria. |
| `templates/ac-coverage.sh` | Verifies every AC-ID in spec.md has a matching test reference in test-plan.md; exits non-zero on gaps. |
| `templates/prompt-authoring.xml` | Structured XML prompt for authoring Gherkin AC with category constraints and ID-continuation rules. |
| `templates/prompt-verification.xml` | Structured XML prompt for test-plan coverage gate: emits {ac_id, has_test, gap_reason} and halts on failure. |
