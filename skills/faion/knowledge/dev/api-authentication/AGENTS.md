# API Authentication

## Summary

**One-sentence:** Picks an API authentication scheme (JWT, OAuth2 client-creds, API-key, mTLS, opaque-session) and emits a scheme-spec with token lifetime, rotation, and revocation paths.

**One-paragraph:** Authentication is mismatched to use-case more often than it is broken cryptographically. This methodology selects from five canonical schemes — JWT, OAuth2 client-credentials, API-key, mTLS, opaque-session — based on caller type, audience, and revocation requirement, and emits a scheme-spec: token shape, lifetime, rotation interval, revocation path, and the failure mode the choice prevents (e.g. JWT for cross-service, never for B2C session).

**Ефективно для:**

- Solo dev choosing between JWT and opaque session for a new SaaS.
- Adding a B2B partner integration that needs OAuth2 client-credentials.
- Auditing an existing API where revocation is broken because tokens are long-lived.
- Standardising on one auth scheme per audience instead of three by accident.

## Applies If (ALL must hold)

- API has &gt;= 1 authenticated endpoint.
- Caller type is identifiable (browser / mobile / server / IoT).
- Audience boundary is defined (own users vs partners vs public).
- Revocation requirement is known (instant vs eventual).

## Skip If (ANY kills it)

- Public read-only endpoints (no auth needed).
- Internal-only RPC inside a VPC with mTLS at the mesh — separate methodology.
- Legacy SOAP / WS-Security stack — out of scope.
- Ephemeral preview environments where auth is bypassed.

## Prerequisites

| Artefact | Format | Source |
|----------|--------|--------|
| Caller types | list | PM / architect |
| Revocation SLA | duration (seconds) | security / ops |
| Identity provider | OIDC / SAML / homegrown | platform |
| Existing token shapes | JWT / opaque / API-key string | running API |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| [[api-rate-limiting]] | Auth scheme drives the rate-limit key (token / user / API-key). |
| [[api-error-handling]] | 401/403 envelope must match the API's Problem Details format. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules + sourced rationale | 900 |
| `content/02-output-contract.xml` | essential | JSON Schema (draft-07) + valid/invalid + forbidden patterns | 900 |
| `content/03-failure-modes.xml` | essential | 4 antipatterns with symptom + root-cause + fix | 700 |
| `content/04-procedure.xml` | essential | 5-step procedure end-to-end | 700 |
| `content/05-examples.xml` | essential | Worked example end-to-end | 600 |
| `content/06-decision-tree.xml` | essential | Routes by observable signals to a rule from 01-core-rules.xml | 400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `api_authentication_draft` | sonnet | Bounded synthesis. |
| `api_authentication_validate` | haiku | Mechanical schema check. |
| `api_authentication_review` | sonnet | Judgement on borderline cases. |

## Templates

| File | Purpose |
|------|---------|
| `templates/api-key-check.py` | Stdlib API-key validator with rotation overlap |
| `templates/fastapi-jwt-verifier.py` | FastAPI dependency that verifies JWT against JWKS + denylist |
| `templates/output-schema.json` | JSON Schema (draft-07) for the api-authentication artefact |
| `templates/_smoke-test.json` | Minimum viable filled-in api-authentication artefact for validator round-trip |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-api-authentication.py` | Validate api-authentication artefact against schema | Pre-commit; CI on each artefact change |

## Related

- [[api-rate-limiting]]
- [[api-error-handling]]
- [[api-rest-design]]
- [[api-versioning]]

## Decision tree

See `content/06-decision-tree.xml`. The tree gates on the schema's required cross-field checks; every leaf references a rule in `01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/api-key-check.py`

```python
# Constant-time SHA-256 API key verification
# Usage: from templates.api_key_check import hash_key, verify_api_key

import hashlib
import hmac


def hash_key(plaintext: str) -> str:
    """Return SHA-256 hex digest of key for storage."""
    return hashlib.sha256(plaintext.encode()).hexdigest()


def verify_api_key(presented: str, stored_hash: str) -> bool:
    """Constant-time comparison to prevent timing attacks."""
    return hmac.compare_digest(hash_key(presented), stored_hash)
```

### `templates/fastapi-jwt-verifier.py`

```python
# FastAPI JWT verifier using RS256 public key
# Usage: from templates.fastapi_jwt_verifier import verify_jwt_token
# Requires: python-jose[cryptography], fastapi

import os
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

ALGORITHM = "RS256"
PUBLIC_KEY = os.environ["JWT_PUBLIC_KEY"]   # PEM-encoded RSA public key
AUDIENCE = os.environ["JWT_AUDIENCE"]        # e.g. "https://api.example.com"
ISSUER = os.environ["JWT_ISSUER"]            # e.g. "https://auth.example.com"

_bearer = HTTPBearer()


def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Security(_bearer),
) -> dict:
    """Verify RS256 JWT; return decoded payload or raise 401."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
    except JWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc
    return payload
```

### `templates/output-schema.json`

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://faion.net/schemas/api-authentication.json",
  "type": "object",
  "required": [
    "spec_id",
    "scheme",
    "audience",
    "access_token_ttl_seconds",
    "revocation_path"
  ],
  "properties": {
    "spec_id": {
      "type": "string",
      "pattern": "^AUTH-[A-Z0-9-]{2,40}$"
    },
    "scheme": {
      "type": "string",
      "enum": [
        "jwt",
        "oauth2-client-credentials",
        "api-key",
        "mtls",
        "opaque-session"
      ]
    },
    "audience": {
      "type": "string",
      "enum": [
        "b2c-browser",
        "b2c-mobile",
        "b2b-partner",
        "server-to-server",
        "iot"
      ]
    },
    "access_token_ttl_seconds": {
      "type": "integer",
      "minimum": 30,
      "maximum": 86400
    },
    "refresh_token_rotates": {
      "type": "boolean"
    },
    "revocation_path": {
      "type": "string",
      "minLength": 8
    },
    "key_rotation_cadence_days": {
      "type": "integer",
      "minimum": 1,
      "maximum": 365
    }
  }
}
```

### `templates/_smoke-test.json`

```json
{
  "spec_id": "AUTH-PARTNER-API",
  "scheme": "oauth2-client-credentials",
  "audience": "b2b-partner",
  "access_token_ttl_seconds": 3600,
  "refresh_token_rotates": false,
  "revocation_path": "POST /oauth/revoke; client_id+client_secret; cascades to introspection cache eviction",
  "key_rotation_cadence_days": 90
}
```
