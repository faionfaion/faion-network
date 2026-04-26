#!/usr/bin/env bash
# kernel-audit.sh — Audit current sysctl values vs recommended baseline
# Prints OK / LOW / HIGH for each parameter
set -euo pipefail

# Format: "parameter" "operator" "recommended_value" "label"
# operator: ge (>=), le (<=), eq (=)
CHECKS=(
    "fs.inotify.max_user_watches      ge  524288  inotify watches (agent workloads)"
    "fs.inotify.max_user_instances    ge  1024    inotify instances"
    "fs.file-max                      ge  2097152 system file descriptor max"
    "vm.swappiness                    le  10      swap aggressiveness"
    "vm.max_map_count                 ge  1048576 memory map areas"
    "vm.dirty_ratio                   le  15      dirty page ratio"
    "net.core.somaxconn               ge  65535   listen() backlog"
    "net.core.rmem_max                ge  16777216 TCP receive buffer max"
    "net.core.wmem_max                ge  16777216 TCP send buffer max"
    "kernel.kptr_restrict             eq  1        hide kernel addresses"
    "kernel.yama.ptrace_scope         eq  1        restrict ptrace"
    "kernel.dmesg_restrict            eq  1        restrict dmesg"
    "net.ipv4.tcp_syncookies          eq  1        SYN cookies"
    "net.ipv4.conf.all.accept_redirects eq 0       ignore ICMP redirects"
)

ok=0; issues=0
printf "%-55s %-12s %-12s %s\n" "PARAMETER" "CURRENT" "RECOMMENDED" "STATUS"
printf '%s\n' "$(printf '─%.0s' {1..95})"

for check in "${CHECKS[@]}"; do
    read -r param op recommended label <<< "$check"
    current=$(sysctl -n "$param" 2>/dev/null || echo "N/A")

    if [[ "$current" == "N/A" ]]; then
        status="MISSING"
        ((issues++)) || true
    else
        case "$op" in
            ge) [[ "$current" -ge "$recommended" ]] 2>/dev/null && status="OK" || { status="LOW"; ((issues++)) || true; } ;;
            le) [[ "$current" -le "$recommended" ]] 2>/dev/null && status="OK" || { status="HIGH"; ((issues++)) || true; } ;;
            eq) [[ "$current" == "$recommended" ]] && status="OK" || { status="MISMATCH"; ((issues++)) || true; } ;;
        esac
        [[ "$status" == "OK" ]] && ((ok++)) || true
    fi

    printf "%-55s %-12s %-12s %s\n" "$param" "$current" "$recommended" "$status"
done

echo ""
printf "Results: %d OK, %d issues\n" "$ok" "$issues"
[[ $issues -eq 0 ]] && echo "All kernel parameters are within recommended range." || echo "Run: sudo sysctl --system  (after installing sysctl.d drop-ins)"
