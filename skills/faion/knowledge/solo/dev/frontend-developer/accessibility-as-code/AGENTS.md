---
slug: accessibility-as-code
tier: solo
group: dev
domain: frontend-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: End-to-end playbook for accessibility as code that walks an operator from trigger to closed outcome with named artefacts at each step.
content_id: "216f553b9111dd9e"
tags: [accessibility, dev, playbook]
---
# Accessibility As Code

## Summary

**One-sentence:** End-to-end playbook for accessibility as code that walks an operator from trigger to closed outcome with named artefacts at each step.

**One-paragraph:** End-to-end playbook for accessibility as code that walks an operator from trigger to closed outcome with named artefacts at each step. Accessibility methodologies live in `ux/accessibility-specialist/` but a working dev needs axe-core in CI, eslint-plugin-jsx-a11y rules, contrast-checking in design tokens. Solo `dev/software-developer/accessibility` is a single doc, not an enforcement playbook.

## Applies If (ALL must hold)

- You are executing the cross-cutting workflow addressed by accessibility as code end to end.
- All inputs the playbook calls for are reachable (people, data, artefacts).
- The output is consumed by a named downstream owner with a deadline.
- Deviations from the steps are logged with a one-line rationale.

## Skip If (ANY kills it)

- Highly contextual one-shot work where playbook constrains the wrong axes.
- Pre-discovery — playbook assumes the problem is named.
- Teams already running a well-tuned variant — re-tooling friction outweighs upside.

## Prerequisites

- Stakeholders, owners, and deadlines named in advance.
- Inputs (data, briefs, accounts) reachable at start.
- Storage location for each step's output decided.

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/dev/frontend-developer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | The 4 testable rules every application enforces | ~900 |
| `content/02-output-contract.xml` | essential | Required output schema, forbidden patterns, allowed transformations | ~700 |
| `content/03-failure-modes.xml` | essential | 5 detector + repair clauses for known agent failures | ~900 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `input_collection` | haiku | Structured gather from inputs |
| `decision_steps` | sonnet | Apply playbook branches against state |
| `synthesis_writeup` | opus | Final artefact authoring |

## Templates

| File | Purpose |
|------|---------|
| `templates/output-schema.json` | JSON Schema for the methodology's required output |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-output.py` | Enforce the output-contract before main agent accepts | After subagent returns, before commit/publish |

## Related

- parent skill: `solo/dev/frontend-developer/`
- peer methodologies: see siblings under `solo/dev/frontend-developer/`
- external: industry references cited inline in `content/01-core-rules.xml`
