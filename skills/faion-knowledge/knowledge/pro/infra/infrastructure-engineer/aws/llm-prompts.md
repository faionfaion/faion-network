# AWS LLM Prompts

Prompts for generating AWS infrastructure configurations, troubleshooting, and documentation.

## Infrastructure Generation

### VPC Architecture

```
Generate a three-tier VPC architecture for {project_name} in {region}.

Requirements:
- Environment: {environment} (dev/staging/prod)
- CIDR: {cidr_block}
- Availability Zones: {num_azs}
- Subnet tiers: public, private (application), database
- NAT Gateway: single for dev/staging, per-AZ for prod
- VPC Endpoints: S3, ECR, Secrets Manager
- VPC Flow Logs enabled

Output format: Terraform HCL using terraform-aws-modules/vpc/aws module.
Include all necessary tags for cost allocation and Kubernetes integration.
```

### Security Groups

```
Generate security groups for a three-tier web application on AWS.

Components:
- ALB (internet-facing, HTTPS only)
- Application servers (port {app_port})
- Database ({db_type} on port {db_port})

Requirements:
- Implement least privilege
- Reference security groups by ID (not CIDR where possible)
- Include descriptions for all rules
- Add egress rules explicitly

Output format: Terraform HCL with proper tagging.
```

### IAM Role

```
Generate an IAM role for {service_type} with the following permissions:

Service: {ec2/lambda/ecs_task/eks_pod}
Namespace/Service Account: {namespace}/{service_account} (for IRSA)

Required permissions:
- S3: {s3_actions} on bucket {bucket_name}
- Secrets Manager: read secrets matching pattern {secret_pattern}
- DynamoDB: {dynamodb_actions} on table {table_name}
- CloudWatch: write logs and metrics

Requirements:
- Use least privilege principle
- Scope resources to specific ARNs
- Add conditions where appropriate
- Include permission boundary

Output format: Terraform HCL with separate policy document resource.
```

### Auto Scaling Configuration

```
Generate Auto Scaling configuration for {application_name}.

Requirements:
- Launch template with IMDSv2 required
- Instance type: {instance_type}
- Min/Max/Desired: {min}/{max}/{desired}
- Health check: {ec2/elb}
- Scaling policies: target tracking on CPU ({target_cpu}%)
- Encrypted EBS volumes
- SSM enabled (no SSH keys)
- Spread across {num_azs} Availability Zones

Output format: Terraform HCL with launch template and ASG resources.
```

## Security Analysis

### Security Audit

```
Analyze the following AWS configuration for security issues:

{paste_configuration}

Check for:
1. IAM permissions (least privilege violations)
2. Network exposure (open security groups, public subnets)
3. Encryption (at-rest, in-transit)
4. Logging and monitoring gaps
5. Credential management issues
6. IMDSv1 usage

Provide:
- Severity rating for each issue (Critical/High/Medium/Low)
- Remediation steps
- Terraform code to fix each issue
```

### IAM Policy Review

```
Review this IAM policy for security best practices:

{paste_policy}

Analyze:
1. Overly permissive actions (wildcards)
2. Missing resource constraints
3. Missing conditions
4. Potential privilege escalation paths
5. Cross-account access risks

Provide a revised policy following least privilege principle.
```

### Security Group Audit

```
Audit these security group rules for compliance:

{paste_security_groups}

Check for:
1. SSH/RDP open to 0.0.0.0/0
2. Large port ranges
3. Missing descriptions
4. Overly permissive CIDR blocks
5. Proper egress rules

Provide remediation recommendations and compliant configurations.
```

## Troubleshooting

### Connectivity Issues

```
Debug AWS connectivity issue:

Source: {source_type} in {source_subnet}
Destination: {destination} (service/instance/endpoint)
Error: {error_message}

Provide troubleshooting steps for:
1. Security group rules
2. Network ACLs
3. Route tables
4. VPC endpoints (if applicable)
5. NAT Gateway (if applicable)
6. DNS resolution

Include AWS CLI commands to diagnose each step.
```

### IAM Permission Denied

```
Debug IAM permission denied error:

Service: {service}
Action: {action}
Resource: {resource}
Principal: {role_or_user_arn}
Error: {error_message}

Provide:
1. CLI commands to check current permissions
2. Policy simulator commands
3. Steps to identify missing permission
4. Minimal policy to grant access
```

### EC2 Instance Issues

```
Troubleshoot EC2 instance:

Instance ID: {instance_id}
Issue: {issue_description}
Expected behavior: {expected}
Actual behavior: {actual}

Provide CLI commands to check:
1. Instance status and system checks
2. Security group and network configuration
3. IAM role and instance profile
4. Instance metadata availability
5. CloudWatch metrics and logs
6. Systems Manager connectivity
```

## Cost Optimization

### Cost Analysis

```
Analyze AWS costs for optimization opportunities:

Current setup:
{paste_infrastructure_description}

Monthly cost: ${current_cost}

Provide recommendations for:
1. Right-sizing (EC2, RDS)
2. Reserved Instances / Savings Plans
3. Spot Instance opportunities
4. Storage optimization (S3 lifecycle, EBS types)
5. Network cost reduction (VPC endpoints, CloudFront)
6. Idle resource identification

Include estimated savings for each recommendation.
```

### Reserved Instance Planning

```
Plan Reserved Instances for these workloads:

{paste_ec2_usage_data}

Consider:
1. Standard vs Convertible RIs
2. 1-year vs 3-year terms
3. All Upfront vs Partial vs No Upfront
4. Regional vs Zonal scope

Provide:
- Recommended RI purchases
- Expected savings percentage
- Break-even analysis
- Risk assessment
```

## Documentation Generation

### Architecture Documentation

```
Generate architecture documentation for:

{paste_terraform_or_cloudformation}

Include:
1. Architecture diagram description (for diagram tools)
2. Component descriptions
3. Data flow explanation
4. Security controls
5. High availability design
6. Disaster recovery considerations
7. Cost estimation breakdown

Output format: Markdown suitable for technical documentation.
```

### Runbook Generation

```
Generate operational runbook for:

Service: {service_name}
Environment: {environment}
Infrastructure: {paste_config}

Include procedures for:
1. Deployment steps
2. Scaling (manual and automatic)
3. Health checks and monitoring
4. Common issues and resolutions
5. Incident response
6. Backup and restore
7. Rollback procedures

Output format: Step-by-step runbook with CLI commands.
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
2. Rollback plan
3. Testing plan
4. Implementation steps
5. Verification steps
6. Communication plan
```

## Migration Planning

### Workload Migration

```
Plan migration for workload to AWS:

Source: {on_prem_or_other_cloud}
Workload: {workload_description}
Requirements:
- Compute: {compute_reqs}
- Storage: {storage_reqs}
- Network: {network_reqs}
- Compliance: {compliance_reqs}

Provide:
1. AWS service mapping
2. Migration strategy (rehost/replatform/refactor)
3. Network connectivity plan
4. Data migration approach
5. Testing strategy
6. Cutover plan
7. Cost comparison
```

### Database Migration

```
Plan database migration to AWS:

Source: {source_db_type} version {version}
Size: {db_size}
RPO: {rpo}
RTO: {rto}
Downtime tolerance: {downtime}

Provide:
1. Target service recommendation (RDS/Aurora/DynamoDB)
2. Migration tool selection (DMS, native tools)
3. Pre-migration checklist
4. Migration steps
5. Validation procedures
6. Fallback plan
```

## Compliance

### Compliance Check

```
Verify AWS configuration against {framework} compliance:

Framework: {cis_benchmark/soc2/pci_dss/hipaa}
Scope: {scope_description}
Current config: {paste_config}

Provide:
1. Compliance gaps identified
2. Severity of each gap
3. Remediation steps
4. Terraform/CloudFormation fixes
5. Evidence collection requirements
```

### Audit Preparation

```
Prepare for {audit_type} audit:

Scope: {services_in_scope}
Time period: {audit_period}

Generate:
1. Evidence collection checklist
2. CLI commands to gather evidence
3. Documentation requirements
4. Common findings to address proactively
5. Remediation timeline recommendations
```

## Sources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Cost Optimization](https://aws.amazon.com/aws-cost-management/)
- [AWS Migration Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-migration-whitepaper/welcome.html)
