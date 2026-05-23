# Dotfiles Management with GNU Stow

## Summary

**One-sentence:** Git-based dotfiles using GNU stow for symlinks: per-tool subdir (bash/, vim/, tmux/), .stowrc for ignore patterns, install procedure on fresh machine, secret separation (private repo vs public).

**One-paragraph:** Dotfiles drift between machines is the root of 'works on my laptop' bugs; manual symlinking is error-prone. GNU stow turns a git repo into per-machine reproducible config in two commands (`git clone && stow -t ~ */`). This methodology produces a verified dotfiles repo report: stow-able directory shape, secret separation, install runbook, and rollback path (`stow -D`).

## Applies If (ALL must hold)

- Operator uses >1 machine (laptop + VPS + maybe second laptop).
- Operator can use git + GNU stow (`apt install stow`).
- Configurations are file-based (not GUI / OS-keychain).

## Skip If (ANY kills it)

- Single machine, no plans for second.
- All config managed via Ansible / Chef / Nix.
- Configs include too many machine-specific paths to template.

**Ефективно для:**

- Solo-розробники з laptop + VPS + рідко-MacBook setup.
- Onboard new machine за 5 хвилин: `git clone && stow */`.
- Розділення public dotfiles (на GitHub) від приватних (1Password vault).
- Команди що хочуть team-shared base dotfiles + personal overrides.

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
| `solo/infra/server-craft/bash-aliases` | .bash_aliases is a dotfile. |
| `solo/infra/server-craft/secrets-management` | Secrets live OUTSIDE dotfiles repo. |

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
| `templates/skeleton.md` | Dotfiles audit listing layout + secret separation + install + override. |
| `templates/_smoke-test.md` | Minimum viable filled-in dotfiles audit. |
| `templates/install.sh` | Dotfiles install script: stow per-tool with conflict-aware backups. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-dotfiles-management.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[bash-aliases]]
- [[secrets-management]]
- [[shell-productivity]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
