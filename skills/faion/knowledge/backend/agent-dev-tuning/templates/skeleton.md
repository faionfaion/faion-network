<!-- purpose: Markdown report listing applied tuning + verify commands. -->
<!-- consumes: see content/02-output-contract.xml inputs -->
<!-- produces: artefact conforming to content/02-output-contract.xml -->
<!-- depends-on: content/01-core-rules.xml -->
<!-- token-budget-impact: ~400-1000 tokens when loaded as context -->

# Agent Dev Tuning — Report

## Host

- hostname:
- distro:
- kernel:
- agent user:

## Settings applied

| key | value | verify_cmd | expected |
|-----|-------|------------|----------|
| fs.inotify.max_user_watches | 524288 | `sysctl fs.inotify.max_user_watches` | 524288 |
| ulimit -n (soft) | 65535 | `ulimit -Sn` | 65535 |
| vm.swappiness | 10 | `sysctl vm.swappiness` | 10 |
| linger | yes | `loginctl show-user $USER` | Linger=yes |

## Worktrees

| repo | worktree dir | branch |
|------|--------------|--------|
| nero-core | ~/work/nero-core-t1 | agent/t1 |

## Sign-off

**Owner:** @handle (role)  •  **Reviewed:** YYYY-MM-DD
