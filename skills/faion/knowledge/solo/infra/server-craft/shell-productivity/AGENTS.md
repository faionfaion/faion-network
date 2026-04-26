# Shell Productivity

## Summary

Modern CLI toolkit for Ubuntu/Debian servers replacing traditional Unix utilities with faster, more informative alternatives: bat (cat), eza (ls), fd (find), ripgrep (grep), delta (git diff), starship (prompt), zoxide (cd), fzf (fuzzy finder), btop (top), duf (df), dust (du). Covers installation from apt and GitHub releases, Ubuntu naming conflicts (batcat/fdfind), shell integration, and fzf/bat/fd cross-wiring.

## Why

Traditional Unix tools work but lack color coding, git integration, and smart defaults. For a solo developer managing multiple projects via SSH, tools like fzf (Ctrl+R history search), zoxide (frecency-based cd), and delta (side-by-side diff) save significant time daily. The modern stack is an investment that compounds with every session.

## When To Use

- Setting up a new Ubuntu VPS where default shell tools slow down daily admin
- Server rebuild: restoring the developer's modern tool stack alongside dotfiles
- Improving agent-generated shell pipelines with tools that have better output formats
- Auditing which tools are installed before writing scripts that depend on them

## When NOT To Use

- Minimal containers or CI environments where image size matters (stick to POSIX tools)
- Scripts that must run on arbitrary servers without knowing what tools are installed
- Environments with strict package policy (air-gapped, compliance-hardened)
- Scripts checked into shared repos where others may not have the same tools

## Content

| File | What's inside |
|------|---------------|
| `content/01-tools.xml` | Tool-by-tool overview, Ubuntu naming conflicts, installation commands, alias wiring |
| `content/02-integration.xml` | fzf/bat/fd cross-wiring, delta git integration, starship config, zoxide usage, agent gotchas |

## Templates

| File | Purpose |
|------|---------|
| `templates/install-cli-tools.sh` | Idempotent install script for all tools on Ubuntu 24.04 |
| `templates/starship.toml` | Minimal server-optimized starship prompt config |
| `templates/fzf-config.sh` | fzf shell integration block with bat preview and fd file source |
