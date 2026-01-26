# FinOps Implementation Checklists

## Phase 1: INFORM - Visibility & Allocation

### Cost Allocation Setup

- [ ] Define tag taxonomy (project, owner, environment, cost-center)
- [ ] Document mandatory vs optional tags
- [ ] Enable tag enforcement policies
  - [ ] AWS: Service Control Policies (SCPs), AWS Config rules
  - [ ] Azure: Azure Policy for required tags
  - [ ] GCP: Organization policies + Terraform automation
- [ ] Set up tag compliance monitoring
- [ ] Target: >90% tag compliance

### Billing & Dashboards

- [ ] Enable detailed billing exports
  - [ ] AWS: Cost and Usage Reports (CUR)
  - [ ] Azure: Cost Management exports
  - [ ] GCP: BigQuery billing export
- [ ] Set up cost allocation reports by:
  - [ ] Team/Department
  - [ ] Project/Application
  - [ ] Environment (prod/staging/dev)
- [ ] Create executive dashboard (weekly spend summary)
- [ ] Create team dashboards (daily granularity)
- [ ] Enable anomaly detection alerts

### Account Structure

- [ ] Review account/subscription hierarchy
- [ ] Implement consolidated billing
- [ ] Set up budget alerts (50%, 75%, 90%, 100% thresholds)
- [ ] Define shared cost allocation strategy

## Phase 2: OPTIMIZE - Efficiency Improvements

### Rightsizing Checklist

- [ ] Review compute utilization reports
  - [ ] AWS: Compute Optimizer recommendations
  - [ ] Azure: Azure Advisor rightsizing
  - [ ] GCP: Active Assist VM recommendations
- [ ] Identify underutilized instances (<20% CPU/memory)
- [ ] Start rightsizing with non-production environments
- [ ] Document rightsizing decisions and results
- [ ] Enable autoscaling for variable workloads
- [ ] Consider ARM-based instances (Graviton, Ampere) for eligible workloads

### Unused Resource Elimination

- [ ] Identify and remove:
  - [ ] Unattached EBS volumes / Azure Disks / GCP Persistent Disks
  - [ ] Unused Elastic IPs / Public IPs
  - [ ] Idle load balancers
  - [ ] Orphaned snapshots (>90 days)
  - [ ] Unused NAT Gateways
- [ ] Schedule dev/test environment downtime
- [ ] Implement auto-shutdown policies
- [ ] Review and delete unused container images

### Commitment Discounts

#### Reserved Instances

- [ ] Analyze 3+ months of stable workload data
- [ ] Calculate baseline vs variable usage
- [ ] Determine RI coverage target (typically 60-80% of baseline)
- [ ] Choose Standard vs Convertible RIs
- [ ] Select 1-year vs 3-year terms
- [ ] Implement RI utilization monitoring

#### Savings Plans

- [ ] Review Savings Plans recommendations
- [ ] Calculate hourly commitment amount
- [ ] Choose Compute vs EC2 Instance Savings Plans
- [ ] Start conservative (cover 50-60% of baseline)
- [ ] Monitor coverage and adjust quarterly

#### Spot Instances

- [ ] Identify spot-eligible workloads:
  - [ ] Batch processing
  - [ ] CI/CD runners
  - [ ] ML training jobs
  - [ ] Stateless web services
- [ ] Implement interruption handling:
  - [ ] Checkpointing for long-running jobs
  - [ ] Graceful shutdown scripts
  - [ ] Multi-AZ diversification
- [ ] Set up Spot Fleet or Spot managed groups
- [ ] Configure fallback to On-Demand

### Storage Optimization

- [ ] Implement lifecycle policies:
  - [ ] Move to infrequent access after 30 days
  - [ ] Archive after 90 days
  - [ ] Delete temporary data automatically
- [ ] Review storage class distribution
- [ ] Enable intelligent tiering where available
- [ ] Compress and deduplicate where possible
- [ ] Clean up old backups beyond retention policy

## Phase 3: OPERATE - Continuous Improvement

### Governance & Automation

- [ ] Implement Infrastructure as Code (IaC) standards
- [ ] Add cost tags in IaC templates
- [ ] Set up automated rightsizing (continuous)
- [ ] Create cost gates in CI/CD pipelines
- [ ] Implement policy-as-code for cost controls

### Review Cadence

- [ ] Daily: Anomaly alert review
- [ ] Weekly: Team cost reviews
- [ ] Monthly: FinOps team analysis
- [ ] Quarterly: Commitment optimization review
- [ ] Annually: Strategy and tooling review

### Culture & Training

- [ ] Establish cost ownership per team
- [ ] Create cost dashboards accessible to engineers
- [ ] Include cost in architecture reviews
- [ ] Share optimization wins organization-wide
- [ ] Provide FinOps training for engineering teams

## AI/ML Specific Checklist

### Training Workloads

- [ ] Use Spot instances with checkpointing
- [ ] Rightsize GPU selection
- [ ] Implement approval workflows for expensive jobs
- [ ] Monitor GPU utilization (target: >80%)
- [ ] Use mixed precision training where possible

### Inference Workloads

- [ ] Implement model quantization
- [ ] Enable response caching
- [ ] Use batch inference where latency allows
- [ ] Consider serverless inference for variable loads
- [ ] Monitor cost per inference request

### AI Cost Tracking

- [ ] Tag AI/ML resources separately
- [ ] Track cost per model
- [ ] Track cost per experiment
- [ ] Monitor cost per 100k tokens/inferences
- [ ] Set budgets per AI project

## Quick Wins (First 30 Days)

1. [ ] Enable billing exports and basic dashboards
2. [ ] Identify and terminate unused resources
3. [ ] Schedule dev environment downtime
4. [ ] Review and accept top rightsizing recommendations
5. [ ] Set up budget alerts
6. [ ] Implement basic tagging policy

## Sources

- [FinOps Foundation Framework](https://www.finops.org/framework/)
- [How to Optimize Cloud Usage](https://www.finops.org/wg/how-to-optimize-cloud-usage/)
- [AWS Cost Optimization Best Practices](https://aws.amazon.com/aws-cost-management/)
- [Azure Cost Management Documentation](https://learn.microsoft.com/en-us/azure/cost-management-billing/)
- [GCP Cost Management](https://cloud.google.com/cost-management)
