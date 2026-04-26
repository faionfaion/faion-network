# API Authentication LLM Prompts

Prompts for AI-assisted API authentication development.

## Design Prompts

### Choosing Authentication Method

```
I'm building [describe your API/service]. The API will be used by:
- [Client type 1: e.g., web app, mobile app, server-to-server]
- [Client type 2]

Key requirements:
- [Requirement 1: e.g., stateless, token expiration, revocation]
- [Requirement 2]
- [Security level: low/medium/high]
- [Compliance: GDPR, HIPAA, none]

Which authentication method should I use (API Keys, JWT, OAuth 2.0, mTLS)?
Explain the tradeoffs and provide implementation guidance.
```

### Scope Design

```
Design a permission/scope system for a [type] API with these resources:
- [Resource 1: e.g., users, projects, files]
- [Resource 2]

Actions per resource:
- [Resource 1]: read, create, update, delete
- [Resource 2]: read, create, update, delete

Create a hierarchical scope system with:
1. Fine-grained scopes (resource:action pattern)
2. Coarse-grained scopes (common bundles)
3. Admin wildcard scope
4. Scope inheritance rules
```

### Token Expiration Strategy

```
Design token expiration strategy for a [SaaS/mobile/enterprise] application:

Context:
- User activity: [constant/intermittent/occasional]
- Security requirements: [low/medium/high]
- UX tolerance for re-auth: [low/medium/high]

Provide recommendations for:
1. Access token lifetime
2. Refresh token lifetime
3. Refresh token rotation strategy
4. Session timeout behavior
5. "Remember me" functionality
```

## Implementation Prompts

### API Key Generator

```
Generate a Python function that creates secure API keys with:
- Prefix system for key identification (e.g., sk_live_, sk_test_)
- Cryptographically secure random generation
- Key hashing for storage
- Metadata tracking (created_at, last_used_at, scopes)
- Database schema (PostgreSQL)

Include:
- Key generation function
- Key validation function
- SQLAlchemy models
- FastAPI dependency for auth
```

### JWT Middleware

```
Create FastAPI middleware for JWT authentication with:
- RS256 algorithm (asymmetric keys)
- Scope-based authorization
- Token refresh endpoint
- Automatic token refresh on 401
- Request ID injection
- Structured logging

Include:
- Token creation/verification functions
- Middleware implementation
- Protected route examples
- Scope checking dependency
- Error handling
```

### OAuth 2.0 Server

```
Implement OAuth 2.0 authorization server supporting:
- Grant types: authorization_code, client_credentials, refresh_token
- PKCE extension for public clients
- Client registration
- Scope validation
- Token introspection endpoint
- Token revocation endpoint

Framework: [FastAPI/Django/Express]
Database: [PostgreSQL/MongoDB]
Storage: [Redis for codes/tokens]

Provide:
- Complete server implementation
- Database models
- Endpoint handlers
- Security considerations
```

## Security Review Prompts

### Code Review

```
Review this authentication implementation for security issues:

[Paste your authentication code]

Check for:
1. Timing attacks in token comparison
2. Secret exposure (logs, errors)
3. Insufficient token entropy
4. Missing rate limiting
5. Insecure token storage
6. CSRF vulnerabilities
7. Missing HTTPS enforcement
8. Weak password hashing
9. SQL injection in auth queries
10. Missing input validation

Provide specific vulnerabilities and fixes.
```

### Penetration Testing Scenarios

```
Generate penetration testing scenarios for this API authentication:

Authentication methods: [API Keys/JWT/OAuth 2.0]
Framework: [FastAPI/Django/Express]

Create test cases for:
1. Brute force attacks
2. Token replay attacks
3. Token tampering
4. Privilege escalation
5. Scope bypass
6. Race conditions
7. Session fixation
8. CSRF attacks

For each scenario, provide:
- Attack vector
- Expected behavior
- Test script (curl/Python)
```

## Debugging Prompts

### Token Debugging

```
Debug this JWT authentication issue:

Symptom: [describe the problem]

Token payload:
[paste decoded JWT payload]

Error message:
[paste error]

Code:
[paste relevant auth code]

Help me:
1. Identify the root cause
2. Explain why it's happening
3. Provide a fix
4. Suggest prevention measures
```

### Rate Limiting Debug

```
My rate limiting is not working correctly:

Implementation: [Sliding window/Token bucket/Fixed window]
Storage: [Redis/In-memory]
Window: [X seconds]
Limit: [Y requests]

Observed behavior:
- [Describe unexpected behavior]

Code:
[paste rate limiting code]

Diagnose the issue and provide a corrected implementation.
```

## Migration Prompts

### Auth System Migration

```
Help me migrate from [old auth system] to [new auth system]:

Current system:
- Method: [API Keys/Session cookies/etc]
- Implementation: [describe]
- Users: [count]
- Clients: [web/mobile/servers]

Target system:
- Method: [JWT/OAuth 2.0/etc]
- Requirements: [describe]

Create a migration plan with:
1. Backward compatibility strategy
2. Step-by-step migration process
3. Rollback procedure
4. Timeline estimation
5. Risk mitigation
6. Code examples for dual-auth support
```

### Legacy Client Support

```
I'm implementing OAuth 2.0 but need to support legacy clients using API keys.

Provide implementation for:
1. Dual authentication middleware (accepts both)
2. Gradual client migration strategy
3. Deprecation timeline
4. Client migration documentation
5. Monitoring/analytics for tracking migration progress

Framework: [FastAPI/Django/Express]
```

## Documentation Prompts

### API Documentation

```
Generate authentication documentation for developers integrating with my API:

Authentication methods supported:
- [Method 1]: [when to use]
- [Method 2]: [when to use]

Include:
1. Getting started guide
2. Code examples (curl, Python, JavaScript)
3. Token format and structure
4. Scope definitions
5. Error codes and messages
6. Rate limits
7. Security best practices
8. FAQ section

Format: Markdown, suitable for developer portal
```

### Security Guidelines

```
Create security guidelines document for developers using our API:

Authentication: [JWT/OAuth 2.0/API Keys]
Audience: [internal/external/partner] developers

Cover:
1. Secure token storage
2. Token rotation procedures
3. Revocation process
4. What to do if credentials are compromised
5. Rate limit handling
6. Security contact and reporting
7. Compliance requirements

Tone: Clear, actionable, non-technical friendly
```

## Testing Prompts

### Test Suite Generation

```
Generate comprehensive test suite for this authentication system:

[Paste authentication implementation]

Create tests for:
1. Happy path scenarios
2. Error scenarios (invalid tokens, expired, missing)
3. Edge cases (clock skew, token at boundary)
4. Security tests (tampering, replay)
5. Performance tests (token validation speed)
6. Integration tests (full auth flow)

Framework: [pytest/unittest/jest]
Include fixtures, mocks, and assertions.
```

### Load Testing

```
Create load testing scenarios for authentication endpoints:

Endpoints:
- POST /login (username/password → JWT)
- POST /refresh (refresh token → new access token)
- GET /protected (requires valid JWT)

Expected load:
- [X] requests/second at peak
- [Y] concurrent users

Generate:
1. Locust/k6/Artillery script
2. Realistic user behavior patterns
3. Success rate criteria
4. Response time thresholds
5. Resource usage monitoring
```

---

## Example Usage

### Prompt for JWT Implementation

```
USER: Generate a Python function that creates secure API keys with:
- Prefix system for key identification (e.g., sk_live_, sk_test_)
- Cryptographically secure random generation
- Key hashing for storage
- Metadata tracking (created_at, last_used_at, scopes)
- Database schema (PostgreSQL)

Include:
- Key generation function
- Key validation function
- SQLAlchemy models
- FastAPI dependency for auth

ASSISTANT: [Provides complete implementation with code examples]
```

---

*API Authentication LLM Prompts v1.0*
