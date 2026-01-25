# Security Architecture

Designing secure systems with defense in depth.

## Security Principles

1. **Defense in Depth** - Multiple security layers
2. **Least Privilege** - Minimal permissions
3. **Zero Trust** - Never trust, always verify
4. **Fail Secure** - Default to deny
5. **Separation of Duties** - Split responsibilities

## Security Layers

```
┌─────────────────────────────────────────────────────┐
│                    Perimeter                         │
│  WAF, DDoS protection, Edge security                │
├─────────────────────────────────────────────────────┤
│                    Network                           │
│  Firewalls, VPCs, Network policies                  │
├─────────────────────────────────────────────────────┤
│                    Identity                          │
│  Authentication, Authorization, IAM                  │
├─────────────────────────────────────────────────────┤
│                    Application                       │
│  Input validation, Output encoding, OWASP           │
├─────────────────────────────────────────────────────┤
│                    Data                              │
│  Encryption, Masking, Classification                │
└─────────────────────────────────────────────────────┘
```

## Authentication Patterns

### Session-based

```
Client ──Login──▶ Server ──Create──▶ Session Store
   │                 │
   │◀──Session ID────│
   │                 │
   ├──Request+Cookie─▶│──Validate──▶ Session Store
```

### Token-based (JWT)

```
Client ──Login──▶ Auth Server ──Generate──▶ JWT
   │                    │
   │◀──────JWT──────────│
   │                    │
   ├──Request+JWT──▶ API Server ──Validate signature
```

### OAuth 2.0 / OIDC

```
User ──▶ Client App ──▶ Authorization Server
                              │
                        ◀─────│ (auth code)
                              │
         Client App ──────────▶ Token endpoint
                              │
                        ◀─────│ (access + refresh tokens)
```

## Authorization Models

| Model | Description | Use Case |
|-------|-------------|----------|
| RBAC | Role-Based Access Control | Most applications |
| ABAC | Attribute-Based | Complex policies |
| ReBAC | Relationship-Based | Social, hierarchies |
| ACL | Access Control Lists | File systems |

### RBAC Example

```yaml
roles:
  admin:
    permissions: [create, read, update, delete]
  editor:
    permissions: [read, update]
  viewer:
    permissions: [read]

users:
  john:
    roles: [admin]
  jane:
    roles: [editor, viewer]
```

## OWASP Top 10 Mitigations

| Vulnerability | Mitigation |
|---------------|------------|
| Injection | Parameterized queries, input validation |
| Broken Auth | MFA, secure session management |
| Sensitive Data | Encryption, secure transmission |
| XXE | Disable external entities |
| Broken Access | RBAC, authorization checks |
| Misconfiguration | Hardening, secure defaults |
| XSS | Output encoding, CSP |
| Insecure Deserialization | Input validation, type checking |
| Vulnerable Components | Dependency scanning, updates |
| Insufficient Logging | Centralized logging, alerting |

## API Security

### API Gateway Security

```
Client ──▶ API Gateway ──▶ Backend Services
              │
              ├── Rate limiting
              ├── Authentication
              ├── Input validation
              ├── IP whitelisting
              └── Request signing
```

### API Security Checklist

- [ ] TLS for all endpoints
- [ ] Authentication required
- [ ] Authorization per endpoint
- [ ] Rate limiting
- [ ] Input validation
- [ ] Output encoding
- [ ] CORS configured
- [ ] No sensitive data in URLs
- [ ] Audit logging

## Data Security

### Encryption

```
At Rest:
┌─────────────────────────────┐
│ Database ──▶ Encrypted │
│ File storage ──▶ Encrypted │
│ Backups ──▶ Encrypted │
└─────────────────────────────┘

In Transit:
Client ◀──TLS──▶ Server ◀──TLS──▶ Database
```

### Key Management

```
┌─────────────────────────────────────┐
│          Key Management Service      │
│  ┌─────────────────────────────┐    │
│  │    Master Key (HSM)         │    │
│  └──────────┬──────────────────┘    │
│             │                        │
│  ┌──────────┴──────────────────┐    │
│  │   Data Encryption Keys      │    │
│  │   (encrypted by master)     │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

**Best practices:**
- Rotate keys regularly
- Separate dev/prod keys
- Use managed KMS (AWS KMS, HashiCorp Vault)
- Never store keys in code

## Secrets Management

### Vault Pattern

```
Application ──▶ Vault ──▶ Secret
                 │
            ┌────┴────┐
            ▼         ▼
         Auth      Audit
        (token)    (log)
```

### Environment-based

```yaml
# DO NOT
password: "secret123"

# DO
password: ${DB_PASSWORD}  # From secrets manager
```

## Network Security

### Zero Trust Network

```
┌─────────────────────────────────────────┐
│           Zero Trust Network             │
│                                         │
│  Every request:                         │
│  1. Verify identity (who)               │
│  2. Verify device (what)                │
│  3. Verify context (where, when)        │
│  4. Grant minimal access                │
│  5. Log everything                      │
│                                         │
│  Trust nothing, verify everything       │
└─────────────────────────────────────────┘
```

### Micro-segmentation

```
┌─────────────────────────────────────────┐
│                 VPC                      │
│  ┌───────────┐    ┌───────────┐         │
│  │ Service A │    │ Service B │         │
│  │  (sg-a)   │◀──▶│  (sg-b)   │         │
│  └───────────┘    └───────────┘         │
│        │                                 │
│        ▼ (explicit allow)               │
│  ┌───────────┐                          │
│  │ Database  │                          │
│  │  (sg-db)  │                          │
│  └───────────┘                          │
└─────────────────────────────────────────┘
```

## Security Monitoring

### Security Events to Monitor

| Category | Events |
|----------|--------|
| Authentication | Failed logins, MFA bypass attempts |
| Authorization | Access denied, privilege escalation |
| Data | Large exports, sensitive access |
| Network | Port scans, unusual traffic |
| System | Config changes, new admins |

### SIEM Integration

```
Sources ──▶ Log Aggregation ──▶ SIEM ──▶ Alerts
│                                        │
├── Application logs                     ├── Dashboard
├── System logs                          ├── Incidents
├── Network logs                         └── Reports
└── Audit logs
```

## Threat Modeling

### STRIDE Model

| Threat | Example | Mitigation |
|--------|---------|------------|
| Spoofing | Fake identity | Authentication |
| Tampering | Modified data | Integrity checks |
| Repudiation | Deny actions | Audit logging |
| Info Disclosure | Data leak | Encryption |
| DoS | Service unavailable | Rate limiting |
| Elevation | Privilege escalation | Authorization |

## Security Architecture Checklist

### Design Phase
- [ ] Threat model completed
- [ ] Security requirements defined
- [ ] Authentication strategy
- [ ] Authorization model
- [ ] Data classification

### Implementation Phase
- [ ] Secure coding practices
- [ ] Dependency scanning
- [ ] Code review for security
- [ ] Security testing

### Operations Phase
- [ ] Logging and monitoring
- [ ] Incident response plan
- [ ] Regular security assessments
- [ ] Patch management

## Related

- [api-gateway-design.md](api-gateway-design.md) - API security
- [service-mesh.md](service-mesh.md) - mTLS
- [reliability-architecture.md](reliability-architecture.md) - Availability
