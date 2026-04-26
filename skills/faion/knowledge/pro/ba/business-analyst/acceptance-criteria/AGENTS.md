# Acceptance Criteria

## Summary

Explicit, testable conditions that define when a requirement is accepted as complete. Written in Given-When-Then (BDD) or rule-based checklist format, covering the happy path, alternative paths, boundaries, error handling, performance, and security. Each criterion maps to at least one test case and forms part of the Definition of Done.

## Why

"Done" means different things to different people: developers consider a feature complete while users disagree; testing cannot run without something to test against; acceptance meetings become disputes. Acceptance criteria create a shared, pre-agreed finish line that eliminates subjective acceptance, drives testability, and prevents disputes at delivery.

## When To Use

- Every user story or requirement before a sprint starts — criteria must exist before development begins
- Bug fixes where the distinction between "expected" and "actual" behavior needs to be documented
- Technical stories where success requires a measurable outcome (throughput, error rate, response time)
- Before UAT to give users a concrete verification script rather than open-ended exploration
- Integrating with BDD tooling (Cucumber, SpecFlow) where Given-When-Then maps directly to test steps

## When NOT To Use

- Vague exploratory stories tagged "spike" or "research" — an output contract is the right artifact, not acceptance criteria
- When writing criteria for 30+ scenarios in one story — the story is too large; split it first
- System-level non-functional requirements (SLOs, capacity) — these belong in the architecture decision record or SLA, not per-story criteria
- Pure infrastructure/ops tasks with no user-visible behavior — a runbook or configuration checklist applies instead

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | BDD and rule-based formats, five coverage categories (happy/alt/boundary/error/nonfunctional), validation steps |
| `content/02-quality-rules.xml` | Testability rules, common mistakes (vagueness, implementation details, untestability), story-type guidelines |
| `content/03-examples.xml` | Login feature (3 BDD scenarios), shopping cart (checklist), requirement-AC-test case hierarchy |

## Templates

| File | Purpose |
|------|---------|
| `templates/ac-bdd.md` | BDD template: scenarios with Given/And/When/Then, non-functional criteria, out-of-scope section |
| `templates/ac-checklist.md` | Rule-based template: functional, validation, error handling, performance, and security criteria as checkboxes |
