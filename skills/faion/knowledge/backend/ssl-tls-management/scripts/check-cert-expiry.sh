#!/usr/bin/env bash
# check-cert-expiry.sh — Report cert expiry for all configured domains, warn at 30 days
set -euo pipefail

WARN_DAYS=30
now=$(date +%s)

echo "=============================="
echo "  Certificate Expiry Report"
echo "  $(date '+%Y-%m-%d %H:%M')"
echo "=============================="

check_domain() {
    local domain="$1"
    expiry_str=$(echo | openssl s_client -connect "${domain}:443" -servername "$domain" 2>/dev/null \
        | openssl x509 -noout -enddate 2>/dev/null \
        | cut -d= -f2)

    if [ -z "$expiry_str" ]; then
        echo "  $domain — ERROR: could not connect or parse cert"
        return
    fi

    expiry_epoch=$(date -d "$expiry_str" +%s 2>/dev/null || date -j -f "%b %d %T %Y %Z" "$expiry_str" +%s 2>/dev/null)
    days_left=$(( (expiry_epoch - now) / 86400 ))

    if [ "$days_left" -le "$WARN_DAYS" ]; then
        echo "  $domain — WARNING: $days_left days left (expires $expiry_str)"
    else
        echo "  $domain — OK: $days_left days left"
    fi
}

# Check all nginx-configured domains
for conf in /etc/nginx/sites-enabled/*; do
    domains=$(grep -oP 'server_name\s+\K[^;]+' "$conf" 2>/dev/null | tr ' ' '\n' | grep -v '_' | head -3)
    for domain in $domains; do
        [ -n "$domain" ] && check_domain "$domain"
    done
done
