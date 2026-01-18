# M-DO-014: Secrets Management

## Metadata
- **Category:** Development/DevOps
- **Difficulty:** Intermediate
- **Tags:** #devops, #security, #secrets, #vault, #methodology
- **Agent:** faion-devops-agent

---

## Problem

Secrets in code, environment files, and configuration are security risks. Credential rotation is manual and error-prone. Audit trails are missing.

## Promise

After this methodology, you will manage secrets securely with HashiCorp Vault or cloud-native solutions. Credentials will be centralized and auditable.

## Overview

Secrets management centralizes sensitive data (API keys, passwords, certificates). This methodology covers Vault, AWS Secrets Manager, and best practices.

---

## Framework

### Step 1: Vault Setup

```yaml
# docker-compose.yml
version: "3.9"

services:
  vault:
    image: hashicorp/vault:1.15
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: myroot
      VAULT_DEV_LISTEN_ADDRESS: 0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    volumes:
      - vault_data:/vault/file
      - ./vault/config:/vault/config

volumes:
  vault_data:
```

```bash
# Initialize Vault (production)
vault operator init

# Unseal (requires 3 of 5 keys)
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>

# Login
vault login <root_token>

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Enable audit logging
vault audit enable file file_path=/vault/logs/audit.log
```

### Step 2: Store Secrets

```bash
# Create secret
vault kv put secret/myapp/database \
  username=admin \
  password=supersecret \
  host=db.example.com

# Read secret
vault kv get secret/myapp/database
vault kv get -field=password secret/myapp/database

# List secrets
vault kv list secret/myapp/

# Delete secret
vault kv delete secret/myapp/database

# Version history
vault kv get -version=2 secret/myapp/database
```

### Step 3: Access Policies

```hcl
# policies/myapp-policy.hcl
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/myapp/*" {
  capabilities = ["list"]
}

path "database/creds/myapp-role" {
  capabilities = ["read"]
}
```

```bash
# Create policy
vault policy write myapp-policy policies/myapp-policy.hcl

# Create token with policy
vault token create -policy=myapp-policy -ttl=1h
```

### Step 4: Application Integration

```javascript
// Node.js with node-vault
const vault = require('node-vault')({
  apiVersion: 'v1',
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
});

async function getSecrets() {
  try {
    const result = await vault.read('secret/data/myapp/database');
    return result.data.data;  // { username, password, host }
  } catch (error) {
    console.error('Failed to read secrets:', error);
    throw error;
  }
}

// With AppRole authentication
async function loginAndGetSecrets() {
  const loginResult = await vault.approleLogin({
    role_id: process.env.VAULT_ROLE_ID,
    secret_id: process.env.VAULT_SECRET_ID,
  });

  vault.token = loginResult.auth.client_token;

  return vault.read('secret/data/myapp/database');
}
```

```python
# Python with hvac
import hvac
import os

client = hvac.Client(
    url=os.environ['VAULT_ADDR'],
    token=os.environ['VAULT_TOKEN'],
)

def get_secrets():
    secret = client.secrets.kv.v2.read_secret_version(
        path='myapp/database',
        mount_point='secret',
    )
    return secret['data']['data']

# With AppRole
def login_and_get_secrets():
    client.auth.approle.login(
        role_id=os.environ['VAULT_ROLE_ID'],
        secret_id=os.environ['VAULT_SECRET_ID'],
    )

    return client.secrets.kv.v2.read_secret_version(
        path='myapp/database',
        mount_point='secret',
    )
```

### Step 5: AWS Secrets Manager

```bash
# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --secret-string '{"username":"admin","password":"supersecret"}'

# Retrieve secret
aws secretsmanager get-secret-value \
  --secret-id myapp/database \
  --query SecretString \
  --output text

# Rotate secret (with Lambda)
aws secretsmanager rotate-secret \
  --secret-id myapp/database \
  --rotation-lambda-arn arn:aws:lambda:...
```

```javascript
// Node.js with AWS SDK
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretId) {
  const response = await client.send(
    new GetSecretValueCommand({ SecretId: secretId })
  );

  return JSON.parse(response.SecretString);
}

// Cache secrets
const secretsCache = new Map();

async function getSecretCached(secretId, ttl = 300000) {
  const cached = secretsCache.get(secretId);

  if (cached && Date.now() - cached.timestamp < ttl) {
    return cached.value;
  }

  const value = await getSecret(secretId);
  secretsCache.set(secretId, { value, timestamp: Date.now() });

  return value;
}
```

### Step 6: Kubernetes Integration

```yaml
# External Secrets Operator
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
spec:
  provider:
    vault:
      server: "http://vault:8200"
      path: "secret"
      version: "v2"
      auth:
        kubernetes:
          mountPath: "kubernetes"
          role: "myapp"

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-secrets
spec:
  refreshInterval: "1h"
  secretStoreRef:
    name: vault-backend
    kind: SecretStore
  target:
    name: myapp-secrets
    creationPolicy: Owner
  data:
    - secretKey: database-password
      remoteRef:
        key: myapp/database
        property: password
```

```yaml
# Using secret in deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  template:
    spec:
      containers:
        - name: app
          env:
            - name: DATABASE_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: myapp-secrets
                  key: database-password
```

---

## Templates

### Terraform Vault Provider

```hcl
provider "vault" {
  address = "http://vault:8200"
}

resource "vault_generic_secret" "database" {
  path = "secret/myapp/database"

  data_json = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = var.db_host
  })
}

data "vault_generic_secret" "database" {
  path = "secret/myapp/database"
}

output "db_host" {
  value     = data.vault_generic_secret.database.data["host"]
  sensitive = true
}
```

### Dynamic Database Credentials

```bash
# Enable database secrets engine
vault secrets enable database

# Configure PostgreSQL
vault write database/config/postgresql \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db:5432/mydb" \
  allowed_roles="myapp-role" \
  username="vault" \
  password="vaultpass"

# Create role
vault write database/roles/myapp-role \
  db_name=postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Get dynamic credentials
vault read database/creds/myapp-role
# Returns: username, password (auto-expires)
```

---

## Examples

### Environment Variable Injection

```bash
# Using envconsul
envconsul \
  -secret secret/myapp/database \
  -upcase \
  ./my-app

# Variables available as:
# SECRET_MYAPP_DATABASE_USERNAME
# SECRET_MYAPP_DATABASE_PASSWORD
```

### Secret Rotation

```javascript
// Watch for secret changes
const chokidar = require('chokidar');
const fs = require('fs');

// Kubernetes secret mounted as volume
const secretPath = '/etc/secrets/database-password';

let dbPassword = fs.readFileSync(secretPath, 'utf8');

chokidar.watch(secretPath).on('change', () => {
  dbPassword = fs.readFileSync(secretPath, 'utf8');
  console.log('Secret rotated, reconnecting...');
  reconnectDatabase();
});
```

---

## Common Mistakes

1. **Secrets in git** - Use .gitignore and pre-commit hooks
2. **Long-lived tokens** - Use short TTL and refresh
3. **No encryption** - Enable encryption at rest
4. **Missing audit** - Enable audit logging
5. **Shared secrets** - Use per-service credentials

---

## Checklist

- [ ] Vault or cloud secrets manager deployed
- [ ] Encryption at rest enabled
- [ ] Audit logging enabled
- [ ] Access policies defined
- [ ] Application integration tested
- [ ] Secret rotation implemented
- [ ] Pre-commit hooks for secret scanning
- [ ] Disaster recovery plan

---

## Next Steps

- M-DO-015: SSL/TLS Certificates
- M-DO-009: Terraform Basics
- M-DO-010: Infrastructure Patterns

---

*Methodology M-DO-014 v1.0*
