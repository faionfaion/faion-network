---
slug: github-repo-bootstrap
tier: free
group: dev
domain: dev
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Create a new GitHub repository and configure it with production-grade defaults in one go: visibility, license,.
content_id: "5b66923ea2a7102a"
tags: [github, repo, bootstrap, gh-cli, branch-protection, dependabot, codeowners, ci]
---
# GitHub Repo Bootstrap with gh CLI

## Summary

**One-sentence:** Create a new GitHub repository and configure it with production-grade defaults in one go: visibility, license,.

**One-paragraph:** Create a new GitHub repository and configure it with production-grade defaults in one go: visibility, license, .gitignore, README, branch protection on the default branch, CI workflow stub, Dependabot, issue and PR templates, CODEOWNERS, secrets, and squash-only merges with linear history. The gh CLI is the primary tool; the Web UI is documented as fallback.

## Applies If (ALL must hold)

- Starting a brand-new project that will be shared with collaborators or shipped publicly.
- Splitting a directory out of a monorepo into its own GitHub repo.
- Handing a project off to a team and needing branch protection plus CODEOWNERS from day one.
- Releasing an open-source project and needing license, README, issue templates, and Dependabot before the first announcement.
- Standardizing existing repos with the same baseline configuration as part of a tooling sweep.

## Skip If (ANY kills it)

- Throwaway scratch repos that will never accept a PR — use `gh repo create --private --no-source` and stop there.
- Ephemeral demo repos generated for a single live presentation; the bootstrap overhead exceeds their lifespan.
- Forks where the upstream already enforces every rule you would set; configure only the deltas you need.

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

- parent skill: `free/dev/devtools-developer/`
