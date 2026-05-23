# SSH Hardening

## Summary

**One-sentence:** Generates a sshd_config drop-in + client config + AllowUsers list — key-only ed25519, modern crypto, second-terminal safety rule — for an Ubuntu/Debian VPS.

**One-paragraph:** Hardening sshd is a controlled risky-edit: drop-in `/etc/ssh/sshd_config.d/99-hardening.conf` with key-only auth, ed25519 host keys, modern KEX/ciphers, and AllowUsers restricted to the operator. The critical safety rule: keep a second terminal session open, reload sshd, test login in a third terminal, and only then close the original. Output: a SshPlan + the drop-in config.

**Ефективно для:**

- Fresh VPS with default sshd open to the internet.
- Adding a new user who needs SSH access — AllowUsers must update.
- Auditing existing sshd against Mozilla SSH guidelines.
- Rotating compromised host or user keys.

## Applies If (ALL must hold)

- Bootstrapping a new VPS — SSH hardening required before any other public service.
- Adding a user who needs SSH access — AllowUsers update.
- Auditing an existing server against Mozilla SSH config.
- Rotating SSH keys after a leak.

## Skip If (ANY kills it)

- Servers behind Tailscale/WireGuard with sshd not reachable from public internet (still good practice; lower urgency).
- Ephemeral containers / CI runners — hardening overhead not worth it.
- Servers with a vetted config — re-running risks lockout if the second-terminal safety sequence is skipped.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Operator ed25519 keypair | ssh-keygen -t ed25519 | operator workstation |
| Current sshd_config snapshot | file | /etc/ssh/sshd_config |
| Allowed users list | list of unix users | operator inventory |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| server-init-bootstrap | Hardening runs in phase 4 of bootstrap; this methodology defines the exact config. |
| firewall-management | UFW must allow the chosen SSH port before sshd reload. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-second-terminal-rule, r2-key-only-auth, r3-allowusers-explicit, r4-modern-crypto, r5-drop-in-config | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the SSH Hardening artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: edit-without-second-terminal, password-auth-left-on, root-permit-yes, weak-kex-algorithms | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-sshd-config` | sonnet | Per-host tweaks with safety constraints. |
| `audit-existing-sshd` | sonnet | Diff live config against rules + Mozilla baseline. |
| `render-client-config` | haiku | Template fill for ~/.ssh/config. |

## Templates

| File | Purpose |
|------|---------|
| `templates/ssh-hardening.json` | SshPlan JSON skeleton. |
| `templates/ssh-hardening.md` | Human-readable audit trail + rollback steps. |
| `templates/99-hardening.conf` | Drop-in sshd_config.d/99-hardening.conf (key-only, modern crypto, AllowUsers). |
| `templates/ssh-client-config` | Reference ~/.ssh/config with multiplexing + host alias. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ssh-hardening.py` | Validate SshPlan JSON against the schema. | Before applying drop-in to /etc/ssh/sshd_config.d/. |

## Related

- [[server-init-bootstrap]]
- [[firewall-management]]
- [[fail2ban-setup]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
