---
name: vps-first-deploy
description: Rent a $6/mo Hetzner CX11 (or DigitalOcean Droplet), harden SSH, create a non-root user, install Caddy for auto-SSL, deploy a Node or Python app as a systemd service, and point a Cloudflare A record at it.
tier: solo
group: server-craft
status: active
owner: ruslan
last_verified: 2026-05-02
version: 1.0.0
---

## Goal

After this playbook you will have a live Ubuntu 24.04 VPS serving your Node.js or Python app over HTTPS at `https://myapp.mydomain.com`, with password auth disabled, a non-root deploy user, your app managed by systemd, and Caddy handling auto-SSL via Let's Encrypt — all for $6/mo.

## Prerequisites

- A domain on Cloudflare nameservers (see `buy-domain-namecheap-cloudflare` + `cloudflare-dns-free-ssl` if not done).
- A Hetzner Cloud account at https://console.hetzner.cloud or a DigitalOcean account at https://cloud.digitalocean.com.
- An SSH keypair on your local machine. Run `ls ~/.ssh/id_ed25519.pub` — if it does not exist, generate one: `ssh-keygen -t ed25519 -C "deploy@myapp"`.
- Your app starts with a single command (`node server.js` or `python3 app.py`) and listens on an internal port (e.g. `3000` for Node, `8000` for Python).
- Basic comfort with SSH and a text editor on the terminal (`nano` is fine).

## Steps

### Provision the server

1. Log in to https://console.hetzner.cloud → click **New Project** → name it `myapp-prod` → click **Add Server**.

2. Choose:
   - **Location**: any (nbg1 is fine for EU, ash1 for US East)
   - **Image**: Ubuntu 24.04
   - **Type**: Shared CPU → CX11 (1 vCPU, 2 GB RAM, $6/mo)
   - **SSH Keys**: click **Add SSH key** → paste the contents of `~/.ssh/id_ed25519.pub` → name it `my-laptop`
   - **Firewalls**: skip for now (you will configure `ufw` on the server)
   - Click **Create & Buy Now**

3. Note the server IPv4 address shown in the dashboard (e.g. `65.108.12.44`).

### Log in and lock down SSH

4. Connect as root using the key you added:

   ```bash
   ssh -i ~/.ssh/id_ed25519 root@65.108.12.44
   ```

5. Create a non-root user named `deploy` with sudo rights:

   ```bash
   adduser deploy
   usermod -aG sudo deploy
   mkdir -p /home/deploy/.ssh
   cp /root/.ssh/authorized_keys /home/deploy/.ssh/
   chown -R deploy:deploy /home/deploy/.ssh
   chmod 700 /home/deploy/.ssh
   chmod 600 /home/deploy/.ssh/authorized_keys
   ```

6. Disable password auth and root login by editing `/etc/ssh/sshd_config`:

   ```bash
   sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
   sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
   systemctl restart ssh
   ```

7. Open a **second terminal** and verify the `deploy` user works before closing root:

   ```bash
   ssh -i ~/.ssh/id_ed25519 deploy@65.108.12.44
   ```

   If this succeeds, close the root session. From now on use the `deploy` user.

### Install dependencies and Caddy

8. Update the system and install build tools:

   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y curl git ufw
   ```

9. Allow traffic through `ufw`:

   ```bash
   sudo ufw allow OpenSSH
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

10. Install Caddy (official Debian/Ubuntu repo):

    ```bash
    sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
    curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
    sudo apt update && sudo apt install -y caddy
    ```

11. Install your runtime. For Node 22 (LTS):

    ```bash
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt install -y nodejs
    node --version   # v22.x.x
    ```

    For Python 3.12 (already included in Ubuntu 24.04 — no extra install needed):

    ```bash
    python3 --version  # 3.12.x
    sudo apt install -y python3-pip python3-venv
    ```

### Deploy your application

12. Copy your app to the server. From your **local machine**:

    ```bash
    rsync -avz --exclude node_modules --exclude .git \
      ./myapp/ deploy@65.108.12.44:/home/deploy/myapp/
    ```

    For Python apps, also exclude `__pycache__/` and `.venv/`.

13. On the server, install dependencies:

    For Node:
    ```bash
    cd /home/deploy/myapp
    npm ci --omit=dev
    ```

    For Python:
    ```bash
    cd /home/deploy/myapp
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

### Create a systemd service unit

14. Create the service file at `/etc/systemd/system/myapp.service`:

    For a Node app (`node server.js` on port `3000`):

    ```bash
    sudo tee /etc/systemd/system/myapp.service > /dev/null << 'EOF'
    [Unit]
    Description=myapp Node.js service
    After=network.target

    [Service]
    Type=simple
    User=deploy
    WorkingDirectory=/home/deploy/myapp
    ExecStart=/usr/bin/node /home/deploy/myapp/server.js
    Restart=on-failure
    RestartSec=5
    Environment=NODE_ENV=production
    Environment=PORT=3000

    [Install]
    WantedBy=multi-user.target
    EOF
    ```

    For a Python app (`python3 app.py` on port `8000`):

    ```bash
    sudo tee /etc/systemd/system/myapp.service > /dev/null << 'EOF'
    [Unit]
    Description=myapp Python service
    After=network.target

    [Service]
    Type=simple
    User=deploy
    WorkingDirectory=/home/deploy/myapp
    ExecStart=/home/deploy/myapp/.venv/bin/python3 /home/deploy/myapp/app.py
    Restart=on-failure
    RestartSec=5
    Environment=PORT=8000

    [Install]
    WantedBy=multi-user.target
    EOF
    ```

15. Enable and start the service:

    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable myapp
    sudo systemctl start myapp
    sudo systemctl status myapp
    ```

    The status output should show `active (running)`.

### Expose port 443 with auto-SSL via Caddy

16. Edit `/etc/caddy/Caddyfile` — replace all existing content:

    ```bash
    sudo tee /etc/caddy/Caddyfile > /dev/null << 'EOF'
    myapp.mydomain.com {
        reverse_proxy localhost:3000
    }
    EOF
    ```

    Replace `myapp.mydomain.com` with your subdomain and `3000` with your app port (`8000` for Python).

17. Reload Caddy:

    ```bash
    sudo systemctl reload caddy
    sudo systemctl status caddy
    ```

    Caddy will automatically obtain a Let's Encrypt certificate for the domain on first request.

### Point a Cloudflare A record at the server

18. Log in to https://dash.cloudflare.com → click your domain → **DNS** → **Records** → **Add record**:

    - **Type**: `A`
    - **Name**: `myapp` (for `myapp.mydomain.com`)
    - **IPv4 address**: `65.108.12.44` (your actual server IP)
    - **Proxy status**: orange cloud (Proxied)
    - **TTL**: Auto

    Click **Save**.

19. Set Cloudflare SSL mode to **Full (strict)** (not Flexible): **SSL/TLS** → **Overview** → select **Full (strict)** → **Save**.

## Verify

From your local machine, wait 1–2 minutes for DNS to propagate, then run:

```bash
curl -sI https://myapp.mydomain.com | head -4
```

Expected: `HTTP/2 200` (or `HTTP/1.1 200 OK`). Also confirm:

```bash
ssh deploy@65.108.12.44 'sudo systemctl status myapp caddy'
```

Both services show `active (running)`.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `ssh: connect to host 65.108.12.44 port 22: Connection refused` | Firewall or wrong IP | Confirm server IP in Hetzner dashboard; check `sudo ufw status` shows port 22 (OpenSSH) allowed |
| `Permission denied (publickey)` on SSH | Wrong key or key not added during provisioning | Re-add your public key via Hetzner console → Server → Access → SSH Keys; run `ssh-copy-id -i ~/.ssh/id_ed25519.pub deploy@65.108.12.44` as a workaround |
| `systemctl status myapp` shows `failed` | App crash on start | Run `journalctl -u myapp -n 50 --no-pager` to see the error; fix the crash, then `sudo systemctl restart myapp` |
| `curl` returns `502 Bad Gateway` from Caddy | App not listening on the declared port | Verify `ExecStart` port matches `reverse_proxy` port in Caddyfile; run `ss -tlnp | grep 3000` to confirm the app is bound |
| Cloudflare shows `526 Invalid SSL Certificate` | SSL mode is Flexible instead of Full (strict) | Set Cloudflare SSL/TLS → Overview → Full (strict) |
| `curl` returns `000` (no response) | DNS not yet propagated | Wait 2–5 minutes; test with `dig +short A myapp.mydomain.com` — should return `65.108.12.44` |
| Caddy fails to get Let's Encrypt cert | Domain not resolving to server IP | Confirm the Cloudflare A record points to the correct IP and is orange-cloud proxied |

## Next

- Add a deploy script: `rsync` + `sudo systemctl restart myapp` chained in a single shell script for zero-friction deploys.
- Set up `nginx-ssl-config` for multi-app hosting on the same VPS (multiple domains, one Caddyfile or nginx vhosts).
- Enable automated security patches: `sudo apt install unattended-upgrades && sudo dpkg-reconfigure unattended-upgrades`.

## References

- [knowledge/solo/infra/server-craft/server-init-bootstrap](../../../knowledge/solo/infra/server-craft/server-init-bootstrap) — the bootstrap sequence in this playbook (adduser, sshd_config hardening, ufw rules) follows the server-init-bootstrap checklist step-for-step, ensuring no lockout after password auth is disabled.
- [knowledge/solo/infra/server-craft/systemd-user-services](../../../knowledge/solo/infra/server-craft/systemd-user-services) — the `[Service]` unit fields (`Restart=on-failure`, `WorkingDirectory`, `Environment`) and the `daemon-reload` + `enable` + `start` sequence come directly from this methodology's service authoring pattern.
- [knowledge/solo/infra/server-craft/ssh-hardening](../../../knowledge/solo/infra/server-craft/ssh-hardening) — `PermitRootLogin no` and `PasswordAuthentication no` are the two minimal changes this methodology requires before exposing any port to the public internet.
- [knowledge/solo/infra/server-craft/ssl-tls-management](../../../knowledge/solo/infra/server-craft/ssl-tls-management) — Caddy's automatic ACME flow (port 80 challenge, cert renewal) is the zero-config TLS path this methodology recommends for solo projects over manual certbot.
- [knowledge/solo/infra/server-craft/cloudflare-domain-dns](../../../knowledge/solo/infra/server-craft/cloudflare-domain-dns) — the orange-cloud proxy + Full (strict) SSL combination in Step 18–19 is the exact pattern this methodology prescribes to avoid the `526` error that Flexible mode causes when the origin has a real cert.
