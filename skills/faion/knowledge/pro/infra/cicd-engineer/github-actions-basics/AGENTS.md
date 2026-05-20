---
slug: github-actions-basics
tier: pro
group: infra
domain: cicd-engineer
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: GitHub Actions is a CI/CD platform integrated directly into GitHub repositories.
content_id: "f0e4e52fdead7db9"
tags: [github-actions, ci-cd, automation, workflows, devops]
---
# GitHub Actions Basics

## Summary

**One-sentence:** GitHub Actions is a CI/CD platform integrated directly into GitHub repositories.

**One-paragraph:** GitHub Actions is a CI/CD platform integrated directly into GitHub repositories. It enables automated workflows triggered by events like pushes, pull requests, and releases, with support for matrix builds, reusable workflows, and extensive marketplace actions. Platform Scale (2025): 11.5 billion minutes used in public/open source projects (35% YoY growth), powering 71 million jobs per day.

## Applies If (ALL must hold)

- Projects hosted on GitHub
- Open source projects needing free CI/CD
- Teams already using GitHub ecosystem
- Workflows requiring GitHub integration (issues, PRs, releases)
- Multi-platform builds (Linux, Windows, macOS)
- Repos hosted on GitHub: GHA is the path of least resistance for CI
- Open source projects — public repos run free, including Linux/Win/Mac matrix
- Teams that want PR checks, status badges, and release automation tied directly to GitHub events
- Simple-to-medium pipelines (build, test, lint, deploy) — most workflows fit comfortably in a single .github/workflows/ci.yml
- First CI/CD setup for a project: GHA's marketplace + minimal config gets a green build in minutes

## Skip If (ANY kills it)

- Code on GitLab/Bitbucket — the native CI is a better fit
- Complex multi-team multi-repo orchestration where reusable workflows / composite actions strain — at that point evaluate true workflow engines
- Heavy long-running batch (greater than 6h on hosted runners; greater than 35 days on self-hosted with ARC) — use Argo Workflows / Airflow / Prefect
- Deeply customized agents needing persistent state — GHA runners are ephemeral; engineering around that is more work than picking a different tool

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
