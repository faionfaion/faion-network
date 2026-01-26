# Secrets Management LLM Prompts

## Analysis Prompts

### Secrets Audit

```
Analyze this codebase for secrets management issues:

1. **Hardcoded Secrets Detection:**
   - Search for passwords, API keys, tokens in source code
   - Check for private keys, certificates
   - Identify AWS/GCP/Azure credentials
   - Look for connection strings with embedded passwords

2. **Configuration Analysis:**
   - Review .env files and their .gitignore status
   - Check environment variable handling
   - Analyze secret injection patterns
   - Review Docker/K8s secret usage

3. **Security Assessment:**
   - Evaluate secret rotation practices
   - Check for secret logging/exposure
   - Assess access control patterns
   - Review audit logging

Provide findings with:
- Severity (Critical/High/Medium/Low)
- Location (file:line)
- Remediation recommendation
- Code example for fix
```

### Tool Selection

```
Help me choose the right secrets management tool:

**Context:**
- Cloud provider(s): [AWS/GCP/Azure/Multi-cloud]
- Kubernetes: [Yes/No]
- GitOps workflow: [Yes/No]
- Team size: [Small/Medium/Large]
- Compliance requirements: [SOC2/HIPAA/PCI-DSS/None]
- Current secret storage: [Env vars/Files/Parameter Store/etc.]
- Budget constraints: [Yes/No]

**Requirements:**
- Dynamic secrets needed: [Yes/No]
- Auto-rotation required: [Yes/No]
- Multi-region deployment: [Yes/No]
- Development environment needs: [Yes/No]

Recommend:
1. Primary tool with justification
2. Complementary tools if needed
3. Migration path from current state
4. Implementation complexity estimate
```

### Architecture Review

```
Review this secrets management architecture:

[Paste architecture diagram or description]

Evaluate:
1. **Security posture:**
   - Encryption at rest and in transit
   - Access control granularity
   - Audit logging coverage
   - Blast radius of compromise

2. **Operational concerns:**
   - High availability
   - Disaster recovery
   - Rotation automation
   - Performance impact

3. **Best practices alignment:**
   - 2025-2026 industry standards
   - Zero-trust principles
   - Identity-based access
   - Short-lived credentials

Provide:
- Gap analysis
- Risk assessment
- Improvement recommendations
- Priority order for changes
```

---

## Implementation Prompts

### HashiCorp Vault Setup

```
Create HashiCorp Vault configuration for:

**Environment:**
- Deployment: [Kubernetes/VM/Docker]
- HA requirement: [Yes/No, node count]
- Auto-unseal: [AWS KMS/GCP KMS/Azure Key Vault/Shamir]
- Auth methods needed: [Kubernetes/OIDC/LDAP/AppRole]
- Secrets engines: [KV/Database/PKI/AWS/GCP]

**Generate:**
1. Server configuration (vault.hcl)
2. Helm values (if K8s)
3. Policies for [application names]
4. Auth method configuration
5. Secrets engine setup commands
6. Monitoring/alerting recommendations

Include:
- Production security hardening
- Backup/restore procedures
- Troubleshooting guide
```

### AWS Secrets Manager Setup

```
Create AWS Secrets Manager infrastructure for:

**Application:** [Name]
**Environment:** [dev/staging/production]
**Secrets needed:**
- [List of secrets with types]

**Requirements:**
- Rotation: [Yes/No, interval]
- Cross-account access: [Yes/No]
- Multi-region: [Yes/No]

**Generate:**
1. Terraform module for secrets
2. IAM policies for application access
3. Rotation Lambda (if needed)
4. Application code for secret retrieval ([Python/Node.js/Go])
5. Cost estimate
```

### SOPS Configuration

```
Create SOPS configuration for GitOps workflow:

**Environment structure:**
- [development/staging/production]

**KMS providers:**
- [AWS KMS/GCP KMS/Azure Key Vault/age]

**Git workflow:**
- [FluxCD/ArgoCD/plain kubectl]

**Generate:**
1. .sops.yaml configuration
2. Example encrypted secrets file
3. CI/CD integration (GitHub Actions/GitLab CI)
4. Key rotation procedure
5. Team onboarding guide
```

### External Secrets Operator Setup

```
Create External Secrets Operator configuration:

**Backend:** [Vault/AWS SM/GCP SM/Azure KV]
**Namespaces:** [List]
**Authentication:** [IRSA/Workload Identity/Static credentials]

**Secrets to sync:**
[List with source paths and target keys]

**Generate:**
1. SecretStore/ClusterSecretStore manifests
2. ExternalSecret manifests
3. RBAC configuration
4. Monitoring/alerting setup
5. Troubleshooting runbook
```

---

## Migration Prompts

### From Environment Variables

```
Create migration plan from environment variables to secrets manager:

**Current state:**
- Environment variables in: [.env files/Docker Compose/K8s ConfigMaps]
- Number of secrets: [X]
- Environments: [dev/staging/prod]

**Target state:**
- Secrets manager: [Vault/AWS SM/etc.]

**Generate:**
1. Secret inventory template
2. Migration script
3. Application code changes
4. Rollback procedure
5. Testing checklist
6. Cutover runbook
```

### From Static Files

```
Create migration plan from static secret files to encrypted secrets:

**Current state:**
- Secret files in: [repo/config server/mounted volumes]
- File formats: [YAML/JSON/properties]
- Git history contains secrets: [Yes/No]

**Target state:**
- SOPS encrypted files in Git

**Generate:**
1. File inventory
2. .sops.yaml configuration
3. Encryption script
4. Git history cleanup (if needed)
5. CI/CD updates
6. Developer workflow documentation
```

### Cross-Platform Migration

```
Migrate secrets from [Source] to [Target]:

**Source:** [AWS SM/GCP SM/Azure KV/Vault/etc.]
**Target:** [AWS SM/GCP SM/Azure KV/Vault/etc.]

**Constraints:**
- Zero downtime required: [Yes/No]
- Dual-write period: [duration]
- Compliance requirements: [list]

**Generate:**
1. Secret mapping (source path -> target path)
2. Migration script with validation
3. Application changes (if any)
4. Rollback procedure
5. Verification tests
6. Cutover timeline
```

---

## Troubleshooting Prompts

### Access Issues

```
Debug secrets access issue:

**Symptoms:**
[Describe the error/behavior]

**Environment:**
- Secrets manager: [type]
- Application runtime: [K8s/Lambda/EC2/etc.]
- Auth method: [type]

**Logs/Errors:**
[Paste relevant logs]

**Help me:**
1. Identify root cause
2. List diagnostic commands
3. Provide fix
4. Prevent recurrence
```

### Rotation Failures

```
Debug secret rotation failure:

**Secrets manager:** [AWS SM/Vault/etc.]
**Secret type:** [Database/API key/etc.]
**Error:**
[Paste error message]

**Help me:**
1. Diagnose the failure
2. Manual rotation steps
3. Fix automation
4. Add monitoring for future failures
```

### Performance Issues

```
Optimize secrets retrieval performance:

**Current behavior:**
- Latency: [X ms]
- Call frequency: [X calls/minute]
- Caching: [Yes/No, TTL]

**Secrets manager:** [type]
**Application:** [language/framework]

**Help me:**
1. Identify bottlenecks
2. Implement caching strategy
3. Optimize API calls
4. Set up monitoring
```

---

## Security Prompts

### Incident Response

```
Secret potentially compromised:

**Secret type:** [type]
**Exposure vector:** [git commit/logs/breach/etc.]
**Scope:** [single secret/multiple/unknown]

**Generate:**
1. Immediate containment steps
2. Rotation procedure
3. Impact assessment checklist
4. Communication template
5. Post-incident improvements
```

### Compliance Audit

```
Prepare for [SOC2/HIPAA/PCI-DSS] compliance audit:

**Secrets management tools:** [list]
**Questions to address:**
- How are secrets encrypted?
- Who has access?
- How is access audited?
- What is rotation policy?

**Generate:**
1. Documentation template
2. Evidence collection checklist
3. Control mapping
4. Gap analysis
5. Remediation priorities
```

### Threat Modeling

```
Perform threat modeling for secrets management:

**Architecture:**
[Describe or paste architecture]

**Generate:**
1. STRIDE analysis
2. Attack vectors
3. Mitigation controls
4. Residual risks
5. Monitoring recommendations
```

---

## Code Generation Prompts

### Application Integration

```
Generate secrets retrieval code:

**Language:** [Python/Node.js/Go/Java]
**Secrets manager:** [Vault/AWS SM/GCP SM]
**Features needed:**
- Caching: [Yes/No, TTL]
- Error handling: [retry/fallback]
- Logging: [Yes/No]
- Health check: [Yes/No]

**Generate:**
1. Main retrieval class/module
2. Configuration handling
3. Unit tests
4. Usage examples
```

### Pre-commit Hook

```
Generate pre-commit hook for secret detection:

**Language/Framework:** [type]
**Patterns to detect:**
- AWS credentials
- API keys
- Private keys
- Custom patterns: [list]

**Generate:**
1. Hook script
2. Configuration file
3. Installation instructions
4. Bypass procedure (with audit)
```

### Rotation Lambda

```
Generate AWS Lambda for secret rotation:

**Secret type:** [RDS/DocumentDB/Redshift/Custom]
**Database:** [PostgreSQL/MySQL/etc.]
**Features:**
- Multi-user rotation: [Yes/No]
- Cross-account: [Yes/No]

**Generate:**
1. Lambda function code
2. IAM role/policy
3. Terraform/CloudFormation
4. Testing procedure
5. Monitoring setup
```

---

## Documentation Prompts

### Runbook Generation

```
Generate operational runbook for secrets management:

**Tools:** [list]
**Scenarios to cover:**
- Secret rotation (scheduled/emergency)
- Access provisioning/revocation
- Disaster recovery
- Incident response
- Compliance audit

**Generate:**
1. Runbook document
2. Decision trees
3. Command references
4. Escalation procedures
```

### Developer Guide

```
Generate developer guide for secrets management:

**Audience:** [Backend/Frontend/DevOps/All]
**Tools:** [list]
**Topics:**
- Local development setup
- Secret retrieval patterns
- Testing with secrets
- Security best practices

**Generate:**
1. Getting started guide
2. Code examples
3. FAQ
4. Troubleshooting guide
```

---

*Use these prompts to assist with secrets management tasks. Customize parameters in brackets.*
