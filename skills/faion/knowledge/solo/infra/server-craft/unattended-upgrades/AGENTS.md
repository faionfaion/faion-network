---
slug: unattended-upgrades
tier: solo
group: infra
domain: backend
version: 1.1.0
status: active
last_reviewed: 2026-05-23
maintainers: [faion-network]
summary: Generates an unattended-upgrades policy — security only, reboot window, mail-on-failure — gated by an upgrade-status report + reboot-required check.
content_id: "fd277815148a2fb0"
complexity: medium
produces: config
est_tokens: 4300
tags: ["unattended-upgrades", "apt", "security", "ubuntu", "auto-patch"]
---
# Unattended Upgrades

## Summary

**One-sentence:** Generates an unattended-upgrades policy — security only, reboot window, mail-on-failure — gated by an upgrade-status report + reboot-required check.

**One-paragraph:** Auto-applying security updates without auto-rebooting at the wrong time is the right default for a solo VPS. This methodology pins the apt policy (Ubuntu-Security only, no `-updates` package class), the reboot window (Sunday 04:00), the failure mail address, and an explicit reboot-required check the operator can read. Output: an UpgradePlan + the two drop-in configs.

**Ефективно для:**

- Solo VPS with no patching schedule.
- Boxes that have shipped CVE-laden binaries because security updates lagged.
- Operators who don't want to apt-upgrade by hand weekly.
- Audit against existing upgrade posture.

## Applies If (ALL must hold)

- Solo VPS running Ubuntu/Debian.
- Operator wants security-only auto-patches (not full upgrades).
- Service tolerance for an automatic reboot in a chosen window.
- Failure notifications wired to a real inbox / tg channel.

## Skip If (ANY kills it)

- Compliance environment with change-control board approval required.
- Machines under config-management (Ansible/Puppet) already patching.
- Hosts where automatic reboot is unacceptable (e.g. single-instance DB).

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Reboot window | day + time | operator preference |
| Failure mail / tg path | address or chat id | monitoring |
| Package classes to auto-patch | list | ubuntu apt origins |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| monitoring-logging | Failure mail / tg path comes from monitoring plan. |
| systemd-user-services | Auto-reboot impacts unit availability — operator must understand. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-security-only, r2-reboot-window-explicit, r3-failure-mail-required, r4-named-owner, r5-reboot-required-check | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the Unattended Upgrades artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: all-updates-not-security, no-failure-mail, mid-day-reboot, no-reboot-check | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-upgrade-plan` | sonnet | Per-host decision on classes + window. |
| `render-config-files` | haiku | Template fill. |

## Templates

| File | Purpose |
|------|---------|
| `templates/unattended-upgrades.json` | UpgradePlan JSON skeleton. |
| `templates/unattended-upgrades.md` | Human-readable audit trail. |
| `templates/50unattended-upgrades.conf` | Reference /etc/apt/apt.conf.d/50unattended-upgrades. |
| `templates/20auto-upgrades.conf` | Reference /etc/apt/apt.conf.d/20auto-upgrades (enables timer). |
| `templates/apt-daily-timer-override.conf` | Override apt-daily.timer window. |
| `templates/apt-daily-upgrade-timer-override.conf` | Override apt-daily-upgrade.timer window. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-unattended-upgrades.py` | Validate UpgradePlan JSON against the schema. | Pre-apply + monthly audit. |
| `scripts/check-reboot-required.sh` | Exit 1 if /var/run/reboot-required present. | Daily cron. |
| `scripts/upgrade-status.sh` | Summarises last-run + pending updates from journal. | On demand + weekly digest. |

## Related

- [[monitoring-logging]]
- [[systemd-user-services]]
- [[server-init-bootstrap]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
