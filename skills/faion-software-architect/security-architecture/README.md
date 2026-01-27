# Security Architecture

Designing secure systems with defense in depth, Zero Trust principles, and modern authentication/authorization patterns.

## Overview

Security architecture is the systematic approach to protecting systems, data, and users through layered defenses. Modern security architecture follows the principle of "never trust, always verify" (Zero Trust) while implementing defense in depth across all layers.

## Core Security Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Defense in Depth** | Multiple security layers | WAF + Network + Identity + Application + Data |
| **Least Privilege** | Minimal permissions required | RBAC/ABAC with granular scopes |
| **Zero Trust** | Never trust, always verify | Continuous authentication, mTLS |
| **Fail Secure** | Default to deny | Whitelist over blacklist |
| **Separation of Duties** | Split responsibilities | Multi-party approval, segregated roles |
| **Assume Breach** | Design for compromise | Segmentation, detection, response |

## Security Layers

```
+---------------------------------------------------------+
|                     Perimeter Layer                      |
|  WAF, DDoS protection, CDN security, Edge computing     |
+---------------------------------------------------------+
|                     Network Layer                        |
|  Firewalls, VPCs, Network policies, Micro-segmentation  |
+---------------------------------------------------------+
|                     Identity Layer                       |
|  Authentication (OAuth/OIDC/Passkeys), Authorization    |
+---------------------------------------------------------+
|                    Application Layer                     |
|  Input validation, Output encoding, OWASP Top 10        |
+---------------------------------------------------------+
|                      Data Layer                          |
|  Encryption (rest/transit/E2E), Classification, DLP     |
+---------------------------------------------------------+
```

## Zero Trust Architecture (NIST SP 800-207)

### The 7 Pillars of Zero Trust

| Pillar | Description | Key Controls |
|--------|-------------|--------------|
| **Identity** | Verify every user/entity | MFA, SSO, continuous auth, identity governance |
| **Device** | Validate device health | EDR, compliance checks, certificate-based identity |
| **Network** | Micro-segment access | Software-defined perimeter, east-west encryption |
| **Application** | Secure app access | CASB, ZTNA, application-level auth |
| **Data** | Protect data everywhere | Classification, DLP, encryption |
| **Infrastructure** | Secure compute/storage | IaC scanning, runtime protection |
| **Visibility** | Monitor everything | SIEM, XDR, continuous monitoring |

### Zero Trust Implementation Approach

```
Traditional: Trust but verify (perimeter-based)
                    |
                    v
Zero Trust: Never trust, always verify (identity-based)

Every request must:
1. Verify identity (who) - Strong authentication
2. Verify device (what) - Device posture check
3. Verify context (where, when) - Risk-based policies
4. Grant minimal access - Just-in-time, just-enough
5. Log everything - Continuous monitoring
```

**NIST SP 1800-35** (2025) provides 19 real-world implementation models with technical configurations for building ZTA.

## Authentication Patterns

### Modern Authentication Stack (2025)

| Method | Use Case | Security Level |
|--------|----------|----------------|
| **Passkeys (FIDO2)** | Primary auth, passwordless | AAL2 (phishing-resistant) |
| **OAuth 2.1 + PKCE** | API/app authorization | High (with proper implementation) |
| **OIDC** | Identity federation | High |
| **mTLS** | Service-to-service | Very High |
| **API Keys** | Machine-to-machine (limited) | Medium (with rotation) |

### OAuth 2.1 / OIDC Flow

```
+--------+                               +---------------+
|        |--(A)-- Authorization Request->|   Resource    |
|        |                               |     Owner     |
|        |<-(B)-- Authorization Grant ---|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(C)-- Authorization Grant -->| Authorization |
| Client |                               |     Server    |
|        |<-(D)------ Access Token ------|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(E)------ Access Token ----->|    Resource   |
|        |                               |     Server    |
|        |<-(F)---- Protected Resource --|               |
+--------+                               +---------------+
```

**OAuth 2.1 Key Requirements (RFC 9700):**
- PKCE required for ALL clients (public and confidential)
- Exact redirect URI matching
- No Implicit grant (response_type=token removed)
- No Resource Owner Password Credentials grant
- Sender-constrained tokens (DPoP or mTLS) recommended
- Refresh token rotation for public clients

### Passkeys (FIDO2/WebAuthn)

```
Registration:
User -> Authenticator -> Generate Key Pair -> Public Key -> Server

Authentication:
Server -> Challenge -> Authenticator -> Sign with Private Key -> Verify
```

**Benefits:**
- Phishing-resistant (origin-bound credentials)
- No shared secrets
- Biometric convenience
- NIST AAL2 compliant
- 74% consumer awareness (2025)

## Authorization Models

### Comparison Matrix

| Model | Best For | Complexity | Flexibility | Scalability |
|-------|----------|------------|-------------|-------------|
| **RBAC** | Static organizations, most apps | Low | Low | Medium |
| **ABAC** | Context-aware policies | High | Very High | Medium |
| **ReBAC** | Social graphs, hierarchies | Medium | High | Very High |
| **PBAC** | Centralized policy management | Medium | High | High |

### RBAC (Role-Based Access Control)

```yaml
roles:
  admin:
    permissions: [users:*, content:*, settings:*]
  editor:
    permissions: [content:read, content:write]
  viewer:
    permissions: [content:read]

users:
  alice:
    roles: [admin]
  bob:
    roles: [editor, viewer]
```

### ABAC (Attribute-Based Access Control)

```yaml
# Policy: Managers can approve discounts > 20% during business hours
policy:
  subject:
    role: manager
    tenure_years: ">= 2"
  resource:
    type: discount
    amount: "> 20%"
  environment:
    time: "09:00-17:00"
    location: corporate_network
  action: approve
```

### ReBAC (Relationship-Based Access Control)

```
# OpenFGA / Zanzibar-style model
type user

type document
  relations
    define owner: [user]
    define editor: [user] or owner
    define viewer: [user] or editor

# Tuples
document:budget.xlsx#owner@user:alice
document:budget.xlsx#viewer@user:bob

# Check: can bob view budget.xlsx?
# Result: true (bob is viewer)
```

**Popular ReBAC Solutions:**
- OpenFGA (CNCF Sandbox)
- SpiceDB/AuthZed
- Ory Keto
- AWS Verified Permissions

## API Security

### OWASP API Security Top 10 (2023)

| Risk | Description | Mitigation |
|------|-------------|------------|
| **API1** | Broken Object-Level Authorization | Per-object authorization checks |
| **API2** | Broken Authentication | OAuth 2.1, MFA, rate limiting |
| **API3** | Broken Object Property-Level Auth | Field-level access control |
| **API4** | Unrestricted Resource Consumption | Rate limiting, pagination |
| **API5** | Broken Function-Level Auth | RBAC per endpoint |
| **API6** | Unrestricted Access to Sensitive Flows | Business logic validation |
| **API7** | Server-Side Request Forgery | URL validation, allowlists |
| **API8** | Security Misconfiguration | Hardening, secure defaults |
| **API9** | Improper Inventory Management | API discovery, documentation |
| **API10** | Unsafe Consumption of APIs | Validate third-party data |

### API Gateway Security Pattern

```
Client -> API Gateway -> Backend Services
              |
              +-- Rate limiting (per client/endpoint)
              +-- Authentication (OAuth/API key validation)
              +-- Authorization (scope/role checking)
              +-- Input validation (schema validation)
              +-- Request signing (HMAC/JWT)
              +-- TLS termination
              +-- Logging/monitoring
```

## Data Security

### Encryption Layers

| Layer | Method | Use Case |
|-------|--------|----------|
| **At Rest** | AES-256-GCM | Databases, file storage, backups |
| **In Transit** | TLS 1.3 | All network communication |
| **End-to-End** | Signal Protocol, libsodium | User-to-user messaging |
| **Application** | Field-level encryption | Sensitive fields (PII, PCI) |

### Key Management Architecture

```
+------------------------------------------+
|           Key Management Service          |
|  +------------------------------------+  |
|  |      Master Key (HSM-protected)    |  |
|  +------------------+-----------------+  |
|                     |                    |
|  +------------------v-----------------+  |
|  |    Data Encryption Keys (DEKs)     |  |
|  |    (encrypted by master key)       |  |
|  +------------------------------------+  |
|                                          |
|  Key Hierarchy:                          |
|  - Root Key (HSM)                        |
|    - Master Keys (per tenant/region)     |
|      - Data Keys (per resource)          |
+------------------------------------------+
```

**Key Management Best Practices:**
- Use managed KMS (AWS KMS, GCP KMS, Azure Key Vault, HashiCorp Vault)
- Rotate keys regularly (90 days for data keys)
- Separate dev/staging/prod keys
- Never store keys in code or config files
- Implement key versioning for rotation
- Use envelope encryption pattern

### Post-Quantum Cryptography

**NIST PQC Standards (2024-2025):**
- **Kyber** - Key encapsulation (replacing RSA/ECDH)
- **Dilithium** - Digital signatures (replacing RSA/ECDSA)
- **SPHINCS+** - Hash-based signatures (stateless)

Start planning hybrid deployments combining classical + PQC algorithms.

## Secrets Management

### HashiCorp Vault Pattern

```
Application -> Vault Agent -> Vault Server -> Secrets Engine
                   |              |
                   |              +-- Auth Methods (K8s, AWS, OIDC)
                   |              +-- Audit Logging
                   |              +-- Secret Rotation
                   |
                   +-- Automatic token renewal
                   +-- Secret caching
                   +-- Template rendering
```

### Secrets Management Comparison

| Solution | Best For | Key Features |
|----------|----------|--------------|
| **HashiCorp Vault** | Multi-cloud, dynamic secrets | Dynamic credentials, PKI, encryption-as-service |
| **AWS Secrets Manager** | AWS-native applications | RDS rotation, cross-account, Lambda integration |
| **AWS Parameter Store** | Simple config/secrets | Free tier, hierarchical, versioning |
| **GCP Secret Manager** | GCP applications | IAM integration, automatic replication |
| **Azure Key Vault** | Azure applications | HSM-backed, certificate management |

### The 18-Point Secrets Management Checklist

1. Centralize all secrets in dedicated vault
2. Use dynamic secrets over static credentials
3. Implement short-lived credentials (TTL)
4. Enable automatic rotation
5. Use RBAC for secret access
6. Enable comprehensive audit logging
7. Encrypt secrets at rest and in transit
8. Use separate secrets for each environment
9. Never commit secrets to version control
10. Implement secret scanning in CI/CD
11. Use application identity (not shared credentials)
12. Implement emergency break-glass procedures
13. Monitor for secret exposure
14. Use hardware security modules for root keys
15. Implement secret versioning
16. Define secret ownership
17. Regular access reviews
18. Incident response plan for compromised secrets

## Microservices Security

### Service Mesh with mTLS

```
+--------------------+     mTLS      +--------------------+
|    Service A       |<------------->|    Service B       |
|  +-------------+   |               |   +-------------+  |
|  |  App Code   |   |               |   |  App Code   |  |
|  +------+------+   |               |   +------+------+  |
|         |          |               |          |         |
|  +------v------+   |               |   +------v------+  |
|  | Sidecar     |   |               |   | Sidecar     |  |
|  | (Envoy)     |<--+-- Encrypted --+-->| (Envoy)     |  |
|  +-------------+   |               |   +-------------+  |
+--------------------+               +--------------------+
         ^                                     ^
         |                                     |
         +------ Istio Control Plane ----------+
                 (Certificate Management)
```

### mTLS Implementation Modes (Istio)

| Mode | Description | Use Case |
|------|-------------|----------|
| **Permissive** | Accept both mTLS and plaintext | Migration period |
| **Strict** | Only accept mTLS traffic | Production |
| **Disable** | No mTLS | Legacy integration |

### Microservices Security Checklist

- [ ] Service-to-service authentication (mTLS)
- [ ] Service identity (SPIFFE/SPIRE)
- [ ] Network policies (east-west traffic)
- [ ] API gateway for north-south traffic
- [ ] Secrets injection (no hardcoding)
- [ ] Container image scanning
- [ ] Runtime security (Falco, etc.)
- [ ] Centralized logging and monitoring
- [ ] Circuit breakers for resilience
- [ ] Rate limiting per service

## Threat Modeling

### STRIDE Model

| Threat | Description | Countermeasure |
|--------|-------------|----------------|
| **S**poofing | Pretending to be someone else | Authentication, digital signatures |
| **T**ampering | Modifying data/code | Integrity checks, HMAC, signing |
| **R**epudiation | Denying actions | Audit logging, digital signatures |
| **I**nformation Disclosure | Unauthorized data access | Encryption, access control |
| **D**enial of Service | Disrupting availability | Rate limiting, scaling, redundancy |
| **E**levation of Privilege | Gaining unauthorized access | Authorization, least privilege |

### PASTA (Process for Attack Simulation and Threat Analysis)

**7 Stages:**
1. **Define Objectives** - Business impact, compliance, risk tolerance
2. **Define Scope** - System boundaries, data flows, trust boundaries
3. **Decompose Application** - Architecture diagrams, component mapping
4. **Threat Analysis** - STRIDE per component, attack trees
5. **Vulnerability Analysis** - Code review, configuration review
6. **Attack Modeling** - Simulate attacks, exploit chains
7. **Risk Analysis** - Impact/probability, mitigation priorities

**When to Use:**
- STRIDE: Quick threat identification, agile teams
- PASTA: Comprehensive risk analysis, regulated industries

## OWASP ASVS 5.0 (May 2025)

The Application Security Verification Standard provides approximately **350 security requirements** across 17 categories:

| Category | Focus |
|----------|-------|
| V1 | Architecture, Design, and Threat Modeling |
| V2 | Authentication |
| V3 | Session Management |
| V4 | Access Control |
| V5 | Validation, Sanitization, and Encoding |
| V6 | Stored Cryptography |
| V7 | Error Handling and Logging |
| V8 | Data Protection |
| V9 | Communication |
| V10 | Malicious Code |
| V11 | Business Logic |
| V12 | Files and Resources |
| V13 | API and Web Services |
| V14 | Configuration |
| V15 | Dependency Management |
| V16 | Build Pipeline |
| V17 | Modern Web Application |

**Verification Levels:**
- Level 1: Low assurance (automated testing)
- Level 2: Standard assurance (manual review)
- Level 3: High assurance (comprehensive audit)

## LLM-Assisted Security Architecture

### Effective Use Cases

| Task | How LLM Can Help |
|------|------------------|
| Threat modeling | Generate STRIDE analysis for components |
| Security requirements | Draft ASVS-based requirements |
| Architecture review | Identify security gaps in designs |
| Policy drafting | Create RBAC/ABAC policies |
| Code review | Identify security vulnerabilities |
| Documentation | Generate security runbooks |

### Best Practices for LLM Usage

1. **Be specific** - Provide context about your stack, compliance requirements
2. **Request structured output** - Ask for tables, checklists, diagrams
3. **Iterate** - Start broad, then drill down into specifics
4. **Validate** - Always review LLM output against authoritative sources
5. **Use as starting point** - LLM output is draft, not final

### Anti-Patterns

- Blindly trusting LLM security recommendations
- Using LLM for cryptographic algorithm implementation
- Sharing sensitive data (credentials, keys) with LLM
- Skipping human review of security-critical changes

## External References

### Standards and Frameworks

- [NIST SP 800-207 Zero Trust Architecture](https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.SP.800-207.pdf)
- [NIST SP 1800-35 Implementing Zero Trust Architecture](https://csrc.nist.gov/news/2025/implementing-a-zero-trust-architecture-sp-1800-35)
- [OWASP ASVS 5.0](https://owasp.org/www-project-application-security-verification-standard/)
- [OWASP API Security Top 10](https://owasp.org/API-Security/)
- [OAuth 2.1 Specification](https://oauth.net/2.1/)
- [RFC 9700 OAuth 2.0 Security Best Practice](https://datatracker.ietf.org/doc/rfc9700/)
- [FIDO2/Passkeys](https://fidoalliance.org/passkeys/)

### Tools and Solutions

- [OpenFGA](https://openfga.dev/) - Fine-grained authorization
- [HashiCorp Vault](https://www.vaultproject.io/) - Secrets management
- [Istio](https://istio.io/) - Service mesh with mTLS
- [cert-manager](https://cert-manager.io/) - Kubernetes certificate management
- [Falco](https://falco.org/) - Runtime security monitoring
- [OWASP ZAP](https://www.zaproxy.org/) - Security testing

### Learning Resources

- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Google Zanzibar Paper](https://research.google/pubs/pub48190/)
- [CISA Zero Trust Maturity Model](https://www.cisa.gov/zero-trust-maturity-model)
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)

## Related Methodologies

| Methodology | Path |
|-------------|------|
| System Design Process | [system-design-process/](../system-design-process/) |
| API Gateway Design | [api-gateway-design/](../api-gateway-design/) |
| Service Mesh | [service-mesh/](../service-mesh/) |
| Microservices Architecture | [microservices-architecture/](../microservices-architecture/) |
| Reliability Architecture | [reliability-architecture/](../reliability-architecture/) |
