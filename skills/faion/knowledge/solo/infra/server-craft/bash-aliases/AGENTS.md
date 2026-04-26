# Bash Aliases

## Summary

Organized bash alias and function methodology for solo developer servers: categorized ~/.bash_aliases with sections for system, navigation, git, Docker, systemd, nginx, network, logs, and project-specific shortcuts. Distinguishes simple aliases from function aliases, covers completion-aware wrappers, and provides a complete 60+ alias reference.

## Why

A well-organized alias file reduces repetitive typing by 30+ keystrokes per common operation, prevents mistakes via safety aliases for destructive commands, and documents common operations in a human-readable runbook format. The aliases are the difference between `systemctl --user status nero-core nero-channel-web` and `nero-status`.

## When To Use

- Setting up a new server or workstation where productivity shortcuts are missing
- Onboarding to a new project where project-specific aliases speed up repetitive tasks
- Auditing existing .bash_aliases for conflicts, missing completions, or undocumented shortcuts
- Consolidating ad-hoc functions scattered across .bashrc into organized alias files

## When NOT To Use

- Environments where shell config is managed by Ansible/Chef — use those tools instead
- Shared servers with multiple users where one developer's aliases conflict with others
- Scripts and pipelines needing portability across shells (zsh, fish, sh)
- Replacing proper scripts: complex multi-step operations belong in ~/bin/ scripts

## Content

| File | What's inside |
|------|---------------|
| `content/01-patterns.xml` | Alias types (simple vs function), naming conventions, safety aliases, tab completion wiring |
| `content/02-antipatterns.xml` | Common mistakes: circular aliases, complex logic in aliases, missing quotes, not sourcing after changes |

## Templates

| File | Purpose |
|------|---------|
| `templates/bash_aliases` | Complete categorized ~/.bash_aliases with 60+ aliases and functions |
