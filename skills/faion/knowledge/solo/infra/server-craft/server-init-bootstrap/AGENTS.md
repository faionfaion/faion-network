---
slug: server-init-bootstrap
tier: solo
group: infra
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates a 5-phase first-login plan for a fresh Ubuntu 24.04 VPS — access, identity, packages, hardening, services foundation — gated by SSH-key-verified non-root login.
content_id: "0f1e596c2ccc9875"
complexity: medium
produces: playbook-step
est_tokens: 4400
tags: ["server-setup", "ubuntu", "ssh", "ufw", "fail2ban"]
---
# Server Init Bootstrap

## Summary

**One-sentence:** Generates a 5-phase first-login plan for a fresh Ubuntu 24.04 VPS — access, identity, packages, hardening, services foundation — gated by SSH-key-verified non-root login.

**One-paragraph:** Fresh VPS bootstrap is a sequenced operation: create a non-root user, install your SSH key, verify login as that user, ONLY THEN disable root login and password auth. This methodology pins the 5-phase order, names the verification gate between each phase, and refuses to advance until SSH login as the new user is confirmed. Output: a BootstrapPlan + verify-bootstrap.sh report.

**Ефективно для:**

- Hetzner / DigitalOcean / Linode cx-class boxes minutes after creation.
- Operators who have locked themselves out at least once and want a checklist.
- Cloud-init user-data authoring for repeatable provisioning.
- Audit against an existing server for missing bootstrap steps.

## Applies If (ALL must hold)

- First login to any new VPS (Hetzner, DO, Linode, Vultr).
- Rebuilding a server after a breach or OS reinstall.
- Authoring cloud-init user-data for repeatable provisioning.
- Auditing an existing server against the bootstrap checklist.

## Skip If (ANY kills it)

- Managed platforms (Heroku, Railway, Render) — OS is abstracted.
- Kubernetes nodes — managed by the cluster control plane.
- Live production server already in use — only at initial setup.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| VPS IP + root credential | string + ssh key OR password | provider dashboard |
| Operator SSH public key | ed25519 pubkey | operator workstation |
| Target hostname | string | operator naming convention |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| ssh-hardening | Phase 4 hardens sshd; this methodology delegates the exact config. |
| firewall-management | Phase 4 installs UFW; delegates rule set. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-verify-user-login-first, r2-loginctl-linger, r3-fail2ban-before-internet, r4-named-hostname, r5-cloud-init-idempotent | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Server Init Bootstrap artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: disabled-root-without-verify, no-linger-systemd-dies, fail2ban-after-exposure, hostname-default-localhost | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-cloud-init` | sonnet | YAML composition with sequence constraints. |
| `audit-existing-server` | sonnet | Diff live config against the 5-phase checklist. |
| `compose-bootstrap-script` | haiku | Mechanical render from BootstrapPlan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/server-init-bootstrap.json` | BootstrapPlan JSON skeleton (phases + verifications). |
| `templates/server-init-bootstrap.md` | Human-readable audit trail. |
| `templates/bootstrap.sh` | Idempotent bootstrap script — phases 1-5 in order. |
| `templates/cloud-init.yml` | user-data for cloud-init provisioning. |
| `templates/verify-bootstrap.sh` | Post-bootstrap audit script — every gate evaluated. |
| `templates/sshd-hardened.conf` | Drop-in sshd_config.d/ file. |
| `templates/fail2ban-jail.local` | Reference fail2ban jail config. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-server-init-bootstrap.py` | Validate BootstrapPlan JSON against the schema. | Before applying to a live host. |
| `scripts/server-status.sh` | Live host status against the 5-phase rule-set. | Post-bootstrap + weekly cron. |

## Related

- [[ssh-hardening]]
- [[firewall-management]]
- [[fail2ban-setup]]
- [[systemd-user-services]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
