#!/usr/bin/env bash
# generate-wg-keys.sh — Generate private, public, preshared keys for a new WireGuard peer
# Usage: bash generate-wg-keys.sh <peer-name>
set -euo pipefail

PEER_NAME="${1:?Usage: $0 <peer-name>}"
KEY_DIR="/etc/wireguard/keys"

sudo mkdir -p "$KEY_DIR"

echo "=== Generating WireGuard keys for: $PEER_NAME ==="

PRIVATE_KEY=$(wg genkey)
PUBLIC_KEY=$(echo "$PRIVATE_KEY" | wg pubkey)
PRESHARED_KEY=$(wg genpsk)

echo "$PRIVATE_KEY"    | sudo tee "$KEY_DIR/${PEER_NAME}_private.key"    > /dev/null
echo "$PUBLIC_KEY"     | sudo tee "$KEY_DIR/${PEER_NAME}_public.key"     > /dev/null
echo "$PRESHARED_KEY"  | sudo tee "$KEY_DIR/${PEER_NAME}_preshared.key"  > /dev/null

sudo chmod 600 "$KEY_DIR/${PEER_NAME}_private.key" "$KEY_DIR/${PEER_NAME}_preshared.key"
sudo chmod 644 "$KEY_DIR/${PEER_NAME}_public.key"

echo "Keys saved to $KEY_DIR/"
echo ""
echo "Public key (add to server [Peer] section):"
echo "$PUBLIC_KEY"
