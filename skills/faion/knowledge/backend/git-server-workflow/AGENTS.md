# Git Server Workflow (Workspace ↔ Runtime)

## Summary

**One-sentence:** Workspace/runtime separation pattern: source in ~/workspace/repos/<name>, runtime in /srv/<project>, rsync as the deploy boundary, no live edits in /srv, git-tagged releases, deploy.sh as the single deploy entrypoint.

**One-paragraph:** The biggest solo-ops mistake is editing files directly in /srv (the runtime); the change works for an hour, the next deploy clobbers it, and the only record of what changed lives in muscle memory. This methodology codifies the separation: source code lives in ~/workspace/repos/<name>, runtime lives in /srv/<project>, every change crosses the boundary via deploy.sh + rsync, and the runtime is never edited live.

## Applies If (ALL must hold)

- Single-VPS deploy where source + runtime share the same host.
- Operator deploys ≥1 service per week (frequent enough to justify discipline).
- Services include any state worth preserving across deploys.

## Skip If (ANY kills it)

- Container-only deploys (everything is rebuilt from Dockerfile).
- Managed PaaS — Vercel / Railway handles the boundary.
- Read-only servers (golden image + image swap).

**Ефективно для:**

- Solo VPS-фаундери що ловили 'працювало вчора' bugs.
- Команди де новачок 'просто змінив у /srv' і ламав release.
- Reproducible-build discipline для compliance.
- Onboarding doc: де source vs де runtime.

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
| `solo/infra/server-craft/deploy-scripts` | deploy.sh is the boundary tool. |
| `solo/infra/server-craft/dotfiles-management` | ~/workspace conventions. |

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
| `templates/skeleton.md` | Workspace/runtime separation audit report. |
| `templates/_smoke-test.md` | Minimum viable filled-in workflow audit. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-git-server-workflow.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[deploy-scripts]]
- [[dotfiles-management]]
- [[systemd-user-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
