---
slug: direnv-mise-versions
tier: solo
group: infra
domain: backend
version: 1.0.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: "Per-project environment management on Ubuntu 24: direnv for auto-load on cd, mise (formerly rtx) for Python/Node/Go/Ruby versions, .envrc + .mise.toml committed to repo, no global pollution."
content_id: "b1d3f1ccef0242aa"
complexity: medium
produces: report
est_tokens: 6000
tags: [direnv, mise, python, environment, versioning]
---
# Direnv + Mise for Per-Project Environments

## Summary

**One-sentence:** Per-project environment management on Ubuntu 24: direnv for auto-load on cd, mise (formerly rtx) for Python/Node/Go/Ruby versions, .envrc + .mise.toml committed to repo, no global pollution.

**One-paragraph:** Solo developers juggle Python 3.10 (legacy), 3.12 (current), and 3.13 (experimental) plus Node 18 LTS and 22 across 5+ repos. Without per-project env, the global PATH gets polluted, `pip install` lands in the wrong venv, and `node --version` lies about which runtime your service uses. This methodology produces a committed `.mise.toml` (versions pinned) + `.envrc` (direnv auto-load) + a verified report that each repo's runtime matches expectation.

## Applies If (ALL must hold)

- Operator has >2 repos with different language versions.
- Linux/macOS with bash/zsh shell that supports direnv hook.
- Operator can install mise (one curl line) and direnv (apt/brew).

## Skip If (ANY kills it)

- Single-language single-version environment; defaults are fine.
- CI-only workflow; direnv has no effect in non-interactive shells.
- Containerized dev (devcontainers); the container pins versions.

**Ефективно для:**

- Соло-devs з Python 3.10 + 3.12 одночасно у різних репо.
- Команди де новачок не може запустити `python manage.py` через wrong version.
- Replace pyenv + nvm + rbenv одним інструментом.
- CI-parity: однакові версії на dev і на прод.

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
| `solo/infra/server-craft/dotfiles-management` | .envrc and .mise.toml are dotfile-managed. |
| `solo/infra/server-craft/shell-productivity` | Shell hook for direnv lives in shell init. |

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
| `templates/skeleton.md` | Per-project env audit listing .mise.toml + .envrc + verify steps. |
| `templates/_smoke-test.md` | Minimum viable filled-in env audit. |
| `templates/.mise.toml` | mise.toml manifest pinning languages for the repo. |
| `templates/.envrc` | direnv envrc that activates mise + repo-local venv. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-direnv-mise-versions.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[dotfiles-management]]
- [[shell-productivity]]
- [[bash-aliases]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
