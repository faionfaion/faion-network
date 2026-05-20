---
slug: dotfiles-management
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Git-based dotfiles management using GNU stow for symlink creation.
content_id: "dbe0c4f370723158"
tags: [dotfiles, stow, git, shell, developer-environment]
---
# Dotfiles Management

## Summary

**One-sentence:** Git-based dotfiles management using GNU stow for symlink creation.

**One-paragraph:** Git-based dotfiles management using GNU stow for symlink creation. Covers repository structure with per-category packages (bash, git, tmux, vim, ssh, scripts), machine-specific overrides (machine-server/machine-workstation), bootstrap scripts for new machines, and strict privacy rules about what must never be committed.

## Applies If (ALL must hold)

- Setting up a new server and need to deploy the developer's standard config.
- Rebuilding a server after data loss — dotfiles bootstrap restores the dev environment.
- Standardizing configuration across multiple machines (workstation + VPS).
- Version-controlling shell/editor configs for reproducibility and change tracking.

## Skip If (ANY kills it)

- Configs containing secrets (SSH private keys, .env files, .bash_history) — never in dotfiles.
- Environments managed by Ansible/Puppet where dotfiles deployment conflicts with CM.
- Shared servers where one developer's dotfiles pollute others' environments.
- Disposable containers where the filesystem is ephemeral.

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
