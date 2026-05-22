---
slug: git-server-workflow
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Workspace/runtime separation pattern for solo VPS deployments: source code lives in `~/workspace/repos/`, services run from `/srv/project/`.
content_id: "775c0c871927405d"
tags: [git, deploy, workflow, vps, rsync]
---
# Git Server Workflow

## Summary

**One-sentence:** Workspace/runtime separation pattern for solo VPS deployments: source code lives in `~/workspace/repos/`, services run from `/srv/project/`.

**One-paragraph:** Workspace/runtime separation pattern for solo VPS deployments: source code lives in `~/workspace/repos/`, services run from `/srv/project/`. Deploy with rsync (not `git pull` to runtime). Rollback by checking out a previous commit in the workspace repo and redeploying. Git worktrees enable parallel agent work on the same repository without branch conflicts.

## Applies If (ALL must hold)

- Solo VPS with multiple services (Python/Node apps + shared SDK)
- Need to deploy from workspace to server without CI/CD
- Need quick rollback (`git checkout HEAD~1 && deploy.sh service`)
- Running multiple parallel Claude Code agents on the same repo (worktrees)
- Push-to-deploy via post-receive hook on a bare server repo

## Skip If (ANY kills it)

- Multi-server deployments — rsync from one machine to many is unwieldy; use Ansible or Capistrano
- When the team uses Docker for the application (use image tags + `docker compose up` instead)
- Monorepos where workspace and runtime are the same directory (no separation needed)

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

- parent skill: `solo/infra/server-craft/`
