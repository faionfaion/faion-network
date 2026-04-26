# WireGuard VPN LLM Prompts

## Setup and Configuration

### Prompt: Design WireGuard Network

```
Design a WireGuard VPN network for my infrastructure.

Infrastructure:
- VPS: [provider, OS, public IP or hostname]
- Home network: [router type, LAN subnet, devices to access]
- Mobile devices: [count, OS]
- Dev machines: [count, OS]

Requirements:
- Full tunnel for mobile: [Yes/No]
- Split tunnel for dev machines: [Yes/No]
- Site-to-site (VPS <-> Home LAN): [Yes/No]
- Restrict SSH to VPN only: [Yes/No]

Provide:
1. IP addressing scheme (VPN subnet, peer IPs)
2. Complete server wg0.conf
3. Client configs for each peer type
4. Firewall rules (UFW)
5. IP forwarding and NAT setup
6. Step-by-step setup commands
7. Verification steps
```

### Prompt: Add New WireGuard Peer

```
I need to add a new peer to my existing WireGuard server.

Current setup:
- Server VPN IP: [e.g., 10.0.0.1/24]
- Server public IP: [IP]
- Existing peers: [list with IPs]
- Server wg0.conf: [paste current config]

New peer:
- Name: [e.g., work-laptop]
- Type: [Linux/macOS/iOS/Android]
- Tunnel mode: [full/split]
- Needs LAN access: [Yes/No, if yes which LAN]
- Behind NAT: [Yes/No]

Provide:
1. Key generation commands
2. Peer section to add to server config
3. Complete client config file
4. QR code generation command (if mobile)
5. Verification steps
```

## Troubleshooting

### Prompt: WireGuard Not Connecting

```
My WireGuard client cannot connect to the server. Help me diagnose.

Server info:
- Public IP: [IP]
- WireGuard port: [e.g., 51820]
- OS: [e.g., Ubuntu 24.04]
- Server wg0.conf: [paste]
- `sudo wg show` output: [paste]
- `sudo ufw status` output: [paste]

Client info:
- OS: [e.g., macOS]
- Client config: [paste]
- `wg show` output: [paste]
- Behind NAT/firewall: [Yes/No]

Symptoms:
- Handshake happening: [Yes/No]
- Can ping server VPN IP: [Yes/No]
- Can reach internet through VPN: [Yes/No]
- Error messages: [paste any]

Diagnose step by step:
1. Is the port reachable? (nc -vzu server 51820)
2. Are keys correct? (public key matches peer config)
3. Is AllowedIPs correct on both sides?
4. Is IP forwarding enabled? (sysctl net.ipv4.ip_forward)
5. Are NAT rules applied? (iptables -t nat -L)
6. Is firewall allowing traffic? (ufw, iptables)
```

### Prompt: WireGuard Performance Issues

```
My WireGuard VPN is slow. Help me diagnose and fix.

Setup:
- Server: [specs, location]
- Client: [specs, location]
- ISP bandwidth: Server [X Mbps], Client [X Mbps]
- VPN throughput: [measured with iperf3]
- Non-VPN throughput: [measured without VPN]

Current config:
- MTU: [default or custom]
- Server wg0.conf: [paste]
- Client wg0.conf: [paste]

Investigate:
1. MTU issues (fragmentation)
2. CPU bottleneck (encryption overhead)
3. Routing issues
4. ISP throttling UDP traffic
5. Kernel/module version issues

Provide specific tuning recommendations.
```

### Prompt: WireGuard DNS Issues

```
DNS resolution fails when connected to WireGuard VPN.

Setup:
- Client OS: [e.g., Ubuntu 24.04]
- DNS configured in WireGuard: [e.g., DNS = 1.1.1.1]
- Full tunnel or split tunnel: [full/split]
- systemd-resolved running: [Yes/No]
- resolvconf installed: [Yes/No]

Symptoms:
- `ping 10.0.0.1` works: [Yes/No]
- `ping 1.1.1.1` works: [Yes/No]
- `dig google.com` works: [Yes/No]
- `cat /etc/resolv.conf` shows: [paste]

Help me fix DNS resolution through the VPN.
```

## Security

### Prompt: Harden WireGuard Setup

```
Review and harden my WireGuard configuration.

Current server config:
[paste wg0.conf]

Current firewall rules:
[paste ufw status]

SSH config:
[relevant ListenAddress lines]

Analyze:
1. Key management (permissions, storage)
2. PresharedKey usage
3. AllowedIPs restrictions
4. Firewall rules tightness
5. SSH access restriction to VPN
6. Unused/stale peers
7. SaveConfig setting
8. PostUp/PostDown security

Provide specific hardening recommendations with configs.
```

### Prompt: WireGuard Key Rotation

```
I need to rotate WireGuard keys for security. Help me plan a zero-downtime key rotation.

Current setup:
- Server with [N] peers
- Some peers are always-on (RPi), others connect occasionally (phone, laptop)

Provide:
1. Key rotation procedure (per-peer, not all-at-once)
2. Commands to generate new keys
3. How to update server config without disrupting other peers
4. How to distribute new configs to each client type
5. Verification that rotation was successful
6. Cleanup of old keys
```

## Advanced Scenarios

### Prompt: Site-to-Site WireGuard

```
I want to set up site-to-site WireGuard between my VPS and home network.

VPS:
- Public IP: [IP]
- WireGuard IP: [e.g., 10.0.0.1]

Home:
- Gateway device: [e.g., Raspberry Pi 5]
- Home LAN subnet: [e.g., 192.168.1.0/24]
- Gateway LAN IP: [e.g., 192.168.1.100]
- Home IP is dynamic: [Yes/No]
- Devices to access from VPS: [list]

Requirements:
- VPS can reach home LAN devices
- Home devices can reach VPS services
- Other WireGuard clients can reach home LAN through VPS

Provide:
1. Complete configs for both sides
2. IP forwarding and NAT rules
3. Routing configuration
4. Firewall rules
5. Testing procedure
6. Handling dynamic home IP (PersistentKeepalive, DDNS)
```

### Prompt: WireGuard with Docker

```
I run services in Docker and want them accessible only through WireGuard VPN.

Docker setup:
- docker-compose.yml: [paste]
- Current port bindings: [list]
- Docker network: [bridge/host]

WireGuard:
- Server IP: 10.0.0.1
- VPN subnet: 10.0.0.0/24

I want to:
1. Bind Docker services to WireGuard interface only (10.0.0.1)
2. Remove public port bindings
3. Keep inter-container communication working
4. Access services from VPN clients

Provide updated docker-compose.yml and any necessary routing/firewall changes.
```
