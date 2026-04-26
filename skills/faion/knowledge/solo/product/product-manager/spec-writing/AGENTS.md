# Product Specification Writing

## Summary

A product specification (PRD) defines WHAT to build and WHY, leaving HOW to design and engineering. Required sections: Overview, Problem, Goals (with current/target metric table), Non-Goals, User Stories (As-a/I-want/So-that with persona IDs), Functional Requirements (FR-N IDs), Non-Functional Requirements, Acceptance Criteria (Given/When/Then per FR), Out of Scope, Open Questions. Every FR must have at least one AC; every goal must be measurable. Spec ends at ~5 pages for most features; beyond that, split or use a Mini-Spec.

## Why

Specs that mix what and how box in engineers and are ignored; specs without acceptance criteria produce untestable scope. Non-Goals explicitly prevent scope creep — their absence is the leading cause of unplanned feature growth. The Open Questions section is mandatory: a spec that has no unknowns signals false confidence and must be questioned before any FR is marked Must.

## When To Use

- Feature is large enough (more than one sprint) that engineers and designers need a shared written contract before work starts.
- Cross-team work where multiple stakeholders must approve scope.
- Building against an external SLA or paid customer commitment requiring traceable requirements.
- Onboarding a contractor — the spec is the briefing artifact.

## When NOT To Use

- Tiny changes (less than one day, no ambiguity) — a backlog item with acceptance criteria is sufficient.
- Highly exploratory discovery work where requirements change weekly. Spec the experiment, not the product.
- After implementation as a retroactive document — that is documentation, not a spec.
- When the team will not maintain the spec post-launch; outdated specs mislead more than they help.

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Required sections, rules for each, and antipatterns (mixing what/how, missing non-goals). |
| `content/02-requirements.xml` | FR/NFR authoring rules, AC format (Given/When/Then), and worked examples. |

## Templates

| File | Purpose |
|------|---------|
| `templates/prd.md` | Full PRD template: all required sections with placeholder guidance. |
| `templates/mini-spec.md` | Mini-Spec for small features: one-liner, problem, solution, requirements, exclusions. |
| `templates/validate-spec.py` | Python script: checks required sections, FR-to-AC traceability, measurable goals table. |
