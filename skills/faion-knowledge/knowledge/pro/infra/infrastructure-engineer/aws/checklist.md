# AWS Checklists

Security, operational, and infrastructure checklists for AWS deployments.

## Security Checklist

### IAM Security

- [ ] Use IAM Identity Center for human users (SSO)
- [ ] Use IAM roles for workloads (not access keys)
- [ ] Implement least privilege permissions
- [ ] Enable MFA for all human users
- [ ] Enable MFA for privileged operations
- [ ] Use IAM Access Analyzer to identify unused permissions
- [ ] Rotate access keys regularly (if used)
- [ ] No root user access for daily operations
- [ ] Review IAM policies quarterly
- [ ] Use resource-based policies where appropriate
- [ ] Implement permission boundaries for delegated administration
- [ ] Use ABAC (attribute-based access control) for scalable permissions

### Network Security

- [ ] Run workloads in private subnets
- [ ] Use security groups with least privilege rules
- [ ] Restrict SSH/RDP to specific IP ranges (never 0.0.0.0/0)
- [ ] Use Network ACLs for additional subnet-level protection
- [ ] Enable VPC Flow Logs for traffic monitoring
- [ ] Use VPC endpoints for AWS service access (PrivateLink)
- [ ] Implement Transit Gateway for multi-VPC connectivity
- [ ] Use WAF for web application protection
- [ ] Configure Route 53 DNS firewall
- [ ] Use CloudFront with origin access identity

### EC2 Security

- [ ] Use IMDSv2 (Instance Metadata Service v2)
- [ ] Disable IMDSv1 on all instances
- [ ] Use Systems Manager Session Manager instead of SSH
- [ ] Install and configure Amazon Inspector
- [ ] Enable EBS encryption by default
- [ ] Use encrypted AMIs
- [ ] Implement security groups per role (web, app, db)
- [ ] Regular patching via Systems Manager Patch Manager
- [ ] Use dedicated tenancy for sensitive workloads
- [ ] Enable termination protection for production instances

### Data Security

- [ ] Enable encryption at rest (EBS, S3, RDS, EFS)
- [ ] Use TLS/HTTPS for data in transit
- [ ] Use customer-managed KMS keys for sensitive data
- [ ] Enable S3 bucket versioning
- [ ] Block public access on S3 buckets
- [ ] Use Secrets Manager for credentials (not hardcoded)
- [ ] Enable RDS encryption
- [ ] Configure S3 Object Lock for compliance
- [ ] Use Certificate Manager for TLS certificates

### Monitoring & Auditing

- [ ] Enable CloudTrail in all regions
- [ ] Enable CloudTrail log file validation
- [ ] Store CloudTrail logs in separate account (audit)
- [ ] Enable Config rules for compliance
- [ ] Enable GuardDuty for threat detection
- [ ] Enable Security Hub for centralized findings
- [ ] Set up CloudWatch Alarms for security events
- [ ] Enable access logging for S3 buckets
- [ ] Enable ELB access logging
- [ ] Configure SNS notifications for security alerts

## Operational Checklist

### High Availability

- [ ] Deploy across minimum 3 Availability Zones
- [ ] Use Auto Scaling groups for EC2 workloads
- [ ] Configure health checks for load balancers
- [ ] Enable Multi-AZ for RDS databases
- [ ] Use Aurora Global Database for critical workloads
- [ ] Configure Route 53 health checks and failover
- [ ] Implement cross-region replication for S3
- [ ] Test failover procedures regularly
- [ ] Document recovery procedures (runbooks)

### Backup & Recovery

- [ ] Enable AWS Backup for centralized backup management
- [ ] Configure backup retention policies
- [ ] Enable cross-region backup replication
- [ ] Test backup restoration regularly
- [ ] Use S3 Cross-Region Replication for critical data
- [ ] Configure RDS automated backups
- [ ] Create AMIs before major changes
- [ ] Document RPO and RTO requirements
- [ ] Use logically air-gapped vaults for critical backups

### Monitoring & Observability

- [ ] Enable Container Insights for EKS/ECS
- [ ] Create centralized CloudWatch dashboards
- [ ] Configure CloudWatch alarms for key metrics
- [ ] Enable X-Ray for distributed tracing
- [ ] Set up log retention policies
- [ ] Configure metric filters for error detection
- [ ] Enable enhanced monitoring for RDS
- [ ] Use Contributor Insights for top-N analysis
- [ ] Implement custom metrics for business KPIs

### Cost Management

- [ ] Enable Cost Explorer and set budgets
- [ ] Review Reserved Instance utilization
- [ ] Configure Savings Plans for predictable workloads
- [ ] Use Spot Instances for fault-tolerant workloads
- [ ] Enable Compute Optimizer recommendations
- [ ] Configure S3 lifecycle policies
- [ ] Delete unused EBS snapshots
- [ ] Right-size EC2 instances
- [ ] Use CloudFront to reduce data transfer costs
- [ ] Use VPC endpoints to avoid NAT gateway charges

## Infrastructure Setup Checklist

### Account Setup

- [ ] Enable Organizations for multi-account management
- [ ] Create separate accounts (dev, staging, prod, security)
- [ ] Enable SCPs (Service Control Policies)
- [ ] Configure consolidated billing
- [ ] Enable AWS SSO / Identity Center
- [ ] Set up cross-account access roles
- [ ] Enable Cost Allocation Tags

### VPC Setup

- [ ] Plan IP address ranges (avoid overlaps)
- [ ] Create VPCs with appropriate CIDR blocks
- [ ] Create public, private, and database subnets
- [ ] Deploy NAT Gateways (one per AZ in production)
- [ ] Configure route tables for each subnet tier
- [ ] Enable DNS hostnames and DNS resolution
- [ ] Create Transit Gateway for multi-VPC connectivity
- [ ] Configure VPC endpoints for AWS services
- [ ] Enable VPC Flow Logs
- [ ] Document network architecture

### Compute Setup (EC2)

- [ ] Select appropriate instance family and size
- [ ] Configure launch templates with best practices
- [ ] Create Auto Scaling groups with appropriate policies
- [ ] Configure Application Load Balancers
- [ ] Set up target groups with health checks
- [ ] Create security groups per application tier
- [ ] Configure Systems Manager for management
- [ ] Set up AMI pipeline for golden images
- [ ] Enable instance metadata options (IMDSv2)

### Container Setup (ECS/EKS)

- [ ] Create ECR repositories with scanning enabled
- [ ] Configure task execution roles with least privilege
- [ ] Set up Fargate or managed node groups
- [ ] Configure service auto-scaling
- [ ] Enable container insights
- [ ] Configure log drivers for CloudWatch
- [ ] Set up secrets management (Secrets Manager/SSM)
- [ ] Implement pod security standards (EKS)
- [ ] Configure IRSA for pod-level IAM (EKS)

## Pre-Production Checklist

- [ ] Security review completed
- [ ] Load testing performed
- [ ] Disaster recovery tested
- [ ] Monitoring and alerting configured
- [ ] Runbooks documented
- [ ] Cost estimates reviewed
- [ ] Compliance requirements verified
- [ ] Change management process defined
- [ ] Rollback procedure documented
- [ ] On-call rotation established

## Sources

- [AWS Security Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [EC2 Security Best Practices](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-best-practices.html)
- [VPC Security Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- [AWS Security Groups Best Practices](https://www.wiz.io/academy/cloud-security/aws-security-groups-best-practices)
- [AWS IAM Best Practices 2026](https://www.strongdm.com/blog/aws-iam-best-practices)
- [AWS Backup 2025 Features](https://aws.amazon.com/blogs/storage/aws-backup-2025-year-in-review-advancing-recovery-resilience/)
