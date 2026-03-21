# WireGuard VPN Checklist

## Pre-Setup

- [ ] Verify kernel version supports WireGuard: `uname -r` (5.6+ has built-in, older needs DKMS)
- [ ] Check if WireGuard is already installed: `which wg`
- [ ] Plan IP addressing scheme (e.g., 10.0.0.0/24 for VPN subnet)
- [ ] Identify all peers and assign VPN IPs
- [ ] Choose UDP port (default 51820, or custom for stealth)
- [ ] Identify server's public IP or hostname
- [ ] Identify server's primary network interface: `ip route | grep default`

## Server Installation

### Install WireGuard

- [ ] Install packages: `sudo apt install wireguard wireguard-tools`
- [ ] Verify kernel module: `sudo modprobe wireguard && lsmod | grep wireguard`

### Generate Server Keys

- [ ] Generate private key: `wg genkey | sudo tee /etc/wireguard/server_private.key`
- [ ] Derive public key: `cat /etc/wireguard/server_private.key | wg pubkey | sudo tee /etc/wireguard/server_public.key`
- [ ] Set key permissions: `sudo chmod 600 /etc/wireguard/server_private.key`

### Generate Client Keys (per client)

- [ ] Generate private key: `wg genkey > client_private.key`
- [ ] Derive public key: `cat client_private.key | wg pubkey > client_public.key`
- [ ] Generate preshared key: `wg genpsk > client_preshared.key`
- [ ] Set key permissions: `chmod 600 client_private.key client_preshared.key`

### Enable IP Forwarding

- [ ] Enable: `sudo sysctl -w net.ipv4.ip_forward=1`
- [ ] Persist: `echo "net.ipv4.ip_forward = 1" | sudo tee /etc/sysctl.d/99-wireguard.conf`
- [ ] Apply: `sudo sysctl -p /etc/sysctl.d/99-wireguard.conf`
- [ ] Verify: `sysctl net.ipv4.ip_forward` (should show `= 1`)

### Create Server Configuration

- [ ] Create `/etc/wireguard/wg0.conf` with Interface and Peer sections
- [ ] Set correct PrivateKey
- [ ] Set Address (e.g., 10.0.0.1/24)
- [ ] Set ListenPort (e.g., 51820)
- [ ] Add PostUp/PostDown for NAT (with correct interface name)
- [ ] Add all peer sections with correct PublicKey and AllowedIPs
- [ ] Set config permissions: `sudo chmod 600 /etc/wireguard/wg0.conf`

### Firewall

- [ ] Open WireGuard port: `sudo ufw allow 51820/udp`
- [ ] Allow forwarding in UFW: edit `/etc/ufw/before.rules` or set DEFAULT_FORWARD_POLICY
- [ ] Reload firewall: `sudo ufw reload`

## Start and Enable

- [ ] Start interface: `sudo wg-quick up wg0`
- [ ] Verify interface is up: `sudo wg show`
- [ ] Enable on boot: `sudo systemctl enable wg-quick@wg0`
- [ ] Verify service: `sudo systemctl status wg-quick@wg0`

## Client Setup

### Linux Client

- [ ] Install WireGuard: `sudo apt install wireguard`
- [ ] Create `/etc/wireguard/wg0.conf` with client config
- [ ] Set correct PrivateKey, Address, DNS
- [ ] Set server's PublicKey, PresharedKey, Endpoint
- [ ] Set AllowedIPs (0.0.0.0/0 for full tunnel, specific ranges for split)
- [ ] Set PersistentKeepalive if behind NAT
- [ ] Start: `sudo wg-quick up wg0`

### macOS Client

- [ ] Install WireGuard from App Store or `brew install wireguard-tools`
- [ ] Import configuration file or create manually
- [ ] Activate tunnel

### iOS/Android Client

- [ ] Install WireGuard app from App Store / Google Play
- [ ] Generate QR code from config: `qrencode -t ansiutf8 < client.conf`
- [ ] Scan QR code in app
- [ ] Activate tunnel

## Verification

### Connectivity

- [ ] From client, ping server VPN IP: `ping 10.0.0.1`
- [ ] From server, ping client VPN IP: `ping 10.0.0.2`
- [ ] Check handshake: `sudo wg show` (should show "latest handshake")
- [ ] Check data transfer: `sudo wg show wg0 transfer`

### Full Tunnel (if configured)

- [ ] Verify external IP changes: `curl ifconfig.me` (should show server's IP)
- [ ] Test DNS resolution: `dig google.com`
- [ ] Check for DNS leaks: visit dnsleaktest.com

### Site-to-Site (if configured)

- [ ] From VPS, ping home LAN device: `ping 192.168.1.x`
- [ ] From home LAN, ping VPS VPN IP: `ping 10.0.0.1`
- [ ] Verify routing table: `ip route show`

### Performance

- [ ] Test throughput: `iperf3 -c 10.0.0.1` (from client)
- [ ] Check MTU issues: `ping -M do -s 1392 10.0.0.1`
- [ ] If MTU issues, set `MTU = 1420` in Interface section

## Security Hardening

- [ ] All private keys have permissions 600
- [ ] wg0.conf has permissions 600
- [ ] SaveConfig is set to false (manual config management)
- [ ] PresharedKey configured for each peer
- [ ] Remove unused/old peers from config
- [ ] Consider restricting SSH to VPN IP only
- [ ] Private keys are NOT committed to any git repository

## Maintenance

- [ ] Document all peers (name, VPN IP, purpose)
- [ ] Set calendar reminder for key rotation (every 6-12 months)
- [ ] Monitor `wg show` for stale peers (no recent handshake)
- [ ] Keep WireGuard packages updated: `sudo apt update && sudo apt upgrade wireguard`
