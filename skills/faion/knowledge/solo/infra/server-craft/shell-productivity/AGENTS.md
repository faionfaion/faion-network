---
slug: shell-productivity
tier: solo
group: infra
domain: server-craft
version: 1.0.0
status: draft
last_reviewed: 2026-05-20
maintainers: [faion-net]
summary: Modern CLI toolkit for Ubuntu/Debian servers replacing traditional Unix utilities with faster, more informative alternatives: bat (cat), eza (ls), fd (find), ripgrep (grep), delta (git diff), starship (prompt), zoxide (cd), fzf (fuzzy finder), btop (top), duf (df), dust (du).
content_id: "fd8b8728ef94586f"
tags: [shell, cli-tools, productivity, ubuntu, fzf]
---
# Shell Productivity

## Summary

**One-sentence:** Modern CLI toolkit for Ubuntu/Debian servers replacing traditional Unix utilities with faster, more informative alternatives: bat (cat), eza (ls), fd (find), ripgrep (grep), delta (git diff), starship (prompt), zoxide (cd), fzf (fuzzy finder), btop (top), duf (df), dust (du).

**One-paragraph:** Modern CLI toolkit for Ubuntu/Debian servers replacing traditional Unix utilities with faster, more informative alternatives: bat (cat), eza (ls), fd (find), ripgrep (grep), delta (git diff), starship (prompt), zoxide (cd), fzf (fuzzy finder), btop (top), duf (df), dust (du). Covers installation from apt and GitHub releases, Ubuntu naming conflicts (batcat/fdfind), shell integration, and fzf/bat/fd cross-wiring.

## Applies If (ALL must hold)

- Setting up a new Ubuntu VPS where default shell tools slow down daily admin
- Server rebuild: restoring the developer's modern tool stack alongside dotfiles
- Improving agent-generated shell pipelines with tools that have better output formats
- Auditing which tools are installed before writing scripts that depend on them

## Skip If (ANY kills it)

- Minimal containers or CI environments where image size matters (stick to POSIX tools)
- Scripts that must run on arbitrary servers without knowing what tools are installed
- Environments with strict package policy (air-gapped, compliance-hardened)
- Scripts checked into shared repos where others may not have the same tools

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
