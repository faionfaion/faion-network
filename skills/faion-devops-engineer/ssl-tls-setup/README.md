# SSL/TLS Setup

## Overview

SSL/TLS (Secure Sockets Layer/Transport Layer Security) provides encryption and authentication for network communications. This methodology covers certificate management, configuration best practices, and implementation across various platforms.

## When to Use

- Securing web applications with HTTPS
- Protecting API communications
- Implementing mutual TLS (mTLS) for service-to-service auth
- Meeting compliance requirements (PCI-DSS, HIPAA)
- Securing internal services
- Kubernetes ingress TLS termination

## Key Concepts

### TLS Versions

| Version | Status | Notes |
|---------|--------|-------|
| TLS 1.0 | Deprecated | Do not use |
| TLS 1.1 | Deprecated | Do not use |
| TLS 1.2 | Supported | Minimum recommended |
| TLS 1.3 | Preferred | Best performance and security |

### Certificate Types

| Type | Validation | Use Case | Issuance |
|------|------------|----------|----------|
| Domain Validated (DV) | Domain ownership | Blogs, personal sites | Minutes |
| Organization Validated (OV) | Domain + org | Business websites | 1-3 days |
| Extended Validation (EV) | Domain + org + legal | E-commerce, banking | 1-5 days |
| Wildcard | Covers subdomains | Multiple subdomains | Varies |
| Multi-domain (SAN) | Multiple domains | Related domains | Varies |

## Certificate Validity Changes (2025-2029)

The CA/Browser Forum approved Ballot SC-081v3 in April 2025, reducing certificate validity periods:

| Date | Max Validity | DCV Reuse |
|------|--------------|-----------|
| Current | 398 days | - |
| March 15, 2026 | 200 days | 200 days |
| March 15, 2027 | 100 days | 100 days |
| March 15, 2029 | 47 days | 10 days |

### Let's Encrypt Timeline

| Date | Change |
|------|--------|
| May 13, 2026 | tlsserver profile: 45-day certs (opt-in) |
| February 10, 2027 | classic profile: 64-day certs |
| February 16, 2028 | classic profile: 45-day certs |

**Implication:** Automation is now mandatory, not optional.

## TLS 1.3 Features

- Removed outdated cryptographic algorithms
- Faster handshake (1-RTT, 0-RTT resumption)
- Perfect forward secrecy enforced by default
- Simplified cipher suite negotiation
- Encrypted handshake metadata

### Post-Quantum Cryptography (PQC)

NIST published 3 PQC standards in August 2024:
- **ML-KEM** (Kyber) - Key encapsulation
- **ML-DSA** (Dilithium) - Digital signatures
- **SLH-DSA** (SPHINCS+) - Hash-based signatures

Hybrid TLS 1.3 + ML-KEM is being deployed by major providers (Cloudflare, Google).

## Certificate Management Best Practices

### Automation Requirements

1. **Discovery** - Identify all certificates across environments
2. **Inventory** - Centralized tracking of expiration dates, CAs, systems
3. **Issuance** - Automated provisioning via ACME
4. **Renewal** - Auto-renewal before expiration (30-day buffer minimum)
5. **Revocation** - Plan for compromised key scenarios

### Security Configuration

1. **TLS 1.2 minimum** - Disable older versions
2. **Strong ciphers** - Follow Mozilla recommendations
3. **HSTS** - Prevent protocol downgrade attacks
4. **OCSP stapling** - Faster certificate verification
5. **CAA records** - Restrict certificate issuance to specific CAs
6. **Certificate Transparency** - Monitor for unauthorized certificates

### Monitoring

| Alert | Threshold |
|-------|-----------|
| Expiry warning | 30, 14, 7 days |
| SSL Labs grade | Below A |
| CT log alerts | New certificate issued |
| Protocol monitoring | Unexpected TLS versions |

## Files in This Directory

| File | Description |
|------|-------------|
| [README.md](README.md) | This overview document |
| [checklist.md](checklist.md) | Implementation and audit checklists |
| [examples.md](examples.md) | Configuration examples for various platforms |
| [templates.md](templates.md) | Reusable configuration templates |
| [llm-prompts.md](llm-prompts.md) | Prompts for SSL/TLS tasks |

## Quick Commands

```bash
# Check certificate expiration
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -dates

# Test TLS configuration
openssl s_client -connect example.com:443 -tls1_3

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt

# Generate DH parameters
openssl dhparam -out dhparam.pem 2048

# Test renewal
sudo certbot renew --dry-run
```

## Sources

- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [SSL Labs Best Practices](https://www.ssllabs.com/projects/best-practices/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [Let's Encrypt 45-Day Certificates](https://letsencrypt.org/2025/12/02/from-90-to-45)
- [SSL Certificate Validity Changes 2025](https://www.wwt.com/blog/ssl-certificate-validity-changes-2025-how-to-prepare-your-business-now)
- [TLS Certificate Management 2026](https://www.cyberark.com/resources/blog/tls-certificate-management-in-2026-the-endless-game-of-whack-a-cert)
