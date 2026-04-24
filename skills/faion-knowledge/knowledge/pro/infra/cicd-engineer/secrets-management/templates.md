# Secrets Management Templates

## HashiCorp Vault

### Production Configuration Template

```hcl
# /etc/vault.d/vault.hcl

# Raft storage (HA)
storage "raft" {
  path    = "/opt/vault/data"
  node_id = "vault-node-1"

  retry_join {
    leader_api_addr = "https://vault-node-2.example.com:8200"
  }
  retry_join {
    leader_api_addr = "https://vault-node-3.example.com:8200"
  }
}

# TLS listener
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault.crt"
  tls_key_file  = "/opt/vault/tls/vault.key"

  # Disable client cert requirement
  tls_require_and_verify_client_cert = false
  tls_disable_client_certs           = true
}

# API and cluster addresses
api_addr     = "https://vault.example.com:8200"
cluster_addr = "https://vault-node-1.example.com:8201"

# UI
ui = true

# Auto-unseal with AWS KMS
seal "awskms" {
  region     = "${AWS_REGION}"
  kms_key_id = "${KMS_KEY_ID}"
}

# Telemetry for Prometheus
telemetry {
  prometheus_retention_time = "30s"
  disable_hostname          = true
}

# Audit logging
# Enable via CLI: vault audit enable file file_path=/var/log/vault/audit.log
```

### Helm Values Template

```yaml
# vault-values.yaml
global:
  enabled: true
  tlsDisable: false

injector:
  enabled: true
  replicas: 2
  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 256Mi
      cpu: 250m

server:
  image:
    repository: hashicorp/vault
    tag: "1.15.4"

  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 256Mi
      cpu: 250m

  readinessProbe:
    enabled: true
    path: "/v1/sys/health?standbyok=true&sealedcode=204&uninitcode=204"

  livenessProbe:
    enabled: true
    path: "/v1/sys/health?standbyok=true"
    initialDelaySeconds: 60

  # HA configuration
  ha:
    enabled: true
    replicas: 3
    raft:
      enabled: true
      setNodeId: true
      config: |
        ui = true

        listener "tcp" {
          tls_disable = 1
          address = "[::]:8200"
          cluster_address = "[::]:8201"
        }

        storage "raft" {
          path = "/vault/data"
        }

        service_registration "kubernetes" {}

  # Auto-unseal
  seal:
    awskms:
      region: "us-east-1"
      kms_key_id: "alias/vault-unseal"

  serviceAccount:
    create: true
    name: vault

  # Audit logging
  auditStorage:
    enabled: true
    size: 10Gi

ui:
  enabled: true
  serviceType: ClusterIP
```

### Policy Templates

```hcl
# policies/application-readonly.hcl
# Read-only access for applications

path "secret/data/{{identity.entity.aliases.auth_kubernetes_xxx.metadata.service_account_namespace}}/*" {
  capabilities = ["read", "list"]
}

path "database/creds/{{identity.entity.aliases.auth_kubernetes_xxx.metadata.service_account_namespace}}-readonly" {
  capabilities = ["read"]
}
```

```hcl
# policies/application-readwrite.hcl
# Read-write access for applications

path "secret/data/{{identity.entity.aliases.auth_kubernetes_xxx.metadata.service_account_namespace}}/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

path "database/creds/{{identity.entity.aliases.auth_kubernetes_xxx.metadata.service_account_namespace}}-readwrite" {
  capabilities = ["read"]
}
```

```hcl
# policies/admin.hcl
# Admin policy

# Manage secrets engines
path "sys/mounts/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Manage auth methods
path "sys/auth/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Manage policies
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Manage entities and groups
path "identity/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Read system health
path "sys/health" {
  capabilities = ["read"]
}

# Read audit logs
path "sys/audit" {
  capabilities = ["read", "list"]
}
```

---

## AWS Secrets Manager

### Terraform Module Template

```hcl
# modules/secrets-manager/main.tf

variable "environment" {
  type = string
}

variable "application" {
  type = string
}

variable "secrets" {
  type = map(object({
    description     = string
    secret_string   = string
    rotation_days   = optional(number)
    rotation_lambda = optional(string)
  }))
}

variable "kms_key_arn" {
  type = string
}

resource "aws_secretsmanager_secret" "this" {
  for_each = var.secrets

  name        = "${var.environment}/${var.application}/${each.key}"
  description = each.value.description
  kms_key_id  = var.kms_key_arn

  tags = {
    Environment = var.environment
    Application = var.application
    ManagedBy   = "terraform"
  }
}

resource "aws_secretsmanager_secret_version" "this" {
  for_each = var.secrets

  secret_id     = aws_secretsmanager_secret.this[each.key].id
  secret_string = each.value.secret_string
}

resource "aws_secretsmanager_secret_rotation" "this" {
  for_each = {
    for k, v in var.secrets : k => v if v.rotation_lambda != null
  }

  secret_id           = aws_secretsmanager_secret.this[each.key].id
  rotation_lambda_arn = each.value.rotation_lambda

  rotation_rules {
    automatically_after_days = coalesce(each.value.rotation_days, 30)
  }
}

output "secret_arns" {
  value = {
    for k, v in aws_secretsmanager_secret.this : k => v.arn
  }
}
```

### Usage Example

```hcl
# main.tf

module "app_secrets" {
  source = "./modules/secrets-manager"

  environment = "production"
  application = "myapp"
  kms_key_arn = aws_kms_key.secrets.arn

  secrets = {
    database = {
      description   = "Database credentials"
      secret_string = jsonencode({
        username = "myapp_user"
        password = random_password.db.result
        host     = aws_rds_cluster.main.endpoint
        port     = 5432
        database = "myapp"
      })
      rotation_days   = 30
      rotation_lambda = aws_lambda_function.rotate_db.arn
    }

    api_keys = {
      description   = "External API keys"
      secret_string = jsonencode({
        stripe_key  = var.stripe_api_key
        sendgrid_key = var.sendgrid_api_key
      })
    }
  }
}
```

### IAM Policy Template

```hcl
# iam.tf

data "aws_iam_policy_document" "secrets_access" {
  statement {
    sid    = "ReadSecrets"
    effect = "Allow"

    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
    ]

    resources = [
      "arn:aws:secretsmanager:${var.region}:${var.account_id}:secret:${var.environment}/${var.application}/*"
    ]
  }

  statement {
    sid    = "DecryptSecrets"
    effect = "Allow"

    actions = [
      "kms:Decrypt",
    ]

    resources = [
      var.kms_key_arn
    ]

    condition {
      test     = "StringEquals"
      variable = "kms:ViaService"
      values   = ["secretsmanager.${var.region}.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "secrets_access" {
  name   = "${var.application}-secrets-access"
  policy = data.aws_iam_policy_document.secrets_access.json
}
```

---

## SOPS

### Configuration Template

```yaml
# .sops.yaml

creation_rules:
  # Production - AWS KMS (multi-region)
  - path_regex: ^secrets/production/.*\.ya?ml$
    kms: >-
      arn:aws:kms:us-east-1:ACCOUNT_ID:key/KEY_ID_1,
      arn:aws:kms:us-west-2:ACCOUNT_ID:key/KEY_ID_2
    encrypted_regex: ^(password|secret|api_key|token|private_key|credentials)$

  # Staging - AWS KMS
  - path_regex: ^secrets/staging/.*\.ya?ml$
    kms: arn:aws:kms:us-east-1:ACCOUNT_ID:key/STAGING_KEY_ID
    encrypted_regex: ^(password|secret|api_key|token|private_key|credentials)$

  # Development - age key (no cloud dependency)
  - path_regex: ^secrets/development/.*\.ya?ml$
    age: age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2kg5sfn9aqmcac8p
    encrypted_regex: ^(password|secret|api_key|token|private_key|credentials)$

  # GCP environments
  - path_regex: ^secrets/gcp/.*\.ya?ml$
    gcp_kms: projects/PROJECT_ID/locations/global/keyRings/KEYRING/cryptoKeys/KEY
    encrypted_regex: ^(password|secret|api_key|token|private_key|credentials)$

  # Azure environments
  - path_regex: ^secrets/azure/.*\.ya?ml$
    azure_keyvault: https://VAULT_NAME.vault.azure.net/keys/KEY_NAME/KEY_VERSION
    encrypted_regex: ^(password|secret|api_key|token|private_key|credentials)$
```

### Secret File Template

```yaml
# secrets/production/myapp.yaml (before encryption)

# Non-sensitive (will not be encrypted)
app:
  name: myapp
  environment: production
  log_level: info

# Sensitive (will be encrypted based on regex)
database:
  host: db.example.com
  port: 5432
  name: myapp
  username: myapp_user
  password: REPLACE_WITH_ACTUAL_PASSWORD  # Will be encrypted

redis:
  host: redis.example.com
  port: 6379
  password: REPLACE_WITH_ACTUAL_PASSWORD  # Will be encrypted

external_apis:
  stripe:
    api_key: REPLACE_WITH_ACTUAL_KEY      # Will be encrypted
    webhook_secret: REPLACE_WITH_ACTUAL   # Will be encrypted
  sendgrid:
    api_key: REPLACE_WITH_ACTUAL_KEY      # Will be encrypted

jwt:
  secret: REPLACE_WITH_ACTUAL_SECRET      # Will be encrypted
  private_key: |                          # Will be encrypted
    -----BEGIN RSA PRIVATE KEY-----
    REPLACE_WITH_ACTUAL_KEY
    -----END RSA PRIVATE KEY-----
```

---

## External Secrets Operator

### AWS SecretStore Template

```yaml
# external-secrets/aws-secretstore.yaml

apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: ${NAMESPACE}
spec:
  provider:
    aws:
      service: SecretsManager
      region: ${AWS_REGION}
      auth:
        # Option 1: IRSA (recommended for EKS)
        jwt:
          serviceAccountRef:
            name: ${SERVICE_ACCOUNT_NAME}
        # Option 2: Static credentials (not recommended)
        # secretRef:
        #   accessKeyIDSecretRef:
        #     name: aws-credentials
        #     key: access-key-id
        #   secretAccessKeySecretRef:
        #     name: aws-credentials
        #     key: secret-access-key
```

### Vault SecretStore Template

```yaml
# external-secrets/vault-secretstore.yaml

apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: vault-backend
  namespace: ${NAMESPACE}
spec:
  provider:
    vault:
      server: ${VAULT_ADDR}
      path: secret
      version: v2
      # Kubernetes auth (recommended)
      auth:
        kubernetes:
          mountPath: kubernetes
          role: ${VAULT_ROLE}
          serviceAccountRef:
            name: ${SERVICE_ACCOUNT_NAME}
      # Optional: custom CA
      # caProvider:
      #   type: ConfigMap
      #   name: vault-ca
      #   key: ca.crt
```

### ExternalSecret Template

```yaml
# external-secrets/externalsecret.yaml

apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: ${APP_NAME}-secrets
  namespace: ${NAMESPACE}
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: ${SECRET_STORE_NAME}
    kind: SecretStore

  target:
    name: ${APP_NAME}-secrets
    creationPolicy: Owner
    deletionPolicy: Retain
    template:
      type: Opaque
      engineVersion: v2
      data:
        # Templated secret (connection string)
        DATABASE_URL: "postgresql://{{ .db_username }}:{{ .db_password }}@{{ .db_host }}:{{ .db_port }}/{{ .db_name }}"
        # Direct mapping
        REDIS_PASSWORD: "{{ .redis_password }}"
        API_KEY: "{{ .api_key }}"

  data:
    # Individual key mappings
    - secretKey: db_username
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/database
        property: username

    - secretKey: db_password
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/database
        property: password

    - secretKey: db_host
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/database
        property: host

    - secretKey: db_port
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/database
        property: port

    - secretKey: db_name
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/database
        property: database

    - secretKey: redis_password
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/redis
        property: password

    - secretKey: api_key
      remoteRef:
        key: ${ENVIRONMENT}/${APP_NAME}/api-keys
        property: stripe_key
```

### ClusterExternalSecret Template (Multi-namespace)

```yaml
# external-secrets/cluster-externalsecret.yaml

apiVersion: external-secrets.io/v1beta1
kind: ClusterExternalSecret
metadata:
  name: shared-secrets
spec:
  # Namespaces to create secrets in
  namespaceSelector:
    matchLabels:
      secrets-injection: enabled

  refreshTime: 1h

  externalSecretSpec:
    secretStoreRef:
      name: vault-backend
      kind: ClusterSecretStore

    target:
      name: shared-secrets
      creationPolicy: Owner

    data:
      - secretKey: DATADOG_API_KEY
        remoteRef:
          key: shared/observability
          property: datadog_api_key

      - secretKey: SENTRY_DSN
        remoteRef:
          key: shared/observability
          property: sentry_dsn
```

---

## Kubernetes Manifests

### Pod with Secret Injection Template

```yaml
# deployments/app-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${APP_NAME}
  namespace: ${NAMESPACE}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ${APP_NAME}
  template:
    metadata:
      labels:
        app: ${APP_NAME}
    spec:
      serviceAccountName: ${APP_NAME}
      containers:
        - name: ${APP_NAME}
          image: ${IMAGE}
          ports:
            - containerPort: 8080

          # Environment variables from secret
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: ${APP_NAME}-secrets
                  key: DATABASE_URL

            - name: REDIS_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: ${APP_NAME}-secrets
                  key: REDIS_PASSWORD

          # Or all keys as env vars
          # envFrom:
          #   - secretRef:
          #       name: ${APP_NAME}-secrets

          # Volume mount for file-based secrets
          volumeMounts:
            - name: tls-certs
              mountPath: /etc/tls
              readOnly: true

          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"

      volumes:
        - name: tls-certs
          secret:
            secretName: ${APP_NAME}-tls
            items:
              - key: tls.crt
                path: server.crt
              - key: tls.key
                path: server.key
                mode: 0400
```

---

## GitHub Actions

### Secrets Workflow Template

```yaml
# .github/workflows/secrets-check.yml

name: Secrets Security Check

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Run Trivy secret scan
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scanners: 'secret'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  sops-decrypt-test:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4

      - name: Install SOPS
        run: |
          curl -LO https://github.com/getsops/sops/releases/download/v3.8.1/sops-v3.8.1.linux.amd64
          chmod +x sops-v3.8.1.linux.amd64
          sudo mv sops-v3.8.1.linux.amd64 /usr/local/bin/sops

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Test SOPS decryption
        run: |
          for file in secrets/**/*.yaml; do
            echo "Testing decryption of $file"
            sops -d "$file" > /dev/null
          done
```

---

*Ready-to-use templates for secrets management infrastructure.*
