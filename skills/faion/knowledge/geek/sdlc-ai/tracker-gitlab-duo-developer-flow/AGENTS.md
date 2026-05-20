---
slug: tracker-gitlab-duo-developer-flow
tier: geek
group: sdlc-ai
domain: sdlc-ai
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Drive every GitLab issue-to-merge-request transition through the GitLab Duo Agent Platform's named flows: Developer Flow turns an issue into an MR, Code Review Flow runs automated review on the MR, Software Development Flow handles multi-step plan-before-execute changes, and CI/CD Flows handle pipeline migrations and failing-build fixes.
content_id: "50dbae547752c9fa"
tags: [gitlab, gitlab-duo, merge-request, agent-platform, tracker]
---
# GitLab Duo Agent Platform Developer Flow

## Summary

**One-sentence:** Drive every GitLab issue-to-merge-request transition through the GitLab Duo Agent Platform's named flows: Developer Flow turns an issue into an MR, Code Review Flow runs automated review on the MR, Software Development Flow handles multi-step plan-before-execute changes, and CI/CD Flows handle pipeline migrations and failing-build fixes.

**One-paragraph:** Drive every GitLab issue-to-merge-request transition through the GitLab Duo Agent Platform's named flows: Developer Flow turns an issue into an MR, Code Review Flow runs automated review on the MR, Software Development Flow handles multi-step plan-before-execute changes, and CI/CD Flows handle pipeline migrations and failing-build fixes. Every flow respects the GitLab project's protected-branch rules, CODEOWNERS, and approval-rule policies — the human approver still merges. Triggers are issue labels (`agent:implement`) or scheduled pipelines, never raw API calls. Pre-18.8 GitLab versions are explicitly out of scope because of the locking bug plus feature-flag config issues tracked in GitLab incident #21171.

## Applies If (ALL must hold)

- Self-managed or GitLab.com customers (any tier with Duo) needing GitLab-native agent runs.
- Pipeline-heavy projects where CI/CD Flows (legacy pipeline conversion, fix-failing-build) compose well with Developer Flow.
- SAST-heavy workflows where false-positive filtering is the bottleneck and Code Review Flow can be tuned per security standard.
- On-prem orgs that cannot use Cloud-only platforms (Atlassian Rovo) and need an in-region agent runner.

## Skip If (ANY kills it)

- Pre-18.8 GitLab versions — locking bug and feature-flag config issues block reliable runs (incident #21171).
- Multi-cloud orgs where the agent must read context outside GitLab's data plane; Duo cannot reach that data.
- Time-critical incident response where Duo's async flow latency is too high for the SLA.
- Single-author solo projects where the flow setup overhead exceeds value.

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

- parent skill: `geek/sdlc-ai/sdlc-ai/`
