#!/usr/bin/env bash
# setup-cloudflare-origin-cert.sh — Place origin cert + key in /etc/nginx/ssl/, set permissions
# Prerequisites: copy cert and key content from Cloudflare Dashboard
# Usage: bash setup-cloudflare-origin-cert.sh cert.pem key.pem
set -euo pipefail

CERT_FILE="${1:?Usage: $0 <cert.pem> <key.pem>}"
KEY_FILE="${2:?Usage: $0 <cert.pem> <key.pem>}"

SSL_DIR="/etc/nginx/ssl"
sudo mkdir -p "$SSL_DIR"

sudo cp "$CERT_FILE" "$SSL_DIR/cloudflare-origin.pem"
sudo cp "$KEY_FILE"  "$SSL_DIR/cloudflare-origin-key.pem"

sudo chmod 644 "$SSL_DIR/cloudflare-origin.pem"
sudo chmod 600 "$SSL_DIR/cloudflare-origin-key.pem"
sudo chown root:root "$SSL_DIR/cloudflare-origin.pem" "$SSL_DIR/cloudflare-origin-key.pem"

echo "Cert installed:"
echo "  $SSL_DIR/cloudflare-origin.pem"
echo "  $SSL_DIR/cloudflare-origin-key.pem"
echo ""

# Show cert expiry
sudo openssl x509 -in "$SSL_DIR/cloudflare-origin.pem" -noout -dates
echo ""
echo "Test nginx config: sudo nginx -t"
echo "Then: sudo systemctl reload nginx"
echo ""
echo "IMPORTANT: Set Cloudflare SSL mode to Full (Strict)"
