# Secrets Management Examples

## HashiCorp Vault

### Installation and Basic Setup

```bash
# Install Vault (Debian/Ubuntu)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault

# Production configuration
vault server -config=/etc/vault.d/vault.hcl
```

### Production Configuration

```hcl
# /etc/vault.d/vault.hcl

storage "raft" {
  path    = "/opt/vault/data"
  node_id = "node1"
}

listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"
}

api_addr     = "https://vault.example.com:8200"
cluster_addr = "https://vault.example.com:8201"

ui = true

# Auto-unseal with AWS KMS
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal"
}
```

### Basic Operations

```bash
# Initialize Vault
vault operator init

# Unseal Vault (if not using auto-unseal)
vault operator unseal <unseal-key>

# Login
vault login <root-token>
vault login -method=userpass username=admin

# Enable secrets engine
vault secrets enable -path=secret kv-v2
vault secrets enable database
vault secrets enable pki

# Write secret
vault kv put secret/myapp/config \
  db_user="admin" \
  db_password="s3cr3t"

# Read secret
vault kv get secret/myapp/config
vault kv get -field=db_password secret/myapp/config

# Enable auth method
vault auth enable kubernetes
vault auth enable oidc
```

### Policy Definition

```hcl
# /etc/vault.d/policies/myapp.hcl

# Read-only access to myapp secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Database credentials
path "database/creds/myapp-db" {
  capabilities = ["read"]
}

# PKI certificates
path "pki/issue/myapp" {
  capabilities = ["create", "update"]
}

# Deny access to admin paths
path "sys/*" {
  capabilities = ["deny"]
}
```

### Dynamic Database Credentials

```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL connection
vault write database/config/mydb \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db.example.com:5432/mydb?sslmode=require" \
  allowed_roles="myapp-readonly,myapp-readwrite" \
  username="vault" \
  password="vaultpassword"

# Create read-only role
vault write database/roles/myapp-readonly \
  db_name=mydb \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Create read-write role
vault write database/roles/myapp-readwrite \
  db_name=mydb \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Get credentials (returns auto-generated, auto-expiring credentials)
vault read database/creds/myapp-readonly
```

### Kubernetes Auth Configuration

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth (from within K8s)
vault write auth/kubernetes/config \
  kubernetes_host="https://$KUBERNETES_PORT_443_TCP_ADDR:443" \
  token_reviewer_jwt="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create role for app
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=myapp-sa \
  bound_service_account_namespaces=production \
  policies=myapp-policy \
  ttl=1h
```

---

## AWS Secrets Manager

### Create and Manage Secrets (CLI)

```bash
# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --description "Database credentials for myapp" \
  --secret-string '{"username":"admin","password":"s3cr3t"}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id myapp/database

# Update secret
aws secretsmanager update-secret \
  --secret-id myapp/database \
  --secret-string '{"username":"admin","password":"newpassword"}'

# Enable rotation
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789:function:RotateSecret \
  --rotation-rules AutomaticallyAfterDays=30
```

### Terraform Configuration

```hcl
# Create secret
resource "aws_secretsmanager_secret" "database" {
  name        = "myapp/database"
  description = "Database credentials for myapp"

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    username = "admin"
    password = random_password.db_password.result
  })
}

resource "random_password" "db_password" {
  length  = 32
  special = true
}

# Rotation configuration
resource "aws_secretsmanager_secret_rotation" "database" {
  secret_id           = aws_secretsmanager_secret.database.id
  rotation_lambda_arn = aws_lambda_function.rotate_secret.arn

  rotation_rules {
    automatically_after_days = 30
  }
}
```

### Application Access (Python)

```python
import boto3
import json
from functools import lru_cache
from botocore.exceptions import ClientError

@lru_cache(maxsize=100)
def get_secret(secret_name: str, region_name: str = "us-east-1") -> dict:
    """Get secret from AWS Secrets Manager with caching."""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise ValueError(f"Secret {secret_name} not found")
        raise

    if 'SecretString' in response:
        return json.loads(response['SecretString'])
    else:
        import base64
        return json.loads(base64.b64decode(response['SecretBinary']))


# Usage
db_creds = get_secret("myapp/database")
db_user = db_creds['username']
db_password = db_creds['password']
```

### Rotation Lambda Function

```python
import boto3
import json
import secrets
import string

def lambda_handler(event, context):
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    client = boto3.client('secretsmanager')

    if step == "createSecret":
        # Generate new password
        alphabet = string.ascii_letters + string.digits + "!@#$%"
        new_password = ''.join(secrets.choice(alphabet) for _ in range(32))

        # Get current secret
        current = client.get_secret_value(SecretId=arn)
        secret_dict = json.loads(current['SecretString'])
        secret_dict['password'] = new_password

        # Store pending secret
        client.put_secret_value(
            SecretId=arn,
            ClientRequestToken=token,
            SecretString=json.dumps(secret_dict),
            VersionStages=['AWSPENDING']
        )

    elif step == "setSecret":
        # Update the database with new password
        pending = client.get_secret_value(
            SecretId=arn,
            VersionStage='AWSPENDING'
        )
        secret_dict = json.loads(pending['SecretString'])
        # TODO: Update database password here
        pass

    elif step == "testSecret":
        # Test that new password works
        pending = client.get_secret_value(
            SecretId=arn,
            VersionStage='AWSPENDING'
        )
        secret_dict = json.loads(pending['SecretString'])
        # TODO: Test database connection here
        pass

    elif step == "finishSecret":
        # Promote pending to current
        metadata = client.describe_secret(SecretId=arn)
        current_version = None
        for version, stages in metadata['VersionIdsToStages'].items():
            if 'AWSCURRENT' in stages:
                current_version = version
                break

        client.update_secret_version_stage(
            SecretId=arn,
            VersionStage='AWSCURRENT',
            MoveToVersionId=token,
            RemoveFromVersionId=current_version
        )
```

---

## Kubernetes Secrets

### Native Kubernetes Secrets

```yaml
# Opaque secret
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secrets
  namespace: default
type: Opaque
stringData:  # Use stringData for plain text (auto base64 encoded)
  db_password: password123
  api_key: abcdef123456

---
# TLS secret
apiVersion: v1
kind: Secret
metadata:
  name: tls-secret
type: kubernetes.io/tls
data:
  tls.crt: <base64-cert>
  tls.key: <base64-key>

---
# Docker registry secret
apiVersion: v1
kind: Secret
metadata:
  name: regcred
type: kubernetes.io/dockerconfigjson
data:
  .dockerconfigjson: <base64-docker-config>
```

### Using Secrets in Pods

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    - name: myapp
      image: myapp:latest

      # Single environment variable from secret
      env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: myapp-secrets
              key: db_password

      # All keys as env vars
      envFrom:
        - secretRef:
            name: myapp-secrets

      # Volume mount
      volumeMounts:
        - name: secrets-volume
          mountPath: /etc/secrets
          readOnly: true

  volumes:
    - name: secrets-volume
      secret:
        secretName: myapp-secrets
        defaultMode: 0400  # Read-only for owner
        items:
          - key: api_key
            path: api-key.txt
```

---

## External Secrets Operator

### SecretStore for AWS Secrets Manager

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa  # Uses IRSA
```

### SecretStore for HashiCorp Vault

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-secrets
  namespace: default
spec:
  provider:
    vault:
      server: "https://vault.example.com:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp"
          serviceAccountRef:
            name: myapp-sa
```

### ExternalSecret Resource

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        # Template allows transformation
        DATABASE_URL: "postgresql://{{ .db_username }}:{{ .db_password }}@db.example.com:5432/mydb"
  data:
    - secretKey: db_username
      remoteRef:
        key: myapp/database
        property: username
    - secretKey: db_password
      remoteRef:
        key: myapp/database
        property: password
```

---

## Vault Secrets Operator

### VaultAuth Configuration

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  name: vault-auth
  namespace: default
spec:
  method: kubernetes
  mount: kubernetes
  kubernetes:
    role: myapp
    serviceAccount: myapp-sa
```

### VaultStaticSecret

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultStaticSecret
metadata:
  name: myapp-secrets
  namespace: default
spec:
  type: kv-v2
  mount: secret
  path: myapp/config
  destination:
    name: myapp-secrets
    create: true
  refreshAfter: 30s
  vaultAuthRef: vault-auth
```

### VaultDynamicSecret (Database)

```yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultDynamicSecret
metadata:
  name: myapp-db-creds
  namespace: default
spec:
  mount: database
  path: creds/myapp-readonly
  destination:
    name: myapp-db-creds
    create: true
  renewalPercent: 67
  vaultAuthRef: vault-auth
```

---

## SOPS (Secrets OPerationS)

### Configuration

```yaml
# .sops.yaml
creation_rules:
  - path_regex: secrets/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/abc123
    pgp: FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4

  - path_regex: secrets/production/.*
    kms: arn:aws:kms:us-east-1:123456789:key/prod-key

  - path_regex: secrets/staging/.*
    kms: arn:aws:kms:us-east-1:123456789:key/staging-key
```

### Operations

```bash
# Create encrypted file (opens editor)
sops secrets/database.yaml

# Encrypt existing file
sops -e secrets.yaml > secrets.enc.yaml

# Decrypt file
sops -d secrets.enc.yaml > secrets.yaml

# Edit encrypted file in place
sops secrets.enc.yaml

# Extract single value
sops -d --extract '["database"]["password"]' secrets.enc.yaml
```

---

## Git Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for potential secrets
PATTERNS=(
    'password\s*=\s*["\047][^"\047]+'
    'api[_-]?key\s*=\s*["\047][^"\047]+'
    'secret\s*=\s*["\047][^"\047]+'
    'AKIA[0-9A-Z]{16}'  # AWS Access Key
    '-----BEGIN (RSA|OPENSSH|EC) PRIVATE KEY-----'
    'ghp_[a-zA-Z0-9]{36}'  # GitHub Personal Access Token
    'sk-[a-zA-Z0-9]{48}'   # OpenAI API Key
)

for pattern in "${PATTERNS[@]}"; do
    matches=$(git diff --cached --name-only | xargs grep -l -E "$pattern" 2>/dev/null)
    if [ -n "$matches" ]; then
        echo "ERROR: Potential secret detected!"
        echo "Pattern: $pattern"
        echo "Files: $matches"
        exit 1
    fi
done

exit 0
```

---

## Application Configuration (Python)

```python
# config.py - Secure configuration loading

import os
from functools import lru_cache
from typing import Optional

class SecretsProvider:
    """Abstract secrets provider."""

    def get_secret(self, key: str) -> Optional[str]:
        raise NotImplementedError


class EnvSecretsProvider(SecretsProvider):
    """Get secrets from environment variables."""

    def get_secret(self, key: str) -> Optional[str]:
        return os.getenv(key)


class VaultSecretsProvider(SecretsProvider):
    """Get secrets from HashiCorp Vault."""

    def __init__(self, vault_addr: str, vault_token: str):
        import hvac
        self.client = hvac.Client(url=vault_addr, token=vault_token)

    @lru_cache(maxsize=100)
    def get_secret(self, key: str) -> Optional[str]:
        path, field = key.rsplit('/', 1)
        secret = self.client.secrets.kv.v2.read_secret_version(path=path)
        return secret['data']['data'].get(field)


class AWSSecretsProvider(SecretsProvider):
    """Get secrets from AWS Secrets Manager."""

    def __init__(self, region: str = "us-east-1"):
        import boto3
        self.client = boto3.client('secretsmanager', region_name=region)

    @lru_cache(maxsize=100)
    def get_secret(self, key: str) -> Optional[str]:
        import json
        response = self.client.get_secret_value(SecretId=key)
        return json.loads(response['SecretString'])


class Settings:
    """Application settings with secure secret loading."""

    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self._provider = self._init_provider()

    def _init_provider(self) -> SecretsProvider:
        if self.environment == 'development':
            return EnvSecretsProvider()
        elif os.getenv('VAULT_ADDR'):
            return VaultSecretsProvider(
                os.environ['VAULT_ADDR'],
                os.environ['VAULT_TOKEN']
            )
        else:
            return AWSSecretsProvider()

    @property
    def db_password(self) -> str:
        return self._provider.get_secret('DB_PASSWORD')

    @property
    def api_key(self) -> str:
        return self._provider.get_secret('API_KEY')


settings = Settings()
```
