---
slug: github-repo-bootstrap
tier: free
group: dev
domain: dev
version: 1.1.0
status: active
last_reviewed: 2026-05-22
maintainers: [faion-network]
summary: Bootstraps a GitHub repo via gh CLI with visibility, license, branch protection, CI, Dependabot, templates, secrets, squash-only merges — emitting an idempotent bootstrap script.
content_id: "ef93ac8b020eead1"
complexity: medium
produces: config
est_tokens: 3700
tags: [github, repo, bootstrap, gh-cli, devtools]
---
# GitHub Repo Bootstrap

## Summary

**One-sentence:** Emits an idempotent bash script that creates / configures a GitHub repo with sensible defaults via gh CLI in under 20 commands.

**One-paragraph:** Bootstrapping a repo by clicking through the GitHub UI is slow, error-prone, and unauditable. This methodology emits a single idempotent bootstrap script using `gh` CLI: creates the repo, sets visibility, license, default branch, applies branch protection (≥1 reviewer + CI required + no force-push), wires Dependabot, drops CI workflow scaffolding (lint + test), adds issue / PR templates, sets required secrets, and switches merge mode to squash-only. Re-running is safe.

**Ефективно для:**

- Net-new репо: 20-команд скрипт замість 30 кліків в UI.
- Шаблон для starter-kit (10 faion-starters): один bootstrap.sh адаптується.
- Org-wide hygiene audit: запустити bootstrap.sh у dry-run для перевірки drift.
- Disaster recovery: restore repo from scratch with all settings intact.

## Applies If (ALL must hold)

- GitHub is the target platform.
- `gh` CLI is installed + authenticated.
- Org / user owns the namespace (no permission blockers).

## Skip If (ANY kills it)

- GitLab / Bitbucket / Codeberg target — wrong tool.
- Repo already configured + actively used — bootstrap is destructive on already-set rules.
- Enterprise restricts `gh repo create` to a wrapper script — defer to enterprise tool.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Repo name + namespace | string | owner decision |
| Visibility | enum | private / public / internal |
| License choice | SPDX id | team policy |
| CI stack | string | language detection or owner choice |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| none | Standalone — no upstream artefacts required. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 rules: idempotent, gh-cli-primary, squash-only, protect-default-branch, secrets-via-secrets-not-env | 1000 |
| `content/02-output-contract.xml` | essential | JSON Schema for bootstrap config | 800 |
| `content/03-failure-modes.xml` | essential | 3 antipatterns: ui-clickops, secrets-in-env, non-idempotent | 700 |
| `content/04-procedure.xml` | essential | 5-step bootstrap procedure | 700 |
| `content/06-decision-tree.xml` | essential | Visibility + license + ci tree | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `detect_stack` | haiku | Lockfile inspection. |
| `draft_bootstrap_script` | sonnet | Per-input customisation. |
| `dry_run` | haiku | Deterministic — runs gh commands with --dry-run. |

## Templates

| File | Purpose |
|------|---------|
| `templates/bootstrap-script.sh` | Idempotent bash bootstrap |
| `templates/dependabot.yml` | Dependabot config template |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-github-repo-bootstrap.py` | Validate bootstrap config + verify gh CLI present | Before running bootstrap |

## Related

- - [[code-review-process]] — branch protection + PR template come from there.
- - [[documentation]] — bootstrap drops a starter AGENTS.md.

## Decision tree

See `content/06-decision-tree.xml`. Branches on visibility (private/public/internal) → license auto-pick; then on detected stack → CI workflow template; then on team-size → required-reviewer count.
