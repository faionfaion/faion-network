<!-- purpose: Kernel tuning audit report listing keys + rationale + verify. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Kernel Tuning — Audit Report

## Host

- hostname:
- kernel:

## Drop-in

- path: /etc/sysctl.d/60-vps-tuning.conf
- in_repo: yes (dotfiles)

## Keys

| key | value | rationale | verify |
|-----|-------|-----------|--------|
| fs.inotify.max_user_watches | 524288 | claude-code workspace | sysctl ... |
| vm.swappiness | 10 | LLM spikes | sysctl ... |
| net.ipv4.tcp_congestion_control | bbr | throughput | sysctl ... |
| net.core.default_qdisc | fq | BBR pair | sysctl ... |

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
