# Secrets Management Checklist

## Initial Setup

### Assessment
- [ ] Inventory all secrets (credentials, keys, certificates)
- [ ] Classify secrets by sensitivity level (critical, high, medium)
- [ ] Document current storage locations
- [ ] Identify compliance requirements (SOC2, HIPAA, PCI-DSS)
- [ ] Map secret consumers (apps, services, users)

### Tool Selection
- [ ] Evaluate multi-cloud requirements
- [ ] Assess Kubernetes integration needs
- [ ] Consider operational overhead tolerance
- [ ] Select primary secrets backend (Vault, AWS SM, etc.)
- [ ] Plan for disaster recovery

## HashiCorp Vault Setup

### Installation
- [ ] Choose deployment model (self-hosted, HCP Vault)
- [ ] Configure HA backend (Raft, Consul)
- [ ] Set up TLS certificates
- [ ] Configure auto-unseal (AWS KMS, GCP KMS, Azure Key Vault)
- [ ] Initialize and store root token securely
- [ ] Distribute unseal keys to key custodians

### Configuration
- [ ] Enable required secrets engines (KV, database, PKI)
- [ ] Configure auth methods (Kubernetes, OIDC, AppRole)
- [ ] Create policies following least privilege
- [ ] Set up audit logging
- [ ] Configure secret TTLs and rotation
- [ ] Enable namespaces for multi-tenancy (Enterprise)

### High Availability
- [ ] Deploy minimum 3 nodes for HA
- [ ] Configure auto-join for cluster
- [ ] Set up load balancer
- [ ] Test failover scenarios
- [ ] Document recovery procedures

## AWS Secrets Manager Setup

### Configuration
- [ ] Create secrets with appropriate naming convention
- [ ] Configure KMS encryption keys
- [ ] Set up IAM policies for access
- [ ] Enable rotation for supported secret types
- [ ] Create rotation Lambda functions for custom secrets
- [ ] Configure VPC endpoints for private access

### Rotation
- [ ] Enable automatic rotation (30 days recommended)
- [ ] Test rotation in staging first
- [ ] Configure rotation Lambda for RDS/Aurora
- [ ] Set up CloudWatch alarms for rotation failures
- [ ] Document manual rotation procedures

## Kubernetes Integration

### External Secrets Operator
- [ ] Install ESO via Helm
- [ ] Create SecretStore/ClusterSecretStore resources
- [ ] Configure authentication to backend (IRSA, Workload Identity)
- [ ] Create ExternalSecret resources
- [ ] Set appropriate refresh intervals
- [ ] Test secret synchronization

### Vault Secrets Operator
- [ ] Install VSO via Helm
- [ ] Configure VaultAuth resource
- [ ] Create VaultStaticSecret/VaultDynamicSecret resources
- [ ] Test secret injection
- [ ] Configure renewal/rotation handling

### Vault Agent Sidecar (Alternative)
- [ ] Enable Vault Agent Injector
- [ ] Configure pod annotations
- [ ] Set up init container for pre-start secrets
- [ ] Configure sidecar for dynamic secrets
- [ ] Test lease renewal

## Security Hardening

### Access Control
- [ ] Implement RBAC for secret access
- [ ] Use service accounts, not user credentials
- [ ] Enable MFA for admin access
- [ ] Review and audit permissions quarterly
- [ ] Implement break-glass procedures

### Encryption
- [ ] Enable encryption at rest
- [ ] Use TLS for transit encryption
- [ ] Rotate encryption keys annually
- [ ] Store master keys in HSM (production)
- [ ] Document key recovery procedures

### Auditing
- [ ] Enable audit logging
- [ ] Ship logs to SIEM
- [ ] Create alerts for suspicious access patterns
- [ ] Review audit logs monthly
- [ ] Implement log retention policy

## Secret Rotation

### Automated Rotation
- [ ] Configure rotation schedule (30 days max)
- [ ] Test rotation in non-production first
- [ ] Implement dual-secret support in applications
- [ ] Set up monitoring for rotation failures
- [ ] Document emergency rotation procedures

### Manual Rotation (Breach Response)
- [ ] Define rotation playbook
- [ ] Identify all affected systems
- [ ] Coordinate with application teams
- [ ] Execute rotation with minimal downtime
- [ ] Verify new credentials work
- [ ] Revoke old credentials
- [ ] Document incident

## Development Practices

### Git Security
- [ ] Add secrets patterns to .gitignore
- [ ] Install pre-commit hooks for secret scanning
- [ ] Enable secret scanning in CI/CD
- [ ] Use SOPS or sealed-secrets for GitOps
- [ ] Never commit .env files

### Application Integration
- [ ] Use SDK/library for secret retrieval
- [ ] Implement caching with TTL
- [ ] Handle secret rotation gracefully
- [ ] Mask secrets in logs
- [ ] Use different secrets per environment

### CI/CD
- [ ] Store CI/CD secrets in secure backend
- [ ] Use OIDC for cloud provider auth
- [ ] Avoid long-lived tokens
- [ ] Rotate CI/CD secrets regularly
- [ ] Audit pipeline secret usage

## Monitoring and Alerting

### Metrics
- [ ] Track secret access patterns
- [ ] Monitor rotation success/failure
- [ ] Alert on unauthorized access attempts
- [ ] Track secret age and expiration
- [ ] Monitor backend health

### Alerts
- [ ] Rotation failure
- [ ] Unusual access patterns
- [ ] Expired certificates
- [ ] Backend unavailability
- [ ] Policy violations

## Disaster Recovery

### Backup
- [ ] Regular backend snapshots
- [ ] Encrypted backup storage
- [ ] Test restore procedures quarterly
- [ ] Document recovery time objectives (RTO)
- [ ] Store recovery keys securely offline

### Testing
- [ ] Conduct DR drills annually
- [ ] Test secret recovery procedures
- [ ] Validate backup integrity
- [ ] Document lessons learned
