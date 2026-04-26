# LLM Prompts for Secrets Management

## Assessment and Planning

### Secret Inventory Assessment

```
Analyze the following codebase/infrastructure for secrets management:

Context:
- Tech stack: [list technologies]
- Cloud provider(s): [AWS/GCP/Azure/hybrid]
- Kubernetes: [yes/no, version]
- Current secrets storage: [env vars, config files, etc.]

Tasks:
1. Identify all locations where secrets are stored or used
2. Classify secrets by type (credentials, API keys, certificates, tokens)
3. Assess current security posture (encryption, access control, rotation)
4. Identify compliance requirements (SOC2, HIPAA, PCI-DSS)
5. Recommend secrets management solution based on requirements

Output format:
- Secret inventory table (location, type, sensitivity)
- Current risks and gaps
- Recommended solution with justification
- Migration plan outline
```

### Tool Selection Decision

```
Help me select the right secrets management solution.

Requirements:
- Cloud environment: [AWS/GCP/Azure/multi-cloud/hybrid]
- Kubernetes: [yes/no]
- Compliance: [SOC2/HIPAA/PCI-DSS/none]
- Team size: [small/medium/large]
- Budget constraints: [managed service OK / self-hosted preferred]
- Dynamic secrets needed: [yes/no]
- Multi-tenant: [yes/no]

Compare and recommend from:
1. HashiCorp Vault (self-hosted or HCP)
2. AWS Secrets Manager
3. GCP Secret Manager
4. Azure Key Vault
5. External Secrets Operator + backend
6. SOPS + GitOps

Provide:
- Comparison matrix (features, cost, complexity)
- Recommended solution with rationale
- Alternative for specific use cases
- Migration path from current state
```

---

## HashiCorp Vault

### Vault Configuration Review

```
Review this HashiCorp Vault configuration for production readiness:

```hcl
[paste vault.hcl configuration]
```

Check for:
1. Storage backend HA configuration
2. TLS configuration security
3. Auto-unseal configuration
4. Audit logging setup
5. Performance tuning
6. Cluster configuration

Provide:
- Security issues (critical/high/medium/low)
- Best practice recommendations
- Missing configurations
- Optimized configuration example
```

### Vault Policy Design

```
Design HashiCorp Vault policies for the following application architecture:

Application: [name]
Components:
- [list services/microservices]

Secret requirements:
- [service1]: database credentials, API keys
- [service2]: TLS certificates, JWT secrets
- [etc.]

Environments: development, staging, production

Requirements:
- Least privilege access
- Separation between environments
- Emergency break-glass access
- Audit trail

Output:
1. Policy files for each service/role
2. Auth method configuration (Kubernetes/OIDC/AppRole)
3. Secret path structure
4. Admin/break-glass policy
```

### Dynamic Database Credentials Setup

```
Configure HashiCorp Vault dynamic database credentials for:

Database: [PostgreSQL/MySQL/MongoDB/etc.]
Host: [hostname]
Database name: [name]
Environments: [dev/staging/prod]

Application roles needed:
- readonly: SELECT only
- readwrite: SELECT, INSERT, UPDATE, DELETE
- admin: ALL (for migrations)

Requirements:
- TTL: 1 hour default, 24 hour max
- Automatic credential rotation
- Connection pooling considerations

Output:
1. Database secrets engine configuration
2. Role definitions for each access level
3. Application code example for credential retrieval
4. Monitoring and alerting recommendations
```

---

## AWS Secrets Manager

### Secret Structure Design

```
Design AWS Secrets Manager structure for:

Application: [name]
Environments: [dev/staging/prod]
AWS accounts: [single/multi-account]

Secrets needed:
- Database credentials
- Third-party API keys
- Application secrets (JWT, encryption keys)
- Service-to-service auth tokens

Requirements:
- Cross-account access if needed
- Rotation strategy
- Cost optimization
- Tagging strategy

Output:
1. Secret naming convention
2. Secret structure (JSON schema)
3. IAM policies for access
4. Rotation configuration
5. Terraform modules
```

### Rotation Lambda Design

```
Design AWS Secrets Manager rotation Lambda for:

Secret type: [database/API key/custom]
Database type: [if applicable: RDS PostgreSQL/MySQL/Aurora]
Rotation frequency: [days]

Requirements:
- Zero-downtime rotation
- Dual-secret support during transition
- Error handling and rollback
- CloudWatch logging and alerts

Output:
1. Lambda function code (Python)
2. IAM role and permissions
3. CloudWatch alarms
4. Testing procedure
5. Terraform configuration
```

---

## Kubernetes Secrets

### External Secrets Operator Setup

```
Configure External Secrets Operator for:

Cluster: [EKS/GKE/AKS/self-managed]
Backend: [AWS Secrets Manager/Vault/GCP Secret Manager]
Authentication: [IRSA/Workload Identity/Service Account]

Namespaces:
- [namespace1]: [list secrets needed]
- [namespace2]: [list secrets needed]

Requirements:
- ClusterSecretStore vs SecretStore
- Refresh intervals
- Template transformations
- Error handling

Output:
1. ESO Helm values
2. SecretStore/ClusterSecretStore manifests
3. ExternalSecret manifests for each namespace
4. RBAC configuration
5. Monitoring setup
```

### Vault Secrets Operator Migration

```
Migrate from [current solution] to Vault Secrets Operator:

Current state:
- [describe current secrets management]

Target state:
- Vault address: [URL]
- Auth method: Kubernetes
- Secret types: static KV, dynamic database

Applications:
- [app1]: [secrets needed]
- [app2]: [secrets needed]

Requirements:
- Zero-downtime migration
- Rollback plan
- Validation steps

Output:
1. VaultAuth configuration
2. VaultStaticSecret/VaultDynamicSecret manifests
3. Migration runbook
4. Validation checklist
5. Rollback procedure
```

---

## Security and Compliance

### Secret Scanning Setup

```
Set up secret scanning for:

Repository: [GitHub/GitLab/Bitbucket]
CI/CD: [GitHub Actions/GitLab CI/Jenkins]
Languages: [list]

Requirements:
- Pre-commit hooks
- CI pipeline scanning
- Historical commit scanning
- Alert/block configuration

Tools to consider:
- TruffleHog
- GitLeaks
- detect-secrets
- GitHub Advanced Security

Output:
1. Pre-commit hook configuration
2. CI pipeline job
3. False positive handling
4. Remediation playbook
```

### Compliance Audit Preparation

```
Prepare secrets management for compliance audit:

Framework: [SOC2/HIPAA/PCI-DSS/ISO27001]
Current setup:
- Secrets backend: [Vault/AWS SM/etc.]
- Access control: [describe]
- Rotation: [describe]
- Audit logging: [describe]

Generate:
1. Control mapping (framework requirement -> implementation)
2. Evidence collection checklist
3. Gap analysis
4. Remediation recommendations
5. Documentation templates
```

---

## Troubleshooting

### Secret Access Issues

```
Troubleshoot secret access issue:

Error: [paste error message]

Environment:
- Secrets backend: [Vault/AWS SM/etc.]
- Application: [language/framework]
- Infrastructure: [K8s/EC2/Lambda/etc.]
- Auth method: [describe]

Recent changes:
- [list any recent changes]

Provide:
1. Likely root causes
2. Diagnostic commands to run
3. Step-by-step resolution
4. Prevention measures
```

### Rotation Failure

```
Troubleshoot failed secret rotation:

Backend: [AWS Secrets Manager/Vault]
Secret type: [database/API key/etc.]
Error: [paste error/logs]

Current state:
- Secret version status
- Application behavior
- Database/service status

Provide:
1. Root cause analysis
2. Immediate remediation steps
3. Verification commands
4. Long-term fixes
```

---

## Migration and Upgrades

### Migration Planning

```
Plan secrets migration:

Source: [env vars/config files/old solution]
Target: [Vault/AWS SM/etc.]

Inventory:
- [list all secrets to migrate]
- [list all applications using secrets]

Constraints:
- Downtime tolerance: [zero/minimal/scheduled]
- Team availability: [describe]
- Compliance requirements: [describe]

Output:
1. Migration phases
2. Detailed runbook for each phase
3. Rollback procedures
4. Validation checklist
5. Communication plan
```

### Vault Upgrade

```
Plan HashiCorp Vault upgrade:

Current version: [X.Y.Z]
Target version: [X.Y.Z]
Deployment: [HA/single node]
Backend: [Raft/Consul/etc.]

Output:
1. Breaking changes review
2. Pre-upgrade checklist
3. Upgrade procedure (step-by-step)
4. Rollback procedure
5. Post-upgrade validation
6. Client library updates needed
```

---

## Architecture Review

### Secrets Architecture Review

```
Review secrets management architecture:

Current architecture:
[describe or paste diagram]

Components:
- Secrets backend(s): [list]
- Applications: [list]
- Authentication: [describe]
- Rotation: [describe]

Evaluate:
1. Security posture
2. Operational complexity
3. Disaster recovery readiness
4. Scalability
5. Cost efficiency
6. Compliance alignment

Output:
- Architecture diagram (improved)
- Risk assessment
- Recommendations (prioritized)
- Implementation roadmap
```

---

## Cost Optimization

### Cost Analysis

```
Analyze secrets management costs:

Current setup:
- Tool: [Vault/AWS SM/etc.]
- Number of secrets: [count]
- API calls/month: [estimate]
- Infrastructure: [describe]

Provide:
1. Current cost breakdown
2. Cost optimization opportunities
3. Alternative solutions comparison
4. ROI analysis for changes
5. Recommended actions
```
