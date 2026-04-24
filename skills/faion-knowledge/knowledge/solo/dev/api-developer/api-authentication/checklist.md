# API Authentication Checklist

Step-by-step checklist for implementing secure API authentication.

## Phase 1: Choose Authentication Method

### Method Selection

- [ ] **Identify use case**
  - [ ] Server-to-server: Consider API Keys or mTLS
  - [ ] User sessions: Consider JWT or OAuth 2.0
  - [ ] Third-party access: OAuth 2.0
  - [ ] High-security: mTLS or OAuth 2.0 with PKCE

- [ ] **Evaluate requirements**
  - [ ] Stateless vs stateful sessions
  - [ ] Token expiration needs
  - [ ] Revocation requirements
  - [ ] Scalability needs
  - [ ] Compliance requirements (GDPR, HIPAA)

## Phase 2: API Keys Implementation

### Setup

- [ ] **Key generation**
  - [ ] Use cryptographically secure random generator
  - [ ] Generate keys with prefix: `sk_live_`, `sk_test_`
  - [ ] Minimum 32 characters length
  - [ ] Hash keys before database storage (bcrypt/argon2)

- [ ] **Storage**
  - [ ] Store only hashed keys in database
  - [ ] Include created_at, last_used_at timestamps
  - [ ] Track key metadata (name, scopes, rate limits)
  - [ ] Implement key rotation mechanism

- [ ] **Validation**
  - [ ] Verify key exists and not revoked
  - [ ] Check rate limits per key
  - [ ] Log all authentication attempts
  - [ ] Return 401 for invalid keys

### Security

- [ ] Never log full API keys
- [ ] Implement key rotation without downtime
- [ ] Add ability to revoke keys immediately
- [ ] Monitor for suspicious usage patterns

## Phase 3: JWT Implementation

### Token Creation

- [ ] **Choose algorithm**
  - [ ] HS256 for single-server (symmetric)
  - [ ] RS256 for distributed systems (asymmetric)
  - [ ] Never use algorithm: "none"

- [ ] **Configure claims**
  - [ ] `sub` - Subject (user ID)
  - [ ] `iss` - Issuer
  - [ ] `aud` - Audience
  - [ ] `exp` - Expiration (15-60 min for access tokens)
  - [ ] `iat` - Issued at
  - [ ] `jti` - Unique token ID (for revocation)
  - [ ] Custom claims (roles, permissions)

- [ ] **Security settings**
  - [ ] Store secret key in environment variables
  - [ ] Use strong secret (min 256 bits for HS256)
  - [ ] Rotate signing keys periodically
  - [ ] Never include sensitive data in payload

### Token Validation

- [ ] **Verify signature**
  - [ ] Validate token signature
  - [ ] Check algorithm matches expected
  - [ ] Verify issuer claim

- [ ] **Check expiration**
  - [ ] Validate `exp` claim
  - [ ] Handle clock skew (allow 30-60s tolerance)
  - [ ] Return 401 for expired tokens

- [ ] **Validate claims**
  - [ ] Check audience matches
  - [ ] Verify required claims present
  - [ ] Validate custom claims

### Refresh Tokens

- [ ] Generate long-lived refresh tokens (7-30 days)
- [ ] Store refresh tokens in database
- [ ] Implement refresh token rotation
- [ ] Revoke old refresh token on use
- [ ] Rate limit refresh endpoint

## Phase 4: OAuth 2.0 Implementation

### Authorization Server Setup

- [ ] **Endpoints**
  - [ ] `/authorize` - Authorization endpoint
  - [ ] `/token` - Token endpoint
  - [ ] `/introspect` - Token introspection (optional)
  - [ ] `/revoke` - Token revocation

- [ ] **Grant types**
  - [ ] Authorization Code (web apps)
  - [ ] Client Credentials (server-to-server)
  - [ ] Refresh Token
  - [ ] PKCE extension for public clients

### Client Registration

- [ ] Store client_id and client_secret
- [ ] Configure redirect_uris whitelist
- [ ] Set allowed grant types
- [ ] Define default scopes
- [ ] Implement client authentication

### Authorization Flow

- [ ] **Authorization request**
  - [ ] Validate client_id
  - [ ] Verify redirect_uri
  - [ ] Check scope validity
  - [ ] Generate and store state/PKCE parameters

- [ ] **Token issuance**
  - [ ] Exchange authorization code for tokens
  - [ ] Validate PKCE code_verifier
  - [ ] Issue access token + refresh token
  - [ ] Return token_type, expires_in

## Phase 5: Scope & Permissions

### Scope Design

- [ ] **Define scopes**
  - [ ] Use resource:action pattern (`read:users`, `write:orders`)
  - [ ] Document all available scopes
  - [ ] Implement scope hierarchy if needed
  - [ ] Create admin wildcard scope

- [ ] **Scope validation**
  - [ ] Check required scopes on protected endpoints
  - [ ] Return 403 for insufficient permissions
  - [ ] Log permission denials
  - [ ] Support multiple scopes per token

### Role-Based Access

- [ ] Map roles to scope sets
- [ ] Implement role hierarchy
- [ ] Support dynamic permission checks
- [ ] Cache role-scope mappings

## Phase 6: Security Hardening

### Transport Security

- [ ] **HTTPS only**
  - [ ] Enforce TLS 1.2+ everywhere
  - [ ] Use HSTS header
  - [ ] Redirect HTTP to HTTPS
  - [ ] Configure secure cookies (if using)

### Token Security

- [ ] **Storage**
  - [ ] Client: Store tokens in httpOnly cookies or secure storage
  - [ ] Server: Never log tokens
  - [ ] Use short expiration times
  - [ ] Implement token revocation

- [ ] **Headers**
  - [ ] Use `Authorization: Bearer <token>` header
  - [ ] Support custom header as fallback
  - [ ] Never send tokens in URL parameters

### Attack Prevention

- [ ] Rate limit authentication endpoints
- [ ] Implement account lockout after failed attempts
- [ ] Log all authentication events
- [ ] Monitor for brute force attacks
- [ ] Validate redirect URIs (OAuth)
- [ ] Implement CSRF protection

## Phase 7: Monitoring & Logging

### Logging

- [ ] **Log all auth events**
  - [ ] Successful logins
  - [ ] Failed attempts
  - [ ] Token refreshes
  - [ ] Key revocations
  - [ ] Permission denials

- [ ] **Include context**
  - [ ] Timestamp
  - [ ] User/client ID
  - [ ] IP address
  - [ ] User agent
  - [ ] Request ID

### Monitoring

- [ ] Track authentication success/failure rates
- [ ] Alert on unusual patterns
- [ ] Monitor token expiration rates
- [ ] Track API key usage
- [ ] Set up dashboards

## Phase 8: Documentation

- [ ] **Developer docs**
  - [ ] Authentication methods supported
  - [ ] How to obtain credentials
  - [ ] Token format and structure
  - [ ] Scope definitions
  - [ ] Code examples (curl, Python, JavaScript)

- [ ] **Security guidelines**
  - [ ] Token storage best practices
  - [ ] Rotation procedures
  - [ ] Revocation process
  - [ ] Security contact

---

## Quick Reference

| Method | Use Case | Token Type | Expiration |
|--------|----------|------------|------------|
| API Key | Server-to-server | Static key | None (manual rotation) |
| JWT | User sessions | Short-lived | 15-60 min |
| OAuth 2.0 | Third-party access | Access + Refresh | Access: 1hr, Refresh: 30d |
| mTLS | High security | Certificate | Based on cert validity |

---

*API Authentication Checklist v1.0*
