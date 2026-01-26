# SSL/TLS Checklists

## New Domain Setup Checklist

### Pre-Implementation

- [ ] Domain ownership verified
- [ ] DNS access available
- [ ] Web server access (root/sudo)
- [ ] Port 80/443 open in firewall
- [ ] Certbot or ACME client installed

### Certificate Issuance

- [ ] Choose certificate type (DV, OV, EV, wildcard)
- [ ] Generate certificate via Let's Encrypt or CA
- [ ] Verify certificate chain is complete
- [ ] Store private key securely (600 permissions)
- [ ] Backup certificate and key

### Web Server Configuration

- [ ] TLS 1.2 and TLS 1.3 only enabled
- [ ] Strong cipher suites configured
- [ ] DH parameters generated (2048+ bit)
- [ ] OCSP stapling enabled
- [ ] Session tickets disabled (or properly rotated)
- [ ] HTTP to HTTPS redirect configured

### Security Headers

- [ ] HSTS enabled (max-age >= 31536000)
- [ ] HSTS includeSubDomains if applicable
- [ ] HSTS preload if committed long-term
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options configured

### DNS Configuration

- [ ] CAA record added (restrict to your CA)
- [ ] AAAA record if IPv6 supported
- [ ] www subdomain configured

### Automation

- [ ] Auto-renewal configured (certbot timer/cron)
- [ ] Renewal hooks set (reload web server)
- [ ] Renewal tested with --dry-run
- [ ] Monitoring for expiration alerts

### Verification

- [ ] SSL Labs test: A+ grade
- [ ] All TLS versions tested
- [ ] Certificate transparency logged
- [ ] Mobile browser tested

---

## Security Audit Checklist

### Protocol Security

- [ ] TLS 1.0 disabled
- [ ] TLS 1.1 disabled
- [ ] TLS 1.2 enabled (minimum)
- [ ] TLS 1.3 enabled (preferred)
- [ ] SSLv2/SSLv3 disabled
- [ ] Compression disabled (CRIME attack)
- [ ] Renegotiation secure or disabled

### Cipher Suite Audit

- [ ] No NULL ciphers
- [ ] No EXPORT ciphers
- [ ] No DES/3DES ciphers
- [ ] No RC4 ciphers
- [ ] No MD5 for MAC
- [ ] ECDHE or DHE for key exchange (forward secrecy)
- [ ] AES-GCM or ChaCha20-Poly1305 preferred

### Certificate Audit

- [ ] RSA key >= 2048 bits OR ECDSA P-256+
- [ ] SHA-256 or stronger signature
- [ ] Valid certificate chain
- [ ] Intermediate certificates present
- [ ] Certificate not expired
- [ ] Certificate matches domain
- [ ] SAN includes all required domains

### HSTS Verification

- [ ] Strict-Transport-Security header present
- [ ] max-age >= 31536000 (1 year)
- [ ] includeSubDomains if all subdomains HTTPS
- [ ] preload if on HSTS preload list

### OCSP Configuration

- [ ] OCSP stapling enabled
- [ ] OCSP response valid
- [ ] Must-staple extension (optional)

### Key Management

- [ ] Private key permissions 600 or stricter
- [ ] Private key not in web root
- [ ] Key not committed to version control
- [ ] Key rotation plan documented

---

## Certificate Renewal Checklist

### Pre-Renewal (30 days before expiry)

- [ ] Verify renewal automation is working
- [ ] Test renewal with --dry-run
- [ ] Check ACME account status
- [ ] Verify DNS/HTTP challenge path accessible

### During Renewal

- [ ] Certificate issued successfully
- [ ] New certificate chain complete
- [ ] New private key generated (if rotating)
- [ ] Old certificate backed up

### Post-Renewal

- [ ] Web server reloaded
- [ ] New certificate serving verified
- [ ] SSL Labs test passed
- [ ] Application tested
- [ ] Monitoring confirmed new expiry date

---

## Kubernetes TLS Checklist

### Ingress TLS

- [ ] TLS secret created with correct data
- [ ] Secret in correct namespace
- [ ] Ingress references correct secret name
- [ ] ssl-redirect annotation enabled
- [ ] force-ssl-redirect annotation enabled

### cert-manager Setup

- [ ] cert-manager installed
- [ ] ClusterIssuer or Issuer created
- [ ] ACME email configured
- [ ] Solver type configured (HTTP-01 or DNS-01)
- [ ] Certificate resource created
- [ ] Certificate status: Ready

### mTLS (Service Mesh)

- [ ] Root CA configured
- [ ] Client certificates generated
- [ ] Server certificate verification enabled
- [ ] Client certificate verification enabled
- [ ] Certificate rotation automated

---

## Incident Response Checklist

### Key Compromise

- [ ] Revoke compromised certificate immediately
- [ ] Generate new private key
- [ ] Request new certificate
- [ ] Deploy new certificate
- [ ] Update all services using the key
- [ ] Audit access logs for unauthorized use
- [ ] Document incident timeline

### Certificate Expiration

- [ ] Identify affected services
- [ ] Issue emergency certificate
- [ ] Deploy to all endpoints
- [ ] Verify service restoration
- [ ] Fix automation failure
- [ ] Add additional monitoring
- [ ] Post-mortem review

---

## Migration Checklist (HTTP to HTTPS)

### Preparation

- [ ] Audit all HTTP resources
- [ ] Update hardcoded HTTP URLs
- [ ] Configure mixed content handling
- [ ] Test in staging environment

### Implementation

- [ ] Deploy SSL certificate
- [ ] Enable HTTPS on web server
- [ ] Implement 301 redirects HTTP -> HTTPS
- [ ] Update canonical URLs
- [ ] Update sitemap URLs
- [ ] Update robots.txt

### Post-Migration

- [ ] Submit new sitemap to search engines
- [ ] Update external links where possible
- [ ] Monitor for mixed content warnings
- [ ] Enable HSTS after verification
- [ ] Update CDN configuration
- [ ] Update monitoring endpoints
