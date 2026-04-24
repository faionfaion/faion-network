# nginx Reverse Proxy Checklist

Step-by-step checklist for setting up nginx as a multi-domain reverse proxy on Ubuntu 24.04.

## Prerequisites

- [ ] Root or sudo access
- [ ] Domain DNS pointing to server (or Cloudflare proxy)
- [ ] Backend services running on localhost ports
- [ ] SSL certificates (or Cloudflare handling SSL)

## Phase 1: Installation

- [ ] **Install nginx**
  ```bash
  sudo apt update
  sudo apt install -y nginx
  ```

- [ ] **Verify installation**
  ```bash
  nginx -v
  sudo systemctl status nginx
  curl -I http://localhost
  ```

## Phase 2: Create Snippets

- [ ] **Create proxy-params snippet**
  ```bash
  sudo tee /etc/nginx/snippets/proxy-params.conf << 'EOF'
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto https;
  proxy_buffering off;
  proxy_request_buffering off;
  EOF
  ```

- [ ] **Create WebSocket snippet**
  ```bash
  sudo tee /etc/nginx/snippets/websocket.conf << 'EOF'
  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection $connection_upgrade;
  proxy_read_timeout 86400;
  proxy_send_timeout 86400;
  EOF
  ```

- [ ] **Create security-headers snippet**
  ```bash
  sudo tee /etc/nginx/snippets/security-headers.conf << 'EOF'
  add_header X-Content-Type-Options "nosniff" always;
  add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
  add_header Referrer-Policy "strict-origin-when-cross-origin" always;
  add_header X-Frame-Options "SAMEORIGIN" always;
  add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
  EOF
  ```

## Phase 3: WebSocket Map

- [ ] **Add WebSocket map to nginx.conf** (in http block)
  ```bash
  # Add before server blocks or in /etc/nginx/conf.d/websocket-map.conf
  sudo tee /etc/nginx/conf.d/websocket-map.conf << 'EOF'
  map $http_upgrade $connection_upgrade {
      default upgrade;
      ''      close;
  }
  EOF
  ```

## Phase 4: Site Configuration

- [ ] **Create site config**
  ```bash
  sudo vim /etc/nginx/sites-available/myapp.example.com
  ```

- [ ] **Enable site**
  ```bash
  sudo ln -sf /etc/nginx/sites-available/myapp.example.com /etc/nginx/sites-enabled/
  ```

- [ ] **Remove default site** (if not needed)
  ```bash
  sudo rm /etc/nginx/sites-enabled/default
  ```

- [ ] **Test configuration**
  ```bash
  sudo nginx -t
  ```

- [ ] **Reload nginx**
  ```bash
  sudo systemctl reload nginx
  ```

## Phase 5: Rate Limiting

- [ ] **Add rate limiting zones** (in http block or conf.d)
  ```bash
  sudo tee /etc/nginx/conf.d/rate-limiting.conf << 'EOF'
  # Rate limiting zones
  limit_req_zone $binary_remote_addr zone=api_general:10m rate=10r/s;
  limit_req_zone $binary_remote_addr zone=api_auth:10m rate=3r/m;
  limit_req_zone $binary_remote_addr zone=api_upload:10m rate=5r/m;
  limit_req_status 429;
  EOF
  ```

- [ ] **Apply to site config**
  ```nginx
  location /api/ {
      limit_req zone=api_general burst=20 nodelay;
      # ... proxy_pass
  }
  ```

## Phase 6: Verification

- [ ] **Test HTTP**
  ```bash
  curl -I http://myapp.example.com
  ```

- [ ] **Test HTTPS** (if configured)
  ```bash
  curl -I https://myapp.example.com
  ```

- [ ] **Test API proxy**
  ```bash
  curl http://myapp.example.com/api/health
  ```

- [ ] **Test WebSocket**
  ```bash
  curl -i -N \
      -H "Connection: Upgrade" \
      -H "Upgrade: websocket" \
      -H "Sec-WebSocket-Key: test" \
      -H "Sec-WebSocket-Version: 13" \
      http://myapp.example.com/ws
  ```

- [ ] **Test security headers**
  ```bash
  curl -sI https://myapp.example.com | grep -E "X-Content-Type|Strict-Transport|X-Frame|Referrer"
  ```

- [ ] **Test rate limiting**
  ```bash
  # Send 30 rapid requests
  for i in $(seq 1 30); do curl -s -o /dev/null -w "%{http_code}\n" http://myapp.example.com/api/test; done
  # Should see 429 responses after burst is exceeded
  ```

## Phase 7: Monitoring

- [ ] **Set up log rotation** (usually default)
  ```bash
  ls /etc/logrotate.d/nginx
  ```

- [ ] **Check access log format**
  ```bash
  head -5 /var/log/nginx/access.log
  ```

- [ ] **Check error log**
  ```bash
  sudo tail -20 /var/log/nginx/error.log
  ```

## Rollback

If nginx breaks:

```bash
# Check what's wrong
sudo nginx -t

# Disable problematic site
sudo rm /etc/nginx/sites-enabled/problematic-site

# Reload
sudo systemctl reload nginx
```
