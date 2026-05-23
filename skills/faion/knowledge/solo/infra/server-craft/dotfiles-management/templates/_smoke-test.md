<!-- purpose: Minimum viable filled-in dotfiles audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Dotfiles — Audit Report

## Repo

- repo: github.com/faion/dotfiles
- branch: main
- public: yes

## Layout

- subdirs: bash/, vim/, tmux/, git/, host-faion-net/
- secret separation: 1Password vault `faion.net` referenced via op read

## Install

- `git clone && cd dotfiles && ./install.sh`
- idempotent: yes
- conflict detection: yes (backup as .bak-YYYYMMDD)

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
