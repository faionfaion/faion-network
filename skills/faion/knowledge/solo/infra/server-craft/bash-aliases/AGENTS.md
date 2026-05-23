---
slug: bash-aliases
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Organized ~/.bash_aliases methodology: simple aliases vs functions, safety flags on destructive commands, modern-tool gating with `command -v`, tab-completion wiring, categorized sections for system / git / docker / systemd / network."
content_id: "e519de369e7369a2"
complexity: medium
produces: report
est_tokens: 6000
tags: [bash, alias, shell-productivity, dotfiles, shortcuts]
---
# Bash Aliases for Solo Developer Productivity

## Summary

**One-sentence:** Organized ~/.bash_aliases methodology: simple aliases vs functions, safety flags on destructive commands, modern-tool gating with `command -v`, tab-completion wiring, categorized sections for system / git / docker / systemd / network.

**One-paragraph:** A well-organized alias file reduces repetitive typing by 30+ keystrokes per common operation, prevents mistakes via safety aliases for destructive commands (rm -i, mv -i, cp -i), and documents common operations in a human-readable runbook format. This methodology produces a categorized, completion-aware, distro-portable alias file with verify steps for each category.

## Applies If (ALL must hold)

- Setting up a new server / workstation where productivity shortcuts are missing.
- Onboarding to a new project with repeatable operations.
- Auditing an existing ~/.bash_aliases for conflicts, missing completions, broken safety flags.

## Skip If (ANY kills it)

- Environment managed by Ansible/Chef — use those tools.
- Shared multi-user server where aliases conflict between users.
- Scripts that must be portable across shells (zsh, fish, sh).

**Ефективно для:**

- Соло-розробники що працюють у tmux 6 годин/день.
- Перехід з macOS на Linux VPS — налаштувати shell-UX за один захід.
- Команди-1-3 людей з dotfiles-репозиторієм.
- Усунути 'я забув ввести -i на rm' incidents.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Versioned space for the artefact | Git repo / wiki with history | team |
| Named owner | Person + role | team / RACI |
| Trigger event | Event / threshold / schedule | operating cadence |
| Upstream methodologies in `Assumes Loaded` | Already routine for the role | team training |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `solo/infra/server-craft/dotfiles-management` | Aliases are version-controlled in dotfiles. |
| `solo/infra/server-craft/shell-productivity` | Sibling — tmux/fzf/starship integration. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + skip-this-methodology | 1200 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid/forbidden examples | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom / root-cause / fix | 900 |
| `content/04-procedure.xml` | essential | Step-by-step procedure to apply the methodology | 900 |
| `content/05-examples.xml` | essential | Worked example from input to verified artefact | 800 |
| `content/06-decision-tree.xml` | essential | Routing tree on observable signals → rule from 01-core-rules.xml | 700 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `scaffold-report` | haiku | Template fill from inventory. |
| `populate-evidence` | sonnet | Per-row evidence link + verification. |
| `outcome-synthesis` | opus | Cross-step synthesis of outcome impact. |

## Templates

| File | Purpose |
|------|---------|
| `templates/skeleton.md` | Markdown bash-aliases audit report. |
| `templates/_smoke-test.md` | Minimum viable filled-in audit. |
| `templates/bash_aliases` | Categorized ~/.bash_aliases template with safety + gating + completion. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-bash-aliases.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[dotfiles-management]]
- [[shell-productivity]]
- [[tmux-power-user]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
