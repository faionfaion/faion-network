# vault-policy.hcl
# Least-privilege Vault policy for a Kubernetes workload.
# Replace: APP_NAME, ENVIRONMENT, db-role-name.
# Apply: vault policy write APP_NAME-policy vault-policy.hcl

# Read static KV secrets scoped to this app and environment
path "secret/data/{{identity.entity.aliases.auth_kubernetes_default.metadata.service_account_namespace}}/APP_NAME/*" {
  capabilities = ["read", "list"]
}

# Read dynamic database credentials (short-lived, auto-rotated)
path "database/creds/ENVIRONMENT-APP_NAME-readonly" {
  capabilities = ["read"]
}

# Allow token self-renewal (required for long-running applications)
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Allow token self-lookup (for health checks)
path "auth/token/lookup-self" {
  capabilities = ["read"]
}

# Explicitly deny all sys/ paths (defense in depth)
path "sys/*" {
  capabilities = ["deny"]
}

# Explicitly deny cross-namespace secret access
path "secret/data/*/other-app/*" {
  capabilities = ["deny"]
}

# ---
# To create the Kubernetes auth role binding this policy:
#
# vault write auth/kubernetes/role/APP_NAME \
#   bound_service_account_names=APP_NAME \
#   bound_service_account_namespaces=ENVIRONMENT \
#   policies=APP_NAME-policy \
#   ttl=1h \
#   max_ttl=24h
# ---
