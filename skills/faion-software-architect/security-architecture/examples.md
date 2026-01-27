# Security Architecture Examples

Real-world security architecture examples for common application types. Each example includes authentication, authorization, data protection, and monitoring strategies.

---

## Example 1: SaaS B2B Application

### Context

Multi-tenant B2B SaaS platform with sensitive customer data, requiring SOC 2 compliance.

**Characteristics:**
- Multi-tenant architecture
- Enterprise SSO requirements
- Role-based access within organizations
- API access for integrations
- Sensitive business data

### Security Architecture

```
                                    +------------------+
                                    |   Identity       |
                                    |   Provider       |
                                    |   (Okta/Auth0)   |
                                    +--------+---------+
                                             |
                                             | OIDC/SAML
                                             v
+-------------+    TLS 1.3    +-------------+-------------+
|   Browser   |-------------->|         CDN/WAF          |
|   Client    |               |     (Cloudflare)         |
+-------------+               +-------------+-------------+
                                            |
                                            v
                              +-------------+-------------+
                              |       API Gateway         |
                              |   - Auth validation       |
                              |   - Rate limiting         |
                              |   - Request logging       |
                              +-------------+-------------+
                                            |
                    +-----------------------+-----------------------+
                    |                       |                       |
                    v                       v                       v
          +-----------------+     +-----------------+     +-----------------+
          |   Auth Service  |     |   Core API      |     |   Async Workers |
          |                 |     |                 |     |                 |
          | - OAuth 2.1     |     | - RBAC checks   |     | - Job processing|
          | - Session mgmt  |     | - Tenant isolation|   | - Notifications |
          | - MFA           |     | - Input validation|   | - Reports       |
          +-----------------+     +-----------------+     +-----------------+
                    |                       |                       |
                    v                       v                       v
          +-----------------+     +-----------------+     +-----------------+
          |   Auth DB       |     |   App DB        |     |   Queue         |
          |   (Encrypted)   |     |   (Encrypted)   |     |   (SQS)         |
          +-----------------+     +-----------------+     +-----------------+
                                            |
                                            v
                              +-------------+-------------+
                              |       SIEM/Monitoring     |
                              |   - Datadog              |
                              |   - Security alerts      |
                              +---------------------------+
```

### Authentication Strategy

```yaml
# Primary: Enterprise SSO
sso:
  protocols: [OIDC, SAML 2.0]
  providers:
    - Okta
    - Azure AD
    - Google Workspace
  mfa: required_for_all_users
  session_duration: 8h
  idle_timeout: 30m

# Fallback: Email/Password with MFA
password_auth:
  enabled: true
  requirements:
    min_length: 12
    complexity: strong
  mfa:
    methods: [totp, webauthn]
    required: true

# API Access: OAuth 2.1
api_auth:
  grant_types: [authorization_code, client_credentials]
  pkce: required
  token_lifetime: 1h
  refresh_token_rotation: true
```

### Authorization Model (Multi-Tenant RBAC)

```yaml
# Tenant isolation
tenants:
  isolation: schema_per_tenant
  context_propagation: jwt_claims
  cross_tenant_access: disabled

# Role hierarchy
roles:
  org_owner:
    inherits: org_admin
    permissions:
      - org:delete
      - billing:manage
      - sso:configure

  org_admin:
    inherits: member
    permissions:
      - users:invite
      - users:remove
      - roles:assign
      - settings:manage

  member:
    inherits: viewer
    permissions:
      - projects:create
      - projects:edit_own
      - data:import

  viewer:
    permissions:
      - projects:read
      - reports:view
      - data:export_own
```

### Data Protection

```yaml
encryption:
  at_rest:
    algorithm: AES-256-GCM
    key_management: AWS KMS
    key_per_tenant: true

  in_transit:
    protocol: TLS 1.3
    internal: mTLS

  field_level:
    pii_fields:
      - email
      - phone
      - ssn
    algorithm: AES-256-GCM
    key_derivation: tenant_specific

data_classification:
  public: []
  internal: [usage_metrics, feature_flags]
  confidential: [customer_data, business_metrics]
  restricted: [credentials, pii, financial_data]
```

### Compliance Controls (SOC 2)

| Control | Implementation |
|---------|----------------|
| CC6.1 - Logical Access | RBAC, MFA, SSO |
| CC6.2 - Auth Mechanisms | OAuth 2.1, SAML, MFA |
| CC6.3 - Access Removal | Automated deprovisioning via SCIM |
| CC7.1 - Configuration Management | IaC, GitOps, change approval |
| CC7.2 - System Monitoring | SIEM, real-time alerts |
| CC8.1 - Change Management | PR reviews, automated testing |

---

## Example 2: Healthcare Application (HIPAA)

### Context

Patient health records system requiring HIPAA compliance with strict audit requirements.

**Characteristics:**
- Protected Health Information (PHI)
- Strict access controls
- Comprehensive audit logging
- Break-glass emergency access
- Patient consent management

### Security Architecture

```
+------------------+
|   Healthcare     |
|   Identity       |
|   Provider       |
+--------+---------+
         |
         | SMART on FHIR
         v
+------------------+     +------------------+
|   Patient        |     |   Provider       |
|   Portal         |     |   Portal         |
+--------+---------+     +--------+---------+
         |                        |
         +------------+-----------+
                      |
                      v
         +------------+------------+
         |       API Gateway       |
         |   - OAuth 2.1           |
         |   - SMART scopes        |
         |   - Audit logging       |
         +------------+------------+
                      |
    +-----------------+-----------------+
    |                 |                 |
    v                 v                 v
+--------+     +--------+     +--------+
| Patient|     | EHR    |     | Audit  |
| Service|     | Service|     | Service|
+--------+     +--------+     +--------+
    |                 |              |
    v                 v              v
+--------+     +--------+     +--------+
|Patient |     |  EHR   |     | Audit  |
|  DB    |     |  DB    |     | Store  |
|(Encrypted)   |(Encrypted)   |(WORM)  |
+--------+     +--------+     +--------+
```

### Authentication (SMART on FHIR)

```yaml
# Patient authentication
patient_auth:
  protocol: SMART on FHIR
  identity_verification:
    - government_id
    - knowledge_based_auth
  mfa:
    required: true
    methods: [sms, totp, push]
  consent:
    required: true
    granular: true

# Provider authentication
provider_auth:
  protocol: OIDC
  identity_provider: organization_idp
  mfa:
    required: true
    methods: [hardware_token, webauthn]
  session:
    duration: 4h
    re_auth_for_phi: true

# Emergency access (break-glass)
break_glass:
  enabled: true
  requires:
    - manager_approval_or
    - emergency_code
  audit: immediate_alert
  auto_expire: 4h
  review: mandatory_within_24h
```

### Authorization (ABAC with Consent)

```yaml
# Attribute-based policies
policies:
  patient_record_access:
    subject:
      role: [physician, nurse, admin]
      department: matches_patient_department
      has_treating_relationship: true
    resource:
      type: patient_record
      sensitivity: [normal, sensitive]
    environment:
      location: approved_facility
      time: during_shift
    action: [read, write]

  sensitive_record_access:
    subject:
      role: [physician]
      has_treating_relationship: true
      consent_on_file: true
    resource:
      type: patient_record
      sensitivity: [mental_health, substance_abuse, hiv]
    action: [read]
    additional_audit: true

# Patient consent management
consent:
  types:
    - treatment
    - payment
    - healthcare_operations
    - research
    - marketing
  granularity: per_record_type
  revocation: immediate
```

### PHI Protection

```yaml
encryption:
  at_rest:
    algorithm: AES-256-GCM
    key_management: dedicated_hsm
    key_rotation: 90_days

  in_transit:
    protocol: TLS 1.3
    certificate_pinning: true

  field_level:
    phi_fields:
      - ssn
      - medical_record_number
      - diagnosis
      - treatment
    algorithm: format_preserving_encryption
    tokenization: enabled

access_controls:
  minimum_necessary: enforced
  role_based_filtering: enabled
  data_masking:
    non_treatment_roles:
      ssn: "XXX-XX-{last4}"
      dob: "{year}-XX-XX"
```

### Audit Requirements

```yaml
audit_logging:
  all_phi_access:
    log_fields:
      - timestamp
      - user_id
      - patient_id
      - record_type
      - action
      - access_reason
      - ip_address
      - device_id
    retention: 7_years
    storage: immutable_worm

  alerts:
    - bulk_record_access: "> 50 records/hour"
    - after_hours_access: true
    - break_glass_usage: immediate
    - failed_auth_attempts: "> 3"

  reporting:
    patient_access_report: on_request
    security_incident_report: within_24h
    periodic_review: quarterly
```

---

## Example 3: Fintech Payment Platform

### Context

Payment processing platform handling financial transactions requiring PCI-DSS compliance.

**Characteristics:**
- Credit card processing
- Financial transactions
- Regulatory compliance (PCI-DSS, SOX)
- High-value fraud target
- Real-time processing

### Security Architecture

```
                              +------------------+
                              |    HSM Cluster   |
                              |  (Card Data Keys)|
                              +--------+---------+
                                       |
+-------------+                        |
|  Merchant   |    TLS 1.3            v
|   Client    |----------->+----------+----------+
+-------------+            |     Load Balancer   |
                           |   (DDoS Protection) |
                           +----------+----------+
                                      |
                           +----------+----------+
                           |    API Gateway      |
                           | - mTLS termination  |
                           | - Request signing   |
                           | - Rate limiting     |
                           +----------+----------+
                                      |
              +-----------------------+-----------------------+
              |                       |                       |
              v                       v                       v
    +-------------------+   +-------------------+   +-------------------+
    |   Auth Service    |   | Payment Service   |   |   Fraud Service   |
    |                   |   |                   |   |                   |
    | - API key auth    |   | - Card tokenization|  | - ML detection    |
    | - OAuth 2.1       |   | - Transaction mgmt|   | - Rule engine     |
    | - Merchant verify |   | - PCI scope       |   | - Risk scoring    |
    +-------------------+   +-------------------+   +-------------------+
              |                       |                       |
              v                       v                       v
    +-------------------+   +-------------------+   +-------------------+
    |   Auth DB         |   | Card Vault (HSM)  |   |   Fraud DB        |
    |   (Encrypted)     |   | (Tokenized PANs)  |   |   (Encrypted)     |
    +-------------------+   +-------------------+   +-------------------+
                                      |
                           +----------+----------+
                           |   Card Networks     |
                           | (Visa, Mastercard)  |
                           +---------------------+
```

### Authentication (Merchant/API)

```yaml
# Merchant authentication
merchant_auth:
  primary: api_key_with_signature
  signature:
    algorithm: HMAC-SHA256
    timestamp_tolerance: 5m
    replay_prevention: true

  oauth:
    enabled: true
    grant_types: [client_credentials]
    scopes:
      - payments:create
      - payments:read
      - refunds:create
      - reports:read
    token_binding: certificate

# Merchant portal
portal_auth:
  protocol: OIDC
  mfa:
    required: true
    methods: [hardware_token, webauthn]
  ip_allowlist: per_merchant
  session_duration: 1h
```

### Request Signing

```python
# Merchant request signing example
import hmac
import hashlib
import time

def sign_request(api_secret, method, path, body, timestamp):
    """
    Create HMAC signature for API request
    """
    message = f"{timestamp}.{method}.{path}.{body}"
    signature = hmac.new(
        api_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

# Request headers
headers = {
    "X-API-Key": "pk_live_xxxxx",
    "X-Timestamp": str(int(time.time())),
    "X-Signature": sign_request(secret, "POST", "/v1/payments", body, timestamp),
    "Idempotency-Key": "unique-request-id"
}
```

### Card Data Protection (PCI-DSS)

```yaml
# Tokenization strategy
tokenization:
  card_numbers:
    storage: hsm_vault
    token_format: "tok_{random_32}"
    mapping: one_to_one
    detokenization: authorized_services_only

  cvv:
    storage: never_stored
    usage: authorization_only

# PCI scope reduction
pci_scope:
  in_scope:
    - payment_service
    - card_vault
    - hsm_cluster
  out_of_scope:
    - merchant_portal
    - fraud_service
    - analytics

  network_segmentation:
    cardholder_data_environment:
      vlan: isolated
      firewall: dedicated
      monitoring: continuous

encryption:
  at_rest:
    algorithm: AES-256
    key_storage: hsm
    key_rotation: annual
    dual_control: required

  in_transit:
    protocol: TLS 1.3
    cipher_suites: [TLS_AES_256_GCM_SHA384]
    certificate_pinning: true
```

### Fraud Detection

```yaml
# Real-time fraud scoring
fraud_detection:
  ml_models:
    - transaction_anomaly_detection
    - velocity_analysis
    - device_fingerprinting
    - behavioral_biometrics

  rule_engine:
    rules:
      - high_value_new_card: "amount > 1000 AND card_age < 7d"
      - velocity_spike: "tx_count_1h > 10"
      - geo_anomaly: "distance_from_last_tx > 500km AND time < 2h"
      - known_fraud_indicators: device_fingerprint IN fraud_list

  actions:
    score_0_30: approve
    score_30_70: step_up_auth
    score_70_90: manual_review
    score_90_100: decline

# 3D Secure
3ds:
  version: "2.2"
  challenge_preference: risk_based
  exemptions:
    - low_value: "< 30 EUR"
    - trusted_merchant: whitelisted
    - transaction_risk_analysis: low_risk
```

### Compliance Controls (PCI-DSS 4.0)

| Requirement | Implementation |
|-------------|----------------|
| 1. Network Security | Dedicated CDE network, firewall rules |
| 2. Secure Configurations | CIS benchmarks, automated hardening |
| 3. Protect Stored Data | HSM tokenization, encryption |
| 4. Encrypt Transmission | TLS 1.3, mTLS internal |
| 5. Anti-Malware | EDR on all CDE systems |
| 6. Secure Development | SAST, DAST, code review |
| 7. Access Control | RBAC, need-to-know |
| 8. User Identification | MFA, unique IDs |
| 9. Physical Security | Data center controls |
| 10. Logging/Monitoring | SIEM, real-time alerts |
| 11. Security Testing | Quarterly scans, annual pentest |
| 12. Security Policies | Documented, trained, enforced |

---

## Example 4: Microservices Platform

### Context

Modern microservices architecture with service mesh, requiring zero-trust security.

**Characteristics:**
- 50+ microservices
- Kubernetes deployment
- Multiple development teams
- Continuous deployment
- Internal and external APIs

### Security Architecture

```
                                +------------------+
External                        |   Keycloak       |
Traffic                         |   (OIDC/SAML)    |
   |                            +--------+---------+
   |                                     |
   v                                     v
+--+---------------------+     +---------+---------+
|     Ingress Gateway    |     |   External IdP    |
|   (Istio + Cert-mgr)   |     |   (Google, Okta)  |
+--+---------------------+     +-------------------+
   |
   | mTLS
   v
+--+---------------------+---------------------+
|                 Service Mesh (Istio)         |
|  +----------------+  +----------------+      |
|  | Auth Service   |  | API Gateway    |      |
|  | (token verify) |  | (rate limit)   |      |
|  +----------------+  +----------------+      |
|                                              |
|  +----------------+  +----------------+      |
|  | Service A      |  | Service B      |      |
|  | (orders)       |  | (inventory)    |      |
|  +-------+--------+  +-------+--------+      |
|          | mTLS              | mTLS          |
|  +-------v--------+  +-------v--------+      |
|  | Service C      |  | Service D      |      |
|  | (payments)     |  | (notifications)|      |
|  +----------------+  +----------------+      |
+----------------------------------------------+
         |
         v
+--------+--------+
|  Vault          |
|  (Secrets)      |
+-----------------+
```

### Service Identity (SPIFFE/SPIRE)

```yaml
# SPIFFE ID format
spiffe_ids:
  format: "spiffe://cluster.local/ns/{namespace}/sa/{service_account}"
  examples:
    - "spiffe://cluster.local/ns/orders/sa/orders-api"
    - "spiffe://cluster.local/ns/payments/sa/payments-processor"

# SPIRE configuration
spire:
  trust_domain: cluster.local
  attestation:
    node:
      - k8s_psat
    workload:
      - k8s
  svid_ttl: 1h
```

### mTLS Configuration (Istio)

```yaml
# Strict mTLS for entire mesh
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT

---
# Authorization policy for orders service
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: orders-api-policy
  namespace: orders
spec:
  selector:
    matchLabels:
      app: orders-api
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/api-gateway/sa/api-gateway"
              - "cluster.local/ns/payments/sa/payments-processor"
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/orders/*"]
```

### Service-to-Service Authorization (OPA)

```rego
# OPA policy for service authorization
package envoy.authz

import input.attributes.request.http as http_request
import input.attributes.source.principal as source_principal

default allow = false

# Allow API gateway to access all services
allow {
    source_principal == "spiffe://cluster.local/ns/api-gateway/sa/api-gateway"
}

# Allow payments to access orders (for order status updates)
allow {
    source_principal == "spiffe://cluster.local/ns/payments/sa/payments-processor"
    http_request.path == "/api/v1/orders/status"
    http_request.method == "PUT"
}

# Allow inventory to access orders (read only)
allow {
    source_principal == "spiffe://cluster.local/ns/inventory/sa/inventory-api"
    glob.match("/api/v1/orders/*", [], http_request.path)
    http_request.method == "GET"
}
```

### Secrets Management (Vault + K8s)

```yaml
# Vault injector configuration
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-api
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "orders-api"
        vault.hashicorp.com/agent-inject-secret-db: "secret/data/orders/database"
        vault.hashicorp.com/agent-inject-template-db: |
          {{- with secret "secret/data/orders/database" -}}
          export DB_HOST="{{ .Data.data.host }}"
          export DB_USER="{{ .Data.data.username }}"
          export DB_PASS="{{ .Data.data.password }}"
          {{- end }}
    spec:
      serviceAccountName: orders-api
      containers:
        - name: orders-api
          command: ["sh", "-c", "source /vault/secrets/db && ./app"]
```

### Network Policies

```yaml
# Default deny all traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: orders
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Allow orders-api specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: orders-api-policy
  namespace: orders
spec:
  podSelector:
    matchLabels:
      app: orders-api
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: istio-system
        - namespaceSelector:
            matchLabels:
              name: api-gateway
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: orders
      ports:
        - protocol: TCP
          port: 5432  # PostgreSQL
    - to:
        - namespaceSelector:
            matchLabels:
              name: vault
```

### Security Monitoring

```yaml
# Falco rules for runtime security
- rule: Unauthorized Process in Orders Container
  desc: Detect unauthorized processes in orders containers
  condition: >
    spawned_process and
    container.name = "orders-api" and
    not proc.name in (node, npm, sh)
  output: >
    Unauthorized process in orders container
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: WARNING

- rule: Sensitive File Access
  desc: Detect access to sensitive files
  condition: >
    open_read and
    container and
    fd.name pmatch (/etc/shadow, /etc/passwd, /root/.ssh/*)
  output: >
    Sensitive file accessed (file=%fd.name container=%container.name)
  priority: CRITICAL
```

---

## Example 5: Consumer Mobile Application

### Context

Consumer-facing mobile app with passwordless authentication and device trust.

**Characteristics:**
- iOS and Android apps
- Passwordless-first authentication
- Device binding
- Sensitive personal data
- Offline capability

### Security Architecture

```
+------------------+                    +------------------+
|   iOS App        |                    |   Android App    |
|   - Secure       |                    |   - Keystore     |
|     Enclave      |                    |   - SafetyNet    |
+--------+---------+                    +--------+---------+
         |                                       |
         | Certificate Pinning                   | Certificate Pinning
         +-------------------+-------------------+
                             |
                             v
                  +----------+-----------+
                  |    CDN/WAF           |
                  |    (Bot Protection)  |
                  +----------+-----------+
                             |
                  +----------+-----------+
                  |    API Gateway       |
                  |    - Device verify   |
                  |    - Rate limiting   |
                  +----------+-----------+
                             |
         +-------------------+-------------------+
         |                   |                   |
         v                   v                   v
+--------+--------+ +--------+--------+ +--------+--------+
|   Auth API      | |   User API      | |   Content API   |
|   - Passkeys    | |   - Profile     | |   - Feed        |
|   - Device bind | |   - Preferences | |   - Media       |
+-----------------+ +-----------------+ +-----------------+
```

### Passwordless Authentication (Passkeys)

```yaml
# Passkey registration flow
registration:
  steps:
    1. user_identity_verification:
        methods: [email_otp, phone_otp]
    2. device_attestation:
        ios: device_check
        android: play_integrity
    3. passkey_creation:
        authenticator: platform
        user_verification: required
        attestation: indirect
    4. backup_method:
        type: recovery_codes
        count: 8

# Passkey authentication flow
authentication:
  challenge:
    length: 32
    timeout: 5m
  user_verification: required
  backup_eligible: true  # Allow synced passkeys

# Device binding
device_binding:
  enabled: true
  factors:
    - device_id
    - passkey_credential_id
    - device_attestation
  max_devices: 5
  suspicious_device_action: step_up_auth
```

### Device Trust

```yaml
# iOS Device Attestation
ios_attestation:
  device_check:
    enabled: true
    app_attest:
      enabled: true
      environment: production

  secure_enclave:
    key_storage: true
    biometric_binding: true

# Android Device Attestation
android_attestation:
  play_integrity:
    enabled: true
    verdict_requirements:
      device_integrity: MEETS_DEVICE_INTEGRITY
      app_integrity: MEETS_STRONG_INTEGRITY

  keystore:
    hardware_backed: required
    user_authentication: biometric_or_credential
    validity_duration: 300  # seconds

# Device risk signals
risk_assessment:
  signals:
    - jailbreak_detection
    - root_detection
    - emulator_detection
    - debugger_detection
    - app_tampering
    - hooking_framework_detection
  action_on_risk:
    low: log_only
    medium: step_up_auth
    high: block_access
```

### Local Data Protection

```swift
// iOS Keychain storage
class SecureStorage {
    func storeCredential(_ credential: Data, forKey key: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecValueData as String: credential,
            kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
            kSecAttrAccessControl as String: SecAccessControlCreateWithFlags(
                nil,
                kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
                [.biometryAny, .devicePasscode],
                nil
            )!
        ]
        SecItemAdd(query as CFDictionary, nil)
    }
}
```

```kotlin
// Android EncryptedSharedPreferences
class SecureStorage(context: Context) {
    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .setUserAuthenticationRequired(true)
        .setUserAuthenticationParameters(
            300, // validity duration
            KeyProperties.AUTH_BIOMETRIC_STRONG or
            KeyProperties.AUTH_DEVICE_CREDENTIAL
        )
        .build()

    private val securePrefs = EncryptedSharedPreferences.create(
        context,
        "secure_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    fun storeCredential(key: String, value: String) {
        securePrefs.edit().putString(key, value).apply()
    }
}
```

### Certificate Pinning

```swift
// iOS certificate pinning with TrustKit
TrustKit.initSharedInstance(withConfiguration: [
    kTSKSwizzleNetworkDelegates: true,
    kTSKPinnedDomains: [
        "api.example.com": [
            kTSKEnforcePinning: true,
            kTSKIncludeSubdomains: true,
            kTSKPublicKeyHashes: [
                "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="  // Backup pin
            ],
            kTSKReportUris: ["https://report.example.com/pin-failure"]
        ]
    ]
])
```

### API Security

```yaml
# Mobile API security headers
api_security:
  headers:
    required:
      - X-Device-ID: device_identifier
      - X-App-Version: semantic_version
      - X-Platform: ios|android
      - X-Device-Attestation: base64_attestation

  rate_limiting:
    per_device: 100/minute
    per_user: 1000/minute
    auth_endpoints: 5/minute

  response_security:
    no_sensitive_data_caching: true
    certificate_transparency: enabled
```

---

## Security Architecture Patterns Summary

| Pattern | Use Case | Key Technologies |
|---------|----------|------------------|
| Enterprise SSO | B2B SaaS | OIDC, SAML, SCIM |
| Break-Glass Access | Healthcare | ABAC, audit logging |
| Tokenization | Payment processing | HSM, PCI-DSS |
| Service Mesh | Microservices | Istio, SPIFFE, OPA |
| Passwordless | Consumer mobile | Passkeys, device attestation |

---

## Related Files

- [README.md](README.md) - Security architecture overview
- [checklist.md](checklist.md) - Security design checklist
- [templates.md](templates.md) - Copy-paste configurations
- [llm-prompts.md](llm-prompts.md) - LLM-assisted security design
