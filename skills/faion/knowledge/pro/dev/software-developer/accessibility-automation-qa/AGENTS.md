---
slug: accessibility-automation-qa
tier: pro
group: dev
domain: software-developer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion]
summary: End-to-end playbook for accessibility automation qa that walks an operator from trigger to closed outcome with named artefacts at each step.
content_id: "309fe06f55bc0c02"
tags: [accessibility, dev, playbook]
---
# Accessibility Automation QA

## Summary

**One-sentence:** End-to-end playbook for accessibility automation qa that walks an operator from trigger to closed outcome with named artefacts at each step.

**One-paragraph:** End-to-end playbook for accessibility automation qa that walks an operator from trigger to closed outcome with named artefacts at each step. A11y methodology exists at pro/ux/accessibility-specialist/a11y-testing but it is framed for designers/specialists. A QA engineer needs the implementation-side methodology: wiring axe-core/pa11y into unit + E2E + CI, choosing severity gates, integrating WCAG 2.2 success criteria into test plans, and assistive-tech smoke tests. The dev/testing-developer corpus is silent.

## Applies If (ALL must hold)

- You are executing the cross-cutting workflow addressed by accessibility automation qa end to end.
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
| `pro/dev/software-developer/AGENTS.md` | Parent skill context (vocabulary, neighbouring methodologies) |

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

- parent skill: `pro/dev/software-developer/`
- peer methodologies: see siblings under `pro/dev/software-developer/`
- external: industry references cited inline in `content/01-core-rules.xml`
