# HashiCorp Vault policy templates
# Apply with: vault policy write <name> <file.hcl>

# ---
# Application policy: read-only access to own path
# ---
# vault policy write app-production production-app.hcl
path "secret/data/production/{{identity.entity.aliases.auth_kubernetes_XXX.metadata.service_account_namespace}}/{{identity.entity.aliases.auth_kubernetes_XXX.metadata.service_account_name}}/*" {
  capabilities = ["read"]
}

# Simpler static path for a named application
path "secret/data/production/myapp/*" {
  capabilities = ["read"]
}

# Allow listing (needed for UI and some apps to enumerate paths)
path "secret/metadata/production/myapp/*" {
  capabilities = ["list", "read"]
}

# ---
# CI/CD policy: write secrets during deploy, read during run
# ---
# vault policy write cicd-deploy cicd-deploy.hcl
path "secret/data/production/*" {
  capabilities = ["create", "update"]
  # Restrict to specific fields if needed:
  # allowed_parameters = {
  #   "data" = []
  # }
}

path "secret/data/staging/*" {
  capabilities = ["create", "update", "read", "delete"]
}

# Allow CI to rotate its own token
path "auth/token/renew-self" {
  capabilities = ["update"]
}

path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# ---
# Admin policy: full control over KV engine (break-glass only)
# ---
# vault policy write kv-admin kv-admin.hcl
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list", "patch"]
}

# Allow managing policies themselves
path "sys/policies/acl/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# ---
# Dynamic database credentials policy
# ---
path "database/creds/production-readonly" {
  capabilities = ["read"]
}

path "database/creds/production-readwrite" {
  capabilities = ["read"]
}

# Allow lease renewal (so apps can extend dynamic creds)
path "sys/leases/renew" {
  capabilities = ["update"]
}

# ---
# PKI: request TLS certificates
# ---
path "pki/issue/internal-services" {
  capabilities = ["create", "update"]
  allowed_parameters = {
    "common_name" = ["*.internal.example.com", "*.svc.cluster.local"]
    "ttl"         = ["24h", "72h"]
  }
}

path "pki/cert/ca" {
  capabilities = ["read"]
}

# ---
# Kubernetes auth role (configure, not a policy file, but shown for reference)
# ---
# vault write auth/kubernetes/role/production-app \
#   bound_service_account_names=myapp \
#   bound_service_account_namespaces=production \
#   policies=app-production \
#   ttl=1h \
#   max_ttl=4h
