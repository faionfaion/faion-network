# Secrets Management Examples

## HashiCorp Vault

### Installation

```bash
# Install Vault (Ubuntu/Debian)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault

# Helm installation (Kubernetes)
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install vault hashicorp/vault \
  --namespace vault \
  --create-namespace \
  --set "server.ha.enabled=true" \
  --set "server.ha.raft.enabled=true"
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
ui           = true

# Auto-unseal with AWS KMS
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "alias/vault-unseal"
}

# Telemetry
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname          = true
}
```

### Basic Operations

```bash
# Initialize Vault
vault operator init -key-shares=5 -key-threshold=3

# Unseal (manual, if no auto-unseal)
vault operator unseal <unseal-key-1>
vault operator unseal <unseal-key-2>
vault operator unseal <unseal-key-3>

# Login
vault login <root-token>
vault login -method=userpass username=admin

# Enable secrets engines
vault secrets enable -path=secret kv-v2
vault secrets enable database
vault secrets enable pki

# Write/Read secrets
vault kv put secret/myapp/config \
  db_user="admin" \
  db_password="$(openssl rand -base64 32)"

vault kv get secret/myapp/config
vault kv get -field=db_password secret/myapp/config

# Enable auth methods
vault auth enable kubernetes
vault auth enable oidc
```

### Policies

```hcl
# policies/myapp-policy.hcl

# Read-only access to myapp secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Database credentials (dynamic)
path "database/creds/myapp-db" {
  capabilities = ["read"]
}

# PKI certificates
path "pki/issue/myapp" {
  capabilities = ["create", "update"]
}

# Deny admin paths
path "sys/*" {
  capabilities = ["deny"]
}
```

```bash
# Apply policy
vault policy write myapp policies/myapp-policy.hcl
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
  username="vault_admin" \
  password="vault_admin_password"

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

# Get credentials (auto-generated, auto-expires)
vault read database/creds/myapp-readonly
```

### Kubernetes Auth

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc" \
  kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt

# Create role for myapp
vault write auth/kubernetes/role/myapp \
  bound_service_account_names=myapp \
  bound_service_account_namespaces=default \
  policies=myapp \
  ttl=1h
```

### Application Integration (Python)

```python
import hvac
import os

def get_vault_client():
    """Get authenticated Vault client."""
    client = hvac.Client(url=os.getenv('VAULT_ADDR'))

    # Kubernetes auth
    if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token'):
        with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as f:
            jwt = f.read()
        client.auth.kubernetes.login(role='myapp', jwt=jwt)
    else:
        # Token auth for development
        client.token = os.getenv('VAULT_TOKEN')

    return client

def get_secret(path: str, key: str) -> str:
    """Get secret from Vault KV v2."""
    client = get_vault_client()
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret['data']['data'][key]

def get_db_credentials() -> tuple[str, str]:
    """Get dynamic database credentials."""
    client = get_vault_client()
    creds = client.secrets.database.generate_credentials(name='myapp-readonly')
    return creds['data']['username'], creds['data']['password']

# Usage
db_password = get_secret('myapp/config', 'db_password')
db_user, db_pass = get_db_credentials()
```

---

## AWS Secrets Manager

### CLI Operations

```bash
# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --description "Database credentials for myapp" \
  --secret-string '{"username":"admin","password":"s3cr3t123!","host":"db.example.com","port":5432}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id myapp/database \
  --query SecretString \
  --output text | jq .

# Update secret
aws secretsmanager update-secret \
  --secret-id myapp/database \
  --secret-string '{"username":"admin","password":"newpassword123!"}'

# Rotate secret manually
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:us-east-1:123456789:function:RotateSecret

# Delete secret (with recovery window)
aws secretsmanager delete-secret \
  --secret-id myapp/database \
  --recovery-window-in-days 7
```

### Terraform Configuration

```hcl
# secrets.tf

resource "random_password" "db_password" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_secretsmanager_secret" "database" {
  name        = "${var.environment}/myapp/database"
  description = "Database credentials for myapp"
  kms_key_id  = aws_kms_key.secrets.arn

  tags = {
    Environment = var.environment
    Application = "myapp"
    ManagedBy   = "terraform"
  }
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    username = "myapp_user"
    password = random_password.db_password.result
    host     = aws_rds_cluster.main.endpoint
    port     = 5432
    database = "myapp"
  })
}

# Rotation configuration
resource "aws_secretsmanager_secret_rotation" "database" {
  secret_id           = aws_secretsmanager_secret.database.id
  rotation_lambda_arn = aws_lambda_function.rotate_secret.arn

  rotation_rules {
    automatically_after_days = 30
  }
}

# IAM policy for application access
resource "aws_iam_policy" "secrets_access" {
  name = "myapp-secrets-access"

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
          aws_secretsmanager_secret.database.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt"
        ]
        Resource = [
          aws_kms_key.secrets.arn
        ]
      }
    ]
  })
}
```

### Application Integration (Python)

```python
import boto3
import json
from functools import lru_cache
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self, region_name: str = "us-east-1"):
        self.client = boto3.client(
            service_name='secretsmanager',
            region_name=region_name
        )

    @lru_cache(maxsize=100)
    def get_secret(self, secret_name: str) -> dict:
        """Get secret with caching."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'ResourceNotFoundException':
                raise ValueError(f"Secret {secret_name} not found")
            elif error_code == 'DecryptionFailure':
                raise PermissionError(f"Cannot decrypt secret {secret_name}")
            else:
                raise

        if 'SecretString' in response:
            return json.loads(response['SecretString'])
        else:
            import base64
            return json.loads(base64.b64decode(response['SecretBinary']))

    def refresh_secret(self, secret_name: str) -> dict:
        """Force refresh cached secret."""
        self.get_secret.cache_clear()
        return self.get_secret(secret_name)

# Usage
secrets = SecretsManager()
db_config = secrets.get_secret("production/myapp/database")

connection_string = (
    f"postgresql://{db_config['username']}:{db_config['password']}"
    f"@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)
```

### Application Integration (Node.js)

```javascript
const { SecretsManagerClient, GetSecretValueCommand } = require("@aws-sdk/client-secrets-manager");

const client = new SecretsManagerClient({ region: "us-east-1" });

// Simple cache
const secretsCache = new Map();
const CACHE_TTL = 300000; // 5 minutes

async function getSecret(secretName) {
  const cached = secretsCache.get(secretName);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.value;
  }

  const command = new GetSecretValueCommand({ SecretId: secretName });
  const response = await client.send(command);

  const secret = JSON.parse(response.SecretString);
  secretsCache.set(secretName, { value: secret, timestamp: Date.now() });

  return secret;
}

// Usage
async function connectDatabase() {
  const dbConfig = await getSecret("production/myapp/database");
  return new Pool({
    host: dbConfig.host,
    port: dbConfig.port,
    user: dbConfig.username,
    password: dbConfig.password,
    database: dbConfig.database,
  });
}
```

---

## SOPS

### Configuration

```yaml
# .sops.yaml
creation_rules:
  # Production secrets - use production KMS key
  - path_regex: secrets/production/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/prod-key-id
    encrypted_regex: ^(password|secret|api_key|token)$

  # Staging secrets
  - path_regex: secrets/staging/.*\.yaml$
    kms: arn:aws:kms:us-east-1:123456789:key/staging-key-id
    encrypted_regex: ^(password|secret|api_key|token)$

  # Development secrets - use age key
  - path_regex: secrets/development/.*\.yaml$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p

  # Default rule - require both KMS keys (multi-region)
  - path_regex: .*\.enc\.yaml$
    kms: >-
      arn:aws:kms:us-east-1:123456789:key/key-id-1,
      arn:aws:kms:us-west-2:123456789:key/key-id-2
```

### Basic Operations

```bash
# Encrypt file (opens editor, encrypts on save)
sops secrets/production/database.yaml

# Encrypt existing file
sops -e plaintext.yaml > encrypted.yaml

# Decrypt file
sops -d encrypted.yaml > plaintext.yaml

# Edit encrypted file in place
sops secrets/production/database.yaml

# Extract single value
sops -d --extract '["database"]["password"]' secrets/production/database.yaml

# Encrypt specific keys only
sops --encrypt --encrypted-regex '^(password|secret)$' config.yaml > config.enc.yaml

# Rotate keys
sops -r secrets/production/database.yaml
```

### Encrypted File Example

```yaml
# secrets/production/database.yaml (after encryption)
database:
  host: db.example.com  # Not encrypted (not matching regex)
  port: 5432            # Not encrypted
  username: ENC[AES256_GCM,data:dGVzdA==,iv:abc123...,tag:def456...,type:str]
  password: ENC[AES256_GCM,data:c2VjcmV0,iv:ghi789...,tag:jkl012...,type:str]
api:
  endpoint: https://api.example.com  # Not encrypted
  api_key: ENC[AES256_GCM,data:YWJjZGVm,iv:mno345...,tag:pqr678...,type:str]
sops:
  kms:
    - arn: arn:aws:kms:us-east-1:123456789:key/prod-key-id
      created_at: "2026-01-15T10:00:00Z"
      enc: AQICAHh...
  lastmodified: "2026-01-15T10:00:00Z"
  version: 3.8.1
```

### FluxCD Integration

```yaml
# flux-system/gotk-sync.yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: myapp
  namespace: flux-system
spec:
  interval: 10m
  path: ./clusters/production
  prune: true
  sourceRef:
    kind: GitRepository
    name: flux-system
  decryption:
    provider: sops
    secretRef:
      name: sops-age
---
apiVersion: v1
kind: Secret
metadata:
  name: sops-age
  namespace: flux-system
type: Opaque
stringData:
  age.agekey: |
    # created: 2026-01-15T10:00:00Z
    # public key: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
    AGE-SECRET-KEY-1QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
```

### ArgoCD Integration

```yaml
# argocd-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
  namespace: argocd
data:
  kustomize.buildOptions: --enable-helm --enable-alpha-plugins
---
# Install KSOPS plugin
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cmp-cm
  namespace: argocd
data:
  plugin.yaml: |
    apiVersion: argoproj.io/v1alpha1
    kind: ConfigManagementPlugin
    metadata:
      name: kustomize-sops
    spec:
      generate:
        command: ["sh", "-c"]
        args: ["kustomize build --enable-alpha-plugins"]
```

---

## External Secrets Operator

### Installation

```bash
# Helm installation
helm repo add external-secrets https://charts.external-secrets.io
helm install external-secrets external-secrets/external-secrets \
  --namespace external-secrets \
  --create-namespace \
  --set installCRDs=true
```

### AWS Secrets Manager Backend

```yaml
# ClusterSecretStore for AWS (use sparingly)
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
            namespace: external-secrets
---
# Namespace-scoped SecretStore (preferred)
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets
  namespace: myapp
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        secretRef:
          accessKeyIDSecretRef:
            name: aws-credentials
            key: access-key-id
          secretAccessKeySecretRef:
            name: aws-credentials
            key: secret-access-key
---
# ExternalSecret
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-database
  namespace: myapp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets
    kind: SecretStore
  target:
    name: myapp-database-secret
    creationPolicy: Owner
    template:
      type: Opaque
      data:
        DATABASE_URL: "postgresql://{{ .username }}:{{ .password }}@{{ .host }}:{{ .port }}/{{ .database }}"
  data:
    - secretKey: username
      remoteRef:
        key: production/myapp/database
        property: username
    - secretKey: password
      remoteRef:
        key: production/myapp/database
        property: password
    - secretKey: host
      remoteRef:
        key: production/myapp/database
        property: host
    - secretKey: port
      remoteRef:
        key: production/myapp/database
        property: port
    - secretKey: database
      remoteRef:
        key: production/myapp/database
        property: database
```

### HashiCorp Vault Backend

```yaml
# SecretStore for Vault
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: myapp
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
            name: myapp
---
# ExternalSecret from Vault
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-config
  namespace: myapp
spec:
  refreshInterval: 15m
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: myapp-config-secret
    creationPolicy: Owner
  dataFrom:
    - extract:
        key: myapp/config
```

### GCP Secret Manager Backend

```yaml
# SecretStore for GCP
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: gcp-secrets
  namespace: myapp
spec:
  provider:
    gcpsm:
      projectID: my-project-id
      auth:
        workloadIdentity:
          clusterLocation: us-central1
          clusterName: my-cluster
          serviceAccountRef:
            name: external-secrets-sa
---
# ExternalSecret from GCP
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-api-key
  namespace: myapp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: gcp-secrets
    kind: SecretStore
  target:
    name: myapp-api-key-secret
  data:
    - secretKey: API_KEY
      remoteRef:
        key: myapp-api-key
        version: latest
```

---

## Secret Rotation

### AWS Lambda Rotation Function

```python
import boto3
import json
import string
import secrets
import psycopg2

def lambda_handler(event, context):
    """AWS Secrets Manager rotation handler."""
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']

    client = boto3.client('secretsmanager')
    metadata = client.describe_secret(SecretId=arn)

    if step == "createSecret":
        create_secret(client, arn, token)
    elif step == "setSecret":
        set_secret(client, arn, token)
    elif step == "testSecret":
        test_secret(client, arn, token)
    elif step == "finishSecret":
        finish_secret(client, arn, token)

def create_secret(client, arn, token):
    """Generate new password and store as pending."""
    # Get current secret
    current = client.get_secret_value(
        SecretId=arn,
        VersionStage="AWSCURRENT"
    )
    current_dict = json.loads(current['SecretString'])

    # Generate new password
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    new_password = ''.join(secrets.choice(alphabet) for _ in range(32))

    # Store pending secret
    new_secret = current_dict.copy()
    new_secret['password'] = new_password

    client.put_secret_value(
        SecretId=arn,
        ClientRequestToken=token,
        SecretString=json.dumps(new_secret),
        VersionStages=['AWSPENDING']
    )

def set_secret(client, arn, token):
    """Update database with new password."""
    pending = client.get_secret_value(
        SecretId=arn,
        VersionId=token,
        VersionStage="AWSPENDING"
    )
    pending_dict = json.loads(pending['SecretString'])

    current = client.get_secret_value(
        SecretId=arn,
        VersionStage="AWSCURRENT"
    )
    current_dict = json.loads(current['SecretString'])

    # Connect with current credentials
    conn = psycopg2.connect(
        host=current_dict['host'],
        port=current_dict['port'],
        user=current_dict['username'],
        password=current_dict['password'],
        database=current_dict['database']
    )

    # Update password
    with conn.cursor() as cur:
        cur.execute(
            f"ALTER USER {current_dict['username']} WITH PASSWORD %s",
            (pending_dict['password'],)
        )
    conn.commit()
    conn.close()

def test_secret(client, arn, token):
    """Test new password works."""
    pending = client.get_secret_value(
        SecretId=arn,
        VersionId=token,
        VersionStage="AWSPENDING"
    )
    pending_dict = json.loads(pending['SecretString'])

    # Test connection
    conn = psycopg2.connect(
        host=pending_dict['host'],
        port=pending_dict['port'],
        user=pending_dict['username'],
        password=pending_dict['password'],
        database=pending_dict['database']
    )
    conn.close()

def finish_secret(client, arn, token):
    """Promote pending to current."""
    metadata = client.describe_secret(SecretId=arn)

    current_version = None
    for version_id, stages in metadata['VersionIdsToStages'].items():
        if 'AWSCURRENT' in stages:
            current_version = version_id
            break

    client.update_secret_version_stage(
        SecretId=arn,
        VersionStage='AWSCURRENT',
        MoveToVersionId=token,
        RemoveFromVersionId=current_version
    )
```

---

## Git Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Patterns to detect
PATTERNS=(
    'password\s*[=:]\s*["\047][^"\047]+'
    'api[_-]?key\s*[=:]\s*["\047][^"\047]+'
    'secret\s*[=:]\s*["\047][^"\047]+'
    'AKIA[0-9A-Z]{16}'                              # AWS Access Key ID
    'aws_secret_access_key\s*[=:]\s*["\047][^"\047]+'
    '-----BEGIN (RSA|OPENSSH|EC|PGP) PRIVATE KEY-----'
    'ghp_[a-zA-Z0-9]{36}'                           # GitHub PAT
    'gho_[a-zA-Z0-9]{36}'                           # GitHub OAuth
    'glpat-[a-zA-Z0-9\-]{20}'                       # GitLab PAT
    'sk-[a-zA-Z0-9]{48}'                            # OpenAI API Key
    'xox[baprs]-[0-9a-zA-Z\-]+'                     # Slack tokens
)

STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACMR)

if [ -z "$STAGED_FILES" ]; then
    exit 0
fi

FOUND_SECRETS=0

for pattern in "${PATTERNS[@]}"; do
    matches=$(echo "$STAGED_FILES" | xargs grep -l -E "$pattern" 2>/dev/null || true)
    if [ -n "$matches" ]; then
        echo "ERROR: Potential secret detected!"
        echo "Pattern: $pattern"
        echo "Files: $matches"
        FOUND_SECRETS=1
    fi
done

if [ $FOUND_SECRETS -eq 1 ]; then
    echo ""
    echo "To bypass this check (use with caution):"
    echo "  git commit --no-verify"
    exit 1
fi

exit 0
```

---

*Examples for Vault, AWS Secrets Manager, SOPS, and External Secrets Operator.*
