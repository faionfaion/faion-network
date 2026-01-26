# AWS Architecture Services - Checklist

Pre-deployment verification checklist for AWS service configurations.

## Service Selection Checklist

### Compute Selection

- [ ] Analyzed traffic patterns (variable vs steady)
- [ ] Evaluated execution duration requirements
- [ ] Considered cold start tolerance
- [ ] Assessed GPU/specialized hardware needs
- [ ] Reviewed team Kubernetes expertise (if EKS)
- [ ] Calculated cost model (invocations vs provisioned)

### Serverless vs Containers Decision

| Criterion | Serverless | Containers | Your Choice |
|-----------|------------|------------|-------------|
| Traffic pattern | Variable/spiky | Steady | [ ] |
| Execution time | < 15 min | Long-running | [ ] |
| Cold start tolerance | Acceptable | Not acceptable | [ ] |
| GPU required | No | Yes | [ ] |
| Custom runtime | No | Yes | [ ] |
| Cost optimization | Pay-per-use | Reserved capacity | [ ] |

## EKS Cluster Checklist

### Network Configuration

- [ ] Cluster deployed in private subnets
- [ ] VPC CNI addon enabled
- [ ] Pod security groups configured
- [ ] Network policies defined
- [ ] Ingress controller deployed

### Node Groups

- [ ] Managed node groups used (not self-managed)
- [ ] Multiple instance types for Spot groups
- [ ] Node taints and labels configured
- [ ] Cluster Autoscaler enabled
- [ ] Graviton instances evaluated

### Security

- [ ] IRSA enabled for pod-level IAM
- [ ] Secrets encryption with KMS
- [ ] aws-auth ConfigMap managed
- [ ] Pod Security Standards enforced
- [ ] Container image scanning enabled

### Add-ons

- [ ] CoreDNS (managed)
- [ ] kube-proxy (managed)
- [ ] VPC CNI (managed)
- [ ] EBS CSI driver (with IRSA)
- [ ] AWS Load Balancer Controller

## RDS Aurora Checklist

### High Availability

- [ ] Multi-AZ deployment (2+ instances)
- [ ] Reader endpoint configured
- [ ] Failover priority set
- [ ] Cross-region replica (if required)

### Security

- [ ] Encryption at rest enabled (KMS)
- [ ] SSL/TLS enforced
- [ ] IAM authentication enabled
- [ ] Security group restricts access
- [ ] No public accessibility

### Operations

- [ ] Backup retention: 30 days (prod)
- [ ] Performance Insights enabled
- [ ] Enhanced Monitoring enabled
- [ ] Auto minor version upgrade enabled
- [ ] Maintenance window scheduled

### Production Guards

- [ ] Deletion protection enabled
- [ ] Final snapshot enabled
- [ ] Parameter group customized
- [ ] Connection pooling configured

## Application Load Balancer Checklist

### Listeners

- [ ] HTTP (80) redirects to HTTPS
- [ ] HTTPS (443) with ACM certificate
- [ ] TLS 1.2+ only
- [ ] Security policy: ELBSecurityPolicy-TLS13-1-2-2021-06

### Target Groups

- [ ] Health check endpoint defined
- [ ] Healthy/unhealthy thresholds set
- [ ] Deregistration delay configured (30s)
- [ ] Stickiness configured (if needed)

### Security

- [ ] Security group: ingress 80, 443 only
- [ ] WAF attached (if required)
- [ ] Access logs to S3 enabled
- [ ] Connection logs enabled

## S3 Bucket Checklist

### Security

- [ ] Block all public access enabled
- [ ] Server-side encryption (AES256 or KMS)
- [ ] Bucket policy restricts access
- [ ] VPC endpoint used for private access
- [ ] Access logging enabled

### Data Management

- [ ] Versioning enabled
- [ ] Lifecycle rules configured
- [ ] Object Lock (if compliance required)
- [ ] Replication (if DR required)

### Access Patterns

- [ ] CORS configured (if web access)
- [ ] Presigned URLs for temporary access
- [ ] CloudFront OAC (not OAI)

## CloudFront Distribution Checklist

### Origin Configuration

- [ ] Origin Access Control (OAC) for S3
- [ ] Custom origin headers (if ALB)
- [ ] Origin shield enabled (if high traffic)
- [ ] Failover origin configured

### Cache Behavior

- [ ] Cache policy selected (or custom)
- [ ] Origin request policy configured
- [ ] Compression enabled
- [ ] HTTP/2 and HTTP/3 enabled

### Security

- [ ] HTTPS only (viewer protocol)
- [ ] TLS 1.2+ minimum
- [ ] ACM certificate (us-east-1)
- [ ] Geographic restrictions (if needed)
- [ ] WAF attached (if needed)

### Edge Functions

- [ ] Lambda@Edge or CloudFront Functions
- [ ] Security headers added
- [ ] URL rewriting configured

## EventBridge Checklist

### Event Bus

- [ ] Default or custom event bus
- [ ] Event archive enabled
- [ ] Schema registry enabled
- [ ] Cross-account access configured (if needed)

### Rules

- [ ] Event pattern defined
- [ ] Dead-letter queue configured
- [ ] Retry policy set
- [ ] Input transformer configured

### Targets

- [ ] Target permissions verified
- [ ] Batch size configured (if applicable)
- [ ] Cross-account targets tested (2025 feature)

## Cost Optimization Checklist

### Compute

- [ ] Graviton instances used where possible
- [ ] Spot instances for fault-tolerant workloads
- [ ] Reserved capacity for steady-state
- [ ] Instance Scheduler for non-prod environments

### Storage

- [ ] S3 lifecycle policies configured
- [ ] Intelligent-Tiering for variable access
- [ ] EBS volume types optimized (gp3 vs gp2)
- [ ] Delete unused snapshots

### Network

- [ ] NAT Gateway usage minimized
- [ ] VPC endpoints for AWS services
- [ ] Data transfer costs analyzed
- [ ] CloudFront for high-volume serving

## Final Verification

- [ ] All resources tagged (Project, Environment, Owner)
- [ ] CloudWatch alarms configured
- [ ] CloudTrail enabled
- [ ] AWS Config rules enabled
- [ ] Cost allocation tags enabled
- [ ] Terraform state stored remotely
- [ ] Documentation updated

---

*AWS Architecture Services Checklist | faion-infrastructure-engineer*
