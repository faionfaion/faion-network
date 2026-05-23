<!-- purpose: Minimum viable filled-in kernel-tuning audit. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Kernel Tuning — Audit Report

## Host

- hostname: faion-net
- kernel: 6.8.0-46-generic

## Drop-in

- path: /etc/sysctl.d/60-vps-tuning.conf
- in_repo: dotfiles/host-faion-net/sysctl.d

## Keys

| key | value | rationale | verify |
|-----|-------|-----------|--------|
| fs.inotify.max_user_watches | 524288 | claude-code workspace | OK |
| vm.swappiness | 10 | LLM response spikes | OK |
| net.ipv4.tcp_congestion_control | bbr | upload throughput | OK |
| net.core.default_qdisc | fq | BBR pair | OK |
| kernel.pid_max | 4194304 | parallel agents | OK |

**Owner:** @ruslan (founder)  •  **Reviewed:** 2026-05-23
