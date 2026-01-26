# Secrets Management Templates

## HashiCorp Vault

### Production Configuration

```hcl
# /etc/vault.d/vault.hcl

# Storage backend (Raft for HA)
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "${NODE_ID}"

  retry_join {
    leader_api_addr = "https://vault-0.vault-internal:8200"
  }
  retry_join {
    leader_api_addr = "https://vault-1.vault-internal:8200"
  }
  retry_join {
    leader_api_addr = "https://vault-2.vault-internal:8200"
  }
}

# Listener configuration
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"

  # Enable client certificate auth (optional)
  # tls_client_ca_file = "/opt/vault/tls/ca.crt"
  # tls_require_and_verify_client_cert = true
}

# API and cluster addresses
api_addr     = "https://${VAULT_FQDN}:8200"
cluster_addr = "https://${VAULT_FQDN}:8201"

# UI
ui = true

# Auto-unseal with AWS KMS
seal "awskms" {
  region     = "${AWS_REGION}"
  kms_key_id = "${KMS_KEY_ID}"
}

# Telemetry
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname          = true
}

# Audit logging
audit "file" {
  file_path = "/var/log/vault/audit.log"
}
```

### Policy Template

```hcl
# policies/application-policy.hcl

# Application read access to its secrets
path "secret/data/${app_name}/*" {
  capabilities = ["read", "list"]
}

# Dynamic database credentials
path "database/creds/${app_name}-*" {
  capabilities = ["read"]
}

# PKI certificate issuance
path "pki/issue/${app_name}" {
  capabilities = ["create", "update"]
}

# Allow token renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Allow token lookup
path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# Deny all admin paths
path "sys/*" {
  capabilities = ["deny"]
}

path "auth/token/root" {
  capabilities = ["deny"]
}
```

### Kubernetes Auth Role

```hcl
# Configure Kubernetes auth role via Terraform

resource "vault_kubernetes_auth_backend_role" "app" {
  backend                          = vault_auth_backend.kubernetes.path
  role_name                        = var.app_name
  bound_service_account_names      = [var.service_account_name]
  bound_service_account_namespaces = [var.namespace]
  token_ttl                        = 3600
  token_max_ttl                    = 86400
  token_policies                   = [vault_policy.app.name]
}
```

---

## Terraform Templates

### AWS Secrets Manager Module

```hcl
# modules/secrets-manager/main.tf

variable "secret_name" {
  description = "Name of the secret"
  type        = string
}

variable "secret_values" {
  description = "Map of secret key-value pairs"
  type        = map(string)
  sensitive   = true
}

variable "rotation_days" {
  description = "Number of days between automatic rotations"
  type        = number
  default     = 30
}

variable "rotation_lambda_arn" {
  description = "ARN of rotation Lambda function"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

resource "aws_secretsmanager_secret" "this" {
  name        = var.secret_name
  description = "Managed secret for ${var.secret_name}"

  tags = merge(var.tags, {
    ManagedBy = "terraform"
  })
}

resource "aws_secretsmanager_secret_version" "this" {
  secret_id     = aws_secretsmanager_secret.this.id
  secret_string = jsonencode(var.secret_values)
}

resource "aws_secretsmanager_secret_rotation" "this" {
  count               = var.rotation_lambda_arn != null ? 1 : 0
  secret_id           = aws_secretsmanager_secret.this.id
  rotation_lambda_arn = var.rotation_lambda_arn

  rotation_rules {
    automatically_after_days = var.rotation_days
  }
}

output "secret_arn" {
  value = aws_secretsmanager_secret.this.arn
}

output "secret_name" {
  value = aws_secretsmanager_secret.this.name
}
```

### Usage

```hcl
# main.tf

module "database_secret" {
  source = "./modules/secrets-manager"

  secret_name = "myapp/production/database"
  secret_values = {
    username = "admin"
    password = random_password.db_password.result
    host     = aws_rds_cluster.main.endpoint
    port     = "5432"
    database = "myapp"
  }
  rotation_days       = 30
  rotation_lambda_arn = aws_lambda_function.rotate_db.arn

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}
```

---

## Kubernetes Templates

### External Secrets Operator

```yaml
# external-secrets/aws-secretstore.yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: ${AWS_REGION}
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets

---
# external-secrets/app-secrets.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: ${APP_NAME}-secrets
    creationPolicy: Owner
    template:
      type: Opaque
      metadata:
        labels:
          app: ${APP_NAME}
  dataFrom:
    - extract:
        key: ${APP_NAME}/${ENVIRONMENT}/config
```

### Vault Secrets Operator

```yaml
# vault-secrets-operator/vault-auth.yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: vault-auth
  namespace: ${NAMESPACE}
spec:
  method: kubernetes
  mount: kubernetes
  kubernetes:
    role: ${APP_NAME}
    serviceAccount: ${APP_NAME}-sa
    audiences:
      - vault

---
# vault-secrets-operator/static-secret.yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: ${APP_NAME}-config
  namespace: ${NAMESPACE}
spec:
  type: kv-v2
  mount: secret
  path: ${APP_NAME}/${ENVIRONMENT}/config
  destination:
    name: ${APP_NAME}-config
    create: true
  refreshAfter: 60s
  vaultAuthRef: vault-auth

---
# vault-secrets-operator/dynamic-secret.yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: ${APP_NAME}-db-creds
  namespace: ${NAMESPACE}
spec:
  mount: database
  path: creds/${APP_NAME}-${ENVIRONMENT}
  destination:
    name: ${APP_NAME}-db-creds
    create: true
  renewalPercent: 67
  vaultAuthRef: vault-auth
```

### Sealed Secrets

```yaml
# sealed-secrets/sealed-secret.yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
spec:
  encryptedData:
    db_password: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
    api_key: AgBy3i4OJSWK+PiTySYZZA9rO43cGDEq...
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    type: Opaque
```

---

## Helm Values Templates

### External Secrets Operator

```yaml
# values-external-secrets.yaml
external-secrets:
  installCRDs: true

  serviceAccount:
    create: true
    name: external-secrets-sa
    annotations:
      eks.amazonaws.com/role-arn: arn:aws:iam::${AWS_ACCOUNT_ID}:role/external-secrets-role

  webhook:
    create: true

  certController:
    create: true
```

### Vault Secrets Operator

```yaml
# values-vault-secrets-operator.yaml
vault:
  address: https://vault.example.com:8200
  caCertSecretRef: vault-ca-cert

defaultAuthMethod:
  enabled: true
  namespace: default
  method: kubernetes
  mount: kubernetes
  kubernetes:
    role: default
    serviceAccount: default
    tokenAudiences:
      - vault
```

---

## Application Templates

### Python Configuration

```python
# config/secrets.py
"""Secrets management configuration."""

import os
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, Dict, Optional


class SecretsBackend(ABC):
    """Abstract secrets backend."""

    @abstractmethod
    def get_secret(self, path: str) -> Dict[str, Any]:
        """Get secret from backend."""
        pass


class EnvSecretsBackend(SecretsBackend):
    """Environment variables backend (development)."""

    def get_secret(self, path: str) -> Dict[str, Any]:
        prefix = path.upper().replace("/", "_")
        result = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                secret_key = key[len(prefix) + 1:].lower()
                result[secret_key] = value
        return result


class VaultSecretsBackend(SecretsBackend):
    """HashiCorp Vault backend."""

    def __init__(self, addr: str, token: Optional[str] = None):
        import hvac
        self.client = hvac.Client(url=addr, token=token)

        # Kubernetes auth if no token provided
        if token is None:
            self._kubernetes_auth()

    def _kubernetes_auth(self):
        with open("/var/run/secrets/kubernetes.io/serviceaccount/token") as f:
            jwt = f.read()
        role = os.getenv("VAULT_ROLE", "default")
        self.client.auth.kubernetes.login(role=role, jwt=jwt)

    @lru_cache(maxsize=100)
    def get_secret(self, path: str) -> Dict[str, Any]:
        response = self.client.secrets.kv.v2.read_secret_version(path=path)
        return response["data"]["data"]


class AWSSecretsBackend(SecretsBackend):
    """AWS Secrets Manager backend."""

    def __init__(self, region: str = "us-east-1"):
        import boto3
        self.client = boto3.client("secretsmanager", region_name=region)

    @lru_cache(maxsize=100)
    def get_secret(self, path: str) -> Dict[str, Any]:
        import json
        response = self.client.get_secret_value(SecretId=path)
        return json.loads(response["SecretString"])


def get_secrets_backend() -> SecretsBackend:
    """Factory function for secrets backend."""
    env = os.getenv("ENVIRONMENT", "development")

    if env == "development":
        return EnvSecretsBackend()
    elif os.getenv("VAULT_ADDR"):
        return VaultSecretsBackend(
            addr=os.environ["VAULT_ADDR"],
            token=os.getenv("VAULT_TOKEN"),
        )
    else:
        return AWSSecretsBackend(
            region=os.getenv("AWS_REGION", "us-east-1")
        )


# Global instance
secrets = get_secrets_backend()
```

### Go Configuration

```go
// pkg/secrets/secrets.go
package secrets

import (
    "context"
    "encoding/json"
    "os"

    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/secretsmanager"
    vault "github.com/hashicorp/vault/api"
)

// Backend defines the secrets backend interface
type Backend interface {
    GetSecret(ctx context.Context, path string) (map[string]string, error)
}

// VaultBackend implements Vault secrets
type VaultBackend struct {
    client *vault.Client
}

// NewVaultBackend creates a new Vault backend
func NewVaultBackend(addr, token string) (*VaultBackend, error) {
    cfg := vault.DefaultConfig()
    cfg.Address = addr

    client, err := vault.NewClient(cfg)
    if err != nil {
        return nil, err
    }

    if token != "" {
        client.SetToken(token)
    } else {
        // Kubernetes auth
        jwt, _ := os.ReadFile("/var/run/secrets/kubernetes.io/serviceaccount/token")
        role := os.Getenv("VAULT_ROLE")
        secret, err := client.Logical().Write("auth/kubernetes/login", map[string]interface{}{
            "role": role,
            "jwt":  string(jwt),
        })
        if err != nil {
            return nil, err
        }
        client.SetToken(secret.Auth.ClientToken)
    }

    return &VaultBackend{client: client}, nil
}

// GetSecret retrieves a secret from Vault
func (b *VaultBackend) GetSecret(ctx context.Context, path string) (map[string]string, error) {
    secret, err := b.client.KVv2("secret").Get(ctx, path)
    if err != nil {
        return nil, err
    }

    result := make(map[string]string)
    for k, v := range secret.Data {
        if s, ok := v.(string); ok {
            result[k] = s
        }
    }
    return result, nil
}

// AWSBackend implements AWS Secrets Manager
type AWSBackend struct {
    client *secretsmanager.Client
}

// NewAWSBackend creates a new AWS Secrets Manager backend
func NewAWSBackend(ctx context.Context, region string) (*AWSBackend, error) {
    cfg, err := config.LoadDefaultConfig(ctx, config.WithRegion(region))
    if err != nil {
        return nil, err
    }

    return &AWSBackend{
        client: secretsmanager.NewFromConfig(cfg),
    }, nil
}

// GetSecret retrieves a secret from AWS Secrets Manager
func (b *AWSBackend) GetSecret(ctx context.Context, secretID string) (map[string]string, error) {
    output, err := b.client.GetSecretValue(ctx, &secretsmanager.GetSecretValueInput{
        SecretId: &secretID,
    })
    if err != nil {
        return nil, err
    }

    var result map[string]string
    if err := json.Unmarshal([]byte(*output.SecretString), &result); err != nil {
        return nil, err
    }
    return result, nil
}
```

---

## CI/CD Templates

### GitHub Actions

```yaml
# .github/workflows/secrets-rotation.yaml
name: Secrets Rotation Check

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  check-rotation:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Check secret rotation status
        run: |
          secrets=$(aws secretsmanager list-secrets --query 'SecretList[*].Name' --output text)
          for secret in $secrets; do
            rotation=$(aws secretsmanager describe-secret --secret-id "$secret" --query 'RotationEnabled' --output text)
            last_rotated=$(aws secretsmanager describe-secret --secret-id "$secret" --query 'LastRotatedDate' --output text)
            echo "Secret: $secret, Rotation: $rotation, Last Rotated: $last_rotated"
          done
```

### GitLab CI

```yaml
# .gitlab-ci.yml
secrets-scan:
  stage: test
  image: trufflesecurity/trufflehog:latest
  script:
    - trufflehog git file://. --only-verified --fail
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## SOPS Configuration

```yaml
# .sops.yaml
creation_rules:
  # Production secrets - AWS KMS
  - path_regex: secrets/production/.*\.yaml$
    kms: arn:aws:kms:us-east-1:${AWS_ACCOUNT_ID}:key/production-key
    encrypted_regex: ^(password|secret|key|token)$

  # Staging secrets - AWS KMS
  - path_regex: secrets/staging/.*\.yaml$
    kms: arn:aws:kms:us-east-1:${AWS_ACCOUNT_ID}:key/staging-key
    encrypted_regex: ^(password|secret|key|token)$

  # Development secrets - age key
  - path_regex: secrets/development/.*\.yaml$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
    encrypted_regex: ^(password|secret|key|token)$

  # Default - PGP
  - pgp: ${PGP_FINGERPRINT}
    encrypted_regex: ^(password|secret|key|token)$
```
