#!/usr/bin/env bash
# pre-deploy-check.sh — Standalone pre-deploy validation
# Exits 0 if ready to deploy, 1 if any errors found.
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/workspace/repos}"
RUNTIME="${RUNTIME:-/srv/nero}"
ENV_FILE="${ENV_FILE:-$HOME/workspace/.env}"
REQUIRED_VARS=(DATABASE_URL REDIS_URL ANTHROPIC_API_KEY)
SERVICES=(nero-sdk nero-core nero-channel-web nero-channel-tg nero-web nero-infra)

errors=0; warnings=0
pass() { echo "[PASS] $*"; }
warn() { echo "[WARN] $*"; ((warnings++)) || true; }
fail() { echo "[FAIL] $*"; ((errors++)) || true; }

echo "=== Pre-Deploy Validation ==="
echo ""
echo "--- Environment ---"

[[ -f "$ENV_FILE" ]] && pass ".env exists" || fail ".env not found at $ENV_FILE"
[[ -d "$RUNTIME" ]] && pass "Runtime $RUNTIME exists" || fail "Runtime $RUNTIME not found"
[[ -d "$WORKSPACE" ]] && pass "Workspace $WORKSPACE exists" || fail "Workspace $WORKSPACE not found"

free_mb=$(df /srv --output=avail -BM 2>/dev/null | tail -1 | tr -d ' M' || echo 0)
[[ "$free_mb" -gt 1024 ]] && pass "Disk: ${free_mb}MB free" || fail "Low disk: ${free_mb}MB free (need >1024MB)"

systemctl --user status >/dev/null 2>&1 && pass "systemd user session active" || fail "no systemd user session"

python3 --version >/dev/null 2>&1 && pass "Python3: $(python3 --version)" || fail "python3 not found"

if [[ -f "$ENV_FILE" ]]; then
    for var in "${REQUIRED_VARS[@]}"; do
        grep -q "^${var}=" "$ENV_FILE" && pass "$var set" || warn "$var not in .env"
    done
fi

echo ""
echo "--- Git Status ---"
for svc in "${SERVICES[@]}"; do
    dir="$WORKSPACE/$svc"
    [[ ! -d "$dir/.git" ]] && continue
    if git -C "$dir" diff-index --quiet HEAD -- 2>/dev/null; then
        pass "$svc: clean"
    else
        warn "$svc: uncommitted changes"
    fi
done

echo ""
echo "--- Backing Services ---"
redis_url="${REDIS_URL:-redis://127.0.0.1:6379}"
redis_host=$(echo "$redis_url" | sed 's|redis://||; s|:.*||')
redis_port=$(echo "$redis_url" | sed 's|.*:||; s|/.*||')
redis-cli -h "$redis_host" -p "$redis_port" ping 2>/dev/null | grep -q PONG && pass "Redis: responding" || warn "Redis not responding at $redis_url"

echo ""
echo "=== Results: $errors errors, $warnings warnings ==="
if [[ $errors -gt 0 ]]; then
    echo "NOT ready to deploy."
    exit 1
else
    echo "Ready to deploy."
fi
