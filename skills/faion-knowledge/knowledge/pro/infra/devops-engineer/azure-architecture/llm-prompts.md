# Azure Architecture LLM Prompts

Prompts for AI-assisted Azure architecture design, review, and troubleshooting.

## Table of Contents

1. [Landing Zone Design](#landing-zone-design)
2. [Well-Architected Review](#well-architected-review)
3. [Governance & Policy](#governance--policy)
4. [Security Review](#security-review)
5. [Cost Optimization](#cost-optimization)
6. [Migration Planning](#migration-planning)
7. [Troubleshooting](#troubleshooting)
8. [Code Generation](#code-generation)

---

## Landing Zone Design

### Design New Landing Zone

```
Design an Azure Landing Zone for [ORGANIZATION_NAME] with:

Business Context:
- Industry: [INDUSTRY]
- Size: [EMPLOYEES] employees
- Compliance: [SOC2/ISO27001/GDPR/HIPAA/PCI-DSS]
- Current cloud maturity: [BEGINNER/INTERMEDIATE/ADVANCED]

Requirements:
- Workload types: [WEB APPS/CONTAINERS/DATA/AI-ML/IOT]
- Environments needed: [DEV/STAGING/PROD/DISASTER-RECOVERY]
- Hybrid connectivity: [YES/NO - VPN/ExpressRoute]
- Multi-region: [YES/NO - which regions]

Please provide:
1. Management group hierarchy recommendation
2. Subscription organization strategy
3. Network topology (hub-spoke vs vWAN)
4. Identity and access model
5. Governance baseline (policies, RBAC)
6. Monitoring strategy
7. Cost management approach
8. Implementation phases

Include Terraform module structure and estimated Azure monthly costs.
```

### Evaluate Existing Landing Zone

```
Review this Azure Landing Zone implementation for alignment with Cloud Adoption Framework:

Current State:
- Management Groups: [DESCRIBE HIERARCHY]
- Subscriptions: [COUNT AND ORGANIZATION]
- Network: [TOPOLOGY DESCRIPTION]
- Identity: [CURRENT APPROACH]
- Governance: [POLICIES IN PLACE]

Assess against:
1. ALZ design principles (subscription democratization, policy-driven governance)
2. 8 design areas completeness
3. Security baseline alignment
4. Operational readiness

Provide:
- Gap analysis with severity ratings
- Prioritized remediation roadmap
- Quick wins vs long-term improvements
- Estimated effort for each remediation
```

---

## Well-Architected Review

### Full WAF Assessment

```
Conduct an Azure Well-Architected Framework assessment for [WORKLOAD_NAME]:

Workload Description:
- Type: [WEB APP/API/DATA PIPELINE/ML MODEL/IOT]
- Architecture: [DESCRIBE COMPONENTS]
- Scale: [REQUESTS/DAY, DATA VOLUME]
- SLA requirement: [99.9%/99.95%/99.99%]

For each of the 5 pillars, evaluate:

RELIABILITY:
- Current availability targets
- Failure mode analysis
- Recovery strategies
- Backup and DR approach

SECURITY:
- Identity and access controls
- Network security
- Data protection
- Threat detection

COST OPTIMIZATION:
- Resource sizing
- Reserved capacity usage
- Auto-scaling configuration
- Waste identification

OPERATIONAL EXCELLENCE:
- IaC coverage
- CI/CD maturity
- Monitoring completeness
- Incident response

PERFORMANCE EFFICIENCY:
- Scaling strategy
- Caching implementation
- Database optimization
- Load testing practices

Provide:
- Score for each pillar (1-5)
- Top 3 risks per pillar
- Recommended improvements with priority
- Azure Advisor alignment check
```

### Single Pillar Deep Dive

```
Deep dive into [RELIABILITY/SECURITY/COST/OPERATIONAL EXCELLENCE/PERFORMANCE] for [WORKLOAD]:

Current Implementation:
[DESCRIBE CURRENT STATE]

Analyze:
1. Current maturity level against WAF checklist
2. Gaps vs best practices
3. Specific Azure services/features to implement
4. Configuration recommendations
5. Monitoring and alerting requirements
6. Trade-offs with other pillars

Provide Terraform/Bicep code for:
- Key configurations
- Diagnostic settings
- Alerting rules
```

---

## Governance & Policy

### Design Policy Initiative

```
Design an Azure Policy initiative for [USE CASE]:

Requirements:
- Scope: [MANAGEMENT GROUP/SUBSCRIPTION]
- Compliance framework: [SOC2/ISO27001/CIS/CUSTOM]
- Enforcement: [AUDIT/DENY/DEPLOYIFNOTEXISTS]

Current gaps:
[LIST COMPLIANCE GAPS TO ADDRESS]

Create:
1. Policy definitions (custom if needed)
2. Initiative structure
3. Parameter schema
4. Exemption strategy
5. Remediation approach
6. Compliance reporting

Include:
- Terraform/Bicep code
- Rollout strategy (pilot first)
- Impact assessment
- Monitoring for policy violations
```

### Management Group Hierarchy Design

```
Design a management group hierarchy for:

Organization:
- Structure: [CENTRALIZED/FEDERATED/HYBRID IT]
- Business units: [LIST]
- Regulatory requirements: [LIST]
- Subscription count: [CURRENT AND PROJECTED]

Constraints:
- Max hierarchy depth: 6 (Azure limit)
- Recommended: 3-4 levels

Consider:
1. Policy inheritance requirements
2. RBAC scope requirements
3. Cost management boundaries
4. Audit and compliance needs

Provide:
- Hierarchy diagram (text-based)
- Purpose of each level
- Policy assignment strategy per level
- RBAC assignment strategy per level
- Subscription placement rules
```

### RBAC Model Design

```
Design RBAC model for Azure Landing Zone:

Teams:
- Platform Team: [RESPONSIBILITIES]
- Security Team: [RESPONSIBILITIES]
- Application Teams: [COUNT, RESPONSIBILITIES]
- External Partners: [IF ANY]

Requirements:
- Least privilege principle
- PIM for privileged access
- Emergency access accounts
- CI/CD service principals

Define:
1. Custom roles needed (with definition)
2. Built-in roles to use
3. Role assignment matrix (role x scope x principal)
4. PIM configuration (eligible vs permanent)
5. Access review schedule
6. Break-glass procedure

Include Terraform code for custom roles and key assignments.
```

---

## Security Review

### Security Posture Assessment

```
Assess Azure security posture for [WORKLOAD/SUBSCRIPTION]:

Evaluate against:
1. Microsoft Cloud Security Benchmark
2. CIS Azure Foundations Benchmark
3. Zero Trust principles

Components to review:
- Identity: [CURRENT CONFIG]
- Network: [CURRENT CONFIG]
- Compute: [CURRENT CONFIG]
- Data: [CURRENT CONFIG]

Provide:
- Security score baseline
- Critical vulnerabilities
- High-priority remediations
- Microsoft Defender recommendations
- Network security group analysis
- Key Vault security review
- Encryption status

Include remediation Terraform code for top 5 findings.
```

### Zero Trust Architecture Review

```
Evaluate Zero Trust implementation for [WORKLOAD]:

Current State:
- Identity provider: [ENTRA ID/OTHER]
- Device management: [INTUNE/OTHER]
- Network model: [DESCRIBE]
- Application access: [DESCRIBE]

Zero Trust Principles:
1. Verify explicitly
2. Use least privilege access
3. Assume breach

Assess:
- Identity verification (MFA, Conditional Access)
- Device compliance requirements
- Network micro-segmentation
- Application proxy/ZTNA
- Data classification and protection
- Continuous monitoring

Provide:
- Gap analysis against Zero Trust maturity model
- Implementation roadmap
- Azure services to implement
- Configuration examples
```

---

## Cost Optimization

### Cost Analysis and Optimization

```
Analyze Azure costs and provide optimization recommendations:

Current Spend:
- Monthly cost: $[AMOUNT]
- Top services: [LIST]
- Growth trend: [%/MONTH]

Workload Profile:
- Production workloads: [LIST]
- Dev/Test workloads: [LIST]
- Data storage: [TB]

Analyze:
1. Rightsizing opportunities (VMs, databases)
2. Reserved capacity candidates
3. Savings Plan eligibility
4. Spot instance opportunities
5. Storage tier optimization
6. Idle resource identification
7. Dev/test pricing eligibility

Provide:
- Estimated savings per recommendation
- Implementation priority
- Risk assessment
- Terraform code for auto-shutdown, scaling
```

### FinOps Maturity Assessment

```
Assess FinOps maturity for Azure environment:

Current Practices:
- Cost visibility: [DESCRIBE]
- Budgets: [YES/NO]
- Tagging: [STRATEGY]
- Showback/chargeback: [YES/NO]
- Optimization cadence: [DESCRIBE]

Evaluate against FinOps Framework:
1. Inform (visibility, allocation, benchmarking)
2. Optimize (rates, usage, architecture)
3. Operate (governance, automation, organization)

Provide:
- Current maturity level (Crawl/Walk/Run)
- Gap analysis
- Improvement roadmap
- Azure tools to implement
- KPIs to track
- Governance recommendations
```

---

## Migration Planning

### Migration Assessment

```
Create Azure migration plan for [WORKLOAD]:

Source Environment:
- Platform: [ON-PREM/AWS/GCP/OTHER]
- Components: [LIST WITH SPECS]
- Dependencies: [LIST]
- Data volume: [SIZE]

Requirements:
- Downtime tolerance: [HOURS]
- Compliance: [REQUIREMENTS]
- Timeline: [TARGET DATE]
- Budget: [AMOUNT]

Provide:
1. Azure service mapping (lift-shift vs modernize)
2. Network connectivity approach
3. Data migration strategy
4. Identity integration
5. Testing strategy
6. Cutover plan
7. Rollback procedure

Include:
- Terraform code for target infrastructure
- Azure Migrate setup guidance
- Risk assessment
- Cost comparison (current vs Azure)
```

### Modernization Roadmap

```
Create modernization roadmap for [APPLICATION]:

Current State:
- Architecture: [MONOLITH/N-TIER/MICROSERVICES]
- Technology: [STACK]
- Database: [TYPE, SIZE]
- Hosting: [VM/PaaS]

Target Goals:
- Availability: [TARGET]
- Scalability: [REQUIREMENTS]
- Development velocity: [GOALS]
- Cost: [TARGETS]

Recommend:
1. Containerization approach (AKS vs Container Apps)
2. Database modernization (managed services)
3. PaaS adoption opportunities
4. Serverless candidates
5. API-first redesign areas

Provide:
- Phased roadmap
- Effort estimates per phase
- Risk mitigation strategies
- Architecture diagrams (target state)
```

---

## Troubleshooting

### Connectivity Issues

```
Troubleshoot Azure network connectivity issue:

Symptoms:
- Source: [RESOURCE/LOCATION]
- Destination: [RESOURCE/LOCATION]
- Error: [ERROR MESSAGE]
- Intermittent: [YES/NO]

Current Configuration:
- VNet: [DETAILS]
- NSGs: [RULES]
- UDRs: [ROUTES]
- Firewall: [IF APPLICABLE]
- Private Endpoints: [IF APPLICABLE]

Provide:
1. Diagnostic steps (Azure tools to use)
2. Common causes for this symptom
3. Specific checks for each cause
4. Resolution steps
5. Prevention recommendations

Include Azure CLI/PowerShell commands for diagnostics.
```

### Performance Issues

```
Troubleshoot Azure performance issue:

Symptoms:
- Service: [AKS/APP SERVICE/VM/DATABASE]
- Symptom: [SLOW RESPONSE/TIMEOUTS/HIGH LATENCY]
- When: [ALWAYS/PEAK TIMES/SPECIFIC CONDITIONS]
- Metrics: [CPU/MEMORY/IOPS/NETWORK]

Current Configuration:
- SKU/Size: [DETAILS]
- Scaling: [CONFIGURATION]
- Caching: [IF APPLICABLE]
- Database: [IF APPLICABLE]

Provide:
1. Diagnostic approach
2. Azure Monitor queries (KQL)
3. Common bottlenecks for this service
4. Optimization recommendations
5. Scaling recommendations

Include specific metric thresholds and alerting rules.
```

### AKS Issues

```
Troubleshoot AKS issue:

Symptoms:
- Issue: [POD FAILURES/SCALING/NETWORKING/STORAGE]
- Error: [ERROR MESSAGE/EVENT]
- Scope: [CLUSTER-WIDE/SPECIFIC PODS]

Cluster Configuration:
- Version: [K8S VERSION]
- Network plugin: [AZURE CNI/KUBENET]
- Node pools: [DETAILS]
- Add-ons: [ENABLED ADD-ONS]

Provide:
1. kubectl commands for diagnosis
2. Azure portal/CLI checks
3. Common causes
4. Resolution steps
5. Prevention measures

Include kubectl commands and Azure CLI commands.
```

---

## Code Generation

### Generate Terraform Module

```
Generate Terraform module for [RESOURCE]:

Requirements:
- Resource: [AKS/POSTGRESQL/STORAGE/KEY VAULT/etc.]
- Features: [LIST SPECIFIC FEATURES NEEDED]
- Security: [PRIVATE ENDPOINTS/ENCRYPTION/etc.]
- Compliance: [REQUIREMENTS]

Module should include:
1. main.tf - resource definitions
2. variables.tf - with validation and descriptions
3. outputs.tf - useful outputs
4. versions.tf - provider requirements
5. README.md - usage documentation

Follow:
- Azure naming conventions
- Tagging strategy
- Environment-aware configuration (dev/staging/prod)
- Security best practices (private endpoints, CMK if applicable)
```

### Generate Bicep Template

```
Generate Bicep template for [RESOURCE]:

Requirements:
- Resource: [SPECIFY]
- Parameters: [LIST]
- Conditions: [ENVIRONMENT-BASED LOGIC]

Include:
1. main.bicep - resource definitions
2. Parameter file for each environment
3. What-if validation commands
4. Deployment commands

Follow Azure Verified Modules patterns if applicable.
```

### Generate CI/CD Pipeline

```
Generate GitHub Actions workflow for Azure Terraform deployment:

Requirements:
- Environments: [dev/staging/prod]
- Approval: [REQUIRED FOR PROD]
- State backend: [AZURE STORAGE]
- Authentication: [WORKLOAD IDENTITY/SERVICE PRINCIPAL]

Include:
1. Terraform format/validate
2. Plan with output
3. Manual approval step
4. Apply with backend config
5. Drift detection schedule
6. Cost estimation (if Infracost)

Use OpenID Connect (workload identity) for authentication.
```

---

## Usage Tips

### Context Loading

Always provide these context files when using prompts:

```
/home/faion/.claude/skills/faion-devops-engineer/azure-architecture/README.md
/home/faion/.claude/skills/faion-devops-engineer/azure-architecture/checklist.md
/home/faion/.claude/skills/faion-devops-engineer/azure-architecture/examples.md
```

### Prompt Chaining

For complex projects, chain prompts:

1. Start with Landing Zone Design
2. Follow with Well-Architected Review
3. Add Security Review
4. Finish with Cost Optimization

### Output Formats

Request specific output formats:

- **Terraform**: For infrastructure code
- **Bicep**: For Azure-native IaC
- **Markdown**: For documentation
- **Mermaid**: For diagrams
- **CSV/Table**: For comparison matrices

### Iteration

After initial response, iterate with:

```
Refine the [SECTION] with:
- More detail on [ASPECT]
- Add [MISSING ELEMENT]
- Optimize for [CONSTRAINT]
```
