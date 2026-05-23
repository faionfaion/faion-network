<!-- purpose: fail2ban audit report listing jail + port + backend + escalation + whitelist + alert. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# fail2ban — Audit Report

## Host

- hostname:
- sshd_port:

## Jail sshd

- backend: nftables
- port: <sshd_port>
- maxretry: 4
- findtime: 10m
- bantime: 1h, increment, factor 4
- ignoreip: 127.0.0.1/8 + WG subnet
- action: alert TG on ban

## Verify

- `fail2ban-client status sshd`
- `journalctl -u fail2ban -n 50`

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
