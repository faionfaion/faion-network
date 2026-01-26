# FinOps Cloud Cost Optimization Checklist

## Pre-Implementation

- [ ] Identify cloud accounts and billing structures
- [ ] Map current spending by service, team, and environment
- [ ] Establish baseline metrics (current monthly spend)
- [ ] Define cost optimization goals and KPIs
- [ ] Identify stakeholders (Engineering, Finance, Leadership)

## Cost Visibility

### Tagging Strategy
- [ ] Define mandatory tag taxonomy
  - [ ] `environment` (prod/staging/dev/sandbox)
  - [ ] `service` or `application`
  - [ ] `team` or `owner`
  - [ ] `business-unit`
  - [ ] `cost-center`
- [ ] Implement tag enforcement policies (AWS SCPs, Azure Policy)
- [ ] Audit existing resources for untagged items
- [ ] Set up automated tag remediation
- [ ] Target: < 5% untagged resources

### Monitoring Setup
- [ ] Enable Cost Explorer / Cost Management
- [ ] Configure budget alerts (50%, 75%, 90%, 100%)
- [ ] Set up anomaly detection
- [ ] Create cost dashboards by team/service
- [ ] Schedule weekly cost review meetings

## Rightsizing

### Compute Instances
- [ ] Enable CloudWatch/Stackdriver detailed monitoring
- [ ] Analyze CPU utilization patterns (4+ weeks of data)
- [ ] Analyze memory utilization patterns
- [ ] Identify instances with < 30% CPU utilization
- [ ] Identify instances with < 40% memory utilization
- [ ] Create rightsizing recommendations report
- [ ] Implement downsizing in non-prod first
- [ ] Validate performance after rightsizing
- [ ] Document savings achieved

### Storage
- [ ] Audit EBS volumes for underutilization
- [ ] Identify unattached volumes
- [ ] Convert GP2 volumes to GP3 (~20% savings)
- [ ] Review snapshot retention policies
- [ ] Implement S3 lifecycle policies
- [ ] Enable Intelligent-Tiering for S3

### Database
- [ ] Analyze RDS/database instance utilization
- [ ] Consider Aurora Serverless for variable workloads
- [ ] Review provisioned IOPS vs actual usage
- [ ] Implement read replicas for read-heavy workloads

## Reserved Instances / Savings Plans

### Analysis
- [ ] Identify steady-state workloads (24/7 running)
- [ ] Calculate baseline compute capacity
- [ ] Review historical usage patterns (6+ months)
- [ ] Model RI vs Savings Plan coverage scenarios
- [ ] Calculate break-even points

### Implementation
- [ ] Start with Convertible RIs for flexibility
- [ ] Target 70-80% coverage of baseline compute
- [ ] Purchase RIs for known long-term workloads
- [ ] Set up RI utilization monitoring
- [ ] Schedule quarterly RI review
- [ ] Consider RI Marketplace for unused capacity

### Savings Plans (AWS)
- [ ] Evaluate Compute Savings Plans vs EC2 Savings Plans
- [ ] Model commitment amounts based on minimum usage
- [ ] Start conservative (80% of minimum)
- [ ] Monitor and adjust commitments quarterly

## Spot Instances

### Architecture Preparation
- [ ] Identify fault-tolerant workloads
- [ ] Implement application checkpointing
- [ ] Add retry logic for interrupted jobs
- [ ] Configure graceful shutdown handlers
- [ ] Set up fallback to on-demand instances

### Implementation
- [ ] Enable Spot for CI/CD pipelines
- [ ] Use Spot for dev/test environments
- [ ] Implement Spot for batch processing
- [ ] Configure Spot Fleet/Instance diversification
- [ ] Monitor interruption rates by instance type
- [ ] Use Spot placement scores for reliability

### Workload Categories
- [ ] **High Spot Fit:** CI/CD, batch, rendering, analytics
- [ ] **Medium Spot Fit:** Dev environments, testing
- [ ] **Low Spot Fit:** Production APIs, databases (avoid)

## Waste Elimination

### Idle Resources
- [ ] Identify unused EC2 instances
- [ ] Find unattached EBS volumes
- [ ] Locate orphaned snapshots
- [ ] Review unused Elastic IPs
- [ ] Identify idle load balancers
- [ ] Check for unused RDS instances
- [ ] Audit NAT Gateway usage

### Scheduled Scaling
- [ ] Implement auto-scaling policies
- [ ] Schedule non-prod shutdown (evenings/weekends)
- [ ] Target 70% cost reduction for non-prod
- [ ] Use Instance Scheduler or similar tools
- [ ] Configure dev environment auto-stop

### Cleanup Automation
- [ ] Set up automated idle resource detection
- [ ] Implement lifecycle policies for temporary resources
- [ ] Create cleanup Lambda functions
- [ ] Schedule regular resource audits

## Network Optimization

- [ ] Review data transfer costs
- [ ] Keep compute and data in same region
- [ ] Use VPC Endpoints to avoid NAT Gateway costs
- [ ] Implement CDN for static content
- [ ] Review cross-region data transfer
- [ ] Optimize API Gateway usage

## AI/ML Workloads

### Training
- [ ] Use Spot instances for training (with checkpointing)
- [ ] Rightsize GPU selection to model requirements
- [ ] Implement training job queuing
- [ ] Schedule training during off-peak hours
- [ ] Set up approval workflows for expensive instances

### Inference
- [ ] Implement model quantization
- [ ] Enable response caching (20-60% savings)
- [ ] Use batch inference where possible
- [ ] Implement auto-scaling for inference endpoints
- [ ] Monitor GPU utilization

## Governance

### Policies
- [ ] Define resource provisioning policies
- [ ] Set up approval workflows for expensive resources
- [ ] Implement service quotas
- [ ] Create cost allocation reports
- [ ] Establish chargeback/showback model

### Culture
- [ ] Train teams on cost awareness
- [ ] Share cost dashboards with engineering
- [ ] Include cost in deployment reviews
- [ ] Celebrate cost optimization wins
- [ ] Make cost a deployment gate

## Continuous Improvement

- [ ] Weekly: Review anomaly alerts
- [ ] Monthly: Cost review meeting
- [ ] Quarterly: RI/SP coverage review
- [ ] Quarterly: Rightsizing analysis
- [ ] Annually: FinOps maturity assessment

## Success Metrics

| Metric | Target |
|--------|--------|
| Cloud waste reduction | > 25% |
| RI/SP coverage | 70-80% |
| Untagged resources | < 5% |
| Spot adoption (eligible workloads) | > 50% |
| Non-prod scheduled savings | 70% |
| Budget variance | < 5% |

---

*Use this checklist iteratively. Start with Quick Wins (waste elimination, non-prod scheduling) before complex implementations (RI purchasing, Spot architecture).*
