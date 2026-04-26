# Kernel Tuning

## Summary

sysctl parameter tuning for Ubuntu 24.04 VPS running web services and AI agent workloads. Four drop-in files under `/etc/sysctl.d/`: network performance (BBR + TCP buffers), agent tuning (inotify watches), memory management (swappiness), and security hardening. Apply with `sudo sysctl --system`. The critical non-obvious rule: inotify `max_user_watches` defaults to 65536 — Claude Code exhausts this on large codebases, causing "No space left on device" errors on file watchers.

## Why

Default kernel parameters are conservative and general-purpose. A VPS running AI agents needs 8x the default inotify watches (524288 vs 65536); a web server benefits from BBR congestion control (~18% throughput gain); a server with abundant RAM should set swappiness=10 to avoid unnecessary swap thrash. Files under `/etc/sysctl.d/` are processed in alphabetical order — use prefix `60-` to override distro defaults without modifying their files.

## When To Use

- New server setup: apply all four sysctl.d files as standard baseline
- Claude Code or file watchers emit "ENOSPC: inotify watches reached" — increase `fs.inotify.max_user_watches`
- Server swaps aggressively despite available RAM — set `vm.swappiness=10`
- WebSocket/API performance is below expectations — enable TCP BBR
- Hardening a production VPS against information leakage

## When NOT To Use

- Kubernetes nodes — resource limits are managed at the pod/container level, not via host sysctl
- Shared hosting where root access is not available
- Containers (Docker) — sysctl changes in containers require `--sysctl` flag or privileged mode

## Content

| File | What's inside |
|------|---------------|
| `content/01-parameters.xml` | Key parameters by category: BBR, TCP buffers, inotify, memory, security, file descriptors |
| `content/02-examples.xml` | Before/after BBR benchmarks, inotify exhaustion diagnosis, swappiness fix, connection handling for WebSockets |

## Templates

| File | Purpose |
|------|---------|
| `templates/60-network-perf.conf` | TCP BBR, buffer sizes, connection handling, keepalive |
| `templates/60-agent-tuning.conf` | inotify watches, file descriptors, process limits |
| `templates/60-memory.conf` | swappiness, dirty pages, cache pressure |
| `templates/60-security.conf` | Kernel address leakage, PTRACE, ASLR, ICMP hardening |
| `templates/99-nero.limits.conf` | Per-user PAM limits (nofile, nproc) |
| `templates/kernel-audit.sh` | Audit current values vs recommended, print diff table |
