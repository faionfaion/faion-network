# Security Architecture Checklist

Step-by-step checklist for designing secure systems. Use this during architecture design, security reviews, and compliance audits.

## Phase 1: Security Requirements

### 1.1 Business Context

- [ ] Identify data classification levels (public, internal, confidential, restricted)
- [ ] Document compliance requirements (GDPR, HIPAA, PCI-DSS, SOC 2, etc.)
- [ ] Define acceptable risk tolerance with stakeholders
- [ ] Identify regulatory jurisdictions and data residency requirements
- [ ] Document business continuity and recovery time objectives
- [ ] Identify critical assets and crown jewels

### 1.2 Threat Landscape

- [ ] Identify threat actors relevant to your domain
- [ ] Review industry-specific threat intelligence
- [ ] Document previous security incidents (if any)
- [ ] Assess supply chain risks
- [ ] Consider insider threat scenarios

### 1.3 Security Requirements Documentation

- [ ] Define authentication requirements (MFA, passwordless, SSO)
- [ ] Define authorization model (RBAC, ABAC, ReBAC)
- [ ] Specify encryption requirements (at-rest, in-transit, E2E)
- [ ] Define audit logging requirements
- [ ] Specify data retention and deletion policies
- [ ] Document incident response requirements

---

## Phase 2: Threat Modeling

### 2.1 System Decomposition

- [ ] Create data flow diagrams (DFD)
- [ ] Identify trust boundaries
- [ ] Document entry points (APIs, UIs, integrations)
- [ ] Map data stores and sensitivity levels
- [ ] Identify external dependencies

### 2.2 STRIDE Analysis

For each component, assess:

- [ ] **Spoofing** - Can an attacker impersonate users/services?
- [ ] **Tampering** - Can data be modified in transit or at rest?
- [ ] **Repudiation** - Can actions be denied without evidence?
- [ ] **Information Disclosure** - Can sensitive data leak?
- [ ] **Denial of Service** - Can the system be disrupted?
- [ ] **Elevation of Privilege** - Can attackers gain unauthorized access?

### 2.3 Attack Surface Analysis

- [ ] Document all external interfaces
- [ ] Identify unauthenticated endpoints
- [ ] Map privileged operations
- [ ] Review file upload/download capabilities
- [ ] Assess third-party integrations
- [ ] Identify debug/admin interfaces

### 2.4 Risk Assessment

- [ ] Calculate risk scores (impact x likelihood)
- [ ] Prioritize threats by risk score
- [ ] Document accepted risks with justification
- [ ] Define risk treatment plans

---

## Phase 3: Zero Trust Architecture

### 3.1 Identity Pillar

- [ ] Implement strong authentication (FIDO2/Passkeys preferred)
- [ ] Enable MFA for all users (phishing-resistant MFA for privileged)
- [ ] Implement SSO with modern protocols (OIDC)
- [ ] Define identity lifecycle management
- [ ] Implement privileged access management (PAM)
- [ ] Enable continuous authentication for sensitive operations

### 3.2 Device Pillar

- [ ] Implement device health attestation
- [ ] Require device compliance (EDR, patches, encryption)
- [ ] Implement certificate-based device identity
- [ ] Define BYOD vs. managed device policies
- [ ] Enable device posture checking before access

### 3.3 Network Pillar

- [ ] Implement micro-segmentation
- [ ] Encrypt all east-west traffic (mTLS)
- [ ] Deploy software-defined perimeter
- [ ] Eliminate implicit trust zones
- [ ] Implement network access control (NAC)

### 3.4 Application Pillar

- [ ] Implement application-level authentication
- [ ] Use Zero Trust Network Access (ZTNA) over VPN
- [ ] Deploy Cloud Access Security Broker (CASB)
- [ ] Implement just-in-time access provisioning
- [ ] Enable application session controls

### 3.5 Data Pillar

- [ ] Classify all data by sensitivity
- [ ] Implement data loss prevention (DLP)
- [ ] Enable data activity monitoring
- [ ] Implement encryption for all sensitive data
- [ ] Define and enforce data handling policies

### 3.6 Visibility Pillar

- [ ] Centralize security logging (SIEM)
- [ ] Implement user and entity behavior analytics (UEBA)
- [ ] Enable real-time alerting
- [ ] Define security metrics and KPIs
- [ ] Implement security orchestration and automation (SOAR)

---

## Phase 4: Authentication Design

### 4.1 Passkeys/FIDO2 Implementation

- [ ] Implement WebAuthn API integration
- [ ] Support platform authenticators (Face ID, Windows Hello)
- [ ] Support roaming authenticators (security keys)
- [ ] Implement passkey registration flow
- [ ] Design account recovery without phishable fallbacks
- [ ] Support synced passkeys for cross-device
- [ ] Plan migration path from passwords

### 4.2 OAuth 2.1 / OIDC Implementation

- [ ] Use Authorization Code flow with PKCE for all clients
- [ ] Implement exact redirect URI matching
- [ ] Remove any Implicit grant usage
- [ ] Remove Resource Owner Password Credentials grant
- [ ] Implement refresh token rotation
- [ ] Use sender-constrained tokens (DPoP) where possible
- [ ] Implement token audience restriction
- [ ] Set appropriate token lifetimes (short-lived access tokens)

### 4.3 Session Management

- [ ] Generate cryptographically secure session IDs
- [ ] Implement session timeout (idle and absolute)
- [ ] Bind sessions to client characteristics
- [ ] Implement secure session storage
- [ ] Enable concurrent session controls
- [ ] Implement session revocation on logout
- [ ] Protect against session fixation

### 4.4 API Authentication

- [ ] Use OAuth 2.1 for user-delegated access
- [ ] Implement API key rotation for machine-to-machine
- [ ] Use mTLS for service-to-service
- [ ] Avoid API keys in URLs
- [ ] Implement request signing for critical APIs

---

## Phase 5: Authorization Design

### 5.1 Access Control Model Selection

- [ ] Assess complexity of access control requirements
- [ ] Choose appropriate model (RBAC/ABAC/ReBAC)
- [ ] Document authorization policies
- [ ] Design for principle of least privilege
- [ ] Plan for separation of duties

### 5.2 RBAC Implementation

- [ ] Define role hierarchy
- [ ] Map permissions to roles
- [ ] Implement role assignment workflow
- [ ] Enable role-based API authorization
- [ ] Implement UI element visibility by role
- [ ] Plan for role explosion prevention

### 5.3 ABAC/ReBAC Implementation

- [ ] Define attribute schema (user, resource, environment)
- [ ] Create policy decision point (PDP)
- [ ] Implement policy enforcement points (PEP)
- [ ] Design policy administration workflow
- [ ] Test policy edge cases
- [ ] Implement policy versioning

### 5.4 Fine-Grained Authorization (OpenFGA/Zanzibar)

- [ ] Design authorization model (types, relations)
- [ ] Define tuple storage strategy
- [ ] Implement relationship management APIs
- [ ] Design check API integration
- [ ] Plan for authorization data consistency
- [ ] Implement list objects/subjects queries

---

## Phase 6: API Security

### 6.1 API Design Security

- [ ] Use TLS 1.3 for all endpoints
- [ ] Implement proper HTTP methods (no GET for mutations)
- [ ] Version APIs appropriately
- [ ] Design idempotent operations where possible
- [ ] Avoid sensitive data in URLs
- [ ] Implement proper error responses (no stack traces)

### 6.2 Input Validation

- [ ] Validate all input parameters
- [ ] Implement schema validation (OpenAPI/JSON Schema)
- [ ] Sanitize input to prevent injection
- [ ] Validate content types
- [ ] Set maximum payload sizes
- [ ] Validate file uploads (type, size, content)

### 6.3 Rate Limiting and Throttling

- [ ] Implement rate limiting per client/API key
- [ ] Set appropriate limits by endpoint sensitivity
- [ ] Implement graduated response (warning before block)
- [ ] Use token bucket or sliding window algorithms
- [ ] Return proper 429 responses with Retry-After
- [ ] Implement quota management for API products

### 6.4 API Gateway Security

- [ ] Deploy API gateway for all external APIs
- [ ] Implement authentication at gateway
- [ ] Enable request/response logging
- [ ] Implement IP allowlisting where appropriate
- [ ] Enable bot protection
- [ ] Configure CORS properly

---

## Phase 7: Data Security

### 7.1 Encryption at Rest

- [ ] Encrypt all databases (transparent data encryption)
- [ ] Encrypt file storage and object storage
- [ ] Encrypt backups
- [ ] Use AES-256-GCM or ChaCha20-Poly1305
- [ ] Implement envelope encryption
- [ ] Use managed KMS for key storage

### 7.2 Encryption in Transit

- [ ] Enforce TLS 1.3 (minimum TLS 1.2)
- [ ] Configure strong cipher suites
- [ ] Implement certificate pinning for mobile apps
- [ ] Enable HSTS with preload
- [ ] Use mTLS for internal services
- [ ] Disable legacy protocols (SSL, TLS 1.0/1.1)

### 7.3 End-to-End Encryption

- [ ] Use established protocols (Signal, MLS)
- [ ] Implement proper key exchange (X25519/Kyber)
- [ ] Use authenticated encryption (AES-GCM)
- [ ] Implement forward secrecy
- [ ] Design secure key backup/recovery
- [ ] Plan for key compromise scenarios

### 7.4 Key Management

- [ ] Use HSM for root/master keys
- [ ] Implement key hierarchy (root -> master -> data)
- [ ] Define key rotation policy (90 days recommended)
- [ ] Implement key versioning
- [ ] Plan emergency key revocation procedure
- [ ] Separate keys by environment

### 7.5 Data Protection

- [ ] Implement field-level encryption for PII
- [ ] Use tokenization for payment data
- [ ] Implement data masking for non-production
- [ ] Enable audit logging for sensitive data access
- [ ] Implement data retention policies
- [ ] Plan secure data deletion procedures

---

## Phase 8: Secrets Management

### 8.1 Secrets Storage

- [ ] Centralize all secrets in vault (Vault, AWS Secrets Manager)
- [ ] Remove hardcoded secrets from code
- [ ] Remove secrets from environment variables in production
- [ ] Encrypt secrets at rest
- [ ] Implement access control for secrets
- [ ] Enable audit logging for secret access

### 8.2 Dynamic Secrets

- [ ] Use dynamic database credentials where possible
- [ ] Implement short-lived credentials (TTL)
- [ ] Use IAM roles instead of static keys (cloud)
- [ ] Implement just-in-time secret provisioning
- [ ] Enable automatic credential rotation

### 8.3 Secret Rotation

- [ ] Define rotation schedules by secret type
- [ ] Implement zero-downtime rotation
- [ ] Test rotation procedures regularly
- [ ] Monitor for rotation failures
- [ ] Document manual rotation procedures

### 8.4 Development Workflow

- [ ] Implement pre-commit hooks for secret detection
- [ ] Integrate secret scanning in CI/CD
- [ ] Use different secrets per environment
- [ ] Implement secure secret injection in deployments
- [ ] Document secret request/approval workflow

---

## Phase 9: Microservices Security

### 9.1 Service Mesh Implementation

- [ ] Deploy service mesh (Istio, Linkerd)
- [ ] Enable mTLS for all service-to-service traffic
- [ ] Start with permissive mode, migrate to strict
- [ ] Implement service identity (SPIFFE)
- [ ] Configure authorization policies

### 9.2 Container Security

- [ ] Use minimal base images
- [ ] Scan images for vulnerabilities
- [ ] Sign and verify images
- [ ] Run containers as non-root
- [ ] Implement read-only root filesystem
- [ ] Define resource limits

### 9.3 Kubernetes Security

- [ ] Enable Pod Security Standards (restricted)
- [ ] Implement network policies
- [ ] Use RBAC for cluster access
- [ ] Enable audit logging
- [ ] Secure etcd encryption
- [ ] Implement admission controllers

### 9.4 Service-to-Service Communication

- [ ] Authenticate all service calls
- [ ] Authorize based on service identity
- [ ] Encrypt all traffic (mTLS)
- [ ] Implement circuit breakers
- [ ] Use service mesh for policy enforcement
- [ ] Log all cross-service calls

---

## Phase 10: Monitoring and Detection

### 10.1 Security Logging

- [ ] Log authentication events (success, failure, MFA)
- [ ] Log authorization decisions (allow, deny)
- [ ] Log sensitive data access
- [ ] Log administrative actions
- [ ] Log security configuration changes
- [ ] Implement tamper-proof logging

### 10.2 SIEM Integration

- [ ] Centralize logs from all sources
- [ ] Define log retention policies
- [ ] Create correlation rules
- [ ] Implement alerting thresholds
- [ ] Enable threat intelligence feeds
- [ ] Configure dashboards and reports

### 10.3 Alerting

- [ ] Define critical security alerts
- [ ] Configure alert routing (PagerDuty, Slack)
- [ ] Implement alert deduplication
- [ ] Create runbooks for common alerts
- [ ] Test alerting regularly
- [ ] Review and tune alert thresholds

### 10.4 Incident Response

- [ ] Document incident response plan
- [ ] Define severity levels
- [ ] Establish communication procedures
- [ ] Create forensic investigation procedures
- [ ] Plan containment strategies
- [ ] Schedule regular incident drills

---

## Phase 11: Compliance and Governance

### 11.1 ASVS Compliance

- [ ] Map requirements to ASVS 5.0 controls
- [ ] Determine target verification level (L1/L2/L3)
- [ ] Document control implementations
- [ ] Plan verification/testing approach
- [ ] Address gaps with remediation plan

### 11.2 Security Documentation

- [ ] Document security architecture
- [ ] Create security policies
- [ ] Maintain threat model
- [ ] Document incident response procedures
- [ ] Create security training materials
- [ ] Maintain compliance evidence

### 11.3 Security Reviews

- [ ] Schedule regular architecture reviews
- [ ] Conduct code security reviews
- [ ] Perform penetration testing
- [ ] Run vulnerability assessments
- [ ] Review third-party dependencies
- [ ] Assess vendor security

### 11.4 Continuous Improvement

- [ ] Track security metrics (MTTD, MTTR)
- [ ] Review and learn from incidents
- [ ] Update threat models regularly
- [ ] Monitor emerging threats
- [ ] Update security training
- [ ] Benchmark against industry standards

---

## Quick Reference: Priority by Project Phase

### MVP/Prototype

**Must Have:**
- [ ] TLS everywhere
- [ ] Basic authentication (OAuth 2.1)
- [ ] Input validation
- [ ] Secrets in environment/vault
- [ ] Basic logging

### Production Launch

**Add:**
- [ ] MFA for all users
- [ ] Rate limiting
- [ ] Security monitoring
- [ ] Incident response plan
- [ ] Penetration test

### Scale/Growth

**Add:**
- [ ] Zero Trust architecture
- [ ] Fine-grained authorization
- [ ] Advanced threat detection
- [ ] Compliance certifications
- [ ] Security automation (SOAR)

---

## Checklist by Role

### For Architects

- [ ] Threat model completed
- [ ] Security requirements documented
- [ ] Authentication/authorization strategy defined
- [ ] Data classification completed
- [ ] Compliance requirements mapped

### For Developers

- [ ] Secure coding training completed
- [ ] Input validation implemented
- [ ] No secrets in code
- [ ] Dependencies scanned
- [ ] Security tests written

### For DevOps/Platform

- [ ] Infrastructure hardened
- [ ] Secrets management configured
- [ ] Security logging enabled
- [ ] Container security implemented
- [ ] Backup/recovery tested

### For Security Team

- [ ] Security monitoring configured
- [ ] Alerting tuned
- [ ] Incident response tested
- [ ] Penetration testing scheduled
- [ ] Compliance evidence collected
