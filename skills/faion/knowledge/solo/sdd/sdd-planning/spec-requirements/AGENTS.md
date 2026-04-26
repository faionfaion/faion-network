# Specification Requirements

## Summary

A structured methodology for translating a plain-language feature request into a traceable set of user personas, INVEST-validated user stories, SMART functional and non-functional requirements (FR-X / NFR-X), and Given-When-Then acceptance criteria (AC-X). Every FR must trace to a user story; every Must FR must have at least one AC. Output is a `spec.md` that the design phase consumes.

## Why

Ambiguous requirements are the single largest source of rework in software projects. SMART criteria make each requirement testable (pass/fail); traceability (FR-X → US-X → AC-X) ensures no requirement is implemented without a verification condition. MoSCoW prioritization enforces scope discipline — without it, every requirement becomes "Must" and MVP never ships.

## When To Use

- Starting any non-trivial feature estimated to touch more than one system layer
- Stakeholder has described a need in plain language that needs translation into testable requirements
- Feature scope is ambiguous and "Out of Scope" must be made explicit before design begins
- Multiple user personas are affected and their needs conflict or overlap
- Acceptance criteria will drive automated BDD tests (Gherkin/Given-When-Then)

## When NOT To Use

- Bug fix with a clear, agreed-upon fix — spec overhead exceeds value
- Purely internal refactor with no user-facing behavior change
- Spike or proof-of-concept — spec assumes known requirements; spikes discover them
- Design is already finalized and requirements are back-filled without intent to use them

## Content

| File | What's inside |
|------|---------------|
| `content/01-requirements-rules.xml` | SMART criteria for FR/NFR, MoSCoW prioritization rules, traceability mandate, Given-When-Then AC format rules |
| `content/02-checklist.xml` | Phase-by-phase checklist: SMART analysis, personas, user story mapping, use cases, FR/NFR, AC, scope definition |
| `content/03-examples.xml` | Concrete FR, NFR, AC, user story, and persona examples; common mistakes with fixes |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-template.md` | Full spec.md skeleton with all sections wired: personas, stories, FR-X, NFR-X, AC-X, scope |
| `templates/prompt-spec-authoring.txt` | Agent prompt for authoring spec.md from a feature brief (personas → stories → FR → AC) |
| `templates/prompt-traceability-review.txt` | Agent prompt for reviewing spec.md traceability: FR-X → US-X → AC-X matrix |
