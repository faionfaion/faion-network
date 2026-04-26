# SSL/TLS Setup Examples

## Let's Encrypt with Certbot

### Basic Certificate Generation

```bash
# Install Certbot (Ubuntu/Debian)
sudo apt update && sudo apt install certbot python3-certbot-nginx

# Nginx automatic (recommended)
sudo certbot --nginx -d example.com -d www.example.com

# Standalone (if web server not running)
sudo certbot certonly --standalone -d example.com

# Webroot (existing web server)
sudo certbot certonly --webroot -w /var/www/html -d example.com

# DNS challenge (for wildcard)
sudo certbot certonly --manual --preferred-challenges=dns -d "*.example.com"

# Non-interactive production
sudo certbot certonly --nginx \
  --non-interactive \
  --agree-tos \
  --email admin@example.com \
  -d example.com -d www.example.com
```

### Certificate Locations

```
/etc/letsencrypt/live/example.com/
├── cert.pem       # Server certificate
├── chain.pem      # Intermediate certificates
├── fullchain.pem  # cert.pem + chain.pem (use this)
├── privkey.pem    # Private key
└── README
```

### Auto-Renewal Setup

```bash
# Test renewal
sudo certbot renew --dry-run

# Systemd timer (preferred, usually auto-installed)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer

# Manual cron (if needed)
# 0 0,12 * * * /usr/bin/certbot renew --quiet --post-hook "systemctl reload nginx"
```

---

## Nginx Configuration

### Modern TLS Configuration (2025)

```nginx
# /etc/nginx/snippets/ssl-params.conf

# Protocols - TLS 1.3 preferred, 1.2 for compatibility
ssl_protocols TLSv1.2 TLSv1.3;

# Ciphers for TLS 1.2
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

# Let client choose cipher (TLS 1.3 handles this automatically)
ssl_prefer_server_ciphers off;

# Session configuration
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# DH parameters (generate: openssl dhparam -out /etc/nginx/dhparam.pem 2048)
ssl_dhparam /etc/nginx/dhparam.pem;

# HSTS (2 years, include subdomains, preload)
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
```

### Server Block

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com www.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    include /etc/nginx/snippets/ssl-params.conf;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

---

## Apache Configuration

```apache
# /etc/apache2/sites-available/example.com-ssl.conf

<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/example.com

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem

    # Protocols
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

    # Ciphers
    SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305
    SSLHonorCipherOrder off

    # HSTS
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"

    # OCSP Stapling
    SSLUseStapling on
    SSLStaplingResponderTimeout 5
    SSLStaplingReturnResponderErrors off

    <Directory /var/www/example.com>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

# Stapling cache (outside VirtualHost)
SSLStaplingCache shmcb:/var/run/ocsp(128000)
```

---

## Self-Signed Certificates

### Basic Self-Signed

```bash
# Generate private key and certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/selfsigned.key \
  -out /etc/ssl/certs/selfsigned.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=example.com"
```

### With Subject Alternative Names (SAN)

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/selfsigned.key \
  -out /etc/ssl/certs/selfsigned.crt \
  -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:10.0.0.1"
```

### Create Internal CA

```bash
# Create CA private key
openssl genrsa -out ca.key 4096

# Create CA certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
  -out ca.crt -subj "/CN=Internal CA"

# Create server private key
openssl genrsa -out server.key 2048

# Create CSR
openssl req -new -key server.key -out server.csr \
  -subj "/CN=example.internal"

# Sign with CA
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out server.crt -days 365 -sha256 \
  -extfile <(printf "subjectAltName=DNS:example.internal,DNS:*.example.internal")
```

---

## Mutual TLS (mTLS)

### Nginx mTLS Configuration

```nginx
server {
    listen 443 ssl http2;
    server_name api.example.com;

    # Server certificate
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;

    # Client certificate verification
    ssl_client_certificate /etc/nginx/ssl/ca.crt;
    ssl_verify_client on;
    ssl_verify_depth 2;

    # Pass client cert info to backend
    location / {
        proxy_pass http://backend;
        proxy_set_header X-SSL-Client-Cert $ssl_client_cert;
        proxy_set_header X-SSL-Client-DN $ssl_client_s_dn;
        proxy_set_header X-SSL-Client-Verify $ssl_client_verify;
    }
}
```

### Generate Client Certificate

```bash
# Create client key
openssl genrsa -out client.key 2048

# Create CSR
openssl req -new -key client.key -out client.csr \
  -subj "/CN=client1/O=MyOrg"

# Sign with CA
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out client.crt -days 365 -sha256

# Create PKCS12 bundle (for browser import)
openssl pkcs12 -export -out client.p12 \
  -inkey client.key -in client.crt -certfile ca.crt

# Test connection
curl --cert client.crt --key client.key \
  --cacert ca.crt https://api.example.com/
```

---

## Kubernetes TLS

### TLS Secret

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: example-tls
  namespace: default
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded-cert>
  tls.key: <base64-encoded-key>
```

```bash
# Create from files
kubectl create secret tls example-tls \
  --cert=server.crt --key=server.key
```

### Ingress with TLS

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: example-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  tls:
    - hosts:
        - example.com
        - www.example.com
      secretName: example-tls
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: web-service
                port:
                  number: 80
```

### cert-manager with Let's Encrypt

```yaml
# ClusterIssuer
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
      - http01:
          ingress:
            class: nginx

---
# Certificate
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: example-cert
  namespace: default
spec:
  secretName: example-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: example.com
  dnsNames:
    - example.com
    - www.example.com
```

---

## Certificate Verification

```bash
# View certificate details
openssl x509 -in cert.pem -text -noout

# Check expiration
openssl x509 -in cert.pem -enddate -noout

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt

# Check remote certificate
openssl s_client -connect example.com:443 -servername example.com

# Check TLS 1.3 support
openssl s_client -connect example.com:443 -tls1_3

# Get expiration from remote
echo | openssl s_client -connect example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Check OCSP stapling
openssl s_client -connect example.com:443 -status 2>/dev/null | \
  grep -A 17 "OCSP Response"
```

---

## DNS CAA Records

```
# Restrict certificate issuance to Let's Encrypt only
example.com.  IN  CAA  0  issue "letsencrypt.org"
example.com.  IN  CAA  0  issuewild "letsencrypt.org"
example.com.  IN  CAA  0  iodef "mailto:security@example.com"
```

---

*SSL/TLS Setup Examples | faion-cicd-engineer*
