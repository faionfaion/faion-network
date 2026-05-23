<!-- purpose: Dotfiles audit listing layout + secret separation + install + override. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Dotfiles — Audit Report

## Repo

- repo:
- branch:
- public: yes/no

## Layout

- subdirs: bash/, vim/, tmux/, git/, host-<name>/
- secret separation: secrets NOT in this repo (reference 1Password)

## Install

- `git clone && cd && ./install.sh`
- idempotent: yes
- conflict detection: yes (backup on conflict)

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
