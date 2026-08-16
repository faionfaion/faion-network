# WireGuard VPN

## Summary

**One-sentence:** Generates a WireGuard server + per-peer config (split-tunnel dev, full-tunnel mobile, site-to-site gateway) — cryptokey routing AllowedIPs per peer — gated by sysctl forwarding.

**One-paragraph:** WireGuard on a Linux VPS gives a private mesh to your dev machine, phone, and home LAN with a kernel-fast tunnel. This methodology pins the server config, three peer templates (split-tunnel, full-tunnel, site-to-site), the cryptokey-routing rule (each peer's AllowedIPs decides which packets route to it), sysctl ipv4 forward + ipv6 forward, and an add-peer script. Output: a VpnPlan + per-peer .conf.

**Ефективно для:**

- Accessing internal VPS services (Postgres, Redis, n8n) without exposing ports publicly.
- Bridging VPS ↔ home LAN for monitoring or media.
- Routing all mobile traffic through the VPS for public-wifi privacy.
- Restricting SSH to VPN subnet only AFTER VPN is confirmed.

## Applies If (ALL must hold)

- Need private access to VPS-internal services (Postgres, Redis, n8n).
- Need site-to-site VPS ↔ home LAN.
- Mobile traffic via VPS for privacy on public Wi-Fi.
- Restrict SSH to VPN subnet (after VPN works).

## Skip If (ANY kills it)

- Need only SSH — `ssh -L` tunnel is simpler.
- Provider already offers managed VPN / private networking.
- Replacement for UFW — WireGuard governs hosts, UFW governs ports; both needed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Server public IP + UDP port choice | IP + port | provider + operator |
| Peer device list | [{name, role, allowed_ips}] | operator inventory |
| Subnet allocation | 10.10.0.0/24 (or chosen) | operator |

## Assumes Loaded

<!-- canonical: meta.json -> assumes_loaded (spec §3.2) -->

| Methodology | Why |
|-------------|-----|
| firewall-management | UFW must allow the WireGuard UDP port + NAT post-route. |
| kernel-tuning | net.ipv4.ip_forward=1 lives in 99-sysctl drop-in. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | ≥5 rules: r1-allowedips-defines-routing, r2-ip-forward-on, r3-keys-never-in-git, r4-named-owner, r5-keepalive-for-mobile | 1100 |
| `content/02-output-contract.xml` | essential | JSON Schema for the WireGuard VPN artefact + valid/invalid examples + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | ≥3 antipatterns: allowedips-overlapping, ip-forward-off, private-key-in-repo, no-keepalive-nat-drop | 800 |
| `content/04-procedure.xml` | essential | Step-by-step procedure for end-to-end application | 800 |
| `content/06-decision-tree.xml` | essential | Maps observable inputs to rule ids in 01-core-rules.xml | 500 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `draft-vpn-plan` | sonnet | Per-peer routing decisions. |
| `generate-keys` | haiku | Mechanical wg genkey calls. |
| `render-peer-config` | haiku | Template fill from plan. |

## Templates

| File | Purpose |
|------|---------|
| `templates/wireguard-vpn.json` | VpnPlan JSON skeleton. |
| `templates/wireguard-vpn.md.j2` | Human-readable audit trail. |
| `templates/wireguard-vpn.md` | Human-readable audit trail. Generated from `templates/wireguard-vpn.md.j2` by `tpl-jinja --migrate`; do not hand-edit. |
| `templates/wg0-server.conf` | Reference server config with PostUp/PostDown NAT rules. |
| `templates/wg0-client-split.conf` | Split-tunnel client — VPN subnet only. |
| `templates/wg0-client-full.conf` | Full-tunnel client — all traffic via VPS. |
| `templates/wg0-client-mobile.conf` | Mobile client with PersistentKeepalive. |
| `templates/wg0-home-gateway.conf` | Site-to-site home LAN gateway. |
| `templates/sysctl-wireguard.conf` | Drop-in: net.ipv4.ip_forward=1, ipv6 forwarding. |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wireguard-vpn.py` | Validate VpnPlan JSON against the schema. | Pre-deploy + post-peer-add. |
| `scripts/generate-wg-keys.sh` | Generate keypair, save with chmod 600. | Per new peer. |
| `scripts/add-wg-peer.sh` | Append peer to server config + render client config. | Adding a new device. |
| `scripts/wg-status.sh` | Show last-handshake per peer. | Daily health check. |

## Related

<!-- canonical: meta.json -> related, wikilink bullets only (spec §3.2) -->

- [[firewall-management]]
- [[kernel-tuning]]
- [[ssh-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/wireguard-vpn.json`

```json
{
  "artefact_id": "vpn-<name>",
  "version": "1.1.0",
  "last_reviewed": "2026-05-23",
  "server_endpoint": "<ip>:<udp_port>",
  "server_subnet": "10.10.0.0/24",
  "peers": [
    {
      "name": "<peer>",
      "role": "split|full|site|mobile",
      "allowed_ips": "10.10.0.<n>/32",
      "keepalive": false
    }
  ],
  "ip_forward": true,
  "owner": "<@handle>"
}
```

### `templates/wg0-server.conf`

```conf
# /etc/wireguard/wg0.conf — WireGuard Server
# VPN subnet: 10.10.0.0/24  |  Server: 10.10.0.1
# Replace eth0 with actual default interface: ip route | grep default

[Interface]
PrivateKey  = SERVER_PRIVATE_KEY_HERE
Address     = 10.10.0.1/24
ListenPort  = 51820
SaveConfig  = false

PostUp   = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

# Peer: Dev laptop (split tunnel — VPN subnet only)
[Peer]
PublicKey    = LAPTOP_PUBLIC_KEY_HERE
PresharedKey = LAPTOP_PRESHARED_KEY_HERE
AllowedIPs   = 10.10.0.2/32

# Peer: Home RPi + LAN (site-to-site)
[Peer]
PublicKey           = RPI_PUBLIC_KEY_HERE
PresharedKey        = RPI_PRESHARED_KEY_HERE
AllowedIPs          = 10.10.0.3/32, 192.168.1.0/24
PersistentKeepalive = 25

# Peer: Phone (full tunnel)
[Peer]
PublicKey           = PHONE_PUBLIC_KEY_HERE
PresharedKey        = PHONE_PRESHARED_KEY_HERE
AllowedIPs          = 10.10.0.4/32
PersistentKeepalive = 25
```

### `templates/wg0-client-split.conf`

```conf
# WireGuard Client — Split Tunnel (VPN subnet only)
# Internet traffic goes through normal gateway.
# /etc/wireguard/wg0.conf on dev machine (Linux/macOS)

[Interface]
PrivateKey = CLIENT_PRIVATE_KEY_HERE
Address    = 10.10.0.2/32

[Peer]
PublicKey           = SERVER_PUBLIC_KEY_HERE
PresharedKey        = CLIENT_PRESHARED_KEY_HERE
Endpoint            = SERVER_PUBLIC_IP:51820
AllowedIPs          = 10.10.0.0/24
PersistentKeepalive = 25
```

### `templates/wg0-client-full.conf`

```conf
# WireGuard Client — Full Tunnel (all traffic through VPN)
# Use for Linux/macOS machines needing full privacy routing.
# /etc/wireguard/wg0.conf

[Interface]
PrivateKey = CLIENT_PRIVATE_KEY_HERE
Address    = 10.10.0.2/32
DNS        = 1.1.1.1, 8.8.8.8

[Peer]
PublicKey           = SERVER_PUBLIC_KEY_HERE
PresharedKey        = CLIENT_PRESHARED_KEY_HERE
Endpoint            = SERVER_PUBLIC_IP:51820
AllowedIPs          = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

### `templates/wg0-client-mobile.conf`

```conf
# WireGuard Mobile Client — Full Tunnel
# Scan as QR code in WireGuard iOS/Android app:
#   sudo apt install qrencode
#   qrencode -t ansiutf8 < wg0-client-mobile.conf

[Interface]
PrivateKey = MOBILE_PRIVATE_KEY_HERE
Address    = 10.10.0.4/32
DNS        = 1.1.1.1

[Peer]
PublicKey           = SERVER_PUBLIC_KEY_HERE
PresharedKey        = MOBILE_PRESHARED_KEY_HERE
Endpoint            = SERVER_PUBLIC_IP:51820
AllowedIPs          = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

### `templates/wg0-home-gateway.conf`

```conf
# WireGuard Home Gateway (RPi / Site-to-Site)
# Bridges home LAN (192.168.1.0/24) to VPS VPN network.
# /etc/wireguard/wg0.conf on home Raspberry Pi

[Interface]
PrivateKey = HOME_GATEWAY_PRIVATE_KEY_HERE
Address    = 10.10.0.3/32

# Replace eth0 with LAN interface (ip route | grep default)
PostUp   = iptables -A FORWARD -i wg0 -o eth0 -j ACCEPT; iptables -A FORWARD -i eth0 -o wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i wg0 -o eth0 -j ACCEPT; iptables -D FORWARD -i eth0 -o wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE

[Peer]
PublicKey           = SERVER_PUBLIC_KEY_HERE
PresharedKey        = HOME_PRESHARED_KEY_HERE
Endpoint            = SERVER_PUBLIC_IP:51820
AllowedIPs          = 10.10.0.0/24
PersistentKeepalive = 25
```

### `templates/sysctl-wireguard.conf`

```conf
# /etc/sysctl.d/99-wireguard.conf
# IP forwarding settings for WireGuard VPN server
# Apply: sudo sysctl -p /etc/sysctl.d/99-wireguard.conf

net.ipv4.ip_forward = 1
net.ipv6.conf.all.forwarding = 1
```
