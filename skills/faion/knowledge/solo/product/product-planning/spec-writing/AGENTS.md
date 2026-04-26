# Spec Writing

## Summary

A product spec defines WHAT to build and WHY, leaving HOW to the design and engineering process. Every functional requirement gets a unique ID and a M/S/C priority. Every feature gets Given-When-Then acceptance criteria. Non-Goals is mandatory and non-empty (minimum 3 items). Open Questions is honest — never "none."

## Why

Specs that mix what and how waste engineering cycles on rework when implementation details change. Specs without acceptance criteria produce untestable requirements; engineers ship what they interpret, not what was intended. The faion-feature-executor and faion-sdd-execution skills consume `spec.md` acceptance criteria directly as test cases.

## When To Use

- Converting an MVP-scoping output or roadmap initiative into a buildable spec before SDD execution.
- A subagent is about to implement a feature and needs WHAT/WHY locked before HOW.
- Stakeholder review is required prior to engineering — the spec is the review artifact.
- Producing acceptance criteria that drive both implementation and tests.

## When NOT To Use

- Tiny bug fixes or refactors — a one-line issue description suffices.
- Rapid prototypes or spikes where the goal is to learn — write a research brief instead.
- Internal-only platform work with no user surface — a design doc or RFC fits better.

## Content

| File | What's inside |
|------|---------------|
| `content/01-framework.xml` | Spec components table, 7-step writing process, what vs how separation rule |
| `content/02-examples.xml` | Search feature spec example with full FR, NFR, and acceptance criteria |
| `content/03-antipatterns.xml` | Mixing what/how, vague NFRs, empty non-goals, fabricated metrics |

## Templates

| File | Purpose |
|------|---------|
| `templates/spec-full.md` | Complete PRD template with all sections |
| `templates/spec-mini.md` | Mini-spec for quick features (1-page) |
| `templates/spec-lint.py` | Validates spec JSON: FR IDs, priorities, AC coverage, non-goals presence |
