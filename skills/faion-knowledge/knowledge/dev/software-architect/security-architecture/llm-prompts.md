# LLM Prompts for Security Architecture

Effective prompts for LLM-assisted security design. Use these as starting points for security architecture discussions.

---

## Table of Contents

1. [Threat Modeling Prompts](#threat-modeling-prompts)
2. [Authentication Design Prompts](#authentication-design-prompts)
3. [Authorization Design Prompts](#authorization-design-prompts)
4. [API Security Prompts](#api-security-prompts)
5. [Data Protection Prompts](#data-protection-prompts)
6. [Infrastructure Security Prompts](#infrastructure-security-prompts)
7. [Security Review Prompts](#security-review-prompts)
8. [Compliance Prompts](#compliance-prompts)

---

## Threat Modeling Prompts

### STRIDE Analysis

```
Perform a STRIDE threat analysis for the following system:

System: [DESCRIBE YOUR SYSTEM]
- Components: [LIST MAJOR COMPONENTS]
- Data flows: [DESCRIBE HOW DATA MOVES]
- Trust boundaries: [WHERE TRUST CHANGES]
- Entry points: [EXTERNAL INTERFACES]

For each STRIDE category (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege):

1. Identify specific threats relevant to this system
2. Rate likelihood (Low/Medium/High)
3. Rate impact (Low/Medium/High)
4. Suggest mitigations

Format output as a table with: Threat Category | Specific Threat | Likelihood | Impact | Mitigation
```

### Attack Surface Analysis

```
Analyze the attack surface for:

Application Type: [WEB APP/API/MOBILE/MICROSERVICES]
Tech Stack: [LIST TECHNOLOGIES]
Deployment: [CLOUD PROVIDER/ON-PREM]
User Types: [ANONYMOUS/AUTHENTICATED/ADMIN]

Identify:
1. All entry points (APIs, UIs, file uploads, webhooks)
2. Authentication mechanisms and their weaknesses
3. Data storage locations and sensitivity
4. Third-party integrations and trust assumptions
5. Admin/debug interfaces

For each entry point, assess:
- Required authentication level
- Input validation requirements
- Potential attack vectors
- Recommended security controls
```

### Threat Actor Profiling

```
Create threat actor profiles for:

Industry: [YOUR INDUSTRY]
Data Types: [WHAT DATA YOU HANDLE]
Business Model: [B2B/B2C/MARKETPLACE]
Geographic Presence: [REGIONS]

For each relevant threat actor type, describe:
1. Motivation (financial, ideological, espionage, disruption)
2. Capabilities (script kiddie to nation-state)
3. Likely attack vectors
4. Potential targets within the system
5. Detection indicators
6. Recommended defenses

Consider: opportunistic attackers, competitors, insiders, hacktivists, organized crime, nation-states
```

### PASTA Threat Model

```
Guide me through a PASTA (Process for Attack Simulation and Threat Analysis) for:

Application: [APPLICATION NAME]
Business Context: [WHAT THE APP DOES]
Compliance Requirements: [GDPR/HIPAA/PCI-DSS/SOC2]

Walk through all 7 stages:

Stage 1 - Define Objectives:
- What are the business objectives?
- What is the risk tolerance?

Stage 2 - Define Scope:
- What are the technical boundaries?
- What data flows exist?

Stage 3 - Application Decomposition:
- What are the architectural components?
- What are the trust boundaries?

Stage 4 - Threat Analysis:
- What threats apply to each component?
- Create attack trees for top threats

Stage 5 - Vulnerability Analysis:
- What vulnerabilities might exist?
- How do they map to threats?

Stage 6 - Attack Modeling:
- How would attacks be executed?
- What are the exploit chains?

Stage 7 - Risk and Impact Analysis:
- What is the business impact?
- How should we prioritize mitigations?
```

---

## Authentication Design Prompts

### Authentication Strategy

```
Design an authentication strategy for:

Application Type: [SPA/MOBILE/API/B2B SAAS]
User Types: [CONSUMERS/EMPLOYEES/BOTH]
Compliance: [ANY SPECIFIC REQUIREMENTS]
Current State: [EXISTING AUTH IF ANY]

Consider and recommend:

1. Primary authentication method
   - Why this method?
   - Implementation complexity
   - User experience impact

2. Multi-factor authentication
   - Required for which users/actions?
   - Which MFA methods to support?
   - Fallback/recovery options

3. Session management
   - Session duration and idle timeout
   - Session storage approach
   - Concurrent session handling

4. Account recovery
   - Recovery flow without creating phishing vectors
   - Identity verification steps

5. Enterprise SSO (if B2B)
   - SAML vs OIDC support
   - Just-in-time provisioning

Provide specific technology recommendations.
```

### Passkey Implementation

```
Help me design a passkey (FIDO2/WebAuthn) implementation for:

Platform: [WEB/MOBILE/BOTH]
Current Auth: [EXISTING AUTHENTICATION]
User Base: [CONSUMER/ENTERPRISE/BOTH]

Address:

1. Registration Flow
   - How to onboard new users with passkeys?
   - Identity verification before passkey registration?
   - Support for platform vs roaming authenticators?

2. Authentication Flow
   - Primary passkey authentication
   - Handling users without passkeys
   - Cross-device authentication scenarios

3. Account Recovery
   - What happens if user loses all passkey devices?
   - Recovery methods that don't undermine security
   - Avoid creating phishing vectors

4. Migration Strategy
   - How to migrate existing password users?
   - Incentives for adoption
   - Timeline for deprecating passwords

5. Technical Implementation
   - WebAuthn API integration
   - Backend credential storage
   - Multi-device passkey support (synced passkeys)

Include code examples for critical flows.
```

### OAuth 2.1 Implementation

```
Review and improve my OAuth 2.1 implementation:

Current Setup:
- Client Type: [PUBLIC/CONFIDENTIAL]
- Grant Types: [AUTHORIZATION_CODE/CLIENT_CREDENTIALS]
- Token Storage: [WHERE TOKENS ARE STORED]
- Refresh Token Strategy: [HOW REFRESH WORKS]

Verify compliance with RFC 9700 (OAuth 2.0 Security BCP):

1. Is PKCE implemented correctly?
2. Are redirect URIs validated with exact matching?
3. Is the Implicit grant disabled?
4. Are refresh tokens rotated (for public clients)?
5. Are tokens properly scoped and audience-restricted?
6. Is sender-constraining (DPoP/mTLS) used where appropriate?

Identify gaps and provide specific fixes with code examples.
```

---

## Authorization Design Prompts

### Authorization Model Selection

```
Help me choose the right authorization model:

Application: [DESCRIBE APPLICATION]
Access Control Requirements:
- [REQUIREMENT 1]
- [REQUIREMENT 2]
- [REQUIREMENT 3]

Current Complexity: [SIMPLE/MODERATE/COMPLEX]
Team Size: [SMALL/MEDIUM/LARGE]
Scalability Needs: [CURRENT SCALE AND GROWTH]

Compare these models for my use case:
1. RBAC (Role-Based Access Control)
2. ABAC (Attribute-Based Access Control)
3. ReBAC (Relationship-Based Access Control)

For each, explain:
- How it would implement my requirements
- Implementation complexity
- Scalability characteristics
- Maintenance burden
- Technology options (OpenFGA, Casbin, OPA, custom)

Provide a recommendation with justification.
```

### RBAC Design

```
Design an RBAC system for:

Application: [APPLICATION TYPE]
User Types: [LIST USER TYPES]
Resources: [LIST RESOURCES/ENTITIES]
Operations: [CRUD + CUSTOM OPERATIONS]

Requirements:
- [SPECIFIC REQUIREMENT 1]
- [SPECIFIC REQUIREMENT 2]

Design:

1. Role Hierarchy
   - Define roles from most to least privileged
   - Define inheritance relationships
   - Handle role explosion prevention

2. Permission Schema
   - Define permission format (resource:action:scope)
   - List all permissions
   - Map permissions to roles

3. Implementation
   - Database schema for roles and permissions
   - API for role assignment
   - Permission check middleware
   - Caching strategy

4. Management
   - UI for role management
   - Audit logging
   - Separation of duties

Provide schema definitions and code examples.
```

### OpenFGA/Zanzibar Model Design

```
Design an OpenFGA authorization model for:

Application: [APPLICATION TYPE]
Entities: [LIST MAIN ENTITIES]
Relationships: [DESCRIBE RELATIONSHIPS]

Requirements:
- [ACCESS CONTROL REQUIREMENT 1]
- [ACCESS CONTROL REQUIREMENT 2]
- [ACCESS CONTROL REQUIREMENT 3]

Create:

1. Type definitions for each entity

2. Relations including:
   - Direct relationships (owner, member, viewer)
   - Computed relationships (can_edit, can_view)
   - Relationship inheritance

3. Example tuples showing:
   - How to grant access
   - How relationships propagate
   - Multi-tenancy patterns

4. Check queries for common authorization scenarios

5. List queries (list objects user can access)

Format the model in OpenFGA DSL syntax.
```

---

## API Security Prompts

### API Security Assessment

```
Assess API security against OWASP API Security Top 10:

API Description: [DESCRIBE YOUR API]
Authentication: [CURRENT AUTH METHOD]
Authorization: [CURRENT AUTHZ METHOD]
Tech Stack: [FRAMEWORK/LANGUAGE]

For each OWASP API risk:

1. API1:2023 - Broken Object-Level Authorization
   - Current state
   - Gaps identified
   - Remediation steps

2. API2:2023 - Broken Authentication
   - Current state
   - Gaps identified
   - Remediation steps

[Continue for all 10...]

Prioritize findings by risk level and provide actionable fixes.
```

### API Gateway Design

```
Design an API gateway security layer:

Requirements:
- Backend Services: [LIST SERVICES]
- Client Types: [WEB/MOBILE/THIRD-PARTY]
- Traffic Volume: [REQUESTS/SECOND]
- Compliance: [ANY REQUIREMENTS]

Design the following:

1. Authentication Layer
   - Token validation approach
   - API key management
   - mTLS for service-to-service

2. Rate Limiting Strategy
   - Per-client limits
   - Per-endpoint limits
   - Burst handling
   - Rate limit headers

3. Input Validation
   - Request schema validation
   - Payload size limits
   - Content type enforcement

4. Security Policies
   - IP allowlisting/blocklisting
   - Geo-blocking
   - Bot protection

5. Logging and Monitoring
   - Security event logging
   - Anomaly detection
   - Alerting rules

Provide configuration examples for [Kong/AWS API Gateway/Nginx/other].
```

### Request Signing Design

```
Design a request signing mechanism for API security:

API Type: [REST/GRAPHQL]
Clients: [SERVER-TO-SERVER/MOBILE/BROWSER]
Security Requirements: [INTEGRITY/NON-REPUDIATION/REPLAY-PREVENTION]

Design:

1. Signature Algorithm
   - HMAC-SHA256 or RSA/ECDSA?
   - Why this choice?

2. Signed Components
   - Which request elements to sign?
   - Timestamp handling
   - Request body canonicalization

3. Signature Format
   - Header format
   - Signature string construction
   - Example signed request

4. Verification Process
   - Server-side verification steps
   - Timestamp tolerance
   - Replay attack prevention

5. Key Management
   - Key generation
   - Key rotation
   - Key distribution to clients

Provide code examples for both client signing and server verification.
```

---

## Data Protection Prompts

### Encryption Architecture

```
Design a data encryption architecture for:

Data Types:
- [DATA TYPE 1]: [SENSITIVITY LEVEL]
- [DATA TYPE 2]: [SENSITIVITY LEVEL]
- [DATA TYPE 3]: [SENSITIVITY LEVEL]

Storage: [DATABASE/OBJECT STORAGE/FILES]
Compliance: [GDPR/HIPAA/PCI-DSS]

Design:

1. Encryption at Rest
   - Database encryption (TDE vs application-level)
   - File/object storage encryption
   - Key hierarchy (root -> master -> data keys)
   - KMS selection (AWS KMS/GCP KMS/Vault)

2. Encryption in Transit
   - TLS configuration
   - Internal service-to-service encryption
   - Certificate management

3. Field-Level Encryption
   - Which fields require additional encryption?
   - Searchable encryption options
   - Key-per-tenant vs shared keys

4. Key Management
   - Key rotation schedule
   - Key access policies
   - Key backup and recovery
   - Audit logging

5. Post-Quantum Considerations
   - Timeline for PQC migration
   - Hybrid approach recommendations

Provide implementation examples.
```

### Secrets Management Design

```
Design a secrets management strategy:

Environment: [KUBERNETES/VMS/SERVERLESS]
Cloud Provider: [AWS/GCP/AZURE/MULTI-CLOUD]
Secret Types:
- Database credentials
- API keys
- TLS certificates
- Encryption keys

Current State: [HOW SECRETS ARE MANAGED NOW]

Design:

1. Secrets Storage
   - Vault vs cloud-native (AWS Secrets Manager, etc.)
   - Multi-region/multi-cloud considerations
   - Encryption and access control

2. Secret Injection
   - How applications receive secrets
   - Kubernetes integration (CSI driver, sidecar)
   - Serverless integration
   - Avoiding secrets in environment variables

3. Dynamic Secrets
   - Database credential rotation
   - Cloud IAM temporary credentials
   - TTL and renewal

4. Static Secret Rotation
   - Rotation schedule by secret type
   - Zero-downtime rotation
   - Notification and monitoring

5. Development Workflow
   - Local development secrets
   - CI/CD pipeline secrets
   - Secret request/approval process

6. Security Controls
   - Access policies
   - Audit logging
   - Secret scanning in code

Provide configuration examples for the recommended solution.
```

---

## Infrastructure Security Prompts

### Zero Trust Architecture

```
Design a Zero Trust architecture for:

Current State:
- Network: [VPN/DIRECT/HYBRID]
- Identity: [CURRENT IDP]
- Applications: [ON-PREM/CLOUD/HYBRID]
- Users: [REMOTE/OFFICE/BOTH]

Compliance Requirements: [NIST/CISA/INDUSTRY-SPECIFIC]

Design across the 7 pillars:

1. Identity
   - Strong authentication (passwordless/MFA)
   - Continuous authentication
   - Identity governance

2. Device
   - Device compliance checking
   - Device identity/certificates
   - MDM/EDR integration

3. Network
   - Micro-segmentation approach
   - Software-defined perimeter
   - East-west traffic encryption

4. Application
   - ZTNA vs VPN
   - Application-level authentication
   - Just-in-time access

5. Data
   - Data classification
   - DLP implementation
   - Access monitoring

6. Infrastructure
   - Workload protection
   - IaC security
   - Runtime security

7. Visibility
   - Logging and SIEM
   - UEBA
   - Security metrics

Create a phased implementation roadmap.
```

### Service Mesh Security

```
Design service mesh security for Kubernetes:

Cluster: [SIZE AND CONFIGURATION]
Services: [NUMBER AND TYPES]
Current State: [EXISTING SECURITY MEASURES]
Compliance: [REQUIREMENTS]

Design:

1. mTLS Configuration
   - Mesh-wide policy (permissive vs strict)
   - Migration strategy from plaintext
   - Certificate management (SPIFFE/SPIRE)

2. Authorization Policies
   - Default deny strategy
   - Service-to-service policies
   - JWT validation for external requests
   - RBAC integration

3. Traffic Policies
   - Rate limiting
   - Circuit breakers
   - Retries and timeouts

4. Observability
   - Security metrics
   - Access logs
   - Distributed tracing for security events

5. Integration
   - External authorization (OPA/OpenFGA)
   - Secret injection
   - Egress control

Provide Istio/Linkerd configuration examples.
```

---

## Security Review Prompts

### Architecture Security Review

```
Review the security of this architecture:

[PASTE ARCHITECTURE DIAGRAM OR DESCRIPTION]

Components:
- [COMPONENT 1]: [PURPOSE]
- [COMPONENT 2]: [PURPOSE]

Data Flows:
- [FLOW 1]
- [FLOW 2]

Analyze:

1. Authentication and Authorization
   - Are all entry points authenticated?
   - Is authorization enforced consistently?
   - Are there any bypass opportunities?

2. Data Protection
   - Is sensitive data encrypted?
   - Are there any data exposure risks?
   - Is data minimization practiced?

3. Network Security
   - Are components properly segmented?
   - Is internal traffic encrypted?
   - Are there unnecessary exposed services?

4. Supply Chain
   - Third-party dependencies?
   - Trust assumptions?
   - Integration security?

5. Operational Security
   - Logging and monitoring?
   - Incident response capability?
   - Backup and recovery?

Provide findings in priority order with specific recommendations.
```

### Code Security Review

```
Review this code for security issues:

```[LANGUAGE]
[PASTE CODE]
```

Context:
- Application Type: [WEB/API/SERVICE]
- Framework: [FRAMEWORK NAME]
- Handles: [WHAT DATA/OPERATIONS]

Check for:

1. Injection vulnerabilities (SQL, NoSQL, Command, LDAP)
2. Authentication/authorization flaws
3. Cryptographic issues
4. Sensitive data exposure
5. Input validation gaps
6. Error handling issues
7. Logging security events properly
8. Hardcoded secrets
9. Race conditions
10. Insecure deserialization

For each finding:
- Severity (Critical/High/Medium/Low)
- Line numbers affected
- Explanation of the risk
- Fixed code example

Also suggest improvements for defense-in-depth.
```

---

## Compliance Prompts

### ASVS Mapping

```
Map my security controls to OWASP ASVS 5.0:

Application: [APPLICATION TYPE]
Current Security Controls:
- [CONTROL 1]
- [CONTROL 2]
- [CONTROL 3]

Target Level: [L1/L2/L3]

For each ASVS chapter:
1. List applicable requirements
2. Map existing controls
3. Identify gaps
4. Prioritize remediation

Focus on:
- V1: Architecture (threat modeling, secure design)
- V2: Authentication
- V3: Session Management
- V4: Access Control
- V5: Validation, Sanitization
- V6: Cryptography
- V7: Error Handling
- V8: Data Protection
- V9: Communication
- V13: API Security
- V14: Configuration

Create a compliance matrix with status: Compliant/Partial/Non-Compliant/N/A
```

### SOC 2 Security Controls

```
Map security architecture to SOC 2 Trust Service Criteria:

System Description: [DESCRIBE SYSTEM]
Scope: [IN-SCOPE COMPONENTS]

For each relevant criterion:

CC6 - Logical and Physical Access:
- CC6.1: How is logical access implemented?
- CC6.2: How are auth credentials managed?
- CC6.3: How is access removed?

CC7 - System Operations:
- CC7.1: How are security configs managed?
- CC7.2: How are vulnerabilities identified?

CC8 - Change Management:
- CC8.1: How are changes authorized and tested?

For each:
1. Current implementation
2. Evidence to collect
3. Gaps requiring attention

Recommend additional controls for any gaps.
```

### GDPR Data Protection

```
Design data protection measures for GDPR compliance:

Data Processing Activities:
- [ACTIVITY 1]: [DATA TYPES]
- [ACTIVITY 2]: [DATA TYPES]

Data Subjects: [WHO]
Processing Locations: [COUNTRIES]

Address:

1. Data Protection by Design
   - Encryption requirements
   - Pseudonymization approach
   - Data minimization controls

2. Access Controls
   - Who can access personal data?
   - Logging and monitoring access
   - Purpose limitation enforcement

3. Data Subject Rights
   - Right of access implementation
   - Right to erasure (technical approach)
   - Data portability format

4. Data Transfers
   - Cross-border transfer mechanisms
   - Standard contractual clauses
   - Technical safeguards

5. Breach Detection and Response
   - Detection capabilities
   - 72-hour notification process
   - Documentation requirements

Provide technical implementation guidance for each requirement.
```

---

## Prompt Best Practices

### Structure Your Prompts

```
1. Context First
   - System/application description
   - Technology stack
   - Current security posture

2. Specific Requirements
   - Compliance needs
   - Business constraints
   - Risk tolerance

3. Clear Ask
   - What output format you want
   - Level of detail needed
   - Any specific areas to focus on

4. Constraints
   - Budget limitations
   - Team capabilities
   - Timeline
```

### Iterative Refinement

```
Start Broad:
"Design authentication for a SaaS application"

Then Narrow:
"Focus on the OAuth 2.1 implementation details"

Then Specific:
"Show me the token validation code with all security checks"

Finally Validate:
"Review this implementation for security gaps"
```

### Request Formats

```
For Documentation: "Create a security design document..."
For Checklists: "Create a checklist for..."
For Code: "Provide code examples for..."
For Review: "Review and identify issues in..."
For Comparison: "Compare options A and B for..."
```

---

## Anti-Patterns to Avoid

### Do Not

1. **Ask for cryptographic implementations**
   - Use established libraries instead
   - LLMs should not implement crypto algorithms

2. **Share real credentials or keys**
   - Use placeholders: `[API_KEY]`, `[SECRET]`
   - Never paste actual secrets

3. **Blindly trust security recommendations**
   - Validate against authoritative sources
   - Test in non-production first

4. **Use LLM for penetration testing**
   - Get proper authorization
   - Use dedicated security tools

5. **Skip human review for security-critical changes**
   - LLM output is a starting point
   - Security experts should validate

---

## Related Files

- [README.md](README.md) - Security architecture overview
- [checklist.md](checklist.md) - Security design checklist
- [examples.md](examples.md) - Real-world examples
- [templates.md](templates.md) - Configuration templates
