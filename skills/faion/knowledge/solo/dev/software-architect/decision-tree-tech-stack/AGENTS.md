---
slug: decision-tree-tech-stack
tier: solo
group: dev
domain: architecture
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Walk this decision tree to select frontend frameworks, backend languages, and mobile platforms.
content_id: "780a229e1ebd3036"
tags: [decision-tree, tech-stack, framework-selection, language-selection, frontend]
---
# Technology Stack Selection Decision Tree

## Summary

**One-sentence:** Walk this decision tree to select frontend frameworks, backend languages, and mobile platforms.

**One-paragraph:** Walk this decision tree to select frontend frameworks, backend languages, and mobile platforms. The tree routes by application type first, then SEO requirements and team expertise. Output: recommended stack, runner-up, and rationale for the choice.

## Applies If (ALL must hold)

- Starting a new project or service and need to pick a technology stack.
- Evaluating whether to adopt a new framework for an existing codebase.
- Onboarding a team that needs a defensible technology choice with documented rationale.
- Filtering 5-10 candidate technologies down to 2-3 for a deeper comparison matrix.

## Skip If (ANY kills it)

- When a hard constraint already gates the choice (contractual, compliance, existing vendor) — the constraint dominates the tree output.
- For low-stakes tooling choices (CLI scripts, one-off automation) — pick what the team knows and move on.
- When the team has deep expertise in one option and no strong counter-indicator — expertise weight will dominate anyway.

## Prerequisites

- TBD — list concrete input artifacts and where they come from

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `TBD/path` | TBD — what upstream output this consumes |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | Testable rules migrated from v1 methodology | ~800 |
| `content/02-output-contract.xml` | essential | Output schema (stub — fill from v1 patterns) | ~800 |
| `content/03-failure-modes.xml` | essential | Antipatterns migrated from v1 methodology | ~800 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| TBD | sonnet | TBD |

## Templates

| File | Purpose |
|------|---------|
| TBD | TBD |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| TBD | TBD | TBD |

## Related

- parent skill: `solo/dev/software-architect/`
