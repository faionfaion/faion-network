# WireGuard VPN Examples

## Example 1: VPS-to-Home Tunnel for NERO Platform

Connect a Hetzner VPS to a home Raspberry Pi, allowing the VPS to access home LAN devices and the RPi to access VPS services directly.

### Network Diagram

```
Hetzner CX53 (VPS)                    Home Network
  eth0: 203.0.113.50                    Router: 192.168.1.1
  wg0:  10.0.0.1/24                    RPi5: 192.168.1.100
    |                                    wg0: 10.0.0.3/32
    |--- UDP 51820 (internet) ---|      NAS: 192.168.1.200
    |                                   Printer: 192.168.1.50
  Dev Laptop
    wg0: 10.0.0.2/32
```

### Step 1: Server Setup (Hetzner VPS)

```bash
# Install
sudo apt install wireguard wireguard-tools qrencode

# Generate server keys
wg genkey | sudo tee /etc/wireguard/keys/server_private.key | wg pubkey | sudo tee /etc/wireguard/keys/server_public.key
sudo chmod 600 /etc/wireguard/keys/server_private.key

# Generate peer keys
for peer in laptop rpi phone; do
    wg genkey | sudo tee /etc/wireguard/keys/${peer}_private.key | wg pubkey | sudo tee /etc/wireguard/keys/${peer}_public.key
    wg genpsk | sudo tee /etc/wireguard/keys/${peer}_preshared.key
    sudo chmod 600 /etc/wireguard/keys/${peer}_private.key /etc/wireguard/keys/${peer}_preshared.key
done

# Enable IP forwarding
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf
```

```ini
# /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
SaveConfig = false

# Dev Laptop
[Peer]
PublicKey = <laptop-pubkey>
PresharedKey = <laptop-psk>
AllowedIPs = 10.0.0.2/32

# Home RPi (bridge to home LAN)
[Peer]
PublicKey = <rpi-pubkey>
PresharedKey = <rpi-psk>
AllowedIPs = 10.0.0.3/32, 192.168.1.0/24
PersistentKeepalive = 25

# Phone
[Peer]
PublicKey = <phone-pubkey>
PresharedKey = <phone-psk>
AllowedIPs = 10.0.0.4/32
```

```bash
# Open firewall port
sudo ufw allow 51820/udp

# Start and enable
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

### Step 2: Home RPi Setup

```bash
# Install on RPi
sudo apt install wireguard

# Enable IP forwarding (RPi acts as gateway to home LAN)
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf
```

```ini
# /etc/wireguard/wg0.conf on RPi
[Interface]
PrivateKey = <rpi-private-key>
Address = 10.0.0.3/32

# Bridge WireGuard traffic to home LAN
PostUp = iptables -A FORWARD -i wg0 -o eth0 -j ACCEPT; iptables -A FORWARD -i eth0 -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -o eth0 -j ACCEPT; iptables -D FORWARD -i eth0 -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey = <server-pubkey>
PresharedKey = <rpi-psk>
Endpoint = 203.0.113.50:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

```bash
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

### Step 3: Verification

```bash
# From VPS: ping RPi through WireGuard
ping 10.0.0.3

# From VPS: reach home NAS through RPi bridge
ping 192.168.1.200

# From RPi: ping VPS through WireGuard
ping 10.0.0.1

# Check tunnel status on VPS
sudo wg show
# interface: wg0
#   public key: ...
#   listening port: 51820
#
# peer: <rpi-pubkey>
#   endpoint: <home-ip>:<port>
#   allowed ips: 10.0.0.3/32, 192.168.1.0/24
#   latest handshake: 12 seconds ago
#   transfer: 1.5 MiB received, 2.3 MiB sent
```

---

## Example 2: Dev Machine Access via Split Tunnel

Access VPS services (PostgreSQL, Redis, RabbitMQ) from a development laptop without routing all internet traffic through VPN.

### Use Case

Instead of exposing database ports to the internet, only expose them on the WireGuard interface:

| Service | Public Port | VPN Access |
|---------|------------|------------|
| PostgreSQL | Closed | 10.0.0.1:5432 |
| Redis | Closed | 10.0.0.1:6379 |
| RabbitMQ | Closed | 10.0.0.1:5672 |
| RabbitMQ Management | Closed | 10.0.0.1:15672 |
| Flower | Closed | 10.0.0.1:5555 |

### Client Config (Split Tunnel)

```ini
# laptop-split.conf
[Interface]
PrivateKey = <laptop-private-key>
Address = 10.0.0.2/32

[Peer]
PublicKey = <server-pubkey>
PresharedKey = <laptop-psk>
Endpoint = 203.0.113.50:51820
AllowedIPs = 10.0.0.0/24
PersistentKeepalive = 25
```

### Server: Bind Services to WireGuard Interface

```bash
# PostgreSQL: listen on WireGuard IP
# /etc/postgresql/16/main/postgresql.conf
listen_addresses = '127.0.0.1, 10.0.0.1'

# pg_hba.conf: allow from WireGuard subnet
host    all    all    10.0.0.0/24    scram-sha-256

# Docker services: bind to WireGuard IP
# docker-compose.yml
services:
  redis:
    ports:
      - "127.0.0.1:6379:6379"
      - "10.0.0.1:6379:6379"
  rabbitmq:
    ports:
      - "127.0.0.1:5672:5672"
      - "10.0.0.1:5672:5672"
      - "10.0.0.1:15672:15672"
```

### Usage from Dev Laptop

```bash
# Connect VPN
sudo wg-quick up wg0

# Now access VPS services as if local
psql -h 10.0.0.1 -U nero -d nero_db
redis-cli -h 10.0.0.1
curl http://10.0.0.1:15672  # RabbitMQ management

# Internet traffic still goes through normal gateway
curl ifconfig.me  # shows laptop's real IP, not VPS IP
```

---

## Example 3: Mobile Phone with Full Tunnel

Route all phone traffic through VPS for privacy on public Wi-Fi.

### Generate Config and QR Code

```bash
# On server, generate client config
sudo tee /etc/wireguard/clients/phone.conf << 'EOF'
[Interface]
PrivateKey = <phone-private-key>
Address = 10.0.0.4/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server-pubkey>
PresharedKey = <phone-psk>
Endpoint = 203.0.113.50:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
EOF

# Generate QR code for mobile app
qrencode -t ansiutf8 < /etc/wireguard/clients/phone.conf
```

### On Phone

1. Install WireGuard app (iOS App Store / Google Play)
2. Tap "+" -> "Create from QR code"
3. Scan the QR code displayed in terminal
4. Name the tunnel (e.g., "VPS")
5. Activate

### Verification

```bash
# On server, check phone is connected
sudo wg show | grep -A 4 "<phone-pubkey>"
#   endpoint: <phone-ip>:<port>
#   latest handshake: 5 seconds ago
#   transfer: 500 KiB received, 1.2 MiB sent

# On phone, visit whatismyip.com - should show VPS IP
```

---

## Example 4: Restrict SSH to VPN Only

After WireGuard is working, restrict SSH access to only the VPN subnet for enhanced security.

### Update SSH Config

```bash
# /etc/ssh/sshd_config
ListenAddress 10.0.0.1
ListenAddress 127.0.0.1
# Remove or comment out: ListenAddress 0.0.0.0
```

### Update Firewall

```bash
# Remove public SSH access
sudo ufw delete allow 22/tcp

# Allow SSH only from WireGuard subnet
sudo ufw allow in on wg0 to any port 22

# Verify
sudo ufw status numbered
```

**Warning:** Always test VPN connectivity before restricting SSH. Keep a console/VNC session open as a backup when making this change on a remote server.

---

## Example 5: WireGuard Status Monitoring

Script to display WireGuard peer status, useful for tmux status bar or monitoring.

```bash
#!/bin/bash
# wg-status.sh - Show WireGuard peer status

set -euo pipefail

echo "=== WireGuard Status ==="
echo ""

# Check if interface is up
if ! sudo wg show wg0 &>/dev/null; then
    echo "wg0: DOWN"
    exit 1
fi

echo "Interface: wg0"
echo "Port: $(sudo wg show wg0 listen-port)"
echo ""

# Parse peer info
sudo wg show wg0 dump | tail -n +2 | while IFS=$'\t' read -r pubkey psk endpoint allowed_ips handshake rx tx keepalive; do
    # Determine peer name from public key (first 8 chars)
    short_key="${pubkey:0:8}..."

    # Calculate handshake age
    if [ "$handshake" != "0" ]; then
        age=$(( $(date +%s) - handshake ))
        if [ "$age" -lt 180 ]; then
            status="ACTIVE (${age}s ago)"
        else
            status="STALE ($((age / 60))m ago)"
        fi
    else
        status="NEVER CONNECTED"
    fi

    # Format transfer
    rx_mb=$(echo "scale=1; $rx / 1048576" | bc 2>/dev/null || echo "0")
    tx_mb=$(echo "scale=1; $tx / 1048576" | bc 2>/dev/null || echo "0")

    echo "Peer: $short_key | IPs: $allowed_ips | $status | RX: ${rx_mb}MB TX: ${tx_mb}MB"
done
```
