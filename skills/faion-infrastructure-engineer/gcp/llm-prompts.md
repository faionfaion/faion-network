# GCP LLM Prompts

Prompts for generating GCP infrastructure configurations, troubleshooting, and documentation.

## Infrastructure Generation

### VPC Architecture

```
Generate a production-ready VPC architecture for {project_name} in {region}.

Requirements:
- Environment: {environment} (dev/staging/prod)
- Subnet tiers: public, private (application), GKE, database
- Private Google Access enabled
- Cloud NAT for outbound internet
- VPC Flow Logs enabled
- Secondary ranges for GKE pods and services

Output format: Terraform HCL.
Include:
- Custom VPC (no default)
- Subnets with appropriate CIDR ranges
- Cloud Router and NAT
- Flow log configuration
- Proper labels and naming
```

### Firewall Rules

```
Generate firewall rules for a three-tier web application on GCP.

Components:
- Global HTTPS Load Balancer
- Application tier (Cloud Run / GKE / Compute Engine on port {app_port})
- Cloud SQL PostgreSQL (port 5432)

Requirements:
- Deny-all default rule
- Allow IAP for SSH (no direct SSH)
- Allow health checks from GCP LB ranges
- Allow app to database only
- Include rule descriptions
- Use network tags

Output format: Terraform HCL or gcloud commands.
```

### Service Account (Least Privilege)

```
Generate a service account configuration for {workload_type} with minimal permissions.

Workload: {cloud_run/gke_pod/compute_engine/cloud_function}
Project: {project_id}

Required permissions:
- Cloud SQL: {client/admin} access
- Secret Manager: read secrets matching pattern {pattern}
- Cloud Storage: {read/write} bucket {bucket_name}
- Pub/Sub: {publish/subscribe} to topic {topic_name}
- Logging: write logs

Requirements:
- Use predefined roles where possible
- Create custom role only if needed
- Include Workload Identity binding for GKE
- No service account keys

Output format: Terraform HCL with separate modules for SA and IAM bindings.
```

### Cloud Run Service

```
Generate a Cloud Run service configuration for {application_name}.

Requirements:
- Image: {image_url}
- Region: {region}
- Minimum instances: {min} (0 for dev, 1+ for prod)
- Maximum instances: {max}
- Memory: {memory}
- CPU: {cpu}
- Concurrency: {concurrency}
- VPC connector for private resources
- Secrets from Secret Manager
- Health check endpoint: {health_path}
- Authentication: {authenticated/public}

Output format: Terraform HCL using google_cloud_run_v2_service.
Include startup and liveness probes.
```

### GKE Cluster

```
Generate a GKE cluster configuration for {project_name}.

Mode: {autopilot/standard}
Environment: {environment}

Requirements:
- Private cluster (no public endpoint for prod)
- Workload Identity enabled
- Network policy enabled
- Release channel: {rapid/regular/stable}
- Region: {region}
- Master authorized networks: {cidr_list}
- Logging: SYSTEM_COMPONENTS, WORKLOADS
- Monitoring: SYSTEM_COMPONENTS with managed Prometheus

For Standard mode also include:
- Node pool configuration
- Autoscaling settings
- Shielded nodes
- Dataplane V2

Output format: Terraform HCL.
```

## Security Analysis

### Security Audit

```
Analyze the following GCP configuration for security issues:

{paste_configuration}

Check for:
1. IAM permissions (overly permissive roles, primitive roles)
2. Network exposure (public IPs, open firewall rules)
3. Missing VPC Service Controls
4. Service account key usage (should be Workload Identity)
5. Encryption settings (CMEK vs Google-managed)
6. Logging and audit gaps
7. Missing Cloud Armor protection

Provide:
- Severity rating for each issue (Critical/High/Medium/Low)
- Remediation steps with specific commands
- Terraform code to fix each issue
```

### IAM Policy Review

```
Review this IAM configuration for security best practices:

{paste_iam_policy}

Analyze:
1. Use of primitive roles (Owner/Editor/Viewer)
2. Overly broad permissions
3. Service account key exposure risks
4. Missing IAM conditions
5. Cross-project access risks
6. Workload Identity usage

Provide:
- Security findings
- Recommended role replacements
- IAM Recommender query to find unused permissions
```

### VPC-SC Configuration Review

```
Review VPC Service Controls configuration:

{paste_vpc_sc_config}

Check for:
1. Correct service perimeter boundaries
2. Ingress/egress rules necessity
3. Access levels configuration
4. Dry-run mode status
5. Audit logging configuration
6. Integration with other security controls

Provide:
- Configuration gaps
- Recommendations for tightening controls
- Testing approach before enforcement
```

## Troubleshooting

### Connectivity Issues

```
Debug GCP connectivity issue:

Source: {source_type} in {source_subnet/project}
Destination: {destination} (Cloud SQL/external API/other service)
Error: {error_message}

Provide troubleshooting steps for:
1. Firewall rules
2. VPC routing
3. Cloud NAT configuration
4. Private Google Access
5. VPC Service Controls perimeters
6. DNS resolution
7. Service account permissions

Include gcloud commands to diagnose each step.
```

### IAM Permission Denied

```
Debug IAM permission denied error:

Service: {gcp_service}
Action: {api_method}
Resource: {resource_name}
Principal: {service_account_or_user}
Error: {error_message}

Provide:
1. Commands to check current permissions
2. Policy troubleshooter usage
3. Audit log query for denied requests
4. Minimal permission grant command
5. Alternative approaches (resource-level vs project-level)
```

### Cloud Run Issues

```
Troubleshoot Cloud Run service:

Service: {service_name}
Region: {region}
Issue: {issue_description}

Symptoms:
- {symptom_1}
- {symptom_2}

Provide diagnostic steps for:
1. Service deployment status
2. Container logs
3. Health check status
4. VPC connector connectivity
5. Secret Manager access
6. Service account permissions
7. Concurrency/scaling issues

Include gcloud commands and log queries.
```

### GKE Pod Issues

```
Troubleshoot GKE pod:

Cluster: {cluster_name}
Namespace: {namespace}
Pod: {pod_name}
Issue: {issue_description}

Check:
1. Pod status and events
2. Container logs
3. Workload Identity configuration
4. Network policies
5. Resource limits
6. Secret/ConfigMap mounts
7. Service account annotation

Provide kubectl and gcloud commands for diagnosis.
```

## Cost Optimization

### Cost Analysis

```
Analyze GCP costs for optimization opportunities:

Current setup:
{paste_infrastructure_description}

Monthly cost: ${current_cost}

Provide recommendations for:
1. Right-sizing (Compute Engine, Cloud SQL, GKE)
2. Committed use discounts
3. Preemptible/Spot VM opportunities
4. Cloud Run minimum instances tuning
5. Storage lifecycle policies
6. Network egress optimization (Private Google Access, VPC endpoints)
7. Unused resource identification

Include:
- Recommender API queries
- BigQuery billing analysis queries
- Estimated savings per recommendation
```

### Committed Use Analysis

```
Plan committed use discounts for these workloads:

{paste_resource_usage_data}

Consider:
1. Spend-based vs resource-based commitments
2. 1-year vs 3-year terms
3. Flexible vs standard CUDs
4. Regional vs global scope

Provide:
- Recommended CUD purchases
- Expected savings percentage
- Break-even analysis
- Risk assessment
```

## Documentation Generation

### Architecture Documentation

```
Generate architecture documentation for:

{paste_terraform_or_gcloud_commands}

Include:
1. Architecture overview
2. Component descriptions
3. Network diagram description (for diagram tools)
4. Data flow explanation
5. Security controls summary
6. High availability design
7. Disaster recovery approach
8. Cost estimation breakdown

Output format: Markdown suitable for technical documentation.
```

### Runbook Generation

```
Generate operational runbook for:

Service: {service_name}
Environment: {environment}
Infrastructure: {paste_config}

Include procedures for:
1. Deployment (gcloud/kubectl commands)
2. Scaling (manual and automatic)
3. Health check verification
4. Common issues and resolutions
5. Incident response
6. Backup and restore
7. Rollback procedures
8. Monitoring and alerting

Output format: Step-by-step runbook with commands.
```

### Change Request

```
Generate change request documentation for:

Change: {change_description}
Reason: {business_reason}
Current state: {current_config}
Target state: {target_config}

Include:
1. Risk assessment
2. Rollback plan (with specific commands)
3. Testing plan
4. Implementation steps
5. Verification steps
6. VPC-SC dry-run results (if applicable)
7. Communication plan
```

## Migration Planning

### Workload Migration to GCP

```
Plan migration for workload to GCP:

Source: {on_prem_or_other_cloud}
Workload: {workload_description}
Requirements:
- Compute: {compute_reqs}
- Storage: {storage_reqs}
- Database: {database_reqs}
- Networking: {network_reqs}
- Compliance: {compliance_reqs}

Provide:
1. GCP service mapping
2. Migration strategy (lift-and-shift/replatform/refactor)
3. Network connectivity plan (Interconnect/VPN)
4. Data migration approach
5. Identity federation setup
6. Testing strategy
7. Cutover plan
8. Cost comparison
```

### Database Migration

```
Plan database migration to GCP:

Source: {source_db_type} version {version}
Size: {db_size}
RPO: {rpo}
RTO: {rto}
Downtime tolerance: {downtime}

Provide:
1. Target service recommendation (Cloud SQL/AlloyDB/Spanner)
2. Migration tool selection (Database Migration Service, native tools)
3. Pre-migration checklist
4. Migration steps
5. Validation procedures
6. Fallback plan
7. Post-migration optimization
```

## Compliance

### Compliance Check

```
Verify GCP configuration against {framework} compliance:

Framework: {cis_benchmark/soc2/pci_dss/hipaa}
Scope: {scope_description}
Current config: {paste_config}

Provide:
1. Compliance gaps identified
2. Severity of each gap
3. Remediation steps
4. Terraform/gcloud fixes
5. Evidence collection requirements
6. Security Command Center findings to enable
```

### Audit Preparation

```
Prepare for {audit_type} audit:

Scope: {services_in_scope}
Time period: {audit_period}

Generate:
1. Evidence collection checklist
2. gcloud commands to gather evidence
3. Cloud Asset Inventory queries
4. Audit log export configuration
5. Common findings to address proactively
6. Remediation timeline recommendations
```

## Quick Task Prompts

### Generate Secret Manager Configuration

```
Create Secret Manager configuration for:

Application: {app_name}
Secrets needed: {list_secrets}
Replication: {automatic/user_managed}
Rotation: {required/not_required}

Include:
- Secret creation commands
- IAM bindings for service accounts
- Cloud Run/GKE integration examples
```

### Create Health Check Configuration

```
Create health check configuration for:

Service: {cloud_run/gke/compute_engine}
Health endpoint: {path}
Port: {port}
Expected response: {status_code}
Startup time: {approximate}

Include:
- Health check resource (Terraform/gcloud)
- Load balancer integration
- Alerting configuration
```

### Generate VPC Connector

```
Create VPC connector for Cloud Run/Cloud Functions:

Region: {region}
VPC: {vpc_name}
CIDR: {connector_cidr}
Min/Max instances: {min}/{max}

Include:
- Connector creation
- Cloud Run service update
- Firewall rules for connector traffic
```

## Prompt Template Variables

Use these placeholders in prompts:

| Variable | Description |
|----------|-------------|
| `{project_id}` | GCP project ID |
| `{region}` | GCP region (us-central1, etc.) |
| `{environment}` | dev, staging, prod |
| `{service_name}` | Cloud Run/GKE service name |
| `{image_url}` | Container image URL |
| `{cidr}` | IP CIDR range |
| `{port}` | Port number |
| `{error_message}` | Error text |
| `{workload_type}` | cloud_run, gke_pod, compute_engine |

## Sources

- [GCP Architecture Framework](https://cloud.google.com/architecture/framework)
- [GCP Security Best Practices](https://cloud.google.com/docs/enterprise/best-practices-for-enterprise-organizations)
- [Cloud Run Best Practices](https://cloud.google.com/run/docs/best-practices)
- [GKE Best Practices](https://cloud.google.com/kubernetes-engine/docs/best-practices)
- [VPC Service Controls](https://cloud.google.com/vpc-service-controls/docs/overview)

---

*GCP LLM Prompts | faion-infrastructure-engineer*
