# baseline-audit

## Purpose
Scores one Hetzner Cloud box against a CIS-derived security baseline, joining the account side over the API (firewall attached, SSH open to the world, Backups paid for, snapshot age) with box-side evidence the caller already gathered, and prints only the items that fail. Use it as the gate before a box carries traffic and after any change to sshd, the firewall or the kernel knobs.

## Invoke
```
python3 {script} --spec {infra.json} [--host {name}] [--sshd-config {sshd-T.txt}] [--listeners {ss.txt}] [--sysctl {sysctl.txt}] [--evidence {evidence.json}] [--waivers {waivers.json}] [--report {audit.md}] [--json] [--self-test]
```

## Inputs
- `--spec {file}` — JSON: `admin_cidrs` (required, CIDR list), `ssh_port` (default 22), `public_ports`, `firewall`, `backup_max_age_days` (default 2), optional `hosts` map of per-host overrides and an inline waiver list. Required unless self-testing. The credential is read from the environment variable `HCLOUD_TOKEN` and nowhere else; there is no flag for it, and a project-scoped Read token is enough.
- `--host {name}` — which host in the spec to audit. Optional when the spec names exactly one.
- `--sshd-config {file}` — output of `sudo sshd -T` on the box. Optional; absent leaves every sshd item unverified, which counts as unmet.
- `--listeners {file}` — output of `sudo ss -tulpnH`. Optional, same rule.
- `--sysctl {file}` — output of `sudo sysctl -a`. Optional, same rule.
- `--evidence {file}` — JSON attestations no single command produces: `admin_user` (a proven `ssh -o BatchMode=yes` key session for a sudo non-root user), `host_firewall` (`ufw status verbose`), `unattended_upgrades` (`apt-config dump`), `intrusion_prevention` (`fail2ban-client status sshd`), `root_password_locked` (`passwd -S root` shows L), `time_sync` (`timedatectl`), `oob_escape` (you opened the Hetzner Cloud Console and saw a login prompt), `containers` (`docker ps`). Optional, same rule.
- `--waivers {file}` — JSON list of `{item, reason, expires}` replacing any in the spec. A live waiver suppresses its item; an expired one does not. Optional.
- `--report {file}` — the full item table plus one remediation line per failure, marked AUTO, AUDIT-ONLY or HOLD. Optional, nothing written by default.
- `--json` — emit the summary line as one line of JSON. Optional.
- `--self-test` — run the built-in fixtures and exit. No network, no credential. Optional.

## Outputs
- Files: `{report}` — every item with its class, status and detail, then the remediation list and the waiver ledger.
- stdout: `baseline-audit: host=X checks=N failed=F waived=W held=H -> path`, or one line of JSON.
- stderr: one line per failing item, plus waiver notes and refusals. A response body is never printed.
- Exit: `0` baseline met · `1` at least one item fails, or a failed self-test · `2` cannot run: no `--spec`, unreadable or malformed input, no such server · `3` HCLOUD_TOKEN is absent · `4` credential rejected · `5` refused by a safety guard — an expired waiver still covering a failing item, or no verified out-of-band escape while auto-fixable items fail, which holds every auto-fix · `6` vendor API error, including a rate limit past RateLimit-Reset.

## When NOT to use
- Fixing anything. Every request is a GET, no command runs on the box, and the remediation is applied by a human with a second session open.
- Auditing a Hetzner Robot dedicated server, or gathering the evidence for you. Robot is a different API with different auth and is out of scope; the evidence arrives over whatever transport you already trust.
- Deciding reachability across address families. A v4 allowlist never covers a v6 arrival and the audit says so as a finding rather than guessing.

## Cost
Zero model calls. Four GETs per run — server by name, firewall by name, backup images, snapshot images — against a 3600-request hourly account limit, so the audit is free at any cadence you would run it.
