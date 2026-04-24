# Security Architecture Templates

Copy-paste templates for common security configurations. Customize for your specific requirements.

---

## Table of Contents

1. [OAuth 2.1 / OIDC Configuration](#oauth-21--oidc-configuration)
2. [Authorization Policies](#authorization-policies)
3. [API Security](#api-security)
4. [Secrets Management](#secrets-management)
5. [TLS Configuration](#tls-configuration)
6. [Service Mesh Security](#service-mesh-security)
7. [Kubernetes Security](#kubernetes-security)
8. [Logging and Monitoring](#logging-and-monitoring)
9. [Security Headers](#security-headers)

---

## OAuth 2.1 / OIDC Configuration

### Keycloak Realm Configuration

```json
{
  "realm": "production",
  "enabled": true,
  "sslRequired": "all",
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5,
  "passwordPolicy": "length(12) and upperCase(1) and lowerCase(1) and specialChars(1) and digits(1) and notUsername and passwordHistory(5)",
  "otpPolicyType": "totp",
  "otpPolicyAlgorithm": "HmacSHA256",
  "otpPolicyDigits": 6,
  "otpPolicyPeriod": 30,
  "webAuthnPolicyRpEntityName": "YourApp",
  "webAuthnPolicySignatureAlgorithms": ["ES256", "RS256"],
  "webAuthnPolicyRpId": "yourapp.com",
  "webAuthnPolicyAttestationConveyancePreference": "indirect",
  "webAuthnPolicyAuthenticatorAttachment": "platform",
  "webAuthnPolicyRequireResidentKey": "Yes",
  "webAuthnPolicyUserVerificationRequirement": "required",
  "clients": [
    {
      "clientId": "web-app",
      "enabled": true,
      "clientAuthenticatorType": "client-secret",
      "redirectUris": ["https://app.yourapp.com/callback"],
      "webOrigins": ["https://app.yourapp.com"],
      "standardFlowEnabled": true,
      "implicitFlowEnabled": false,
      "directAccessGrantsEnabled": false,
      "serviceAccountsEnabled": false,
      "publicClient": true,
      "protocol": "openid-connect",
      "attributes": {
        "pkce.code.challenge.method": "S256",
        "access.token.lifespan": "3600",
        "client.session.idle.timeout": "1800"
      }
    },
    {
      "clientId": "api-service",
      "enabled": true,
      "clientAuthenticatorType": "client-secret",
      "serviceAccountsEnabled": true,
      "publicClient": false,
      "protocol": "openid-connect",
      "attributes": {
        "access.token.lifespan": "300"
      }
    }
  ]
}
```

### Auth0 Configuration (Terraform)

```hcl
# Auth0 tenant configuration
resource "auth0_tenant" "main" {
  friendly_name           = "YourApp Production"
  support_email           = "security@yourapp.com"
  default_directory       = "Username-Password-Authentication"
  session_lifetime        = 168  # hours
  idle_session_lifetime   = 72   # hours

  flags {
    enable_client_connections = false
    disable_clickjack_protection_headers = false
  }

  session_cookie {
    mode = "persistent"
  }
}

# Application (Client)
resource "auth0_client" "web_app" {
  name                = "Web Application"
  app_type            = "spa"
  oidc_conformant     = true
  token_endpoint_auth_method = "none"

  callbacks           = ["https://app.yourapp.com/callback"]
  allowed_origins     = ["https://app.yourapp.com"]
  allowed_logout_urls = ["https://app.yourapp.com"]
  web_origins         = ["https://app.yourapp.com"]

  jwt_configuration {
    alg                 = "RS256"
    lifetime_in_seconds = 3600
  }

  refresh_token {
    rotation_type                = "rotating"
    expiration_type              = "expiring"
    token_lifetime               = 2592000  # 30 days
    infinite_idle_token_lifetime = false
    idle_token_lifetime          = 1296000  # 15 days
    infinite_token_lifetime      = false
  }

  grant_types = ["authorization_code", "refresh_token"]
}

# API (Resource Server)
resource "auth0_resource_server" "api" {
  name        = "YourApp API"
  identifier  = "https://api.yourapp.com"
  signing_alg = "RS256"

  enforce_policies                                = true
  token_dialect                                   = "access_token_authz"
  skip_consent_for_verifiable_first_party_clients = true

  token_lifetime         = 3600
  token_lifetime_for_web = 3600

  scopes {
    value       = "read:users"
    description = "Read user profiles"
  }

  scopes {
    value       = "write:users"
    description = "Update user profiles"
  }

  scopes {
    value       = "admin:users"
    description = "Manage all users"
  }
}

# MFA configuration
resource "auth0_guardian" "mfa" {
  policy = "all-applications"

  webauthn_platform {
    enabled = true
  }

  webauthn_roaming {
    enabled = true
  }

  push {
    enabled = false
  }

  otp {
    enabled = true
  }

  phone {
    enabled      = false
    message_types = []
  }
}
```

### OIDC Client (Python)

```python
# FastAPI OIDC configuration
from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI, Depends, HTTPException
from starlette.config import Config

config = Config(".env")
oauth = OAuth(config)

# OIDC provider configuration
oauth.register(
    name="oidc",
    server_metadata_url="https://auth.yourapp.com/.well-known/openid-configuration",
    client_id=config("OIDC_CLIENT_ID"),
    client_secret=config("OIDC_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
        "code_challenge_method": "S256",  # PKCE
    },
)

# Token verification
from jose import jwt, JWTError
from functools import lru_cache
import httpx

@lru_cache()
def get_jwks():
    """Fetch and cache JWKS"""
    response = httpx.get("https://auth.yourapp.com/.well-known/jwks.json")
    return response.json()

async def verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        jwks = get_jwks()
        unverified_header = jwt.get_unverified_header(token)

        # Find the key
        rsa_key = None
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = key
                break

        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid token")

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience="https://api.yourapp.com",
            issuer="https://auth.yourapp.com/",
            options={
                "verify_exp": True,
                "verify_iat": True,
                "verify_nbf": True,
            }
        )
        return payload

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {e}")
```

---

## Authorization Policies

### RBAC Configuration (YAML)

```yaml
# roles.yaml - Role definitions
roles:
  # Super admin - full access
  super_admin:
    description: "Full system access"
    permissions:
      - "*:*"
    inherits: []

  # Organization admin
  org_admin:
    description: "Organization administrator"
    permissions:
      - "org:read"
      - "org:update"
      - "users:*"
      - "teams:*"
      - "billing:read"
      - "settings:*"
    inherits:
      - member

  # Team lead
  team_lead:
    description: "Team leader"
    permissions:
      - "team:read"
      - "team:update"
      - "team:members:manage"
      - "projects:create"
    inherits:
      - member

  # Regular member
  member:
    description: "Organization member"
    permissions:
      - "profile:read"
      - "profile:update"
      - "projects:read"
      - "projects:update:own"
      - "comments:create"
      - "comments:update:own"
      - "comments:delete:own"
    inherits:
      - viewer

  # Read-only viewer
  viewer:
    description: "Read-only access"
    permissions:
      - "projects:read"
      - "comments:read"
      - "reports:read"

  # API service account
  api_service:
    description: "Machine-to-machine API access"
    permissions:
      - "api:read"
      - "api:write"
    rate_limit: 10000/hour

# Permission format: resource:action[:scope]
# Scopes: own (user's own resources), team (team resources), org (org resources)
```

### OpenFGA Authorization Model

```dsl
# OpenFGA model for document collaboration
model
  schema 1.1

type user

type organization
  relations
    define owner: [user]
    define admin: [user] or owner
    define member: [user] or admin

type team
  relations
    define organization: [organization]
    define lead: [user]
    define member: [user] or lead
    define can_create_project: lead or admin from organization

type project
  relations
    define organization: [organization]
    define team: [team]
    define owner: [user]
    define editor: [user] or owner or member from team
    define viewer: [user] or editor or member from organization
    define can_delete: owner or admin from organization
    define can_share: owner or lead from team

type document
  relations
    define project: [project]
    define owner: [user]
    define editor: [user] or owner or editor from project
    define viewer: [user] or editor or viewer from project
    define can_delete: owner or can_delete from project
```

```python
# OpenFGA client usage (Python)
from openfga_sdk import OpenFgaClient, ClientConfiguration
from openfga_sdk.models import TupleKey, CheckRequest

config = ClientConfiguration(
    api_url="http://openfga:8080",
    store_id="your-store-id",
)
client = OpenFgaClient(config)

# Write relationship tuple
async def grant_access(user_id: str, document_id: str, relation: str):
    await client.write(
        writes=[
            TupleKey(
                user=f"user:{user_id}",
                relation=relation,
                object=f"document:{document_id}"
            )
        ]
    )

# Check authorization
async def can_edit(user_id: str, document_id: str) -> bool:
    response = await client.check(
        CheckRequest(
            tuple_key=TupleKey(
                user=f"user:{user_id}",
                relation="editor",
                object=f"document:{document_id}"
            )
        )
    )
    return response.allowed
```

### OPA (Open Policy Agent) Policy

```rego
# policy.rego - API authorization policy
package api.authz

import rego.v1

default allow := false

# Allow admins full access
allow if {
    input.user.roles[_] == "admin"
}

# Allow users to read their own data
allow if {
    input.method == "GET"
    input.path = ["api", "v1", "users", user_id]
    input.user.id == user_id
}

# Allow users to update their own profile
allow if {
    input.method in ["PUT", "PATCH"]
    input.path = ["api", "v1", "users", user_id, "profile"]
    input.user.id == user_id
}

# Allow team members to read team resources
allow if {
    input.method == "GET"
    input.path = ["api", "v1", "teams", team_id, _]
    input.user.team_memberships[_].team_id == team_id
}

# Allow team leads to manage team
allow if {
    input.method in ["PUT", "PATCH", "DELETE"]
    input.path = ["api", "v1", "teams", team_id, _]
    membership := input.user.team_memberships[_]
    membership.team_id == team_id
    membership.role == "lead"
}

# Rate limiting check
rate_limit_exceeded if {
    input.rate_limit.requests_per_minute > 100
}

# Deny if rate limit exceeded
deny["rate limit exceeded"] if {
    rate_limit_exceeded
}
```

---

## API Security

### API Gateway Configuration (Kong)

```yaml
# kong.yaml - Kong declarative configuration
_format_version: "3.0"
_transform: true

services:
  - name: users-api
    url: http://users-service:8080
    connect_timeout: 5000
    read_timeout: 60000
    write_timeout: 60000
    retries: 3

    routes:
      - name: users-route
        paths:
          - /api/v1/users
        strip_path: false
        protocols:
          - https

    plugins:
      # JWT validation
      - name: jwt
        config:
          secret_is_base64: false
          claims_to_verify:
            - exp
            - nbf
          key_claim_name: iss
          header_names:
            - Authorization

      # Rate limiting
      - name: rate-limiting
        config:
          minute: 100
          hour: 1000
          policy: redis
          redis_host: redis
          redis_port: 6379

      # Request size limiting
      - name: request-size-limiting
        config:
          allowed_payload_size: 10  # MB

      # CORS
      - name: cors
        config:
          origins:
            - https://app.yourapp.com
          methods:
            - GET
            - POST
            - PUT
            - PATCH
            - DELETE
          headers:
            - Authorization
            - Content-Type
          exposed_headers:
            - X-RateLimit-Remaining
          credentials: true
          max_age: 3600

      # IP restriction (for admin endpoints)
      - name: ip-restriction
        config:
          allow:
            - 10.0.0.0/8
          status: 403
          message: "Access denied"

      # Request transformation (remove sensitive headers)
      - name: request-transformer
        config:
          remove:
            headers:
              - X-Forwarded-For
              - X-Real-IP

      # Response transformation
      - name: response-transformer
        config:
          add:
            headers:
              - "X-Content-Type-Options:nosniff"
              - "X-Frame-Options:DENY"
              - "Strict-Transport-Security:max-age=31536000; includeSubDomains"

# Global plugins
plugins:
  - name: prometheus
    config:
      per_consumer: true

  - name: file-log
    config:
      path: /var/log/kong/access.log
      reopen: true
```

### FastAPI Security Middleware

```python
# security.py - FastAPI security configuration
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
import uuid

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.yourapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-RateLimit-Remaining", "X-Request-ID"],
    max_age=3600,
)

# Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.yourapp.com", "*.yourapp.com"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response

app.add_middleware(SecurityHeadersMiddleware)

# Request ID middleware
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response

app.add_middleware(RequestIDMiddleware)

# Input validation
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class UserCreate(BaseModel):
    email: str = Field(..., max_length=255)
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=12, max_length=128)

    @validator("email")
    def validate_email(cls, v):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v):
            raise ValueError("Invalid email format")
        return v.lower()

    @validator("password")
    def validate_password(cls, v):
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain special character")
        return v
```

---

## Secrets Management

### HashiCorp Vault Configuration

```hcl
# vault-config.hcl - Vault server configuration
storage "raft" {
  path    = "/vault/data"
  node_id = "vault-1"
}

listener "tcp" {
  address         = "0.0.0.0:8200"
  tls_cert_file   = "/vault/certs/vault.crt"
  tls_key_file    = "/vault/certs/vault.key"
  tls_min_version = "tls13"
}

api_addr     = "https://vault.yourapp.com:8200"
cluster_addr = "https://vault.yourapp.com:8201"
ui           = true

# Audit logging
audit_device "file" {
  path = "/vault/logs/audit.log"
}

# Telemetry
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname          = true
}
```

```hcl
# vault-policies.hcl - Vault policies

# Application policy - read-only access to app secrets
path "secret/data/{{identity.entity.aliases.auth_kubernetes_*.metadata.service_account_namespace}}/*" {
  capabilities = ["read"]
}

path "database/creds/{{identity.entity.aliases.auth_kubernetes_*.metadata.service_account_name}}" {
  capabilities = ["read"]
}

# Admin policy - manage secrets
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "database/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# PKI policy - issue certificates
path "pki/issue/web-certs" {
  capabilities = ["create", "update"]
}

path "pki/revoke" {
  capabilities = ["update"]
}
```

```yaml
# Kubernetes Vault Agent Injector
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-status: "update"
        vault.hashicorp.com/role: "api-server"

        # Database credentials
        vault.hashicorp.com/agent-inject-secret-db-creds: "database/creds/api-server"
        vault.hashicorp.com/agent-inject-template-db-creds: |
          {{- with secret "database/creds/api-server" -}}
          export DATABASE_URL="postgresql://{{ .Data.username }}:{{ .Data.password }}@db.yourapp.com:5432/api"
          {{- end }}

        # API keys
        vault.hashicorp.com/agent-inject-secret-api-keys: "secret/data/api/keys"
        vault.hashicorp.com/agent-inject-template-api-keys: |
          {{- with secret "secret/data/api/keys" -}}
          export STRIPE_API_KEY="{{ .Data.data.stripe_key }}"
          export SENDGRID_API_KEY="{{ .Data.data.sendgrid_key }}"
          {{- end }}

    spec:
      serviceAccountName: api-server
      containers:
        - name: api
          image: api-server:latest
          command: ["sh", "-c", "source /vault/secrets/db-creds && source /vault/secrets/api-keys && ./server"]
```

### AWS Secrets Manager (Terraform)

```hcl
# secrets.tf - AWS Secrets Manager configuration

# Database credentials with rotation
resource "aws_secretsmanager_secret" "db_credentials" {
  name        = "production/api/database"
  description = "Production database credentials"
  kms_key_id  = aws_kms_key.secrets.arn

  tags = {
    Environment = "production"
    Application = "api"
  }
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = "api_user"
    password = random_password.db_password.result
    host     = aws_db_instance.main.address
    port     = 5432
    database = "api"
  })
}

# Automatic rotation
resource "aws_secretsmanager_secret_rotation" "db_rotation" {
  secret_id           = aws_secretsmanager_secret.db_credentials.id
  rotation_lambda_arn = aws_lambda_function.rotate_secret.arn

  rotation_rules {
    automatically_after_days = 30
  }
}

# KMS key for encryption
resource "aws_kms_key" "secrets" {
  description             = "KMS key for secrets encryption"
  deletion_window_in_days = 30
  enable_key_rotation     = true

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM policies"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow Secrets Manager"
        Effect = "Allow"
        Principal = {
          Service = "secretsmanager.amazonaws.com"
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey*"
        ]
        Resource = "*"
      }
    ]
  })
}

# IAM policy for application access
resource "aws_iam_policy" "secrets_access" {
  name        = "api-secrets-access"
  description = "Allow API to access secrets"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.db_credentials.arn,
          "arn:aws:secretsmanager:*:*:secret:production/api/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = aws_kms_key.secrets.arn
      }
    ]
  })
}
```

---

## TLS Configuration

### Nginx TLS Configuration

```nginx
# nginx-ssl.conf - Production TLS configuration

# SSL/TLS settings
ssl_protocols TLSv1.3 TLSv1.2;
ssl_prefer_server_ciphers off;

# TLS 1.3 ciphers (preferred)
ssl_conf_command Ciphersuites TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_128_GCM_SHA256;

# TLS 1.2 ciphers (fallback)
ssl_ciphers ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305;

# ECDH curve
ssl_ecdh_curve X25519:secp384r1;

# Session settings
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# Certificate paths
ssl_certificate /etc/nginx/certs/fullchain.pem;
ssl_certificate_key /etc/nginx/certs/privkey.pem;
ssl_trusted_certificate /etc/nginx/certs/chain.pem;

# DH parameters (if using RSA)
ssl_dhparam /etc/nginx/certs/dhparam.pem;

# Server block
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.yourapp.com;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Hide server version
    server_tokens off;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name api.yourapp.com;
    return 301 https://$host$request_uri;
}
```

### cert-manager Configuration (Kubernetes)

```yaml
# cert-manager.yaml - Let's Encrypt certificates

# ClusterIssuer for Let's Encrypt
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: security@yourapp.com
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
      - http01:
          ingress:
            class: nginx
      - dns01:
          cloudflare:
            email: admin@yourapp.com
            apiTokenSecretRef:
              name: cloudflare-api-token
              key: api-token

---
# Certificate for API
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls
  namespace: production
spec:
  secretName: api-tls-secret
  duration: 2160h  # 90 days
  renewBefore: 360h  # 15 days
  isCA: false
  privateKey:
    algorithm: ECDSA
    size: 256
  usages:
    - server auth
    - client auth
  dnsNames:
    - api.yourapp.com
    - "*.api.yourapp.com"
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer

---
# Ingress with TLS
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: production
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
spec:
  tls:
    - hosts:
        - api.yourapp.com
      secretName: api-tls-secret
  rules:
    - host: api.yourapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api-service
                port:
                  number: 80
```

---

## Service Mesh Security

### Istio mTLS Configuration

```yaml
# istio-security.yaml - Istio security configuration

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
# Namespace-specific mTLS (permissive during migration)
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: legacy-services
spec:
  mtls:
    mode: PERMISSIVE

---
# Authorization policy - deny all by default
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  {}  # Empty spec denies all traffic

---
# Allow traffic from API gateway to services
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-api-gateway
  namespace: production
spec:
  selector:
    matchLabels:
      app: user-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"
      to:
        - operation:
            methods: ["GET", "POST", "PUT", "DELETE"]
            paths: ["/api/v1/*"]

---
# Allow service-to-service communication
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-order-to-inventory
  namespace: production
spec:
  selector:
    matchLabels:
      app: inventory-service
  action: ALLOW
  rules:
    - from:
        - source:
            principals:
              - "cluster.local/ns/production/sa/order-service"
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/v1/inventory/*"]

---
# JWT authentication for external requests
apiVersion: security.istio.io/v1beta1
kind: RequestAuthentication
metadata:
  name: jwt-auth
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  jwtRules:
    - issuer: "https://auth.yourapp.com/"
      jwksUri: "https://auth.yourapp.com/.well-known/jwks.json"
      audiences:
        - "https://api.yourapp.com"
      forwardOriginalToken: true

---
# Require JWT for external requests
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: require-jwt
  namespace: production
spec:
  selector:
    matchLabels:
      app: api-gateway
  action: ALLOW
  rules:
    - from:
        - source:
            requestPrincipals: ["https://auth.yourapp.com/*"]
      when:
        - key: request.auth.claims[scope]
          values: ["api:read", "api:write"]
```

---

## Kubernetes Security

### Pod Security Standards

```yaml
# pod-security.yaml - Pod security configuration

# Namespace with restricted security
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted

---
# Secure deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-server
  namespace: production
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api-server
  template:
    metadata:
      labels:
        app: api-server
    spec:
      serviceAccountName: api-server
      automountServiceAccountToken: false

      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
        - name: api
          image: api-server:v1.0.0
          imagePullPolicy: Always

          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi

          ports:
            - containerPort: 8080
              protocol: TCP

          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 10

          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5

          volumeMounts:
            - name: tmp
              mountPath: /tmp
            - name: cache
              mountPath: /app/cache

      volumes:
        - name: tmp
          emptyDir: {}
        - name: cache
          emptyDir: {}

---
# Network policy - default deny
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress

---
# Network policy - allow specific traffic
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-server-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: api-server
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: istio-system
        - podSelector:
            matchLabels:
              app: istio-ingressgateway
      ports:
        - protocol: TCP
          port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - protocol: TCP
          port: 5432
    - to:
        - namespaceSelector:
            matchLabels:
              name: vault
      ports:
        - protocol: TCP
          port: 8200
    - to:
        - namespaceSelector: {}
          podSelector:
            matchLabels:
              k8s-app: kube-dns
      ports:
        - protocol: UDP
          port: 53
```

---

## Logging and Monitoring

### Security Logging Configuration

```yaml
# fluent-bit-security.yaml - Security-focused logging

apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: logging
data:
  fluent-bit.conf: |
    [SERVICE]
        Flush         1
        Log_Level     info
        Daemon        off
        Parsers_File  parsers.conf

    [INPUT]
        Name              tail
        Path              /var/log/containers/*.log
        Parser            docker
        Tag               kube.*
        Mem_Buf_Limit     5MB
        Skip_Long_Lines   On

    [FILTER]
        Name                kubernetes
        Match               kube.*
        Kube_URL            https://kubernetes.default.svc:443
        Kube_CA_File        /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
        Kube_Token_File     /var/run/secrets/kubernetes.io/serviceaccount/token
        Merge_Log           On
        K8S-Logging.Parser  On
        K8S-Logging.Exclude Off

    # Security event detection
    [FILTER]
        Name          grep
        Match         kube.*
        Regex         log (authentication|authorization|security|audit|error|failed|denied|blocked)

    # Mask sensitive data
    [FILTER]
        Name          lua
        Match         kube.*
        Script        mask_sensitive.lua
        Call          mask_sensitive

    [OUTPUT]
        Name            es
        Match           kube.*
        Host            elasticsearch.logging.svc
        Port            9200
        Index           security-logs
        Type            _doc
        Logstash_Format On
        Retry_Limit     False

  mask_sensitive.lua: |
    function mask_sensitive(tag, timestamp, record)
        -- Mask passwords
        if record["log"] then
            record["log"] = string.gsub(record["log"], "password[\"']?%s*[:=]%s*[\"']?[^\"'%s,}]+", "password=***MASKED***")
            record["log"] = string.gsub(record["log"], "api[_-]?key[\"']?%s*[:=]%s*[\"']?[^\"'%s,}]+", "api_key=***MASKED***")
            record["log"] = string.gsub(record["log"], "token[\"']?%s*[:=]%s*[\"']?[^\"'%s,}]+", "token=***MASKED***")
        end
        return 1, timestamp, record
    end
```

### Prometheus Security Alerts

```yaml
# prometheus-security-rules.yaml - Security alerting rules

apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: security-alerts
  namespace: monitoring
spec:
  groups:
    - name: authentication
      rules:
        - alert: HighAuthenticationFailureRate
          expr: |
            sum(rate(auth_login_failures_total[5m])) by (service)
            / sum(rate(auth_login_attempts_total[5m])) by (service) > 0.1
          for: 5m
          labels:
            severity: warning
            category: security
          annotations:
            summary: "High authentication failure rate"
            description: "{{ $labels.service }} has >10% auth failure rate"

        - alert: BruteForceAttackDetected
          expr: |
            sum(rate(auth_login_failures_total[1m])) by (source_ip) > 10
          for: 2m
          labels:
            severity: critical
            category: security
          annotations:
            summary: "Potential brute force attack"
            description: "IP {{ $labels.source_ip }} has >10 failed logins/min"

    - name: authorization
      rules:
        - alert: UnauthorizedAccessAttempts
          expr: |
            sum(rate(authz_denied_total[5m])) by (service, resource) > 5
          for: 5m
          labels:
            severity: warning
            category: security
          annotations:
            summary: "High rate of unauthorized access attempts"
            description: "{{ $labels.service }} denied access to {{ $labels.resource }}"

        - alert: PrivilegeEscalationAttempt
          expr: |
            sum(rate(authz_denied_total{reason="privilege_escalation"}[5m])) > 0
          for: 1m
          labels:
            severity: critical
            category: security
          annotations:
            summary: "Privilege escalation attempt detected"
            description: "Attempted privilege escalation detected"

    - name: data-access
      rules:
        - alert: SensitiveDataBulkAccess
          expr: |
            sum(rate(sensitive_data_access_total[1h])) by (user, data_type) > 1000
          for: 10m
          labels:
            severity: warning
            category: security
          annotations:
            summary: "Unusual bulk access to sensitive data"
            description: "User {{ $labels.user }} accessed {{ $value }} {{ $labels.data_type }} records"

    - name: network
      rules:
        - alert: SuspiciousOutboundTraffic
          expr: |
            sum(rate(network_egress_bytes_total{destination!~"internal.*"}[5m])) by (pod) > 10000000
          for: 10m
          labels:
            severity: warning
            category: security
          annotations:
            summary: "Unusual outbound network traffic"
            description: "Pod {{ $labels.pod }} sending high volume to external destinations"

    - name: certificates
      rules:
        - alert: CertificateExpiringSoon
          expr: |
            (cert_expiry_timestamp_seconds - time()) / 86400 < 30
          for: 1h
          labels:
            severity: warning
            category: security
          annotations:
            summary: "Certificate expiring soon"
            description: "Certificate {{ $labels.cn }} expires in {{ $value }} days"

        - alert: CertificateExpired
          expr: |
            cert_expiry_timestamp_seconds < time()
          for: 0m
          labels:
            severity: critical
            category: security
          annotations:
            summary: "Certificate has expired"
            description: "Certificate {{ $labels.cn }} has expired"
```

---

## Security Headers

### Content Security Policy

```javascript
// csp-config.js - Content Security Policy configuration

const cspConfig = {
  // Base policies
  directives: {
    // Default - block everything not explicitly allowed
    defaultSrc: ["'self'"],

    // Scripts
    scriptSrc: [
      "'self'",
      "'strict-dynamic'",  // Allow dynamically created scripts if parent is trusted
      // Add nonce for inline scripts: `'nonce-${nonce}'`
    ],

    // Styles
    styleSrc: [
      "'self'",
      "'unsafe-inline'",  // Required for many CSS-in-JS solutions
    ],

    // Images
    imgSrc: [
      "'self'",
      "data:",
      "https://cdn.yourapp.com",
      "https://*.gravatar.com",
    ],

    // Fonts
    fontSrc: [
      "'self'",
      "https://fonts.gstatic.com",
    ],

    // Connections (fetch, XHR, WebSocket)
    connectSrc: [
      "'self'",
      "https://api.yourapp.com",
      "wss://realtime.yourapp.com",
      "https://analytics.yourapp.com",
    ],

    // Media (audio, video)
    mediaSrc: [
      "'self'",
      "https://cdn.yourapp.com",
    ],

    // Object, embed, applet
    objectSrc: ["'none'"],

    // Frames
    frameSrc: [
      "'self'",
      "https://www.youtube.com",
      "https://player.vimeo.com",
    ],

    // Frame ancestors (who can embed this page)
    frameAncestors: ["'self'"],

    // Form submissions
    formAction: ["'self'"],

    // Base URI
    baseUri: ["'self'"],

    // Upgrade insecure requests
    upgradeInsecureRequests: [],

    // Block mixed content
    blockAllMixedContent: [],

    // Report violations
    reportUri: ["/api/csp-report"],
    reportTo: ["csp-endpoint"],
  },

  // Report-Only mode for testing
  reportOnly: false,
};

// Express middleware
function cspMiddleware(req, res, next) {
  const nonce = crypto.randomBytes(16).toString('base64');
  res.locals.cspNonce = nonce;

  const directives = { ...cspConfig.directives };
  directives.scriptSrc = [...directives.scriptSrc, `'nonce-${nonce}'`];

  const cspHeader = Object.entries(directives)
    .map(([key, values]) => {
      const directive = key.replace(/([A-Z])/g, '-$1').toLowerCase();
      return `${directive} ${values.join(' ')}`;
    })
    .join('; ');

  const headerName = cspConfig.reportOnly
    ? 'Content-Security-Policy-Report-Only'
    : 'Content-Security-Policy';

  res.setHeader(headerName, cspHeader);
  next();
}
```

### Complete Security Headers (Helmet.js)

```javascript
// security-headers.js - Complete security headers configuration

const helmet = require('helmet');

const securityHeaders = helmet({
  // Content Security Policy
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'", "'strict-dynamic'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.yourapp.com"],
      fontSrc: ["'self'", "https://fonts.gstatic.com"],
      objectSrc: ["'none'"],
      frameAncestors: ["'self'"],
      formAction: ["'self'"],
      upgradeInsecureRequests: [],
    },
  },

  // Strict Transport Security
  strictTransportSecurity: {
    maxAge: 31536000,  // 1 year
    includeSubDomains: true,
    preload: true,
  },

  // X-Content-Type-Options
  xContentTypeOptions: true,  // nosniff

  // X-Frame-Options
  xFrameOptions: { action: 'deny' },

  // X-XSS-Protection (legacy, but still useful)
  xXssProtection: true,

  // Referrer-Policy
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin',
  },

  // Permissions-Policy (formerly Feature-Policy)
  permittedCrossDomainPolicies: false,

  // DNS Prefetch Control
  dnsPrefetchControl: { allow: false },

  // Download Options (IE)
  xDownloadOptions: true,

  // Powered-By (remove)
  xPoweredBy: false,

  // Origin-Agent-Cluster
  originAgentCluster: true,

  // Cross-Origin headers
  crossOriginEmbedderPolicy: { policy: 'require-corp' },
  crossOriginOpenerPolicy: { policy: 'same-origin' },
  crossOriginResourcePolicy: { policy: 'same-origin' },
});

module.exports = securityHeaders;
```

---

## Related Files

- [README.md](README.md) - Security architecture overview
- [checklist.md](checklist.md) - Security design checklist
- [examples.md](examples.md) - Real-world examples
- [llm-prompts.md](llm-prompts.md) - LLM-assisted security design
