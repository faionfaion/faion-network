#!/usr/bin/env bash
# purpose: Template fixture for server-init-bootstrap: verify-bootstrap.sh
# consumes: content/01-core-rules.xml
# produces: executable script
# depends-on: content/02-output-contract.xml
# token-budget-impact: small
# verify-bootstrap.sh — Post-bootstrap verification checklist
# Run as the non-root user after completing all 5 phases.
set -euo pipefail

USER="${1:-$(whoami)}"
PASS=0
FAIL=0

check() {
    local label="$1" result="$2"
    if [ "$result" = "ok" ]; then
        echo "  [OK]  $label"
        PASS=$(( PASS + 1 ))
    else
        echo "  [FAIL] $label — $result"
        FAIL=$(( FAIL + 1 ))
    fi
}

echo "=============================="
echo "  Bootstrap Verification"
echo "  $(hostname) — $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

check "hostname set" "$(hostname | grep -v localhost > /dev/null && echo ok || echo 'still localhost')"
check "timezone set" "$(timedatectl | grep -v 'UTC$' > /dev/null && echo ok || echo 'still UTC')"
check "NTP sync"     "$(timedatectl | grep -q 'synchronized: yes' && echo ok || echo 'not synchronized')"
check "UFW active"   "$(sudo ufw status | grep -q '^Status: active' && echo ok || echo 'inactive')"
check "SSH in UFW"   "$(sudo ufw status | grep -qE 'ALLOW.*2202[0-9]' && echo ok || echo 'no SSH rule')"
check "fail2ban running" "$(systemctl is-active fail2ban 2>/dev/null | grep -q active && echo ok || echo 'not running')"
check "no root SSH"  "$(grep -q 'PermitRootLogin no' /etc/ssh/sshd_config && echo ok || echo 'root login still enabled')"
check "no password auth" "$(grep -q 'PasswordAuthentication no' /etc/ssh/sshd_config && echo ok || echo 'password auth still enabled')"
check "unattended-upgrades" "$(dpkg -l unattended-upgrades 2>/dev/null | grep -q '^ii' && echo ok || echo 'not installed')"
check "linger enabled" "$(loginctl show-user $USER 2>/dev/null | grep -q 'Linger=yes' && echo ok || echo 'linger not enabled')"

echo ""
echo "--- Summary: $PASS passed, $FAIL failed ---"
[ "$FAIL" -eq 0 ] && echo "Bootstrap verified." || echo "Fix failed items before proceeding."
exit "$FAIL"
