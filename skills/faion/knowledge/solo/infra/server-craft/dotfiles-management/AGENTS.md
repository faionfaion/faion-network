# Dotfiles Management

## Summary

Git-based dotfiles management using GNU stow for symlink creation. Covers repository structure with per-category packages (bash, git, tmux, vim, ssh, scripts), machine-specific overrides (machine-server/machine-workstation), bootstrap scripts for new machines, and strict privacy rules about what must never be committed.

## Why

A reproducible developer environment means a fresh server is productive in minutes, not hours. Stow creates $HOME symlinks from the repo so configs are version-controlled yet live at their expected paths. Machine-specific overrides via separate stow packages keep server and workstation configs cleanly separated without branching.

## When To Use

- Setting up a new server and need to deploy the developer's standard config
- Rebuilding a server after data loss — dotfiles bootstrap restores the dev environment
- Standardizing configuration across multiple machines (workstation + VPS)
- Version-controlling shell/editor configs for reproducibility and change tracking

## When NOT To Use

- Configs containing secrets (SSH private keys, .env files, .bash_history) — never in dotfiles
- Environments managed by Ansible/Puppet where dotfiles deployment conflicts with CM
- Shared servers where one developer's dotfiles pollute others' environments
- Disposable containers where the filesystem is ephemeral

## Content

| File | What's inside |
|------|---------------|
| `content/01-structure.xml` | Repo layout, how stow creates symlinks, package categories, machine-specific pattern |
| `content/02-privacy.xml` | What to never commit: SSH keys, .bash_history, .env, .gnupg, Claude project configs |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap.sh` | Clone repo, install stow, backup conflicts, stow all packages, detect machine type |
| `templates/gitignore-dotfiles` | .gitignore for the dotfiles repo: SSH keys, history, secrets, editor state |
