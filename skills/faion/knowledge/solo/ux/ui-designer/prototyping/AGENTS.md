# Prototyping

## Summary

Prototyping is the practice of building interactive representations of a product — from paper sketches to code — at the fidelity level required to answer a specific learning objective before committing to production development.

## Why

Static designs cannot convey how interactions behave, which means usability issues remain hidden until expensive development is underway. Prototypes surface these issues early, align stakeholders on expected behavior, and provide a testable artifact for usability research — at a fraction of the cost of discovering the problem in production.

## When To Use

- Validating interaction flows before writing production code
- Presenting design concepts to stakeholders who cannot read wireframes
- Running usability tests when no real product exists yet
- Deciding between two competing UX patterns before committing to development
- Documenting expected behavior for handoff to engineers

## When NOT To Use

- When the feature scope is a single static content page with no interaction
- When a fully working staging environment already exists and can be tested directly
- When the only unknown is visual aesthetics — use static mockups instead
- When the timeline is so compressed that prototype iteration would delay the actual build

## Content

| File | What's inside |
|------|---------------|
| `content/01-process.xml` | Five-step prototyping process: define goals, choose fidelity, create prototype, test, iterate; fidelity levels and prototype types; handoff artifact list |
| `content/02-examples.xml` | Paper, clickable (Figma), and interactive prototype examples; antipatterns (over-polishing, no hypothesis, ignoring findings) |

## Templates

| File | Purpose |
|------|---------|
| `templates/prototype-plan.md` | Prototype plan: objectives, fidelity rationale, scope, user flows, interactive elements, and testing plan |
| `templates/testing-notes.md` | Per-participant testing notes: task success, observations, quotes, issues found, and recommendations |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/export-frames.sh` | Bash script to export all Figma frames from a named page to PNG via the Figma REST API |
