# SSL/TLS Setup

## Overview

SSL/TLS (Secure Sockets Layer/Transport Layer Security) provides encryption and authentication for network communications. This methodology covers certificate management, configuration best practices, and implementation across various platforms.

## When to Use

- Securing web applications with HTTPS
- Protecting API communications
- Implementing mutual TLS (mTLS) for service-to-service auth
- Meeting compliance requirements (PCI-DSS, HIPAA)
- Securing internal services
- Kubernetes Ingress TLS termination

## Key Concepts

### TLS Versions (2025-2026)

| Version | Status | Notes |
|---------|--------|-------|
| TLS 1.0/1.1 | Deprecated | Do not use |
| TLS 1.2 | Supported | Legacy fallback only |
| TLS 1.3 | **Required** | Expected baseline for 2025+ |

**TLS 1.3 advantages:**
- Simplified handshake (1-RTT vs 2-RTT)
- Removed legacy cryptography
- Only 5 secure defaults vs 15-20 negotiable options in TLS 1.2
- Zero-RTT resumption support

### Certificate Types

| Type | Validation | Use Case | Issuance |
|------|------------|----------|----------|
| DV (Domain Validated) | Domain ownership | Blogs, APIs | Minutes |
| OV (Organization Validated) | Domain + org | Business sites | 1-3 days |
| EV (Extended Validation) | Domain + org + legal | E-commerce, banking | 1-5 days |
| Wildcard | `*.example.com` | Multiple subdomains | Varies |
| Multi-domain (SAN) | Multiple domains | Related domains | Varies |

### Let's Encrypt Updates (2025-2026)

| Feature | Status | Timeline |
|---------|--------|----------|
| 6-day certificates | Available | Feb 2025+ |
| IP address certificates | Available | 2025+ |
| 45-day certificates | Coming | May 2026 |
| 64-day certificates | Coming | Feb 2027 |
| Client Auth EKU removal | Feb 2026 | Alternative profile until May 2026 |

**Short-lived certificates (6-day):**
- Reduced compromise window
- No OCSP/CRL URLs needed
- Better security posture

### Key Size Recommendations

| Algorithm | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| RSA | 2048-bit | 3072-bit | 128-bit security requires 3072-bit |
| ECDSA | 256-bit (P-256) | P-256 or P-384 | Better performance than RSA |
| X25519 | - | Preferred | Modern key exchange |

### Recommended Cipher Suites

**TLS 1.3 (mandatory support):**
```
TLS_AES_128_GCM_SHA256
TLS_AES_256_GCM_SHA384
TLS_CHACHA20_POLY1305_SHA256
```

**TLS 1.2 (legacy fallback):**
```
ECDHE-ECDSA-AES128-GCM-SHA256
ECDHE-RSA-AES128-GCM-SHA256
ECDHE-ECDSA-AES256-GCM-SHA384
ECDHE-RSA-AES256-GCM-SHA384
ECDHE-ECDSA-CHACHA20-POLY1305
ECDHE-RSA-CHACHA20-POLY1305
```

**Avoid:**
- RC4, DES, 3DES, export-grade ciphers
- Static RSA key exchange (no PFS)
- CBC mode ciphers

## Process Overview

### 1. Certificate Acquisition

```
Choose CA → Generate CSR → Validate → Install → Configure → Test
```

**Options:**
- Let's Encrypt (free, automated, 90/45/6-day)
- Commercial CAs (DV/OV/EV)
- Self-signed (dev/internal only)

### 2. Server Configuration

```
Install cert → Configure protocols → Set cipher suites → Enable HSTS → Enable OCSP
```

### 3. Maintenance

```
Monitor expiry → Auto-renew → Rotate keys → Test configuration
```

## Related Files

| File | Purpose |
|------|---------|
| [checklist.md](checklist.md) | Implementation checklist |
| [examples.md](examples.md) | Configuration examples |
| [templates.md](templates.md) | Ready-to-use templates |
| [llm-prompts.md](llm-prompts.md) | AI assistant prompts |

## Tools

| Tool | Purpose |
|------|---------|
| Certbot | Let's Encrypt automation |
| OpenSSL | Certificate operations |
| cert-manager | Kubernetes certificate automation |
| SSL Labs | Configuration testing |
| Mozilla SSL Config Generator | Configuration generation |

## Sources

- [Mozilla SSL Configuration Generator](https://ssl-config.mozilla.org/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Let's Encrypt - Decreasing Certificate Lifetimes](https://letsencrypt.org/2025/12/02/from-90-to-45)
- [Let's Encrypt - 6-Day Certificates](https://letsencrypt.org/2025/01/16/6-day-and-ip-certs)
- [SSL Labs Best Practices](https://github.com/ssllabs/research/wiki/SSL-and-TLS-Deployment-Best-Practices)
- [Cloudflare Cipher Suite Recommendations](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/cipher-suites/recommendations/)
- [Networking TLS Best Practices Q1 2025](https://community.citrix.com/tech-zone/build/tech-papers/networking-tls-best-practices-2025/)
- [cert-manager Documentation](https://cert-manager.io/docs/)

---

*SSL/TLS Setup | faion-cicd-engineer*
