# Writing Specifications

## Summary

A structured 9-phase process for writing spec.md — the document that answers "WHAT are we building and WHY?" before design or implementation begins. Covers problem analysis, user personas, user story mapping, SMART functional and non-functional requirements, Given-When-Then acceptance criteria, and explicit scope boundaries.

## Why

Projects fail when teams build the wrong thing because requirements are vague, stakeholders have different mental models, or there is no single written source of truth. A spec written with SMART criteria, FR traceability, and testable ACs reduces this risk: every FR has an ID, every AC has a pass/fail test, and out-of-scope items are explicitly named — preventing scope creep during design.

## When To Use

- Feature is new and requirements have not been written down anywhere.
- Existing feature needs scope expansion and the current spec is absent or too vague to drive design.
- Stakeholder and developer have different mental models of what the feature does.
- Requirements exist informally (Slack messages, verbal agreements) and need to be formalized.
- Constitution is new and needs to capture tech decisions before development begins.

## When NOT To Use

- Bug report with a clear reproduction path — write a task directly, not a spec.
- Infrastructure change (server config, deployment pipeline) with no user-visible behavior.
- Feature already has an approved spec — open and amend it rather than rewriting from scratch.
- Experiment/spike where the output will determine whether to proceed at all.

## Content

| File | What's inside |
|------|---------------|
| `content/01-process-and-rules.xml` | 9-phase writing process, document hierarchy (spec vs design vs impl-plan), common mistakes with fixes, SMART and INVEST criteria applied to requirements. |
| `content/02-checklist.xml` | Phase-by-phase checklist: context loading, problem analysis, user research, requirements definition, AC writing, scope definition, quality gates, review and approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap-feature.sh` | Shell script to create the `.aidocs/features/backlog/NN-slug/` directory and seed a blank spec.md. |

## Scripts

none
