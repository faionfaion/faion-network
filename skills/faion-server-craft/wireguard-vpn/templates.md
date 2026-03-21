# WireGuard VPN Templates

## Server Configuration Template

```ini
# /etc/wireguard/wg0.conf
# WireGuard Server Configuration
# VPN Subnet: 10.0.0.0/24
# Server VPN IP: 10.0.0.1

[Interface]
PrivateKey = SERVER_PRIVATE_KEY_HERE
Address = 10.0.0.1/24
ListenPort = 51820

# NAT for internet access through VPN
# Replace eth0 with your actual interface (check: ip route | grep default)
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE; ip6tables -A FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE; ip6tables -D FORWARD -i wg0 -j ACCEPT; ip6tables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Do not auto-save config (manage manually)
SaveConfig = false

# --- Peers ---

# Peer: Dev Laptop
[Peer]
PublicKey = LAPTOP_PUBLIC_KEY_HERE
PresharedKey = LAPTOP_PRESHARED_KEY_HERE
AllowedIPs = 10.0.0.2/32

# Peer: Home RPi (with LAN access)
[Peer]
PublicKey = RPI_PUBLIC_KEY_HERE
PresharedKey = RPI_PRESHARED_KEY_HERE
AllowedIPs = 10.0.0.3/32, 192.168.1.0/24
PersistentKeepalive = 25

# Peer: Phone
[Peer]
PublicKey = PHONE_PUBLIC_KEY_HERE
PresharedKey = PHONE_PRESHARED_KEY_HERE
AllowedIPs = 10.0.0.4/32
```

## Client Configuration Template: Linux

```ini
# /etc/wireguard/wg0.conf
# WireGuard Client Configuration (Linux)
# Full tunnel: all traffic through VPN

[Interface]
PrivateKey = CLIENT_PRIVATE_KEY_HERE
Address = 10.0.0.2/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
PresharedKey = CLIENT_PRESHARED_KEY_HERE
Endpoint = SERVER_PUBLIC_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

## Client Configuration Template: Split Tunnel

```ini
# /etc/wireguard/wg0.conf
# WireGuard Client Configuration (Split Tunnel)
# Only VPN and home LAN traffic through VPN

[Interface]
PrivateKey = CLIENT_PRIVATE_KEY_HERE
Address = 10.0.0.2/32

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
PresharedKey = CLIENT_PRESHARED_KEY_HERE
Endpoint = SERVER_PUBLIC_IP:51820
AllowedIPs = 10.0.0.0/24, 192.168.1.0/24
PersistentKeepalive = 25
```

## Client Configuration Template: macOS

```ini
# wg0.conf for macOS
# Import via WireGuard app or wg-quick

[Interface]
PrivateKey = CLIENT_PRIVATE_KEY_HERE
Address = 10.0.0.2/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
PresharedKey = CLIENT_PRESHARED_KEY_HERE
Endpoint = SERVER_PUBLIC_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

## Client Configuration Template: iOS/Android

```ini
# mobile.conf
# Scan as QR code in WireGuard mobile app
# Generate QR: qrencode -t ansiutf8 < mobile.conf

[Interface]
PrivateKey = MOBILE_PRIVATE_KEY_HERE
Address = 10.0.0.4/32
DNS = 1.1.1.1

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
PresharedKey = MOBILE_PRESHARED_KEY_HERE
Endpoint = SERVER_PUBLIC_IP:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

## Key Generation Script

```bash
#!/bin/bash
# generate-wg-keys.sh
# Generate WireGuard key pair and preshared key for a new peer

set -euo pipefail

PEER_NAME="${1:?Usage: $0 <peer-name>}"
KEY_DIR="/etc/wireguard/keys"

sudo mkdir -p "$KEY_DIR"

echo "=== Generating WireGuard keys for: $PEER_NAME ==="

# Generate private key
PRIVATE_KEY=$(wg genkey)
echo "$PRIVATE_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_private.key" > /dev/null

# Derive public key
PUBLIC_KEY=$(echo "$PRIVATE_KEY" | wg pubkey)
echo "$PUBLIC_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_public.key" > /dev/null

# Generate preshared key
PRESHARED_KEY=$(wg genpsk)
echo "$PRESHARED_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_preshared.key" > /dev/null

# Set permissions
sudo chmod 600 "$KEY_DIR/${PEER_NAME}_private.key"
sudo chmod 600 "$KEY_DIR/${PEER_NAME}_preshared.key"
sudo chmod 644 "$KEY_DIR/${PEER_NAME}_public.key"

echo ""
echo "Keys generated:"
echo "  Private:   $KEY_DIR/${PEER_NAME}_private.key"
echo "  Public:    $KEY_DIR/${PEER_NAME}_public.key"
echo "  Preshared: $KEY_DIR/${PEER_NAME}_preshared.key"
echo ""
echo "Public key: $PUBLIC_KEY"
echo "(Share this with the peer's server config)"
```

## Add Peer Script

```bash
#!/bin/bash
# add-wg-peer.sh
# Add a new peer to WireGuard server and generate client config

set -euo pipefail

PEER_NAME="${1:?Usage: $0 <peer-name> <vpn-ip> [full|split]}"
VPN_IP="${2:?Usage: $0 <peer-name> <vpn-ip> [full|split]}"
TUNNEL_MODE="${3:-full}"

SERVER_PUBLIC_IP=$(curl -s ifconfig.me)
SERVER_PUBKEY=$(sudo cat /etc/wireguard/keys/server_public.key 2>/dev/null || sudo wg show wg0 public-key)
WG_PORT=$(sudo wg show wg0 listen-port 2>/dev/null || echo "51820")
KEY_DIR="/etc/wireguard/keys"
CLIENT_DIR="/etc/wireguard/clients"

sudo mkdir -p "$KEY_DIR" "$CLIENT_DIR"

echo "=== Adding WireGuard peer: $PEER_NAME ($VPN_IP) ==="

# Generate keys for new peer
PRIVATE_KEY=$(wg genkey)
PUBLIC_KEY=$(echo "$PRIVATE_KEY" | wg pubkey)
PRESHARED_KEY=$(wg genpsk)

# Save keys
echo "$PRIVATE_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_private.key" > /dev/null
echo "$PUBLIC_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_public.key" > /dev/null
echo "$PRESHARED_KEY" | sudo tee "$KEY_DIR/${PEER_NAME}_preshared.key" > /dev/null
sudo chmod 600 "$KEY_DIR/${PEER_NAME}_private.key" "$KEY_DIR/${PEER_NAME}_preshared.key"

# Determine AllowedIPs for client config
if [ "$TUNNEL_MODE" = "full" ]; then
    CLIENT_ALLOWED_IPS="0.0.0.0/0, ::/0"
    CLIENT_DNS="DNS = 1.1.1.1, 8.8.8.8"
else
    CLIENT_ALLOWED_IPS="10.0.0.0/24"
    CLIENT_DNS=""
fi

# Generate client config
sudo tee "$CLIENT_DIR/${PEER_NAME}.conf" > /dev/null << EOF
# WireGuard Client: $PEER_NAME
# Mode: $TUNNEL_MODE tunnel

[Interface]
PrivateKey = $PRIVATE_KEY
Address = ${VPN_IP}/32
${CLIENT_DNS}

[Peer]
PublicKey = $SERVER_PUBKEY
PresharedKey = $PRESHARED_KEY
Endpoint = ${SERVER_PUBLIC_IP}:${WG_PORT}
AllowedIPs = $CLIENT_ALLOWED_IPS
PersistentKeepalive = 25
EOF

sudo chmod 600 "$CLIENT_DIR/${PEER_NAME}.conf"

# Add peer to running interface
sudo wg set wg0 peer "$PUBLIC_KEY" \
    preshared-key <(echo "$PRESHARED_KEY") \
    allowed-ips "${VPN_IP}/32"

echo ""
echo "Peer added to running interface."
echo "Client config: $CLIENT_DIR/${PEER_NAME}.conf"
echo ""
echo "IMPORTANT: Also add this peer to /etc/wireguard/wg0.conf for persistence:"
echo ""
echo "# Peer: $PEER_NAME"
echo "[Peer]"
echo "PublicKey = $PUBLIC_KEY"
echo "PresharedKey = $PRESHARED_KEY"
echo "AllowedIPs = ${VPN_IP}/32"
echo ""

# Generate QR code if qrencode is available
if command -v qrencode &>/dev/null; then
    echo "=== QR Code (scan in WireGuard mobile app) ==="
    sudo cat "$CLIENT_DIR/${PEER_NAME}.conf" | qrencode -t ansiutf8
fi
```

## Site-to-Site Template (Home Gateway)

```ini
# /etc/wireguard/wg0.conf on Home RPi/Gateway
# Bridges home LAN to VPS WireGuard network

[Interface]
PrivateKey = HOME_GATEWAY_PRIVATE_KEY_HERE
Address = 10.0.0.3/32

# Forward traffic between wg0 and local LAN
# Replace eth0 with your LAN interface
PostUp = iptables -A FORWARD -i wg0 -o eth0 -j ACCEPT; iptables -A FORWARD -i eth0 -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -o eth0 -j ACCEPT; iptables -D FORWARD -i eth0 -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = SERVER_PUBLIC_KEY_HERE
PresharedKey = HOME_PRESHARED_KEY_HERE
Endpoint = SERVER_PUBLIC_IP:51820
# Route VPN subnet + other site LANs through VPN
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

## Sysctl Template for WireGuard

```ini
# /etc/sysctl.d/99-wireguard.conf
# IP forwarding for WireGuard VPN

# IPv4 forwarding
net.ipv4.ip_forward = 1

# IPv6 forwarding (if using IPv6 in VPN)
net.ipv6.conf.all.forwarding = 1
```
