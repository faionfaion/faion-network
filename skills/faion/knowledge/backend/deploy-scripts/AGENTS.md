# Deploy Scripts for Solo VPS

## Summary

**One-sentence:** Bash deploy orchestrator: rsync source to runtime, virtualenv via `pip install -e .`, systemd reload, pre/post hooks, atomic switch, rollback path, exit-code propagation.

**One-paragraph:** Solo deploys break in predictable ways: half-rsync leaves the runtime in a Frankenstein state, pip install fails after the new code is already in place, systemd reload races with the in-flight request. This methodology produces a deploy script with the four invariants: atomic switch (rsync to staging dir, mv into place), exit-code propagation (`set -euo pipefail`), pre-deploy verify (lint + tests gate), post-deploy smoke (health endpoint must return 200).

## Applies If (ALL must hold)

- Single-VPS deploy without orchestration platform (no k8s, no Nomad).
- Runtime is Python / Node / Go service managed by systemd.
- Workspace/runtime separation (~/workspace/repo vs /srv/project).

## Skip If (ANY kills it)

- Managed platform (Vercel, Railway, Fly.io) does the deploy.
- Multi-node cluster — needs orchestration, not bash.
- Greenfield prototype without paying users — `git pull && systemctl restart` is enough.

**Ефективно для:**

- Solo VPS-фаундери з 3-10 сервісами на одному хості.
- Сервіси що повинні зберігати state під час deploy (websocket / sticky session).
- Команди де deploy.sh — це і документація операцій.
- Restore-after-failure: rollback за одну команду.

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
| `solo/infra/server-craft/git-server-workflow` | Workspace/runtime separation foundation. |
| `solo/infra/server-craft/systemd-user-services` | systemd reload patterns. |
| `solo/infra/server-craft/health-checks-autoheal` | Post-deploy smoke calls health endpoint. |

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
| `templates/skeleton.md` | Deploy script audit report listing pre-gate + atomic switch + smoke + rollback. |
| `templates/_smoke-test.md` | Minimum viable filled-in deploy audit. |
| `templates/deploy.sh` | Deploy script template with atomic switch + smoke check + rollback path. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-deploy-scripts.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[git-server-workflow]]
- [[systemd-user-services]]
- [[health-checks-autoheal]]
- [[one-person-rollback-runbook]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
