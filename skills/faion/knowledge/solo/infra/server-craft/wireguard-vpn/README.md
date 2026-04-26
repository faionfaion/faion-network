# WireGuard VPN

WireGuard configuration for solo developers running VPS infrastructure. Covers server setup, client configuration, routing, split tunneling, and site-to-site connections between VPS and home network.

## Overview

WireGuard is a modern VPN protocol that is simpler, faster, and more secure than OpenVPN or IPSec. It runs as a kernel module (built into Linux 5.6+) and uses state-of-the-art cryptography.

| Feature | WireGuard | OpenVPN | IPSec/IKEv2 |
|---------|-----------|---------|-------------|
| Codebase | ~4,000 lines | ~100,000 lines | ~400,000 lines |
| Protocol | UDP only | TCP or UDP | UDP (500, 4500) |
| Encryption | ChaCha20, Curve25519 | OpenSSL (configurable) | Configurable |
| Performance | Near wire speed | Moderate | Moderate |
| Configuration | Simple INI files | Complex config | Very complex |
| Roaming | Built-in | Reconnect needed | Partial |

## Key Concepts

### Cryptokey Routing

WireGuard uses a concept called "Cryptokey Routing" -- each peer has a public key and a list of allowed IPs. When a packet arrives, WireGuard checks which peer's AllowedIPs matches the destination and encrypts with that peer's key.

```
Peer A (10.0.0.1) -> AllowedIPs: 10.0.0.2/32 -> encrypts with Peer B's pubkey
Peer B (10.0.0.2) -> AllowedIPs: 10.0.0.1/32 -> encrypts with Peer A's pubkey
```

### Key Pairs

Each peer generates a key pair independently. No certificate authority needed.

```bash
# Generate private key
wg genkey > privatekey

# Derive public key
cat privatekey | wg pubkey > publickey

# Generate preshared key (optional, for post-quantum resistance)
wg genpsk > presharedkey
```

| Key Type | Purpose | Sharing |
|----------|---------|---------|
| Private key | Decrypt incoming, sign outgoing | NEVER share |
| Public key | Verify peer identity | Share with peers |
| Preshared key | Additional symmetric encryption | Share between specific peer pair |

### Network Architecture

```
VPS (WireGuard Server)
  wg0: 10.0.0.1/24
  eth0: <public-ip>
    |
    |--- UDP 51820
    |
  Peer: Dev Machine
    wg0: 10.0.0.2/32
    |
  Peer: Home RPi
    wg0: 10.0.0.3/32
    LAN: 192.168.1.0/24
    |
  Peer: Phone
    wg0: 10.0.0.4/32
```

## Server Configuration

### Interface Section

```ini
[Interface]
# Server's private key
PrivateKey = <server-private-key>

# VPN subnet address for this server
Address = 10.0.0.1/24

# UDP port to listen on
ListenPort = 51820

# NAT and forwarding rules (applied when interface goes up/down)
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Optional: save config on interface down
SaveConfig = false
```

| Field | Purpose | Notes |
|-------|---------|-------|
| PrivateKey | Server's private key | Generated with `wg genkey` |
| Address | Server's VPN IP | Use /24 for the server |
| ListenPort | UDP port | Default 51820, can change |
| PostUp | Commands run when wg0 starts | NAT for internet access |
| PostDown | Commands run when wg0 stops | Clean up NAT rules |
| SaveConfig | Auto-save peer changes | Set false for manual management |

### Peer Section

```ini
[Peer]
# Client's public key
PublicKey = <client-public-key>

# Optional preshared key
PresharedKey = <preshared-key>

# Which IPs this peer is allowed to send from
AllowedIPs = 10.0.0.2/32

# Optional: keep connection alive (for peers behind NAT)
PersistentKeepalive = 25
```

| Field | Purpose | Notes |
|-------|---------|-------|
| PublicKey | Peer's public key | From peer's `wg pubkey` |
| PresharedKey | Extra encryption layer | Optional but recommended |
| AllowedIPs | Peer's VPN IP(s) | /32 for single device |
| PersistentKeepalive | NAT keepalive interval | 25 seconds typical |

## Client Configuration

### Full Tunnel (Route All Traffic)

```ini
[Interface]
PrivateKey = <client-private-key>
Address = 10.0.0.2/32
DNS = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey = <server-public-key>
PresharedKey = <preshared-key>
Endpoint = <server-public-ip>:51820
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

`AllowedIPs = 0.0.0.0/0` routes ALL traffic through VPN (full tunnel).

### Split Tunnel (Only VPN Traffic)

```ini
[Interface]
PrivateKey = <client-private-key>
Address = 10.0.0.2/32

[Peer]
PublicKey = <server-public-key>
PresharedKey = <preshared-key>
Endpoint = <server-public-ip>:51820
AllowedIPs = 10.0.0.0/24, 192.168.1.0/24
PersistentKeepalive = 25
```

`AllowedIPs = 10.0.0.0/24` only routes VPN subnet traffic (split tunnel). Internet traffic goes through normal gateway.

## Routing and NAT

### IP Forwarding

Required on the server for peers to reach each other or the internet:

```bash
# Enable immediately
sudo sysctl -w net.ipv4.ip_forward=1

# Persist across reboots
echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf
sudo sysctl -p /etc/sysctl.d/99-wireguard.conf
```

### NAT (Masquerade)

For peers to access the internet through the VPN server:

```bash
# In PostUp/PostDown of wg0.conf:
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

**Important:** Replace `eth0` with your actual network interface name (check with `ip route | grep default`).

### Site-to-Site Routing

To reach a peer's LAN (e.g., home network 192.168.1.0/24):

Server side -- add LAN to peer's AllowedIPs:
```ini
[Peer]
PublicKey = <home-rpi-pubkey>
AllowedIPs = 10.0.0.3/32, 192.168.1.0/24
```

Home RPi side -- enable forwarding and NAT for the LAN:
```ini
[Interface]
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
```

## DNS

### Server-Side DNS

For full-tunnel clients, set DNS in the client config:

```ini
[Interface]
DNS = 1.1.1.1, 8.8.8.8
```

For internal DNS resolution, run a local DNS resolver (e.g., systemd-resolved, dnsmasq) on the WireGuard server and point clients to it:

```ini
[Interface]
DNS = 10.0.0.1
```

### DNS Leak Prevention

On Linux clients, WireGuard uses `resolvconf` to set DNS. Ensure it is installed:

```bash
sudo apt install resolvconf
```

## Kill Switch

Prevent traffic from leaking if VPN disconnects:

### Method 1: iptables-based (in client PostUp/PostDown)

```ini
[Interface]
PostUp = iptables -I OUTPUT ! -o wg0 -m mark ! --mark $(wg show wg0 fwmark) -m addrtype ! --dst-type LOCAL -j REJECT
PreDown = iptables -D OUTPUT ! -o wg0 -m mark ! --mark $(wg show wg0 fwmark) -m addrtype ! --dst-type LOCAL -j REJECT
```

### Method 2: AllowedIPs-based (simpler)

Setting `AllowedIPs = 0.0.0.0/0` already acts as a kill switch because all traffic is routed to the tunnel. If the tunnel is down, traffic has nowhere to go.

## Multi-Peer Setup

A WireGuard server can have multiple peers. Each gets a unique IP and key pair.

```ini
# /etc/wireguard/wg0.conf on server

[Interface]
PrivateKey = <server-private-key>
Address = 10.0.0.1/24
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
# Dev laptop
PublicKey = <laptop-pubkey>
AllowedIPs = 10.0.0.2/32

[Peer]
# Home RPi (with LAN access)
PublicKey = <rpi-pubkey>
AllowedIPs = 10.0.0.3/32, 192.168.1.0/24
PersistentKeepalive = 25

[Peer]
# Phone
PublicKey = <phone-pubkey>
AllowedIPs = 10.0.0.4/32
```

## Management Commands

| Command | Purpose |
|---------|---------|
| `wg show` | Show interface status and peers |
| `wg show wg0 transfer` | Show data transferred per peer |
| `wg showconf wg0` | Show running config |
| `wg-quick up wg0` | Start interface |
| `wg-quick down wg0` | Stop interface |
| `wg set wg0 peer <pubkey> remove` | Remove a peer |
| `wg set wg0 peer <pubkey> allowed-ips 10.0.0.5/32` | Add/update peer |
| `systemctl enable wg-quick@wg0` | Enable on boot |
| `systemctl status wg-quick@wg0` | Check service status |

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Key exposure | Store private keys with `chmod 600`, never commit to git |
| Port scanning | WireGuard silently drops unauthenticated packets (stealth) |
| Brute force | Curve25519 makes brute force infeasible |
| Post-quantum | Use PresharedKey for additional symmetric encryption layer |
| Firewall | Only open UDP 51820 to expected source IPs if possible |
| Key rotation | Regenerate keys periodically, remove unused peers |

## Troubleshooting

| Problem | Diagnosis | Fix |
|---------|-----------|-----|
| No handshake | `wg show` shows no "latest handshake" | Check endpoint, port, firewall, keys |
| Handshake but no traffic | AllowedIPs mismatch | Verify AllowedIPs on both sides |
| Slow speed | MTU issues | Set `MTU = 1420` in Interface |
| DNS not working | resolvconf not installed | `apt install resolvconf` |
| Connection drops | NAT timeout | Set `PersistentKeepalive = 25` |
| Can't reach peer's LAN | IP forwarding disabled | Enable `net.ipv4.ip_forward = 1` |

## Related Methodologies

- `firewall-management/` -- open UDP port for WireGuard
- `ssh-hardening/` -- restrict SSH access to VPN IPs only
- `kernel-tuning/` -- IP forwarding settings
