# Agent Integration — WireGuard VPN

## When to use
- Securing internal service access (PostgreSQL, RabbitMQ) so they are only reachable over VPN
- Connecting a developer laptop or home network to the VPS without exposing SSH to the internet
- Setting up site-to-site tunnels between VPS and a home Raspberry Pi (LAN bridging)
- Replacing SSH port-forwarding with a proper VPN for multiple services
- Enabling VPN-only SSH access (remove public SSH rule from UFW after VPN is stable)

## When NOT to use
- Team VPN with many users and complex routing — use a managed solution (Tailscale, Netbird, Headscale) instead of hand-rolling WireGuard config
- Situations where UDP is blocked (some corporate networks, some hotel WiFi) — WireGuard is UDP-only; OpenVPN with TCP 443 may be required
- When you need a VPN killswitch on a cloud server — full-tunnel on the server itself will drop SSH access
- Temporary access needs — use SSH certificate-based access with short TTL instead

## Where it fails / limitations
- WireGuard is UDP-only; it will not work through firewalls that block all UDP (some strict corporate environments)
- No built-in key distribution or PKI — key management (adding/removing peers) is entirely manual; there is no "certificate revoke" equivalent, only removing the peer's `[Peer]` block
- `SaveConfig = true` causes wg0.conf to be overwritten on `wg-quick down` — this replaces any manual edits with the in-memory state, which may differ; always use `SaveConfig = false` with manual config management
- IP forwarding must be explicitly enabled on the server (`net.ipv4.ip_forward = 1`) — without it, peers can reach the VPN server but not the internet or each other
- PostUp/PostDown iptables commands reference a specific interface name (`eth0`, `ens3`) which varies by server — wrong interface name silently breaks NAT without obvious error
- MTU mismatches cause slow throughput and packet loss; default MTU 1420 works for most cases but may need adjustment for certain ISPs

## Agentic workflow
An agent sets up WireGuard by generating key pairs for each peer, writing the server config, distributing peer configs, and verifying connectivity with `wg show`. For existing setups, the agent reads the current config, adds or removes peer blocks, applies changes with `wg syncconf` (no restart needed for peer changes), and verifies with `wg show wg0 transfer`. Key generation must happen on the respective machine — private keys must never be transmitted over plaintext channels. The agent must confirm the actual network interface name before writing PostUp/PostDown NAT rules.

### Recommended subagents
- `faion-sdd-executor-agent` — execute VPN setup as part of a server hardening SDD feature

### Prompt pattern
```
Set up WireGuard on this VPS as a hub-and-spoke VPN.
Server VPN IP: 10.0.0.1/24, listen port: 51820.
Peers: dev-laptop (10.0.0.2), raspi-home (10.0.0.3, also expose LAN 192.168.1.0/24).
Steps:
1. Show key generation commands for each machine (private key stays on each machine).
2. Output server wg0.conf template with placeholders for peer public keys.
3. Output client configs for dev-laptop and raspi-home.
4. List firewall commands (UFW) and sysctl settings needed on the server.
```

```
Add a new peer to the existing WireGuard server at /etc/wireguard/wg0.conf.
Peer name: new-phone, VPN IP: 10.0.0.5/32.
Key generation happens on the phone; I will provide the public key.
Output: the [Peer] block to append, and the wg set command to add it without restart.
```

## CLI tools
| Tool | Purpose | Install / docs |
|------|---------|----------------|
| `wg` | WireGuard management (show, set, genkey, pubkey, genpsk) | `apt install wireguard` |
| `wg-quick` | Interface up/down with full config file | Part of `wireguard-tools` |
| `wg show` | Display current interface state and peer stats | Built-in |
| `wg syncconf` | Apply config changes to a running interface without restart | Built-in |
| `qrencode` | Generate QR code for mobile client config | `apt install qrencode` |
| `ip route` | Check routing table; verify default interface name for PostUp | Built-in (iproute2) |
| `ping` / `traceroute` | Test VPN connectivity between peers | Built-in |

## Services & apps
| Service | Type (SaaS/OSS) | Agent-friendly? | Notes |
|---------|-----------------|-----------------|-------|
| Tailscale | SaaS (free tier) | Yes | Managed WireGuard mesh; automatic key distribution; no server config needed; CLI-driven |
| Headscale | OSS | Yes | Self-hosted Tailscale control plane; REST API available |
| Netbird | OSS/SaaS | Yes | Zero-trust WireGuard mesh with web UI and REST API |
| wg-easy | OSS | Yes | Docker-based WireGuard UI with QR code generation ([GitHub](https://github.com/wg-easy/wg-easy)) |
| WireGuard Android/iOS | Mobile app | Manual | Client apps; config can be imported via QR code |

## Templates & scripts
See templates.md for full server and client config templates. Key peer addition script:

```bash
#!/usr/bin/env bash
# add-peer.sh — Add a WireGuard peer without restarting the interface
# Usage: bash add-peer.sh <peer-name> <peer-pubkey> <vpn-ip>
set -euo pipefail

PEER_NAME="$1"
PEER_PUBKEY="$2"
VPN_IP="$3"          # e.g., 10.0.0.5/32
WG_CONF="/etc/wireguard/wg0.conf"

# Apply to running interface immediately (no restart)
sudo wg set wg0 peer "$PEER_PUBKEY" allowed-ips "$VPN_IP"

# Append to config file for persistence
sudo tee -a "$WG_CONF" <<EOF

[Peer]
# $PEER_NAME
PublicKey = $PEER_PUBKEY
AllowedIPs = $VPN_IP
PersistentKeepalive = 25
EOF

echo "Peer $PEER_NAME added: $VPN_IP"
sudo wg show wg0
```

## Best practices
- Store private keys with `chmod 600`; never commit wg0.conf to git (it contains the server private key)
- Use `SaveConfig = false` and manage the config file manually — `SaveConfig = true` overwrites the file on shutdown and can destroy carefully written comments and formatting
- Always check `ip route | grep default` to get the actual interface name before writing PostUp/PostDown — servers routinely use `ens3`, `eth0`, `enp0s3`, or similar
- Use `wg syncconf wg0 <(wg-quick strip wg0)` to reload config without dropping existing peer connections
- Generate a preshared key (`wg genpsk`) per peer pair for post-quantum resistance
- Set `PersistentKeepalive = 25` on clients behind NAT to keep the UDP mapping alive
- Test with `wg show wg0 transfer` — if bytes received from a peer stay at 0 after traffic should have flowed, the peer's AllowedIPs is misconfigured
- Use split tunneling (`AllowedIPs = 10.0.0.0/24` only) unless the peer needs full internet routing through the VPN

## AI-agent gotchas
- Private keys must never be generated by the agent on behalf of the remote peer — each machine generates its own key pair; the agent only exchanges public keys
- `wg-quick down wg0` followed by `wg-quick up wg0` drops all existing VPN connections including the agent's SSH tunnel if it runs over VPN — agent must confirm it has an alternative connectivity path before doing this
- Adding `AllowedIPs = 0.0.0.0/0` on a server-side peer config routes all internet traffic through that peer (effectively making it the internet gateway) — this is almost never intended for server-to-server config
- MTU issues manifest as TCP sessions hanging after small exchanges — the symptom looks like a firewall issue but is actually an MTU black hole; fix with `MTU = 1420` in `[Interface]`
- `wg set wg0 peer ... allowed-ips ...` is additive for new peers but replaces allowed-ips for existing peers — agent must not accidentally restrict a peer's routing by applying an incomplete AllowedIPs list

## References
- https://www.wireguard.com/quickstart/
- https://man7.org/linux/man-pages/man8/wg.8.html
- https://github.com/wg-easy/wg-easy
- https://tailscale.com/kb/1151/what-is-tailscale
- https://www.procustodibus.com/blog/2021/01/wireguard-endpoints-and-ip-addresses/
