# GCP Architecture Basics LLM Prompts

## Resource Hierarchy Design

### Design Organization Structure

```
Design a GCP resource hierarchy for [ORGANIZATION DESCRIPTION]:

Organization Context:
- Company size: [startup/SMB/enterprise]
- Teams: [list teams/departments]
- Environments: [dev/staging/prod/sandbox]
- Compliance requirements: [GDPR/HIPAA/SOC2/none]
- Multi-region: [yes/no, which regions]

Requirements:
1. Design folder structure reflecting organizational boundaries
2. Propose naming conventions for projects
3. Identify shared services projects needed
4. Define IAM inheritance strategy
5. Recommend organization policies

Deliverables:
- Visual hierarchy diagram (text-based)
- Folder and project naming conventions
- IAM role recommendations per level
- Organization policies to enforce
```

### Migrate to Organization

```
Help migrate from standalone GCP projects to organization structure:

Current State:
- Projects: [list existing projects]
- Billing accounts: [number and purpose]
- Current IAM: [describe current access model]

Target State:
- Organization domain: [domain.com]
- Desired folder structure: [describe]
- Environment separation: [requirements]

Requirements:
1. Migration path from standalone to org
2. Project migration order and dependencies
3. IAM migration strategy
4. Billing account consolidation
5. Minimal disruption approach
```

## IAM Design

### Design IAM Strategy

```
Design IAM strategy for GCP [PROJECT/ORGANIZATION]:

Context:
- Team structure: [describe teams and roles]
- Access requirements: [who needs what access]
- Compliance: [any regulatory requirements]
- Service accounts: [workloads needing identity]

Requirements:
1. Define role assignments per team
2. Design service account strategy
3. Implement least privilege
4. Set up Workload Identity for GKE
5. Define break-glass access procedures

Constraints:
- No basic roles (Owner/Editor/Viewer) in production
- No service account keys
- All access auditable
```

### Audit IAM Permissions

```
Audit and remediate IAM permissions for [PROJECT_ID]:

Current Concerns:
- [List known issues or areas of concern]

Audit Requirements:
1. Identify overly permissive roles
2. Find unused service accounts
3. Check for external access grants
4. Verify service account key usage
5. Review conditional access policies

Output:
- List of findings with severity
- Remediation recommendations
- Terraform changes if applicable
- Timeline for implementation
```

### Design Workload Identity

```
Design Workload Identity setup for GKE:

Workloads:
- [List workloads and their GCP API needs]

GKE Context:
- Cluster: [cluster name/project]
- Namespaces: [list namespaces]
- Kubernetes Service Accounts: [list KSAs]

Requirements:
1. Map workloads to GSA permissions
2. Create GSA per workload or shared
3. Bind KSA to GSA
4. Annotate KSA for Workload Identity
5. Test access patterns
```

## Project Organization

### Design Project Structure

```
Design project structure for [APPLICATION/PLATFORM]:

Application Context:
- Type: [web app/data platform/ML/microservices]
- Components: [list major components]
- Data sensitivity: [public/internal/confidential]
- Traffic patterns: [describe load]

Environment Requirements:
- Development: [requirements]
- Staging: [requirements]
- Production: [requirements]

Design Requirements:
1. Project per environment vs shared
2. API enablement per project
3. Network connectivity between projects
4. Shared resources strategy
5. Cost attribution approach
```

### Review Project Setup

```
Review GCP project [PROJECT_ID] configuration:

Check Areas:
1. APIs enabled (minimal required)
2. Default service account status
3. IAM bindings (least privilege)
4. Labels attached
5. Billing account linked
6. Network configuration
7. Logging and monitoring setup

Output:
- Compliance score
- Issues found with severity
- Remediation steps
- Terraform code to fix issues
```

## Billing and Cost Management

### Design Cost Management Strategy

```
Design cost management strategy for GCP [ORGANIZATION/PROJECT]:

Context:
- Monthly budget: [amount]
- Teams/cost centers: [list]
- Chargeback requirements: [describe]
- Existing spending: [current patterns]

Requirements:
1. Budget alert configuration
2. Cost allocation via labels
3. BigQuery billing export setup
4. Looker Studio dashboard
5. Committed use discount analysis
6. Rightsizing recommendations

Deliverables:
- Budget configuration per project
- Label taxonomy for cost allocation
- Dashboard queries
- Cost optimization checklist
```

### Optimize GCP Costs

```
Analyze and optimize GCP costs for [PROJECT/ORGANIZATION]:

Current Spending:
- Monthly cost: [amount]
- Top services: [list]
- Growth trend: [describe]

Optimization Areas:
1. Idle resources identification
2. Rightsizing opportunities
3. Committed use discounts
4. Preemptible/Spot VM opportunities
5. Storage class optimization
6. Network egress reduction

Output:
- Potential savings by category
- Implementation steps
- Risk assessment
- Monitoring setup post-optimization
```

## Organization Policies

### Design Organization Policies

```
Design organization policies for [ORGANIZATION]:

Security Requirements:
- [List security requirements]

Compliance Requirements:
- [List compliance frameworks]

Policy Areas:
1. Resource location restrictions
2. External access prevention
3. Service account constraints
4. Network security policies
5. Encryption requirements

Deliverables:
- Policy list with rationale
- Terraform implementation
- Exception handling process
- Monitoring and alerting
```

### Implement Security Baseline

```
Implement GCP security baseline for [PROJECT/ORGANIZATION]:

Security Level: [basic/standard/high]

Baseline Components:
1. Organization policies
2. VPC Service Controls (if high)
3. Audit logging configuration
4. Security Command Center
5. IAM recommendations
6. Network security

Context:
- Existing security tools: [list]
- Compliance requirements: [list]
- Team security expertise: [basic/intermediate/advanced]

Output:
- Prioritized implementation plan
- Terraform modules
- Validation checklist
- Ongoing monitoring setup
```

## Troubleshooting

### Debug IAM Permission Denied

```
Debug IAM "Permission Denied" error:

Error Details:
- Error message: [exact error]
- User/SA: [identity trying to access]
- Resource: [resource being accessed]
- Operation: [what they're trying to do]

Investigation Steps:
1. Identify required permission
2. Check effective IAM policy
3. Verify resource hierarchy inheritance
4. Check organization policies
5. Verify service account status
6. Check VPC Service Controls

Provide:
- Root cause identification
- Fix recommendation
- Prevention measures
```

### Audit Resource Hierarchy

```
Audit GCP resource hierarchy for [ORGANIZATION]:

Audit Areas:
1. Folder depth and complexity
2. Naming consistency
3. IAM policy inheritance issues
4. Organization policy gaps
5. Orphaned projects
6. Billing account assignments

Output:
- Current state assessment
- Issues by severity
- Remediation recommendations
- Migration plan if restructuring needed
```

## Multi-Project Architecture

### Design Multi-Project Architecture

```
Design multi-project architecture for [PLATFORM]:

Platform Requirements:
- Workloads: [describe workloads]
- Data sharing: [requirements]
- Network connectivity: [requirements]
- Security boundaries: [requirements]

Architecture Patterns:
1. Hub-and-spoke networking
2. Shared VPC vs VPC peering
3. Shared services model
4. Data project isolation
5. Cross-project IAM

Output:
- Project structure diagram
- Network architecture
- IAM strategy
- Terraform module structure
```

### Design Landing Zone

```
Design GCP landing zone for [ORGANIZATION]:

Organization Context:
- Size: [number of teams/projects expected]
- Existing cloud: [AWS/Azure migration or greenfield]
- Governance model: [centralized/federated]

Landing Zone Components:
1. Resource hierarchy
2. Identity and access management
3. Networking architecture
4. Security baseline
5. Logging and monitoring
6. Billing and cost management
7. CI/CD for infrastructure

Deliverables:
- Architecture documentation
- Terraform modules
- Deployment pipeline
- Operations runbook
```

---

*GCP Architecture Basics LLM Prompts | faion-infrastructure-engineer*
