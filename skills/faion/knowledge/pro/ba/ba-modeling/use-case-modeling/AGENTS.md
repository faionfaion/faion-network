# Use Case Modeling

## Summary

A technique for expressing functional requirements as actor-system interaction sequences. Each use case captures WHO achieves WHAT goal with the system and HOW the system responds across normal, alternative, and exception flows. Use case names follow Verb+Noun convention; each has preconditions, a main flow (5-9 steps), alternative flows, exception flows, and postconditions.

## Why

Requirements written as feature lists omit actor context, miss edge cases, and produce untestable specs. Use cases force the BA to name a concrete actor and trace every path — including failures — before development starts. Each flow maps directly to a test path, closing the gap between "specified" and "testable".

## When To Use

- Functional requirements for transactional systems (line-of-business apps, regulated software) before development starts
- Multiple actor types interact with the system and cross-actor collisions have already caused bugs
- Compliance/audit context (FDA 21 CFR Part 11, SOX) requiring actor-goal → flow → code → test traceability
- Legacy system migration where screens are reverse-engineered into a controlled spec
- Test engineers need a deterministic scenario source for end-to-end test design
- Pre-development alignment when stakeholders speak features and developers need flows

## When NOT To Use

- Pure discovery phase — Opportunity Solution Trees give better signal than premature formalization
- Agile teams operating well with user stories + acceptance criteria — UC specs duplicate work
- Pure data/analytics platforms where data flow models fit better than actor-goal sequences
- ML/LLM features with probabilistic responses — use cases assume deterministic system behavior
- Tiny CRUD apps with one actor and fewer than 10 screens — an acceptance criteria sheet is faster
- Event-driven systems where event topology matters more than actor goals; use event storming or BPMN

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Actor types, use case components, step-by-step modeling process, relationship types (include/extend/generalize) |
| `content/02-quality-rules.xml` | Testability rules, step-count heuristics, naming convention, exception-flow requirement, agentic gotchas |
| `content/03-examples.xml` | Place Order use case (main + alternative + exception flows), actor-goal mapping example |

## Templates

| File | Purpose |
|------|---------|
| `templates/use-case-spec.md` | Full use case specification shell (ID, actors, preconditions, main/alt/exception flows, postconditions, business rules) |
| `templates/use-case-diagram.md` | Diagram notation template listing actors, use cases, and relationships |
| `templates/uc-drafter-prompt.txt` | LLM prompt for drafting one UC with hard rules (verb+noun, 5-9 steps, no UI nouns, required exception flows) |
| `templates/uc-reviewer-prompt.txt` | LLM prompt for scoring a UC against quality checklist, output JSON |
