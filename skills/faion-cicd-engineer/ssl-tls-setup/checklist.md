# SSL/TLS Setup Checklist

## Pre-Implementation

- [ ] Identify all domains requiring certificates
- [ ] Determine certificate type needed (DV/OV/EV/Wildcard)
- [ ] Choose certificate authority (Let's Encrypt recommended)
- [ ] Plan certificate renewal automation
- [ ] Document current TLS configuration baseline

## Certificate Acquisition

### Let's Encrypt

- [ ] Install Certbot or ACME client
- [ ] Configure webroot or standalone validation
- [ ] Generate certificates for all domains
- [ ] Verify certificate chain is complete
- [ ] Set up automatic renewal (systemd timer or cron)
- [ ] Test renewal with `--dry-run`
- [ ] Configure ARI (ACME Renewal Information) checks

### Commercial CA

- [ ] Generate CSR with proper key size (2048+ RSA or P-256+ ECDSA)
- [ ] Submit for validation
- [ ] Download full certificate chain
- [ ] Store private key securely (chmod 600)

## Server Configuration

### Protocol Settings

- [ ] Enable TLS 1.3 (required)
- [ ] Enable TLS 1.2 (legacy fallback if needed)
- [ ] Disable TLS 1.0 and TLS 1.1
- [ ] Disable SSL 2.0 and SSL 3.0

### Cipher Suites

- [ ] Configure TLS 1.3 ciphers:
  - [ ] TLS_AES_128_GCM_SHA256
  - [ ] TLS_AES_256_GCM_SHA384
  - [ ] TLS_CHACHA20_POLY1305_SHA256
- [ ] Configure TLS 1.2 ciphers (ECDHE + AEAD only)
- [ ] Disable RC4, DES, 3DES, export ciphers
- [ ] Disable static RSA key exchange
- [ ] Set `ssl_prefer_server_ciphers off` for TLS 1.3

### Security Headers

- [ ] Enable HSTS (`max-age=63072000; includeSubDomains; preload`)
- [ ] Consider HSTS preload submission
- [ ] Configure OCSP stapling
- [ ] Set resolver for OCSP

### Performance

- [ ] Enable session resumption
- [ ] Configure session cache
- [ ] Disable session tickets (or rotate keys)
- [ ] Generate DH parameters (2048-bit minimum)

## Kubernetes/Cloud

### cert-manager

- [ ] Install cert-manager
- [ ] Configure ClusterIssuer for Let's Encrypt
- [ ] Set up staging issuer for testing
- [ ] Configure Certificate resources
- [ ] Verify auto-renewal works

### Ingress

- [ ] Configure TLS termination
- [ ] Set minimum TLS version annotation
- [ ] Configure cipher suites annotation
- [ ] Enable HSTS annotation

## DNS Configuration

- [ ] Configure CAA records to restrict issuers
- [ ] Set up CAA iodef for notifications
- [ ] Consider DANE/TLSA records for additional security

## Monitoring & Alerting

- [ ] Set up certificate expiry monitoring
- [ ] Configure alerts at 30, 14, 7, 3 days
- [ ] Monitor SSL Labs grade (maintain A+)
- [ ] Set up CT log monitoring
- [ ] Monitor TLS version usage in logs

## Testing

- [ ] Test with SSL Labs (target A+ rating)
- [ ] Verify certificate chain with OpenSSL
- [ ] Test from multiple locations/browsers
- [ ] Verify HTTP to HTTPS redirect
- [ ] Test HSTS header presence
- [ ] Verify OCSP stapling works
- [ ] Test mTLS if configured

## Security Hardening

- [ ] Secure private key permissions (600)
- [ ] Store keys in secrets manager if possible
- [ ] Document key rotation procedure
- [ ] Plan revocation process
- [ ] Enable Certificate Transparency monitoring

## Documentation

- [ ] Document certificate locations
- [ ] Document renewal process
- [ ] Document emergency procedures
- [ ] Update runbooks

## Post-Implementation

- [ ] Verify production traffic uses TLS 1.3
- [ ] Check for mixed content warnings
- [ ] Validate all APIs accessible via HTTPS
- [ ] Confirm no certificate warnings in browsers
- [ ] Schedule quarterly configuration review

---

## Quick Verification Commands

```bash
# Check certificate expiry
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates

# Check TLS version support
openssl s_client -connect example.com:443 -tls1_3

# Check cipher suites
nmap --script ssl-enum-ciphers -p 443 example.com

# Test certificate chain
openssl verify -CAfile chain.pem cert.pem

# Check OCSP stapling
openssl s_client -connect example.com:443 -status

# Test renewal
sudo certbot renew --dry-run
```

---

*SSL/TLS Setup Checklist | faion-cicd-engineer*
