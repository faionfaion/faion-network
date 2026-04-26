#!/usr/bin/env bash
# nginx-audit.sh — Audit active sites, snippets, rate-limit zones, security headers, recent errors
set -euo pipefail

echo "=============================="
echo "  nginx Configuration Audit"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

echo ""
echo "--- Version ---"
nginx -v 2>&1

echo ""
echo "--- Config Test ---"
sudo nginx -t 2>&1

echo ""
echo "--- Active Sites ---"
ls -la /etc/nginx/sites-enabled/ 2>/dev/null || echo "(none)"

echo ""
echo "--- Listening Ports ---"
sudo ss -tlnp | grep nginx || echo "(nginx not listening)"

echo ""
echo "--- Snippets ---"
ls /etc/nginx/snippets/ 2>/dev/null || echo "(no snippets)"

echo ""
echo "--- Rate Limit Zones ---"
sudo nginx -T 2>/dev/null | grep limit_req_zone || echo "(none defined)"

echo ""
echo "--- Security Headers Check ---"
for site in $(ls /etc/nginx/sites-enabled/ 2>/dev/null); do
    echo "  $site:"
    printf "    HSTS:          " && grep -q "Strict-Transport-Security" "/etc/nginx/sites-enabled/$site" && echo "YES" || echo "NO"
    printf "    X-Content-Type:" && grep -q "X-Content-Type-Options"    "/etc/nginx/sites-enabled/$site" && echo "YES" || echo "NO"
    printf "    CSP:           " && grep -q "Content-Security-Policy"   "/etc/nginx/sites-enabled/$site" && echo "YES" || echo "NO"
done

echo ""
echo "--- Recent Errors ---"
sudo tail -20 /var/log/nginx/error.log 2>/dev/null || echo "(no error log)"
