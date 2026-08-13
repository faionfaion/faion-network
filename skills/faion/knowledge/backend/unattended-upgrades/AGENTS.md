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

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

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

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/unattended-upgrades.json`

```json
{
  "artefact_id": "upgrades-<host>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "allowed_origins": [
    "${distro_id}:${distro_codename}-security"
  ],
  "auto_reboot": true,
  "reboot_time": "04:00",
  "mail_to": "<ops@example.com>",
  "owner": "<@handle>"
}
```

### `templates/50unattended-upgrades.conf`

```conf
// /etc/apt/apt.conf.d/50unattended-upgrades
// Production config: security origins, Docker blacklist, auto-reboot at 04:00, cleanup

Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}";
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";
    "${distro_id}ESM:${distro_codename}-infra-security";
};

Unattended-Upgrade::Package-Blacklist {
    "docker-ce";
    "docker-ce-cli";
    "containerd.io";
    "docker-buildx-plugin";
    "docker-compose-plugin";
    // "postgresql-16";
    // "nginx";
};

Unattended-Upgrade::Automatic-Reboot           "true";
Unattended-Upgrade::Automatic-Reboot-WithUsers "true";
Unattended-Upgrade::Automatic-Reboot-Time      "04:00";

Unattended-Upgrade::Remove-Unused-Dependencies     "true";
Unattended-Upgrade::Remove-New-Unused-Dependencies "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages  "true";
Unattended-Upgrade::MinimalSteps                   "true";
Unattended-Upgrade::AutoFixInterruptedDpkg         "true";

Unattended-Upgrade::SyslogEnable   "true";
Unattended-Upgrade::SyslogFacility "daemon";

Dpkg::Options {
    "--force-confdef";
    "--force-confold";
};
```

### `templates/20auto-upgrades.conf`

```conf
// /etc/apt/apt.conf.d/20auto-upgrades
// Schedule: daily update check, download, install, weekly autoclean

APT::Periodic::Update-Package-Lists         "1";
APT::Periodic::Download-Upgradeable-Packages "1";
APT::Periodic::Unattended-Upgrade           "1";
APT::Periodic::AutocleanInterval            "7";
```

### `templates/apt-daily-timer-override.conf`

```conf
# /etc/systemd/system/apt-daily.timer.d/override.conf
# Fix apt-daily timer to run at exactly 2 AM (not random 6h window)
# Apply: sudo systemctl daemon-reload && sudo systemctl restart apt-daily.timer

[Timer]
OnCalendar=
OnCalendar=*-*-* 02:00:00
RandomizedDelaySec=0
```

### `templates/apt-daily-upgrade-timer-override.conf`

```conf
# /etc/systemd/system/apt-daily-upgrade.timer.d/override.conf
# Fix apt-daily-upgrade timer to run at exactly 3 AM (after apt-daily at 2 AM)
# Apply: sudo systemctl daemon-reload && sudo systemctl restart apt-daily-upgrade.timer

[Timer]
OnCalendar=
OnCalendar=*-*-* 03:00:00
RandomizedDelaySec=0
```
