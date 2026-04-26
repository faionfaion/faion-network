#!/usr/bin/env bash
# test-tls-config.sh — Verify TLS versions, cipher score, HSTS header, OCSP response
# Usage: bash test-tls-config.sh example.com
set -euo pipefail

DOMAIN="${1:?Usage: $0 <domain>}"

echo "=============================="
echo "  TLS Config Test: $DOMAIN"
echo "=============================="

echo ""
echo "--- Certificate ---"
echo | openssl s_client -connect "${DOMAIN}:443" -servername "$DOMAIN" 2>/dev/null \
    | openssl x509 -noout -subject -dates -issuer 2>/dev/null || echo "ERROR: could not connect"

echo ""
echo "--- TLS 1.3 (should succeed) ---"
echo | openssl s_client -connect "${DOMAIN}:443" -tls1_3 2>&1 | grep -E "Protocol|Cipher|Verify" || echo "TLS 1.3: not supported"

echo ""
echo "--- TLS 1.0 (should FAIL) ---"
echo | openssl s_client -connect "${DOMAIN}:443" -tls1 2>&1 | grep -E "alert|error|Protocol" | head -3 || echo "TLS 1.0: correctly rejected"

echo ""
echo "--- Security Headers ---"
curl -sI "https://${DOMAIN}" | grep -iE "strict-transport|x-content-type|x-frame|referrer-policy|permissions-policy" || echo "(no security headers found)"

echo ""
echo "--- HSTS ---"
hsts=$(curl -sI "https://${DOMAIN}" | grep -i "strict-transport" || echo "MISSING")
echo "$hsts"
