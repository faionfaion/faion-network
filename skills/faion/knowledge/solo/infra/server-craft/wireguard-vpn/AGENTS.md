# WireGuard VPN

## Summary

Configure WireGuard as a VPN server on a Linux VPS with multiple peer types: split-tunnel dev machine (VPN subnet only), full-tunnel mobile (all traffic), and site-to-site gateway (VPS to home LAN). Uses cryptokey routing — each peer's AllowedIPs list determines which packets are routed to it.

## Why

WireGuard is ~4,000 lines vs OpenVPN's 100,000+, runs as a kernel module (built-in since Linux 5.6), and achieves near-wire speed. For solo developers it eliminates exposing database ports publicly — services bind to 127.0.0.1 on the VPS and are accessible only through the VPN tunnel.

## When To Use

- Accessing internal VPS services (PostgreSQL, Redis, RabbitMQ) securely without exposing ports to the internet
- Creating a site-to-site tunnel between a VPS and home network/Raspberry Pi
- Routing all mobile traffic through the VPS for privacy on public Wi-Fi
- Restricting SSH access to VPN subnet only (after VPN is confirmed working)

## When NOT To Use

- When you only need SSH access — an SSH tunnel (`ssh -L`) is simpler and requires no server-side setup
- When your provider already offers a managed VPN or private networking between servers — use that instead
- As a replacement for UFW — WireGuard controls which hosts can connect; UFW controls which ports are exposed. Both are needed.

## Content

| File | What's inside |
|------|---------------|
| `content/01-concepts.xml` | Cryptokey routing, key pair types, network architecture diagram, IP forwarding + NAT |
| `content/02-configuration.xml` | Server Interface/Peer sections, full-tunnel vs split-tunnel AllowedIPs, site-to-site routing, DNS |
| `content/03-examples.xml` | VPS-to-home RPi tunnel, dev machine split tunnel, mobile full tunnel, restrict SSH to VPN |

## Templates

| File | Purpose |
|------|---------|
| `templates/wg0-server.conf` | Server config with multiple peer types (laptop, RPi+LAN, phone) |
| `templates/wg0-client-full.conf` | Linux/macOS full-tunnel client (0.0.0.0/0) |
| `templates/wg0-client-split.conf` | Split-tunnel client (VPN subnet only) |
| `templates/wg0-client-mobile.conf` | Mobile client config (scan as QR code) |
| `templates/wg0-home-gateway.conf` | Home RPi/gateway site-to-site config |
| `templates/sysctl-wireguard.conf` | IP forwarding settings for WireGuard server |

## Scripts

| File | Purpose |
|------|---------|
| `scripts/generate-wg-keys.sh` | Generate private, public, preshared keys for a new peer |
| `scripts/add-wg-peer.sh` | Add peer to running interface, generate client config and QR code |
| `scripts/wg-status.sh` | Show peer handshake age, data transfer, active/stale status |
