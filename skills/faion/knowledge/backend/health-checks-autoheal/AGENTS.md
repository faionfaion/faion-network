# Health Checks + Auto-Heal

## Summary

**One-sentence:** Health monitoring and automatic recovery for multi-service platforms on Ubuntu 24: per-service health endpoint, journald-based check loop, systemd OnFailure auto-restart, escalation to Telegram after N retries.

**One-paragraph:** A solo VPS with 5+ services needs auto-heal: when one service crashes at 3am the operator should not be woken by every incident. systemd's `Restart=on-failure` covers process crashes; what's missing is health-endpoint failures (process up, endpoint 500). This methodology produces a per-service health-check script + systemd OnFailure hook + cron loop that restarts misbehaving services after N retries and escalates to Telegram only when auto-heal exhausts.

## Applies If (ALL must hold)

- VPS with ≥3 long-running services (API, worker, scheduler).
- Each service exposes a `/health` HTTP endpoint or equivalent.
- Operator can install jq + curl + systemd-user.

## Skip If (ANY kills it)

- Kubernetes / Nomad — they own the health-check loop.
- Single-service deploy — `Restart=on-failure` is enough.
- Pure batch workloads — no long-running service to check.

**Ефективно для:**

- Solo-stack з 3-10 systemd services що ловили крокування о 3 ночі.
- Webhook receivers де відмова обходиться у missed events.
- Команди що хочуть SRE-grade reliability без SRE-команди.
- FLOW-style monitoring: silent OK, loud FAIL.

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
| `solo/infra/server-craft/cron-automation` | Health loop runs from cron. |
| `solo/infra/server-craft/monitoring-logging` | Sibling — feeds the alert pipeline. |
| `solo/infra/server-craft/systemd-user-services` | OnFailure hook lives in systemd unit. |

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
| `templates/skeleton.md` | Health-check audit report listing endpoints + retries + escalation. |
| `templates/_smoke-test.md` | Minimum viable filled-in health audit. |
| `templates/health-check.sh` | Per-service health-check loop with retry + silent-OK + TG-on-fail. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-health-checks-autoheal.py` | Validate artefact against the JSON Schema in content/02-output-contract.xml. Stdlib-only. | On artefact change; pre-commit. |

## Related

- [[cron-automation]]
- [[monitoring-logging]]
- [[systemd-user-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable signals (input shape, scope, evidence presence, owner presence, status of prerequisites) to a concrete action, each leaf referencing a rule from `01-core-rules.xml`. Use it when in doubt about which variant of the methodology to apply.
