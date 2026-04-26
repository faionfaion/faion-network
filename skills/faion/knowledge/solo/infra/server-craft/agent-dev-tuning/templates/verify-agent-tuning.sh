#!/usr/bin/env bash
# verify-agent-tuning.sh — Verify all agent tuning is applied, print OK/LOW per item
set -euo pipefail

ok=0; low=0
check() {
    local label="$1" actual="$2" op="$3" expected="$4"
    local status
    case "$op" in
        ge) [[ "$actual" -ge "$expected" ]] 2>/dev/null && status="OK" || { status="LOW"; ((low++)) || true; } ;;
        le) [[ "$actual" -le "$expected" ]] 2>/dev/null && status="OK" || { status="HIGH"; ((low++)) || true; } ;;
        eq) [[ "$actual" == "$expected" ]] && status="OK" || { status="MISMATCH (want $expected)"; ((low++)) || true; } ;;
    esac
    [[ "$status" == "OK" ]] && ((ok++)) || true
    printf "  %-50s %-12s %s\n" "$label" "$actual" "$status"
}

echo "=== Agent Dev Tuning Verification ==="
echo ""
echo "Kernel / sysctl:"
check "fs.inotify.max_user_watches"   "$(sysctl -n fs.inotify.max_user_watches 2>/dev/null || echo 0)"   ge  524288
check "fs.inotify.max_user_instances" "$(sysctl -n fs.inotify.max_user_instances 2>/dev/null || echo 0)" ge  1024
check "fs.file-max"                   "$(sysctl -n fs.file-max 2>/dev/null || echo 0)"                   ge  2097152
check "vm.swappiness"                 "$(sysctl -n vm.swappiness 2>/dev/null || echo 60)"                le  10
check "vm.max_map_count"              "$(sysctl -n vm.max_map_count 2>/dev/null || echo 0)"              ge  1048576

echo ""
echo "Swap:"
swap_total=$(free | awk '/^Swap:/{print $2}')
if [[ "$swap_total" -gt 3000000 ]]; then
    echo "  Swap total: $(free -h | awk '/^Swap:/{print $2}')                                   OK"
    ((ok++)) || true
else
    echo "  Swap total: $(free -h | awk '/^Swap:/{print $2}')                                   LOW (want >= 4G)"
    ((low++)) || true
fi

echo ""
echo "PAM limits (current session):"
nofile_soft=$(ulimit -n)
check "nofile (soft)"  "$nofile_soft"  ge  65535

echo ""
echo "tmux linger:"
linger=$(loginctl show-user "$(whoami)" 2>/dev/null | grep Linger | cut -d= -f2 || echo "no")
if [[ "$linger" == "yes" ]]; then
    echo "  loginctl linger                                     yes          OK"
    ((ok++)) || true
else
    echo "  loginctl linger                                     no           LOW (run: loginctl enable-linger $(whoami))"
    ((low++)) || true
fi

echo ""
printf "Results: %d OK, %d issues\n" "$ok" "$low"
[[ $low -eq 0 ]] && echo "All agent tuning applied." || echo "Fix issues above, then re-run."
