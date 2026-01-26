# SSL/TLS Setup LLM Prompts

## Certificate Generation

### Generate Let's Encrypt Certificate

```
Generate Certbot commands to obtain SSL certificates for the following configuration:

Domain: [DOMAIN]
Additional domains: [LIST]
Web server: [nginx/apache/standalone]
Validation method: [http/dns/webroot]
Environment: [production/staging]
Non-interactive: [yes/no]

Include:
1. Installation commands for the OS
2. Certificate generation command
3. Auto-renewal setup
4. Post-renewal hook if needed
```

### Generate Self-Signed Certificate

```
Generate OpenSSL commands to create a self-signed certificate with:

Common Name: [CN]
Subject Alternative Names: [DNS names, IP addresses]
Key algorithm: [RSA 2048/RSA 4096/ECDSA P-256/ECDSA P-384]
Validity: [days]
Purpose: [development/internal/mTLS]

Include the complete command with all necessary extensions.
```

### Create Internal CA

```
Generate OpenSSL commands to create an internal Certificate Authority and sign server certificates:

CA Name: [CA_NAME]
CA Validity: [years]
Server domains: [LIST]
Client certificates needed: [yes/no]

Provide:
1. CA key and certificate generation
2. Server certificate signing
3. Client certificate signing (if needed)
4. Verification commands
```

---

## Server Configuration

### Configure Nginx SSL/TLS

```
Generate a modern Nginx SSL/TLS configuration for:

Domain: [DOMAIN]
Certificate path: [PATH]
TLS versions: [1.2+1.3 / 1.3 only]
HSTS: [yes/no]
OCSP stapling: [yes/no]
HTTP/2: [yes/no]

Requirements:
- A+ rating on SSL Labs
- Forward secrecy
- Modern cipher suites only
- Proper security headers

Provide both the ssl-params.conf snippet and the server block.
```

### Configure Apache SSL/TLS

```
Generate a modern Apache SSL/TLS configuration for:

Domain: [DOMAIN]
Certificate path: [PATH]
TLS versions: [1.2+1.3 / 1.3 only]
HSTS: [yes/no]
OCSP stapling: [yes/no]

Include:
1. VirtualHost for HTTP redirect
2. VirtualHost for HTTPS
3. Modern cipher configuration
4. Security headers
```

### Configure mTLS

```
Configure mutual TLS (mTLS) for:

Server: [nginx/apache/traefik]
Server certificate: [PATH]
CA certificate for client verification: [PATH]
Verify depth: [NUMBER]
Backend: [URL if proxying]

Include:
1. Server configuration
2. Client certificate generation commands
3. Testing command with curl
```

---

## Kubernetes Configuration

### Setup cert-manager

```
Generate Kubernetes manifests for cert-manager with Let's Encrypt:

Email: [ADMIN_EMAIL]
Environments: [staging/production/both]
Challenge type: [http01/dns01]
Ingress class: [nginx/traefik/other]
Namespace: [default/custom]

Provide:
1. ClusterIssuer resources
2. Example Certificate resource
3. Example Ingress with TLS
4. Annotations for automatic certificate management
```

### Configure Ingress TLS

```
Generate Kubernetes Ingress with TLS for:

Domains: [LIST]
Service name: [NAME]
Service port: [PORT]
Namespace: [NAMESPACE]
cert-manager issuer: [NAME]
Additional annotations: [LIST]

Include TLS configuration, HSTS, and redirect settings.
```

---

## Monitoring & Troubleshooting

### Certificate Monitoring Script

```
Generate a shell script to monitor SSL certificate expiration for:

Domains: [LIST]
Alert threshold: [DAYS]
Critical threshold: [DAYS]
Notification method: [email/slack/webhook]

Include:
1. Certificate expiry check
2. Alert logic
3. Output formatting
4. Error handling for unreachable domains
```

### Debug SSL Connection

```
I'm having SSL/TLS issues with [DOMAIN]. Help me debug:

Error message: [ERROR]
Web server: [nginx/apache/other]
Certificate source: [Let's Encrypt/commercial/self-signed]

Provide:
1. OpenSSL commands to diagnose the issue
2. Common causes for this error
3. Resolution steps
```

### Fix Certificate Chain

```
My SSL certificate shows a chain error. Help me fix:

Domain: [DOMAIN]
CA: [CA_NAME]
Certificate files available: [LIST]
Web server: [nginx/apache]

Provide:
1. Commands to check the current chain
2. How to create the correct fullchain
3. Server configuration to use the chain
```

---

## Migration & Upgrade

### Migrate to TLS 1.3

```
Help me migrate from TLS 1.2 to TLS 1.3:

Current server: [nginx/apache]
Current TLS config: [paste config]
Must maintain TLS 1.2 fallback: [yes/no]
Operating system: [OS]

Provide:
1. Prerequisites check
2. Updated configuration
3. Testing commands
4. Rollback plan
```

### Migrate Certificates

```
Help me migrate SSL certificates to a new server:

Source server: [IP/hostname]
Destination server: [IP/hostname]
Certificate type: [Let's Encrypt/commercial]
Domains: [LIST]
Web server: [nginx/apache]

Provide:
1. Certificate export steps
2. Certificate import steps
3. Renewal configuration
4. Verification steps
```

---

## Security Hardening

### Audit SSL Configuration

```
Audit this SSL/TLS configuration for security issues:

[PASTE CONFIGURATION]

Check for:
1. Deprecated protocols
2. Weak ciphers
3. Missing security features
4. Performance optimizations
5. Compliance issues

Provide specific recommendations for improvement.
```

### Configure CAA Records

```
Generate DNS CAA records for:

Domain: [DOMAIN]
Allowed CAs: [LIST]
Security contact: [EMAIL]
Wildcard issuance: [same CA/different CA/none]

Provide:
1. CAA record format
2. Explanation of each record
3. Testing command
```

---

## Cloud-Specific

### AWS Certificate Manager

```
Generate Terraform/CloudFormation for ACM certificate:

Domain: [DOMAIN]
Subject alternative names: [LIST]
Validation method: [DNS/email]
Route53 zone: [yes/no]
Use with: [ALB/CloudFront/API Gateway]

Include:
1. Certificate resource
2. Validation records (if DNS)
3. Integration with load balancer
```

### GCP Managed Certificates

```
Generate configuration for Google-managed SSL certificates:

Domain: [DOMAIN]
Additional domains: [LIST]
Load balancer type: [HTTPS/SSL Proxy]

Provide:
1. ManagedCertificate resource
2. Ingress annotation
3. Verification steps
```

---

## Quick Prompts

### Check Certificate Expiry

```
Generate a one-liner to check SSL certificate expiry for [DOMAIN]
```

### Decode Certificate

```
Decode this certificate and explain its contents:
[PASTE CERTIFICATE]
```

### Generate CSR

```
Generate a CSR for [DOMAIN] with [RSA 2048/ECDSA P-256] key
```

### Test TLS Connection

```
Generate OpenSSL commands to test TLS connection to [DOMAIN]:
- Check supported protocols
- Check cipher suites
- Verify certificate chain
- Check OCSP stapling
```

---

## Response Format Guidelines

When using these prompts, expect responses that include:

1. **Commands**: Ready-to-run shell commands
2. **Configuration**: Copy-paste ready config files
3. **Verification**: Commands to verify the setup works
4. **Troubleshooting**: Common issues and solutions
5. **Security notes**: Important security considerations

---

*SSL/TLS Setup LLM Prompts | faion-cicd-engineer*
