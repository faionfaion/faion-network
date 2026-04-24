# AWS Architecture Checklist

## Pre-Architecture Review

- [ ] Business requirements documented
- [ ] Compliance requirements identified (GDPR, HIPAA, SOC2)
- [ ] RTO/RPO targets defined
- [ ] Budget constraints understood
- [ ] Team expertise assessed

---

## Well-Architected Pillars

### Operational Excellence

#### Prepare

- [ ] Infrastructure as Code (Terraform/CDK)
- [ ] Runbooks for common operations
- [ ] Automated deployment pipelines
- [ ] Pre-deployment testing

#### Operate

- [ ] CloudWatch dashboards configured
- [ ] Alarms for key metrics
- [ ] Log aggregation (CloudWatch Logs/OpenSearch)
- [ ] Distributed tracing (X-Ray)

#### Evolve

- [ ] Post-incident review process
- [ ] Continuous improvement backlog
- [ ] Architecture review schedule

### Security

#### Identity and Access

- [ ] IAM roles for workloads (not users)
- [ ] Least privilege policies
- [ ] MFA for all human access
- [ ] IAM Access Analyzer enabled
- [ ] SCPs for organization guardrails

#### Detection

- [ ] CloudTrail enabled (all regions)
- [ ] GuardDuty enabled
- [ ] Security Hub enabled
- [ ] Config rules for compliance
- [ ] VPC Flow Logs enabled

#### Infrastructure Protection

- [ ] Private subnets for workloads
- [ ] Security groups (deny by default)
- [ ] NACLs for subnet protection
- [ ] WAF for public endpoints
- [ ] Shield for DDoS protection

#### Data Protection

- [ ] Encryption at rest (KMS)
- [ ] Encryption in transit (TLS 1.2+)
- [ ] S3 bucket policies (no public access)
- [ ] Secrets in Secrets Manager
- [ ] Data classification implemented

#### Incident Response

- [ ] Incident response plan documented
- [ ] Automated containment procedures
- [ ] Forensics capability (isolated VPC)
- [ ] Backup and recovery tested

### Reliability

#### Foundations

- [ ] Service quotas reviewed
- [ ] Multi-AZ deployment (minimum 2 AZs)
- [ ] Multi-region for critical workloads
- [ ] Network topology documented

#### Workload Architecture

- [ ] Loosely coupled components
- [ ] Idempotent operations
- [ ] Graceful degradation
- [ ] Circuit breakers implemented
- [ ] Retry with exponential backoff

#### Change Management

- [ ] Blue/green or canary deployments
- [ ] Automated rollback capability
- [ ] Health checks configured
- [ ] Auto-scaling policies

#### Failure Management

- [ ] Failure scenarios documented
- [ ] Recovery procedures tested
- [ ] Backup strategy implemented
- [ ] Cross-region replication (if needed)

### Performance Efficiency

#### Compute

- [ ] Graviton instances evaluated
- [ ] Right-sizing analysis done
- [ ] Spot instances for fault-tolerant workloads
- [ ] Auto-scaling configured
- [ ] Reserved capacity for baseline

#### Storage

- [ ] Storage class matches access patterns
- [ ] S3 lifecycle policies
- [ ] EBS type optimization (gp3 vs io2)
- [ ] Caching strategy implemented

#### Database

- [ ] Database type matches workload
- [ ] Read replicas for read-heavy
- [ ] Connection pooling (RDS Proxy)
- [ ] Query optimization
- [ ] Indexing strategy

#### Network

- [ ] CloudFront for static content
- [ ] Global Accelerator for global users
- [ ] VPC endpoints for AWS services
- [ ] Transfer Acceleration for S3

### Cost Optimization

#### Expenditure Awareness

- [ ] Cost allocation tags
- [ ] AWS Budgets configured
- [ ] Cost Explorer dashboards
- [ ] Reserved Instance/Savings Plans analysis

#### Cost-Effective Resources

- [ ] Graviton instances (20% cheaper)
- [ ] Spot instances (up to 90% cheaper)
- [ ] Savings Plans purchased
- [ ] Reserved Instances for steady-state

#### Manage Demand and Supply

- [ ] Auto-scaling policies
- [ ] Scheduled scaling for predictable patterns
- [ ] Serverless for variable workloads
- [ ] Right-sizing recommendations applied

#### Optimize Over Time

- [ ] Trusted Advisor recommendations
- [ ] Compute Optimizer analysis
- [ ] Unused resource cleanup
- [ ] Storage tiering implemented

### Sustainability

#### Region Selection

- [ ] Low-carbon region considered
- [ ] Region proximity to users

#### Resource Efficiency

- [ ] Managed services preferred
- [ ] Serverless where appropriate
- [ ] Efficient instance types (Graviton)
- [ ] Auto-scaling to match demand

#### Data Efficiency

- [ ] Data lifecycle policies
- [ ] Compression enabled
- [ ] Unnecessary data removed
- [ ] Efficient data transfer

---

## Architecture Patterns

### Three-Tier Architecture

- [ ] Public subnets for load balancers only
- [ ] Private subnets for application tier
- [ ] Database subnets (no internet access)
- [ ] NAT Gateway for outbound (private subnets)
- [ ] At least 2 AZs

### Serverless Architecture

- [ ] API Gateway with throttling
- [ ] Lambda with appropriate memory/timeout
- [ ] DynamoDB with on-demand or auto-scaling
- [ ] Step Functions for orchestration
- [ ] EventBridge for event routing

### Container Architecture

- [ ] EKS or ECS with Fargate
- [ ] Container registry (ECR)
- [ ] Service mesh (optional)
- [ ] Pod/container security policies
- [ ] Resource limits defined

### Event-Driven Architecture

- [ ] EventBridge for routing
- [ ] SQS for buffering
- [ ] SNS for fan-out
- [ ] Dead letter queues
- [ ] Idempotent consumers

---

## Network Design

### VPC Structure

- [ ] CIDR planning (non-overlapping)
- [ ] Subnet sizing (future growth)
- [ ] Public/private/database subnet tiers
- [ ] VPC Flow Logs enabled

### Connectivity

- [ ] VPC peering or Transit Gateway
- [ ] VPN for on-premises
- [ ] Direct Connect for high bandwidth
- [ ] PrivateLink for service access

### DNS

- [ ] Route 53 for DNS
- [ ] Private hosted zones
- [ ] Health checks for failover
- [ ] Latency-based routing (global)

---

## Monitoring and Observability

### Metrics

- [ ] CloudWatch agent on EC2
- [ ] Container Insights for EKS/ECS
- [ ] Custom metrics for business KPIs
- [ ] Dashboards for each tier

### Logging

- [ ] Centralized logging
- [ ] Log retention policies
- [ ] Log analysis (CloudWatch Logs Insights)
- [ ] Audit logging (CloudTrail)

### Tracing

- [ ] X-Ray for distributed tracing
- [ ] Lambda tracing enabled
- [ ] API Gateway tracing
- [ ] Service map visualization

### Alerting

- [ ] Alarms for all critical metrics
- [ ] SNS for notifications
- [ ] PagerDuty/Opsgenie integration
- [ ] Runbook links in alerts

---

## Deployment

### CI/CD

- [ ] Automated builds
- [ ] Automated testing
- [ ] Infrastructure as Code
- [ ] Staged deployments (dev/staging/prod)

### Deployment Strategies

- [ ] Blue/green for zero-downtime
- [ ] Canary for gradual rollout
- [ ] Feature flags for controlled release
- [ ] Rollback automation

### Environment Management

- [ ] Environment parity
- [ ] Configuration management
- [ ] Secrets injection
- [ ] Environment-specific scaling

---

## Disaster Recovery

### Backup

- [ ] Automated backups enabled
- [ ] Cross-region backup replication
- [ ] Backup retention policies
- [ ] Backup testing schedule

### Recovery

- [ ] Recovery procedures documented
- [ ] Recovery time tested
- [ ] Runbooks for DR scenarios
- [ ] DR drills scheduled

### Multi-Region (if applicable)

- [ ] Active-active or active-passive
- [ ] Data replication strategy
- [ ] DNS failover configured
- [ ] Regional independence
