# GCP Architecture Basics Checklist

## Organization Setup

- [ ] Organization resource created (via Cloud Identity or Workspace)
- [ ] Organization Admin role assigned to designated admins
- [ ] Organization policies configured (constraints)
- [ ] Billing Account linked to organization
- [ ] Audit logging enabled at org level

## Resource Hierarchy Design

- [ ] Folder structure reflects organizational boundaries
- [ ] Environment separation: dev/staging/prod folders
- [ ] Shared services folder for common resources
- [ ] Bootstrap folder for IaC and automation
- [ ] Hierarchy kept flat (minimize nesting depth)

## Project Configuration

- [ ] Standardized naming convention applied
- [ ] Project ID follows naming standards
- [ ] Required labels attached (env, team, cost-center)
- [ ] Only necessary APIs enabled
- [ ] Default service account reviewed/disabled
- [ ] Project linked to correct billing account

## IAM Configuration

### Principles
- [ ] Basic roles (Owner/Editor/Viewer) avoided in production
- [ ] Predefined roles used over custom when possible
- [ ] Least privilege principle enforced
- [ ] No service account keys in use (Workload Identity instead)

### Organization Level
- [ ] Organization Admin limited to break-glass access
- [ ] Billing Admin role assigned appropriately
- [ ] Security Admin role assigned to security team
- [ ] Audit Viewer role assigned for compliance

### Folder Level
- [ ] Folder IAM reflects team/department boundaries
- [ ] Environment-specific folders have appropriate access
- [ ] Shared services folder has limited write access

### Project Level
- [ ] Project IAM follows least privilege
- [ ] Service accounts have minimal required roles
- [ ] IAM conditions used where applicable
- [ ] No allUsers or allAuthenticatedUsers grants

## Service Accounts

- [ ] Dedicated service accounts per workload
- [ ] No default service account usage
- [ ] Workload Identity configured for GKE
- [ ] Service account key rotation (if keys unavoidable)
- [ ] Service account impersonation over keys
- [ ] Activity logging for service accounts

## Billing and Cost Management

- [ ] Billing account configured with alerts
- [ ] Budget alerts set at multiple thresholds (50%, 90%, 100%)
- [ ] Billing exports to BigQuery enabled
- [ ] Cost allocation labels defined and enforced
- [ ] Committed use discounts evaluated
- [ ] Billing reports configured by folder/project

## Security Foundations

- [ ] VPC Service Controls evaluated
- [ ] Organization policies for security constraints
- [ ] Cloud Audit Logs enabled
- [ ] Access Transparency enabled (if applicable)
- [ ] Security Command Center enabled
- [ ] Cloud Asset Inventory configured

## Networking Foundations

- [ ] Custom VPC created (not default)
- [ ] Private Google Access enabled
- [ ] Cloud NAT for private resources
- [ ] Firewall rules follow least privilege
- [ ] VPC Flow Logs enabled

## Monitoring and Logging

- [ ] Cloud Monitoring workspace created
- [ ] Logging sinks configured for retention
- [ ] Alert policies for critical metrics
- [ ] Uptime checks for public endpoints
- [ ] Log-based metrics for key events

## Common Mistakes to Avoid

| Mistake | Risk | Solution |
|---------|------|----------|
| Basic roles in production | Over-permissioning | Use predefined/custom roles |
| Service account keys | Key exposure | Use Workload Identity |
| Mixed environments in project | Accidental changes | Separate dev/staging/prod |
| No resource labels | Cost tracking gaps | Enforce labels via org policy |
| Default VPC usage | Security gaps | Create custom VPCs |
| Deeply nested hierarchy | Policy complexity | Keep hierarchy flat |

## Verification Commands

```bash
# List organization
gcloud organizations list

# List folders in organization
gcloud resource-manager folders list --organization=ORG_ID

# List projects in folder
gcloud projects list --filter="parent.id=FOLDER_ID"

# Check IAM policy on project
gcloud projects get-iam-policy PROJECT_ID

# List enabled APIs
gcloud services list --enabled --project=PROJECT_ID

# Check billing account
gcloud billing projects describe PROJECT_ID
```

---

*GCP Architecture Basics Checklist | faion-infrastructure-engineer*
