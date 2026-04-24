# SSL/TLS LLM Prompts

## Certificate Issuance

### Let's Encrypt Setup

```
Set up Let's Encrypt SSL certificate for [DOMAIN] with the following requirements:
- Web server: [nginx/apache/standalone]
- Challenge type: [http-01/dns-01]
- Include subdomains: [www.DOMAIN, api.DOMAIN, etc.]
- Auto-renewal: enabled

Provide:
1. Installation commands
2. Certificate generation command
3. Web server configuration
4. Auto-renewal setup
5. Verification steps
```

### Wildcard Certificate

```
Generate wildcard SSL certificate for *.DOMAIN using Let's Encrypt:
- DNS provider: [cloudflare/route53/manual]
- Include root domain: [yes/no]

Provide:
1. DNS challenge setup
2. API credentials configuration (if automated)
3. Certificate generation command
4. Renewal automation for DNS challenge
```

---

## Web Server Configuration

### Nginx SSL Optimization

```
Optimize Nginx SSL/TLS configuration for [DOMAIN]:
- TLS versions: TLS 1.2 and 1.3 only
- Cipher suites: Mozilla Intermediate
- Enable: HSTS, OCSP stapling
- Certificate path: [/path/to/cert]

Generate:
1. ssl-params.conf snippet
2. Server block configuration
3. DH parameters generation command
4. Security headers
```

### Apache SSL Setup

```
Configure Apache SSL for [DOMAIN] with:
- Modern TLS settings (TLS 1.2+)
- OCSP stapling
- HSTS header
- HTTP to HTTPS redirect

Output:
1. VirtualHost configuration
2. Required Apache modules
3. Stapling cache configuration
```

---

## Certificate Troubleshooting

### Debug SSL Issues

```
Diagnose SSL certificate issue:
- Domain: [DOMAIN]
- Error: [error message or symptom]
- Web server: [nginx/apache/other]

Provide:
1. Diagnostic commands to run
2. Common causes for this error
3. Step-by-step resolution
4. Verification commands
```

### Certificate Chain Issues

```
Fix certificate chain for [DOMAIN]:
- Symptom: [incomplete chain/wrong order/missing intermediate]
- Certificate source: [Let's Encrypt/DigiCert/other]

Provide:
1. Commands to inspect current chain
2. Correct chain order
3. How to obtain missing certificates
4. Web server configuration fix
```

---

## Kubernetes TLS

### Ingress TLS Setup

```
Configure TLS for Kubernetes Ingress:
- Domain: [DOMAIN]
- Ingress controller: [nginx/traefik/other]
- Certificate management: [cert-manager/manual]
- Namespace: [NAMESPACE]

Generate:
1. TLS Secret (if manual)
2. Ingress resource with TLS
3. cert-manager resources (if automated)
4. Required annotations
```

### cert-manager Configuration

```
Set up cert-manager for automatic Let's Encrypt certificates:
- Challenge type: [http-01/dns-01]
- DNS provider: [cloudflare/route53/other] (if dns-01)
- Ingress class: [nginx/traefik]

Generate:
1. cert-manager installation command
2. ClusterIssuer resource
3. Certificate resource
4. Ingress annotations for auto-issuance
```

---

## mTLS Setup

### Service-to-Service mTLS

```
Implement mutual TLS between services:
- Server: [service name]
- Clients: [list of client services]
- Platform: [bare metal/kubernetes/docker]

Provide:
1. CA setup and certificate generation
2. Server configuration for client verification
3. Client certificate generation
4. Client configuration
5. Testing commands
```

### Nginx mTLS Proxy

```
Configure Nginx as mTLS-terminating reverse proxy:
- Backend: [backend service URL]
- Client verification: [required/optional]
- Pass client info to backend: [yes/no]

Generate:
1. Nginx server configuration
2. Client certificate generation script
3. Testing curl commands
```

---

## Monitoring and Alerts

### Certificate Expiry Monitoring

```
Create certificate expiry monitoring for:
- Domains: [list of domains]
- Alert thresholds: [30, 14, 7 days]
- Notification: [slack/email/pagerduty]

Provide:
1. Bash monitoring script
2. Cron job configuration
3. Notification integration
4. Prometheus alerting rules (optional)
```

### SSL Labs Automation

```
Automate SSL Labs testing for [DOMAIN]:
- Schedule: [weekly/after deployment]
- Minimum grade: [A+/A/B]
- Alert on regression: yes

Provide:
1. SSL Labs API script
2. CI/CD integration
3. Alerting on grade drop
```

---

## Migration Tasks

### HTTP to HTTPS Migration

```
Migrate [DOMAIN] from HTTP to HTTPS:
- Current setup: [describe current state]
- Content: [static/dynamic/mixed]
- SEO consideration: [yes/no]

Provide step-by-step:
1. Pre-migration checklist
2. Certificate setup
3. Redirect configuration
4. Mixed content fixes
5. SEO updates (sitemap, canonical)
6. Verification steps
```

### TLS Version Upgrade

```
Upgrade TLS configuration from [current] to TLS 1.2/1.3 only:
- Web server: [nginx/apache]
- Client compatibility requirements: [modern browsers only/legacy support]

Provide:
1. Compatibility impact analysis
2. Configuration changes
3. Testing commands for each TLS version
4. Rollback procedure
```

---

## Security Audit

### SSL Security Assessment

```
Perform SSL/TLS security assessment for [DOMAIN]:
- Check: protocols, ciphers, certificates, headers
- Compliance: [PCI-DSS/HIPAA/general]

Provide:
1. Assessment commands and tools
2. Expected secure configuration
3. Gap analysis format
4. Remediation recommendations
```

### CAA Record Setup

```
Configure CAA DNS records for [DOMAIN]:
- Authorized CAs: [letsencrypt.org, digicert.com]
- Wildcard issuance: [same CA/different CA/disallow]
- Incident reporting: [security email]

Provide:
1. CAA record values
2. DNS provider configuration
3. Verification commands
```

---

## Automation Scripts

### Certbot Automation

```
Create automated certificate management for multiple domains:
- Domains: [list with challenge type for each]
- Hooks: [pre/post/deploy]
- Notifications: [on success/failure]

Generate:
1. Certbot CLI wrapper script
2. Renewal hooks
3. Logging configuration
4. Error handling and notifications
```

### Certificate Rotation

```
Implement certificate rotation procedure for [environment]:
- Current method: [manual/certbot/cert-manager]
- Rotation trigger: [scheduled/on-demand]
- Zero-downtime requirement: [yes/no]

Provide:
1. Rotation script/procedure
2. Validation steps
3. Rollback procedure
4. Logging and audit trail
```

---

## Prompt Templates for Specific Scenarios

### Quick SSL Fix

```
I'm getting SSL error "[ERROR MESSAGE]" when accessing [DOMAIN].

Current setup:
- Web server: [TYPE]
- Certificate: [SOURCE]
- Last working: [DATE/never]

What I've tried:
- [LIST ATTEMPTS]

Help me fix this issue.
```

### New Domain SSL

```
Set up SSL for new domain [DOMAIN]:
- Purpose: [website/API/internal]
- Expected traffic: [low/medium/high]
- Budget for SSL: [free/paid]
- Required features: [wildcard/EV/multi-domain]

Provide complete setup guide.
```

### SSL Renewal Failed

```
Certbot renewal failed with error:
```
[PASTE ERROR]
```

Domain: [DOMAIN]
Challenge type: [http-01/dns-01]
Last successful renewal: [DATE]

Help diagnose and fix.
```

---

## Context Variables for Prompts

When using these prompts, provide these context variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `[DOMAIN]` | Target domain | `example.com` |
| `[WEB_SERVER]` | Web server type | `nginx`, `apache` |
| `[CERT_PATH]` | Certificate file path | `/etc/letsencrypt/live/example.com` |
| `[NAMESPACE]` | K8s namespace | `production` |
| `[CA]` | Certificate Authority | `letsencrypt`, `digicert` |
| `[CHALLENGE]` | ACME challenge type | `http-01`, `dns-01` |
| `[ERROR]` | Error message | Full error text |
