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

# The EFFECTIVE sshd config, never the file. `grep 'PermitRootLogin no'
# /etc/ssh/sshd_config` matches the commented-out `#PermitRootLogin no` that
# ships by default, so a box with `PermitRootLogin yes` two lines below reported
# [OK] no root SSH. `sshd -T` resolves includes, drop-ins and defaults and
# prints one lowercase `key value` line per setting.
SSHD_EFFECTIVE="$(sudo sshd -T 2>/dev/null || true)"
SSH_PORT="$(awk '$1=="port"{print $2; exit}' <<<"$SSHD_EFFECTIVE")"
SSH_PORT="${SSH_PORT:-22}"

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
check "timezone set" "$(test "$(timedatectl show -p Timezone --value)" != UTC && echo ok || echo 'still UTC')"
check "NTP sync"     "$(test "$(timedatectl show -p NTPSynchronized --value)" = yes && echo ok || echo 'not synchronized')"
check "UFW active"   "$(grep -q '^Status: active' <<<"$(sudo ufw status)" && echo ok || echo 'inactive')"
check "SSH on a non-default port" "$(test "$SSH_PORT" != 22 && echo ok || echo 'sshd still on 22')"
check "SSH in UFW"   "$(grep -qE "(^|[[:space:]])${SSH_PORT}/tcp[[:space:]]+(LIMIT|ALLOW)" <<<"$(sudo ufw status)" && echo ok || echo "no rule for port $SSH_PORT")"
check "fail2ban running" "$(test "$(systemctl is-active fail2ban 2>/dev/null)" = active && echo ok || echo 'not running')"
check "fail2ban watches $SSH_PORT" "$(grep -qE "^\\s*port\\s*=\\s*$SSH_PORT\\b" /etc/fail2ban/jail.local 2>/dev/null && echo ok || echo 'jail watches a different port')"
check "no root SSH"  "$(grep -qx 'permitrootlogin no' <<<"$SSHD_EFFECTIVE" && echo ok || echo 'root login still enabled')"
check "no password auth" "$(grep -qx 'passwordauthentication no' <<<"$SSHD_EFFECTIVE" && echo ok || echo 'password auth still enabled')"
check "unattended-upgrades" "$(grep -q '^ii' <<<"$(dpkg -l unattended-upgrades 2>/dev/null)" && echo ok || echo 'not installed')"
check "linger enabled" "$(grep -q 'Linger=yes' <<<"$(loginctl show-user "$USER" 2>/dev/null)" && echo ok || echo 'linger not enabled')"

echo ""
echo "--- Summary: $PASS passed, $FAIL failed ---"
[ "$FAIL" -eq 0 ] && echo "Bootstrap verified." || echo "Fix failed items before proceeding."
exit "$FAIL"
