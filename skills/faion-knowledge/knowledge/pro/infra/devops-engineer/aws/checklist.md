# AWS Well-Architected Checklists

Checklists based on the AWS Well-Architected Framework 2025-2026.

---

## Operational Excellence Checklist

### Organization

- [ ] Document workload requirements and priorities
- [ ] Define team roles and responsibilities
- [ ] Establish runbooks for routine procedures
- [ ] Create playbooks for incident response

### Prepare

- [ ] Design workloads to understand state
- [ ] Implement observability (logs, metrics, traces)
- [ ] Automate deployment with IaC (CloudFormation/Terraform)
- [ ] Use feature flags for safe deployments

### Operate

- [ ] Define operational health metrics
- [ ] Implement automated alerting
- [ ] Use dashboards for operational visibility
- [ ] Automate responses to events where possible

### Evolve

- [ ] Conduct post-incident reviews
- [ ] Share learnings across teams
- [ ] Implement improvements from learnings
- [ ] Regularly review and update runbooks

---

## Security Checklist

### Identity and Access Management

- [ ] Enable MFA for all human users
- [ ] Use IAM roles instead of long-term credentials
- [ ] Apply least-privilege permissions
- [ ] Use AWS Organizations with SCPs
- [ ] Enable CloudTrail in all regions
- [ ] Protect root account with hardware MFA
- [ ] Review IAM Access Analyzer findings

### Detection

- [ ] Enable AWS Security Hub
- [ ] Enable Amazon GuardDuty
- [ ] Configure AWS Config rules
- [ ] Set up VPC Flow Logs
- [ ] Enable S3 access logging
- [ ] Configure CloudWatch alarms for security events

### Infrastructure Protection

- [ ] Use VPCs for network isolation
- [ ] Implement security groups with minimal access
- [ ] Use NACLs for subnet-level filtering
- [ ] Enable AWS WAF for web applications
- [ ] Use AWS Shield for DDoS protection
- [ ] Implement network segmentation

### Data Protection

- [ ] Enable encryption at rest for all data stores
- [ ] Use TLS 1.2+ for data in transit
- [ ] Manage keys with AWS KMS
- [ ] Enable S3 bucket versioning
- [ ] Block public access on S3 buckets
- [ ] Use Secrets Manager for credentials

### Incident Response

- [ ] Create incident response runbooks
- [ ] Conduct regular tabletop exercises
- [ ] Configure automated remediation
- [ ] Set up AWS Backup for critical data
- [ ] Enable cross-region replication for DR

---

## Reliability Checklist

### Foundations

- [ ] Set appropriate service quotas
- [ ] Plan network topology with redundancy
- [ ] Implement multi-AZ deployments
- [ ] Document recovery procedures

### Workload Architecture

- [ ] Use loosely coupled dependencies
- [ ] Implement circuit breakers
- [ ] Design for graceful degradation
- [ ] Use async communication where appropriate

### Change Management

- [ ] Automate deployments with CI/CD
- [ ] Use blue-green or canary deployments
- [ ] Implement automated rollback
- [ ] Test deployments in staging environment

### Failure Management

- [ ] Define RTO and RPO for workloads
- [ ] Implement health checks
- [ ] Use Auto Scaling for fault tolerance
- [ ] Test recovery procedures regularly
- [ ] Enable automated backup

---

## Performance Efficiency Checklist

### Selection

- [ ] Evaluate compute options (EC2, Lambda, containers)
- [ ] Choose appropriate storage class
- [ ] Select right database type for workload
- [ ] Consider Graviton processors (40% better price-perf)

### Review

- [ ] Monitor resource utilization
- [ ] Use Compute Optimizer recommendations
- [ ] Review architecture against best practices
- [ ] Evaluate new AWS services regularly

### Monitoring

- [ ] Set up performance dashboards
- [ ] Configure performance alarms
- [ ] Use X-Ray for distributed tracing
- [ ] Monitor latency percentiles (p50, p95, p99)

### Tradeoffs

- [ ] Implement caching where beneficial
- [ ] Use read replicas for read-heavy workloads
- [ ] Consider edge locations (CloudFront)
- [ ] Balance consistency vs availability

---

## Cost Optimization Checklist

### Cloud Financial Management

- [ ] Create AWS Budgets with alerts
- [ ] Enable Cost Allocation Tags
- [ ] Assign cost ownership to teams
- [ ] Review Cost Explorer monthly
- [ ] Track cost anomalies

### Expenditure Awareness

- [ ] Tag all resources for cost allocation
- [ ] Use AWS Cost Categories
- [ ] Set up cost anomaly detection
- [ ] Review AWS Billing dashboard regularly

### Cost-Effective Resources

- [ ] Use Savings Plans for predictable usage (72% savings)
- [ ] Use Spot Instances for fault-tolerant workloads (90% savings)
- [ ] Choose Graviton instances where possible (40% savings)
- [ ] Right-size instances with Compute Optimizer
- [ ] Use appropriate storage classes (S3 lifecycle policies)

### Demand Management

- [ ] Implement Auto Scaling
- [ ] Schedule non-production resources
- [ ] Use Spot Instances for batch jobs
- [ ] Optimize data transfer costs

### Optimize Over Time

- [ ] Review and delete unused resources
- [ ] Identify and remove orphaned EBS volumes
- [ ] Release unused Elastic IPs
- [ ] Delete old snapshots
- [ ] Review and optimize reserved capacity

---

## Sustainability Checklist

### Region Selection

- [ ] Choose regions with lower carbon intensity
- [ ] Use regions closer to users

### Alignment to Demand

- [ ] Use Auto Scaling to match resources to load
- [ ] Schedule resources during off-hours
- [ ] Implement dynamic scaling policies

### Software and Architecture

- [ ] Optimize code for efficiency
- [ ] Use managed services where appropriate
- [ ] Implement caching to reduce computation

### Data Management

- [ ] Implement data lifecycle policies
- [ ] Use appropriate storage tiers
- [ ] Delete unnecessary data

### Hardware and Services

- [ ] Use Graviton processors (more efficient)
- [ ] Adopt serverless where appropriate
- [ ] Use latest generation instance types

---

## New Account Setup Checklist

### Security Baseline

- [ ] Enable MFA on root account
- [ ] Create IAM admin user (don't use root)
- [ ] Enable CloudTrail in all regions
- [ ] Enable AWS Config
- [ ] Enable Security Hub
- [ ] Enable GuardDuty
- [ ] Set password policy

### Cost Management

- [ ] Enable Cost Explorer
- [ ] Create budget alerts
- [ ] Enable cost allocation tags
- [ ] Set up billing alerts

### Networking

- [ ] Plan VPC CIDR ranges
- [ ] Create VPCs in required regions
- [ ] Set up VPC Flow Logs
- [ ] Configure NAT Gateways

### Monitoring

- [ ] Create CloudWatch dashboards
- [ ] Set up SNS topics for alerts
- [ ] Configure alarm thresholds
- [ ] Enable X-Ray for tracing

---

## Pre-Production Checklist

### Security Review

- [ ] IAM policies follow least privilege
- [ ] No hardcoded secrets in code
- [ ] Data encryption enabled
- [ ] Security groups reviewed
- [ ] Public access blocked on S3

### Performance Testing

- [ ] Load testing completed
- [ ] Performance baselines established
- [ ] Scaling policies tested
- [ ] Database performance validated

### Reliability Testing

- [ ] Failure scenarios tested
- [ ] Recovery procedures validated
- [ ] Backup and restore tested
- [ ] Multi-AZ failover verified

### Operational Readiness

- [ ] Monitoring dashboards created
- [ ] Alerts configured
- [ ] Runbooks documented
- [ ] On-call procedures established

---

## Sources

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)
- [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/welcome.html)
- [AWS Cost Optimization](https://aws.amazon.com/aws-cost-management/cost-optimization/)
