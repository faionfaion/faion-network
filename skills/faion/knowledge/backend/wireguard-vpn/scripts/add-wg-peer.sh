#!/usr/bin/env bash
# add-wg-peer.sh — Add peer to running wg0 interface, generate client config and QR code
# Usage: bash add-wg-peer.sh <peer-name> <vpn-ip> [full|split]
# Example: bash add-wg-peer.sh laptop 10.0.0.2 split
set -euo pipefail

PEER_NAME="${1:?Usage: $0 <peer-name> <vpn-ip> [full|split]}"
VPN_IP="${2:?Usage: $0 <peer-name> <vpn-ip> [full|split]}"
TUNNEL_MODE="${3:-full}"

SERVER_PUBLIC_IP=$(curl -sf ifconfig.me)
SERVER_PUBKEY=$(sudo wg show wg0 public-key)
WG_PORT=$(sudo wg show wg0 listen-port)
KEY_DIR="/etc/wireguard/keys"
CLIENT_DIR="/etc/wireguard/clients"

sudo mkdir -p "$KEY_DIR" "$CLIENT_DIR"

PRIVATE_KEY=$(wg genkey)
PUBLIC_KEY=$(echo "$PRIVATE_KEY" | wg pubkey)
PRESHARED_KEY=$(wg genpsk)

echo "$PRIVATE_KEY"   | sudo tee "$KEY_DIR/${PEER_NAME}_private.key"   > /dev/null
echo "$PUBLIC_KEY"    | sudo tee "$KEY_DIR/${PEER_NAME}_public.key"     > /dev/null
echo "$PRESHARED_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_preshared.key"  > /dev/null
sudo chmod 600 "$KEY_DIR/${PEER_NAME}_private.key" "$KEY_DIR/${PEER_NAME}_preshared.key"

if [ "$TUNNEL_MODE" = "full" ]; then
    CLIENT_ALLOWED="0.0.0.0/0, ::/0"
    CLIENT_DNS="DNS = 1.1.1.1, 8.8.8.8"
else
    CLIENT_ALLOWED="10.0.0.0/24"
    CLIENT_DNS=""
fi

sudo tee "$CLIENT_DIR/${PEER_NAME}.conf" > /dev/null << EOF
[Interface]
PrivateKey = ${PRIVATE_KEY}
Address    = ${VPN_IP}/32
${CLIENT_DNS}

[Peer]
PublicKey           = ${SERVER_PUBKEY}
PresharedKey        = ${PRESHARED_KEY}
Endpoint            = ${SERVER_PUBLIC_IP}:${WG_PORT}
AllowedIPs          = ${CLIENT_ALLOWED}
PersistentKeepalive = 25
EOF

sudo chmod 600 "$CLIENT_DIR/${PEER_NAME}.conf"

sudo wg set wg0 peer "$PUBLIC_KEY" \
    preshared-key <(echo "$PRESHARED_KEY") \
    allowed-ips "${VPN_IP}/32"

echo "Peer $PEER_NAME added to wg0."
echo "Client config: $CLIENT_DIR/${PEER_NAME}.conf"
echo ""
echo "Add to /etc/wireguard/wg0.conf for persistence:"
echo "[Peer]"
echo "PublicKey    = $PUBLIC_KEY"
echo "PresharedKey = $PRESHARED_KEY"
echo "AllowedIPs   = ${VPN_IP}/32"
echo ""

if command -v qrencode &>/dev/null; then
    echo "=== QR Code ==="
    sudo cat "$CLIENT_DIR/${PEER_NAME}.conf" | qrencode -t ansiutf8
fi
