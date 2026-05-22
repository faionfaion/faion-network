---
slug: bash-aliases
tier: solo
group: infra
domain: backend
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Organized bash alias and function methodology for solo developer servers: categorized ~/.
content_id: "e519de369e7369a2"
tags: [bash, alias, shell-productivity, dotfiles, shortcuts]
---
# Bash Aliases for Solo Developer Productivity

## Summary

**One-sentence:** Organized bash alias and function methodology for solo developer servers: categorized ~/.

**One-paragraph:** Organized bash alias and function methodology for solo developer servers: categorized ~/.bash_aliases with sections for system, navigation, git, Docker, systemd, nginx, network, logs, and project-specific shortcuts. Distinguishes simple aliases from function aliases, covers completion-aware wrappers, and provides a complete 60+ alias reference.

## Applies If (ALL must hold)

- Setting up a new server or workstation where productivity shortcuts are missing
- Onboarding to a new project where project-specific aliases speed up repetitive tasks
- Auditing existing .bash_aliases for conflicts, missing completions, or undocumented shortcuts
- Consolidating ad-hoc functions scattered across .bashrc into organized alias files

## Skip If (ANY kills it)

- Environments where shell config is managed by Ansible/Chef — use those tools instead
- Shared servers with multiple users where one developer's aliases conflict with others
- Scripts and pipelines needing portability across shells (zsh, fish, sh)
- Replacing proper scripts: complex multi-step operations belong in ~/bin/ scripts

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
