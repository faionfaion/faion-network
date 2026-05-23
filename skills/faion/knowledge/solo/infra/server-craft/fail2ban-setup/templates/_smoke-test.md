<!-- purpose: Minimum viable filled-in fail2ban audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# fail2ban — Audit Report

## Host

- hostname: faion-net
- sshd_port: 22022

## Jail sshd

- backend: nftables
- port: 22022
- maxretry: 4
- findtime: 10m
- bantime: 1h, increment, factor 4
- ignoreip: 127.0.0.1/8 10.66.66.0/24
- action: telegram-alert

## Verify

- `fail2ban-client status sshd` → 14 banned today
- `journalctl -u fail2ban -n 50` → alerts firing

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
