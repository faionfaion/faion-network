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
| Subnet allocation | 10.66.66.0/24 (or chosen) | operator |

## Assumes Loaded

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
| `templates/wireguard-vpn.md` | Human-readable audit trail. |
| `templates/wg0-server.conf` | Reference server config with PostUp/PostDown NAT rules. |
| `templates/wg0-client-split.conf` | Split-tunnel client — VPN subnet only. |
| `templates/wg0-client-full.conf` | Full-tunnel client — all traffic via VPS. |
| `templates/wg0-client-mobile.conf` | Mobile client with PersistentKeepalive. |
| `templates/wg0-home-gateway.conf` | Site-to-site home LAN gateway. |
| `templates/sysctl-wireguard.conf` | Drop-in: net.ipv4.ip_forward=1, ipv6 forwarding. |

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-wireguard-vpn.py` | Validate VpnPlan JSON against the schema. | Pre-deploy + post-peer-add. |
| `scripts/generate-wg-keys.sh` | Generate keypair, save with chmod 600. | Per new peer. |
| `scripts/add-wg-peer.sh` | Append peer to server config + render client config. | Adding a new device. |
| `scripts/wg-status.sh` | Show last-handshake per peer. | Daily health check. |

## Related

- [[firewall-management]]
- [[kernel-tuning]]
- [[ssh-hardening]]

## Decision tree

See `content/06-decision-tree.xml`. The tree maps observable input fields to one of the rules in `content/01-core-rules.xml`. Use it before drafting the artefact: it decides apply-vs-skip, the verdict label, and which template variant to fill.
