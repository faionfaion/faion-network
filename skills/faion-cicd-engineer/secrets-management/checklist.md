# Secrets Management Checklist

## Initial Assessment

- [ ] Inventory all secrets (credentials, certs, tokens, keys)
- [ ] Classify secrets by sensitivity (critical, high, medium, low)
- [ ] Identify current storage locations (env vars, files, hardcoded)
- [ ] Document access patterns (who/what needs which secrets)
- [ ] Assess compliance requirements (SOC2, HIPAA, PCI-DSS)

## Tool Selection

### Choose HashiCorp Vault If:
- [ ] Multi-cloud or hybrid environment
- [ ] Need dynamic secrets (DB, AWS, PKI)
- [ ] Regulated industry (banking, healthcare)
- [ ] Have platform team for operations
- [ ] Need complex access policies

### Choose AWS Secrets Manager If:
- [ ] AWS-only infrastructure
- [ ] Want zero operational overhead
- [ ] Need native AWS service integration
- [ ] Budget for per-secret/per-call pricing

### Choose SOPS If:
- [ ] GitOps workflow (Flux, ArgoCD)
- [ ] Small team
- [ ] Don't need dynamic secrets
- [ ] Want encrypted secrets in Git

### Choose External Secrets Operator If:
- [ ] Kubernetes workloads
- [ ] Have existing secrets backend
- [ ] Need automatic sync to K8s secrets
- [ ] Multi-cluster deployments

## HashiCorp Vault Implementation

### Setup
- [ ] Install Vault (package or Helm)
- [ ] Configure storage backend (Raft recommended)
- [ ] Enable TLS (production mandatory)
- [ ] Configure auto-unseal (AWS KMS, GCP KMS, Azure Key Vault)
- [ ] Initialize and store recovery keys securely
- [ ] Enable UI (optional)

### High Availability
- [ ] Deploy 3-5 node Raft cluster
- [ ] Distribute across availability zones
- [ ] Configure load balancer
- [ ] Test failover scenarios
- [ ] Set up monitoring alerts

### Auth Methods
- [ ] Enable Kubernetes auth
- [ ] Enable OIDC/LDAP for humans
- [ ] Enable AppRole for applications
- [ ] Disable unused auth methods

### Secrets Engines
- [ ] Enable KV v2 for static secrets
- [ ] Enable database engine for dynamic DB creds
- [ ] Enable PKI for certificate management
- [ ] Enable AWS/GCP/Azure for cloud credentials

### Policies
- [ ] Create least-privilege policies
- [ ] Deny sys/* by default
- [ ] Scope paths to specific applications
- [ ] Review policies quarterly

### Operations
- [ ] Configure audit logging
- [ ] Set up backup procedures
- [ ] Document recovery procedures
- [ ] Create rotation schedules
- [ ] Establish incident response plan

## AWS Secrets Manager Implementation

### Setup
- [ ] Create secrets with proper naming convention
- [ ] Enable encryption with KMS (CMK recommended)
- [ ] Configure resource policies
- [ ] Set up IAM roles for access

### Rotation
- [ ] Create rotation Lambda function
- [ ] Configure rotation schedule (30 days recommended)
- [ ] Test rotation in staging
- [ ] Monitor rotation failures

### Integration
- [ ] Update application code to fetch secrets at runtime
- [ ] Implement caching (reduce API calls)
- [ ] Handle SecretBinary vs SecretString
- [ ] Add error handling for throttling

### Cost Optimization
- [ ] Consolidate related secrets (JSON)
- [ ] Cache secrets appropriately
- [ ] Monitor API call volume
- [ ] Consider Secrets Manager vs Parameter Store

## SOPS Implementation

### Setup
- [ ] Install SOPS CLI
- [ ] Configure KMS keys (AWS/GCP/Azure)
- [ ] Create .sops.yaml configuration
- [ ] Set up key rotation schedule

### GitOps Integration
- [ ] Configure path regex for different environments
- [ ] Set up Flux/ArgoCD decryption
- [ ] Test encrypt/decrypt cycle
- [ ] Add pre-commit hooks for unencrypted secrets

### Key Management
- [ ] Use multiple master keys (2+ regions)
- [ ] Document key recovery procedures
- [ ] Rotate KMS keys annually
- [ ] Audit key access

## External Secrets Operator Implementation

### Setup
- [ ] Install ESO via Helm
- [ ] Configure RBAC permissions
- [ ] Set up monitoring

### SecretStore Configuration
- [ ] Create SecretStore per namespace (preferred)
- [ ] Use ClusterSecretStore sparingly
- [ ] Configure authentication to backend
- [ ] Test connectivity

### ExternalSecret Configuration
- [ ] Set appropriate refreshInterval
- [ ] Configure target secret name/namespace
- [ ] Map remote keys to local keys
- [ ] Set creationPolicy (Owner recommended)

### Security
- [ ] Minimize RBAC permissions
- [ ] Namespace isolation for SecretStores
- [ ] Audit ClusterSecretStore usage
- [ ] Monitor sync failures

## Security Hardening

### Secret Scanning
- [ ] Enable pre-commit hooks
- [ ] Configure CI secret scanning (GitLeaks, Trivy)
- [ ] Enable GitHub/GitLab secret detection
- [ ] Regular codebase audits

### Access Control
- [ ] Implement least privilege
- [ ] Regular access reviews
- [ ] Remove unused credentials
- [ ] Disable direct secret access in production

### Logging & Monitoring
- [ ] Enable audit logging on all systems
- [ ] Alert on unusual access patterns
- [ ] Monitor for credential leaks
- [ ] Track rotation compliance

### Incident Response
- [ ] Document credential compromise procedure
- [ ] Test rapid rotation capability
- [ ] Establish communication plan
- [ ] Regular incident drills

## Compliance

### Documentation
- [ ] Secret inventory maintained
- [ ] Access policies documented
- [ ] Rotation schedules documented
- [ ] Recovery procedures documented

### Auditing
- [ ] Regular access reviews
- [ ] Audit log retention (meet compliance)
- [ ] Third-party security assessments
- [ ] Penetration testing

### Testing
- [ ] DR recovery testing
- [ ] Rotation testing
- [ ] Access revocation testing
- [ ] Failover testing

## Migration Checklist

### From Environment Variables
- [ ] Inventory all env vars
- [ ] Migrate to secrets manager
- [ ] Update application code
- [ ] Remove hardcoded values
- [ ] Verify in staging
- [ ] Cut over in production

### From Static Files
- [ ] Identify all secret files
- [ ] Encrypt with SOPS or migrate to vault
- [ ] Update deployment process
- [ ] Remove unencrypted files
- [ ] Update .gitignore

---

*Use this checklist to ensure comprehensive secrets management implementation.*
