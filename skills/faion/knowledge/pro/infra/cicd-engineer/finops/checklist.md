# FinOps Implementation Checklist

## Phase 1: INFORM (Cost Visibility)

### Tagging Strategy

- [ ] Define mandatory tag keys (project, environment, owner, cost-center)
- [ ] Document tag naming conventions
- [ ] Implement tag enforcement policies
- [ ] Create tag compliance reports
- [ ] Set up alerts for untagged resources
- [ ] Review and remediate untagged resources weekly

### Cost Allocation

- [ ] Enable cost allocation tags in cloud provider
- [ ] Set up cost allocation accounts/projects structure
- [ ] Configure showback reports by team/project
- [ ] Implement chargeback model (if applicable)
- [ ] Map costs to business units/products
- [ ] Establish cost allocation hierarchy

### Visibility & Dashboards

- [ ] Enable detailed billing exports
- [ ] Set up cost management tool (native or third-party)
- [ ] Create executive dashboard with KPIs
- [ ] Build team-level cost dashboards
- [ ] Configure daily/weekly cost reports
- [ ] Implement cost anomaly detection
- [ ] Set up forecast vs actual tracking

### Baseline Metrics

- [ ] Document current monthly cloud spend
- [ ] Calculate current waste percentage
- [ ] Measure cost allocation accuracy
- [ ] Identify top 10 cost drivers
- [ ] Establish cost per unit of work baselines

## Phase 2: OPTIMIZE (Efficiency)

### Rightsizing

- [ ] Review and rightsize overprovisioned VMs
- [ ] Audit database instance sizes
- [ ] Optimize container resource requests/limits
- [ ] Review and adjust auto-scaling parameters
- [ ] Analyze CPU/memory utilization trends
- [ ] Document rightsizing decisions

### Idle Resource Cleanup

- [ ] Identify and remove unused EBS/disk volumes
- [ ] Delete unattached Elastic IPs/static IPs
- [ ] Remove unused load balancers
- [ ] Clean up orphaned snapshots
- [ ] Terminate stopped instances (>7 days)
- [ ] Archive or delete unused S3 buckets
- [ ] Set up automated idle detection

### Commitment Discounts

- [ ] Analyze usage patterns for RI/Savings Plans
- [ ] Calculate optimal commitment coverage (target 70-80%)
- [ ] Purchase Reserved Instances for stable workloads
- [ ] Set up Savings Plans for flexible coverage
- [ ] Schedule quarterly commitment reviews
- [ ] Track commitment utilization rate

### Spot/Preemptible Instances

- [ ] Identify spot-eligible workloads
- [ ] Implement checkpointing for spot workloads
- [ ] Configure spot instance pools
- [ ] Set up fallback to on-demand
- [ ] Monitor spot interruption rates

### Storage Optimization

- [ ] Implement S3/GCS lifecycle policies
- [ ] Move infrequent data to cold storage
- [ ] Enable intelligent tiering
- [ ] Compress and deduplicate where possible
- [ ] Review and optimize snapshot retention

### Network Optimization

- [ ] Review data transfer costs
- [ ] Optimize cross-region traffic
- [ ] Use CDN for static content
- [ ] Implement VPC endpoints for AWS services
- [ ] Review NAT gateway usage

## Phase 3: OPERATE (Governance)

### Policies & Guardrails

- [ ] Define approved instance types/sizes
- [ ] Set spending limits per team/project
- [ ] Implement approval workflows for large resources
- [ ] Create policy for dev/test auto-shutdown
- [ ] Establish data retention policies
- [ ] Define GPU/AI resource approval process

### Budget Management

- [ ] Set budgets at account/project level
- [ ] Configure budget alerts (50%, 75%, 90%, 100%)
- [ ] Enable forecast-based alerts
- [ ] Implement automatic cost caps where possible
- [ ] Review budget vs actual monthly

### Automation

- [ ] Automate dev/test shutdown schedules
- [ ] Implement auto-scaling policies
- [ ] Set up automated rightsizing recommendations
- [ ] Create IaC templates with cost controls
- [ ] Automate compliance reporting
- [ ] Implement automated anomaly response

### Cost in CI/CD

- [ ] Add cost estimation to pull requests
- [ ] Integrate infracost or similar tool
- [ ] Block deployments exceeding cost thresholds
- [ ] Include cost metrics in deployment dashboards
- [ ] Track cost impact of releases

### FinOps Review Cadence

- [ ] Weekly: Review anomalies and quick wins
- [ ] Monthly: Team cost reviews
- [ ] Quarterly: Commitment optimization
- [ ] Annually: Strategy and tool evaluation

## AI/ML Specific

### Training Workloads

- [ ] Use spot instances with checkpointing
- [ ] Rightsize GPU selection
- [ ] Implement training approval workflows
- [ ] Schedule training during off-peak
- [ ] Track cost per training run

### Inference Workloads

- [ ] Implement response caching
- [ ] Use model quantization where applicable
- [ ] Batch inference requests
- [ ] Monitor GPU utilization
- [ ] Track cost per inference

### AI Cost Tracking

- [ ] Tag all AI/ML resources
- [ ] Create AI-specific cost dashboards
- [ ] Track cost per model/experiment
- [ ] Monitor token/API usage costs
- [ ] Set AI spending alerts

## Team & Culture

### FinOps Team

- [ ] Identify FinOps champion/lead
- [ ] Form cross-functional FinOps team
- [ ] Define roles and responsibilities
- [ ] Establish meeting cadence
- [ ] Get executive sponsorship

### Training & Awareness

- [ ] Train engineers on cost-aware practices
- [ ] Share cost reports with teams
- [ ] Celebrate cost optimization wins
- [ ] Include cost in architecture reviews
- [ ] Gamify cost optimization

### Documentation

- [ ] Document FinOps policies
- [ ] Create cost optimization playbook
- [ ] Maintain decision log
- [ ] Track optimization history
- [ ] Share lessons learned

## Measurement

### KPIs to Track

- [ ] Total cloud spend (trend)
- [ ] Cost per environment
- [ ] Waste percentage
- [ ] Commitment coverage
- [ ] Cost per customer/transaction
- [ ] Cost allocation accuracy
- [ ] Anomaly detection rate
- [ ] Time to remediate waste

---

*FinOps Checklist | faion-cicd-engineer*
