# AWS Architecture Foundations Checklist

## Multi-Account Setup

### AWS Organizations

- [ ] Create dedicated management account (no workloads)
- [ ] Enable AWS Organizations with all features
- [ ] Enable root access management for member accounts
- [ ] Set up organization-wide CloudTrail
- [ ] Enable AWS Config across all accounts
- [ ] Configure consolidated billing

### OU Structure

- [ ] Create Security OU with log archive account
- [ ] Create Infrastructure OU for shared services
- [ ] Create Workloads OU with Prod/Non-Prod separation
- [ ] Create Sandbox OU for developer experimentation
- [ ] Create Suspended OU for decommissioned accounts
- [ ] Create Policy Staging OU for SCP testing

### AWS Control Tower

- [ ] Deploy Control Tower in management account
- [ ] Configure IAM Identity Center as identity source
- [ ] Enable mandatory guardrails
- [ ] Enable recommended guardrails for production OUs
- [ ] Set up Account Factory for provisioning
- [ ] Configure notification settings

## Well-Architected Review

### Operational Excellence

- [ ] Infrastructure as Code (Terraform/CloudFormation)
- [ ] Automated deployments via CI/CD
- [ ] Runbooks for common operations
- [ ] Incident response procedures documented
- [ ] Post-incident review process
- [ ] Change management process

### Security

- [ ] IAM Identity Center configured
- [ ] MFA required for all users
- [ ] Root account MFA enabled
- [ ] Root access disabled for member accounts
- [ ] SCPs enforcing security baseline
- [ ] GuardDuty enabled organization-wide
- [ ] Security Hub aggregating findings
- [ ] WAF protecting public endpoints

### Reliability

- [ ] Multi-AZ deployment (minimum 3 AZs)
- [ ] Auto Scaling configured
- [ ] Health checks implemented
- [ ] Backup strategy defined
- [ ] Disaster recovery plan documented
- [ ] RTO/RPO defined for each workload

### Performance Efficiency

- [ ] Instance types right-sized
- [ ] CloudFront for static content
- [ ] ElastiCache for database queries
- [ ] Read replicas for read-heavy workloads
- [ ] Performance testing baseline established

### Cost Optimization

- [ ] Cost allocation tags defined
- [ ] Savings Plans evaluated
- [ ] Reserved Instances for baseline
- [ ] Spot Instances for fault-tolerant workloads
- [ ] S3 lifecycle policies configured
- [ ] Unused resources identified and removed
- [ ] Cost budgets and alerts configured

### Sustainability

- [ ] Right-sized resources (no over-provisioning)
- [ ] Auto Scaling for demand matching
- [ ] Managed services preferred
- [ ] Energy-efficient regions considered

## VPC Design

### Network Architecture

- [ ] CIDR block sized for growth (minimum /16)
- [ ] 3 AZs configured
- [ ] Public subnets for load balancers
- [ ] Private subnets for applications
- [ ] Database subnets isolated
- [ ] Subnet tags for EKS if applicable

### Connectivity

- [ ] NAT Gateway per AZ (production)
- [ ] Internet Gateway for public access
- [ ] VPC Endpoints for AWS services (S3, ECR, etc.)
- [ ] Transit Gateway for multi-VPC (if applicable)
- [ ] VPN or Direct Connect (if hybrid)

### Security

- [ ] VPC Flow Logs to CloudWatch/S3
- [ ] Default security group locked down
- [ ] Network ACLs for defense in depth
- [ ] DNS hostnames and support enabled

## IAM Configuration

### Identity Management

- [ ] IAM Identity Center as primary access
- [ ] External IdP integration (if applicable)
- [ ] Permission sets for common roles
- [ ] Account assignment policies
- [ ] Temporary credentials only

### Policies

- [ ] Custom policies use least privilege
- [ ] No `*` in resource ARNs
- [ ] Condition keys for extra restrictions
- [ ] Service-linked roles used where available
- [ ] Policy size optimized (avoid duplication)

### EKS Pod Identity (IRSA)

- [ ] OIDC provider configured for cluster
- [ ] Service accounts with IAM role annotations
- [ ] Policies scoped to specific resources
- [ ] No instance profile for pod access

## Monitoring and Observability

### CloudWatch

- [ ] Log groups with retention policies
- [ ] Custom metrics for application KPIs
- [ ] Dashboards for each environment
- [ ] Alarms for critical metrics
- [ ] SNS topics for notifications

### Tracing and Auditing

- [ ] X-Ray enabled for distributed tracing
- [ ] CloudTrail organization trail
- [ ] CloudTrail log file validation
- [ ] CloudTrail logs encrypted with KMS

### Compliance

- [ ] AWS Config rules for compliance
- [ ] Security Hub standards enabled
- [ ] Automated remediation where possible
- [ ] Regular Well-Architected reviews scheduled

## Encryption

### Data at Rest

- [ ] S3 default encryption enabled
- [ ] EBS encryption by default
- [ ] RDS encryption enabled
- [ ] Customer-managed KMS keys for sensitive data
- [ ] Key rotation enabled

### Data in Transit

- [ ] TLS 1.2 minimum enforced
- [ ] ACM certificates for public endpoints
- [ ] VPC endpoints for AWS service traffic
- [ ] Database connections over TLS

### Secrets Management

- [ ] Secrets Manager for credentials
- [ ] Automatic rotation configured
- [ ] No secrets in code or environment variables
- [ ] Parameter Store for non-sensitive config

## Disaster Recovery

### Backup Strategy

- [ ] AWS Backup configured
- [ ] Cross-region replication for critical data
- [ ] RDS automated backups enabled
- [ ] S3 versioning for important buckets
- [ ] Backup testing schedule

### Recovery

- [ ] Recovery runbooks documented
- [ ] Pilot light or warm standby (if required)
- [ ] DNS failover configured
- [ ] Recovery testing schedule
