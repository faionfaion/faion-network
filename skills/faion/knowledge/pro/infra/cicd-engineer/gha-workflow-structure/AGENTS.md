---
slug: gha-workflow-structure
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Model every workflow as a DAG of jobs using needs: before writing YAML.
content_id: "66466701291a2d49"
tags: [github-actions, workflow, ci, concurrency, triggers]
---
# GitHub Actions Workflow Structure

## Summary

**One-sentence:** Model every workflow as a DAG of jobs using needs: before writing YAML.

**One-paragraph:** Model every workflow as a DAG of jobs using needs: before writing YAML. Assign concurrency groups per trigger context (PR builds cancel on new push; deployment jobs do not). Use environment: for all deploy targets so secrets are scoped and approvals are trackable. Run scheduled workflows at low-traffic UTC times and always add workflow_dispatch as a manual escape hatch.

## Applies If (ALL must hold)

- Structuring a new workflow from scratch — model the DAG before writing YAML.
- Diagnosing slow CI — look for unnecessary sequential jobs and missing cache/artifact handoffs.
- Adding a new environment (staging, production, preview) — wire up GitHub Environment for scoped secrets and approvals.
- Setting up scheduled maintenance (security scans, dependency updates, DB backups) — use schedule + workflow_dispatch.

## Skip If (ANY kills it)

- Single-step workflows — a one-job workflow needs no DAG analysis.
- Local-only prototyping without a GitHub remote — use act for local testing instead.

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

- parent skill: `pro/infra/cicd-engineer/`
