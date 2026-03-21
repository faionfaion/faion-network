# Add New Project to Existing Server Checklist

## Planning

- [ ] Choose project name and domain
- [ ] Allocate port range (check /srv/port-registry.txt for conflicts)
- [ ] Determine resource requirements (RAM, CPU, disk)
- [ ] Verify available resources: `free -h`, `df -h /`
- [ ] Decide: shared or isolated backing services
- [ ] Plan directory structure

## Port Allocation

- [ ] Choose base port (next available 100-range: 8200, 8300, etc.)
- [ ] Assign +00 for backend API
- [ ] Assign +01 for frontend
- [ ] Update /srv/port-registry.txt with new entries
- [ ] Verify no port conflicts: `ss -tlnp | grep <port>`

## Directory Setup

- [ ] Create runtime directory: `mkdir -p /srv/<project>/`
- [ ] Create source directory: `mkdir -p ~/projects/<project>/`
- [ ] Set ownership: all directories owned by service user
- [ ] Create .env file for the project: `touch /srv/<project>/.env && chmod 600 /srv/<project>/.env`

## Shared Database Setup

- [ ] Connect to PostgreSQL: `psql -U postgres`
- [ ] Create database: `CREATE DATABASE <project>;`
- [ ] Create user: `CREATE USER <project>_user WITH PASSWORD 'password';`
- [ ] Grant access: `GRANT ALL PRIVILEGES ON DATABASE <project> TO <project>_user;`
- [ ] Test connection from application
- [ ] Add DATABASE_URL to project .env

## Shared Redis Setup (if needed)

- [ ] Choose Redis database number (check existing allocations)
- [ ] Test connection: `redis-cli -n <db-number> ping`
- [ ] Add REDIS_URL to project .env

## systemd Services

- [ ] Create service file: `~/.config/systemd/user/<project>-be.service`
- [ ] Configure EnvironmentFile pointing to project .env
- [ ] Set memory limits (MemoryMax, MemoryHigh)
- [ ] Set OOMScoreAdjust
- [ ] Set restart policy (Restart=on-failure)
- [ ] Daemon reload: `systemctl --user daemon-reload`
- [ ] Enable service: `systemctl --user enable <project>-be`
- [ ] Start service: `systemctl --user start <project>-be`
- [ ] Verify: `systemctl --user status <project>-be`
- [ ] Repeat for frontend service if applicable

## nginx Configuration

- [ ] Create site config: `/etc/nginx/sites-available/<domain>`
- [ ] Configure SSL (Cloudflare Origin Certificate or Let's Encrypt)
- [ ] Configure proxy_pass to correct backend port
- [ ] Configure WebSocket upgrade (if applicable)
- [ ] Configure frontend proxy/static serving
- [ ] Include shared snippets (proxy-params, security-headers)
- [ ] Enable site: `sudo ln -s /etc/nginx/sites-available/<domain> /etc/nginx/sites-enabled/`
- [ ] Test config: `sudo nginx -t`
- [ ] Reload nginx: `sudo systemctl reload nginx`

## Cloudflare DNS

- [ ] Add A record pointing to server IP
- [ ] Enable Cloudflare proxy (orange cloud)
- [ ] Set SSL mode to Full (Strict)
- [ ] Generate Origin Certificate if using Full (Strict)
- [ ] Install Origin Certificate on server
- [ ] Test: `curl -I https://<domain>`

## Deploy Script

- [ ] Create deploy script for new project (or extend existing)
- [ ] Test deploy: sync code, install deps, restart service
- [ ] Verify service starts after deploy
- [ ] Verify health endpoint (if applicable)

## Firewall

- [ ] Verify UFW allows 80/tcp and 443/tcp (already done if not first project)
- [ ] No need to open application ports (nginx proxies)
- [ ] Verify backing service ports are NOT exposed externally

## Health Monitoring

- [ ] Add health endpoint to new service (if HTTP)
- [ ] Add service to watcher script (if using auto-heal)
- [ ] Test health check works

## Resource Verification

- [ ] Check total memory usage after adding project: `free -h`
- [ ] Check CPU usage: `htop`
- [ ] Check disk usage: `df -h /`
- [ ] All existing services still healthy
- [ ] New service responding correctly

## Documentation

- [ ] Update port-registry.txt
- [ ] Update server documentation (if any)
- [ ] Document deploy procedure for new project
- [ ] Document rollback procedure
